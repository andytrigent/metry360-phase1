# AWS Lambda Deployment Guide - SOJPE C2H Phase 1 Backend

## Architecture Overview

```
Frontend (Vercel)
    ↓ (API calls)
API Gateway (AWS)
    ↓
Lambda Functions (AWS)
    ├─ POST /upload → Process 7 files (15 min timeout)
    ├─ GET  /reports → List reports
    ├─ GET  /reports/{id} → Get report details
    ├─ POST /reports/{id}/approve → Approve report
    └─ GET  /reports/{id}/files → Download raw files
    ↓
S3 (file storage)
DynamoDB (reports metadata)
```

## Prerequisites

✅ AWS CLI configured (ap-south-1 region)
✅ IAM user with permissions
✅ Python 3.11+ installed locally

## Step 1: Create S3 Bucket

```bash
# Create S3 bucket for file uploads
aws s3api create-bucket \
  --bucket trigent-c2h-files \
  --region ap-south-1 \
  --create-bucket-configuration LocationConstraint=ap-south-1

# Enable versioning
aws s3api put-bucket-versioning \
  --bucket trigent-c2h-files \
  --versioning-configuration Status=Enabled

# Block public access
aws s3api put-public-access-block \
  --bucket trigent-c2h-files \
  --public-access-block-configuration \
  "BlockPublicAcls=true,IgnorePublicAcls=true,BlockPublicPolicy=true,RestrictPublicBuckets=true"
```

## Step 2: Create DynamoDB Table

```bash
# Create DynamoDB table for reports
aws dynamodb create-table \
  --table-name sojpe-reports \
  --attribute-definitions \
    AttributeName=report_id,AttributeType=S \
    AttributeName=timestamp,AttributeType=N \
  --key-schema \
    AttributeName=report_id,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region ap-south-1 \
  --tags Key=Project,Value=SOJPE Key=Environment,Value=Production

# Create GSI for status-based queries
aws dynamodb update-table \
  --table-name sojpe-reports \
  --attribute-definitions AttributeName=status,AttributeType=S \
  --global-secondary-indexes \
    "IndexName=status-timestamp-index,Keys=[{AttributeName=status,KeyType=HASH},{AttributeName=timestamp,KeyType=RANGE}],Projection={ProjectionType=ALL}" \
  --region ap-south-1
```

## Step 3: Create IAM Role for Lambda

```bash
# Create trust policy
cat > lambda-trust-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "lambda.amazonaws.com"
      },
      "Action": "sts:AssumeRole"
    }
  ]
}
EOF

# Create IAM role
aws iam create-role \
  --role-name sojpe-lambda-role \
  --assume-role-policy-document file://lambda-trust-policy.json \
  --region ap-south-1

# Attach policies
aws iam attach-role-policy \
  --role-name sojpe-lambda-role \
  --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

# Create custom policy for S3 + DynamoDB
cat > lambda-s3-dynamodb-policy.json <<'EOF'
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": ["s3:*"],
      "Resource": ["arn:aws:s3:::trigent-c2h-files/*", "arn:aws:s3:::trigent-c2h-files"]
    },
    {
      "Effect": "Allow",
      "Action": [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:Scan",
        "dynamodb:UpdateItem"
      ],
      "Resource": "arn:aws:dynamodb:ap-south-1:*:table/sojpe-reports*"
    }
  ]
}
EOF

aws iam put-role-policy \
  --role-name sojpe-lambda-role \
  --policy-name sojpe-s3-dynamodb-access \
  --policy-document file://lambda-s3-dynamodb-policy.json
```

## Step 4: Package Lambda Function

```bash
# Create deployment package
mkdir lambda-deployment
cd lambda-deployment

# Copy app.py and create requirements
cp ../app.py .
cat > requirements.txt <<'EOF'
flask==2.3.2
boto3==1.28.0
pandas==2.0.3
openpyxl==3.1.2
aws-lambda-powertools==2.19.0
EOF

# Install dependencies
pip install -r requirements.txt -t .

# Zip package
zip -r lambda-deployment.zip .
```

## Step 5: Create Lambda Function

```bash
# Get ARN of Lambda role (save for later)
ROLE_ARN=$(aws iam get-role --role-name sojpe-lambda-role --query 'Role.Arn' --output text)

# Create Lambda function
aws lambda create-function \
  --function-name sojpe-data-pipeline \
  --runtime python3.11 \
  --role $ROLE_ARN \
  --handler app.lambda_handler \
  --timeout 900 \
  --memory-size 3008 \
  --zip-file fileb://lambda-deployment.zip \
  --environment Variables="{S3_BUCKET=trigent-c2h-files,DYNAMODB_TABLE=sojpe-reports,AWS_REGION=ap-south-1}" \
  --region ap-south-1

# Update function configuration for long-running tasks
aws lambda put-function-concurrency \
  --function-name sojpe-data-pipeline \
  --reserved-concurrent-executions 10 \
  --region ap-south-1
```

## Step 6: Create API Gateway

```bash
# Create REST API
API_ID=$(aws apigateway create-rest-api \
  --name sojpe-c2h-api \
  --description "SOJPE C2H Dashboard Backend API" \
  --endpoint-configuration types=REGIONAL \
  --region ap-south-1 \
  --query 'id' --output text)

echo "API ID: $API_ID"

# Get root resource
ROOT_ID=$(aws apigateway get-resources \
  --rest-api-id $API_ID \
  --region ap-south-1 \
  --query 'items[0].id' --output text)

# Create /upload resource
UPLOAD_ID=$(aws apigateway create-resource \
  --rest-api-id $API_ID \
  --parent-id $ROOT_ID \
  --path-part upload \
  --region ap-south-1 \
  --query 'id' --output text)

# Create POST method for /upload
aws apigateway put-method \
  --rest-api-id $API_ID \
  --resource-id $UPLOAD_ID \
  --http-method POST \
  --authorization-type NONE \
  --region ap-south-1

# Create Lambda integration
LAMBDA_ARN="arn:aws:lambda:ap-south-1:YOUR_ACCOUNT_ID:function:sojpe-data-pipeline"
aws apigateway put-integration \
  --rest-api-id $API_ID \
  --resource-id $UPLOAD_ID \
  --http-method POST \
  --type AWS_PROXY \
  --integration-http-method POST \
  --uri "$LAMBDA_ARN" \
  --region ap-south-1

# Create deployment
DEPLOYMENT_ID=$(aws apigateway create-deployment \
  --rest-api-id $API_ID \
  --stage-name prod \
  --region ap-south-1 \
  --query 'id' --output text)

echo "API Endpoint: https://$API_ID.execute-api.ap-south-1.amazonaws.com/prod"
```

## Step 7: Update Lambda to Handle API Gateway Events

Modify app.py:

```python
from aws_lambda_powertools import Logger
import json
import base64

logger = Logger()

def lambda_handler(event, context):
    """Handle API Gateway proxy integration"""
    
    # Parse API Gateway event
    http_method = event.get('httpMethod', 'POST')
    path = event.get('path', '/')
    body = event.get('body', '{}')
    
    if event.get('isBase64Encoded'):
        body = base64.b64decode(body)
    
    try:
        # Route to appropriate handler
        if path == '/upload' and http_method == 'POST':
            return handle_upload(json.loads(body) if isinstance(body, str) else body)
        elif path.startswith('/reports'):
            return handle_reports(path, http_method, body)
        else:
            return error_response(404, 'Not Found')
    
    except Exception as e:
        logger.exception(f"Error: {str(e)}")
        return error_response(500, str(e))

def error_response(status_code, message):
    """Return error response in API Gateway format"""
    return {
        'statusCode': status_code,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'error': message})
    }

def success_response(data, status_code=200):
    """Return success response in API Gateway format"""
    return {
        'statusCode': status_code,
        'headers': {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*'
        },
        'body': json.dumps(data)
    }
```

## Step 8: Enable CORS

```bash
# Create CORS model
aws apigateway put-method-response \
  --rest-api-id $API_ID \
  --resource-id $UPLOAD_ID \
  --http-method POST \
  --status-code 200 \
  --response-models '{"application/json": "Empty"}' \
  --region ap-south-1

aws apigateway put-integration-response \
  --rest-api-id $API_ID \
  --resource-id $UPLOAD_ID \
  --http-method POST \
  --status-code 200 \
  --response-parameters '{"method.response.header.Access-Control-Allow-Origin": "'"'"'*'"'"'"}' \
  --region ap-south-1
```

## Step 9: Environment Variables in Vercel

In Vercel project settings, add:

```
API_BASE_URL=https://YOUR_API_ID.execute-api.ap-south-1.amazonaws.com/prod
AWS_REGION=ap-south-1
```

## Step 10: Update Frontend to Use Lambda API

In dashboard.html and upload.html, replace:

```javascript
// Before (local Flask)
const API_URL = 'http://localhost:5000/api';

// After (AWS Lambda)
const API_URL = process.env.API_BASE_URL || '/api';
```

## Monitoring & Logging

```bash
# View Lambda logs
aws logs tail /aws/lambda/sojpe-data-pipeline --follow

# Monitor Lambda metrics
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Duration \
  --dimensions Name=FunctionName,Value=sojpe-data-pipeline \
  --start-time 2024-06-22T00:00:00Z \
  --end-time 2024-06-22T23:59:59Z \
  --period 3600 \
  --statistics Average,Maximum
```

## Cost Optimization

1. **Lambda**: ~$0.02 per million requests + compute time
2. **S3**: ~$0.023 per GB stored
3. **DynamoDB**: Pay-per-request billing (~$1.25 per million read/write units)
4. **API Gateway**: $3.50 per million requests

**Estimated Monthly Cost**: $50-150 depending on usage

## Next Steps

1. Deploy frontend to Vercel: `vercel --prod --yes --scope trigent-ark-os`
2. Test API endpoints
3. Set up CloudWatch alerts
4. Configure auto-scaling
5. Plan Phase 2 migration to Spring Boot + PostgreSQL

---

**Questions?** Check AWS documentation or contact DevOps team.
