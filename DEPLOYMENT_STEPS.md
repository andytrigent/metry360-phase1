# SOJPE C2H Phase 1 - Deployment Steps

## Quick Reference

**Repository**: https://github.com/andytrigent/metry360-phase1  
**AWS Region**: ap-south-1  
**Status**: Ready for deployment

---

## Phase 1: Frontend Deployment to Vercel (NOW)

### Command to Deploy:

```bash
cd D:\experiments\gcc-qmetry\metry360-phase1
vercel --prod --yes --scope trigent-ark-os
```

**What this does:**
- Deploys frontend (HTML/CSS/JS) to Vercel CDN
- Creates environment variables
- Sets up CI/CD pipeline for automatic deployments
- Generates production URL

**After deployment:**
- Note the Vercel URL (e.g., https://metry360-phase1-production.vercel.app)
- Update `.env.local.backup` with the Vercel URL
- These are the environment variables Vercel will manage:
  - `API_BASE_URL` → Points to AWS Lambda API Gateway
  - `AWS_REGION` → ap-south-1

---

## Phase 2: Backend Deployment to AWS Lambda (Next)

### 1. Create AWS Resources (5-10 minutes)

Follow the steps in **AWS_LAMBDA_DEPLOYMENT.md**:

```bash
# Step 1: Create S3 bucket
aws s3api create-bucket \
  --bucket trigent-c2h-files \
  --region ap-south-1 \
  --create-bucket-configuration LocationConstraint=ap-south-1

# Step 2: Create DynamoDB table
aws dynamodb create-table \
  --table-name sojpe-reports \
  --attribute-definitions AttributeName=report_id,AttributeType=S \
  --key-schema AttributeName=report_id,KeyType=HASH \
  --billing-mode PAY_PER_REQUEST \
  --region ap-south-1

# Step 3: Create IAM role
# (See AWS_LAMBDA_DEPLOYMENT.md for detailed IAM setup)

# Step 4: Package and deploy Lambda function
# (See AWS_LAMBDA_DEPLOYMENT.md)

# Step 5: Create API Gateway
# (See AWS_LAMBDA_DEPLOYMENT.md)
```

### 2. Expected Endpoints After Deployment

```
API Gateway Base URL:
https://YOUR_API_ID.execute-api.ap-south-1.amazonaws.com/prod

Endpoints:
- POST /upload → Upload 7 files, process 83-step pipeline
- GET  /reports → List all reports
- GET  /reports/{id} → Get specific report
- POST /reports/{id}/approve → Approve report (Akash only)
- GET  /reports/{id}/files → Download raw files
- GET  /health → Health check
```

### 3. Update Vercel Environment Variables

After Lambda is deployed, add to Vercel project:

**Settings → Environment Variables:**
```
API_BASE_URL = https://YOUR_API_ID.execute-api.ap-south-1.amazonaws.com/prod
AWS_REGION = ap-south-1
```

Then redeploy:
```bash
vercel --prod --yes --scope trigent-ark-os
```

---

## Architecture After Deployment

```
┌─────────────────────────────────────────┐
│           VERCEL (Frontend)             │
│  - dashboard.html                       │
│  - upload.html                          │
│  - index.html                           │
│  https://metry360-phase1.vercel.app     │
└──────────────┬──────────────────────────┘
               │ API Calls
               ↓
┌─────────────────────────────────────────┐
│      API GATEWAY (AWS)                  │
│  https://xxx.execute-api.               │
│  ap-south-1.amazonaws.com/prod          │
└──────────────┬──────────────────────────┘
               │
        ┌──────┴──────┐
        ↓             ↓
    ┌───────────┐  ┌────────────┐
    │  LAMBDA   │  │  S3        │
    │  Process  │  │  Storage   │
    │  83 steps │  │  (Files)   │
    └─────┬─────┘  └────────────┘
          │
          ↓
    ┌────────────┐
    │ DynamoDB   │
    │ (Reports   │
    │  Metadata) │
    └────────────┘
```

---

## Deployment Checklist

### Pre-Deployment ✅
- [x] Code pushed to GitHub
- [x] Vercel configuration created (vercel.json)
- [x] AWS Lambda deployment guide created
- [x] AWS CLI configured (ap-south-1)
- [x] IAM credentials set up

### Frontend Deployment (NOW)
- [ ] Run: `vercel --prod --yes --scope trigent-ark-os`
- [ ] Note the production URL
- [ ] Test: Open URL in browser
- [ ] Verify: All dashboard views load
- [ ] Check: No console errors

### Backend Deployment (NEXT)
- [ ] Create S3 bucket (trigent-c2h-files)
- [ ] Create DynamoDB table (sojpe-reports)
- [ ] Create IAM role (sojpe-lambda-role)
- [ ] Package Lambda function
- [ ] Deploy Lambda (sojpe-data-pipeline)
- [ ] Create API Gateway
- [ ] Test endpoints with curl/Postman
- [ ] Update Vercel environment variables
- [ ] Redeploy frontend
- [ ] End-to-end testing

### Post-Deployment
- [ ] Monitor CloudWatch logs
- [ ] Set up alarms
- [ ] Document API endpoints
- [ ] Update team on production URLs
- [ ] Schedule training session with Akash

---

## Rollback Plan

If something goes wrong:

**Vercel:** 
```bash
# Automatic rollback to previous deployment
# Vercel dashboard → Deployments → Rollback
```

**AWS Lambda:**
```bash
# Restore previous version
aws lambda update-function-code \
  --function-name sojpe-data-pipeline \
  --zip-file fileb://lambda-deployment-backup.zip
```

**Database:**
- S3: Versioning enabled (restore old version)
- DynamoDB: On-demand backup (restore from backup)

---

## Monitoring Links

After deployment:

- **Vercel**: https://vercel.com/trigent-ark-os/metry360-phase1
- **CloudWatch Logs**: https://console.aws.amazon.com/cloudwatch/home?region=ap-south-1
- **Lambda**: https://console.aws.amazon.com/lambda/home?region=ap-south-1
- **API Gateway**: https://console.aws.amazon.com/apigateway/home?region=ap-south-1
- **S3**: https://s3.console.aws.amazon.com/s3/buckets?region=ap-south-1
- **DynamoDB**: https://console.aws.amazon.com/dynamodb/home?region=ap-south-1

---

## Next Steps After Deployment

1. ✅ Frontend on Vercel
2. ✅ Backend on AWS Lambda
3. Next: Phase 2 Planning
   - React 19 frontend
   - Spring Boot backend
   - PostgreSQL database
   - Live API integration
   - User authentication

---

## Support

- **Questions about Vercel?** → https://vercel.com/docs
- **Questions about AWS Lambda?** → See AWS_LAMBDA_DEPLOYMENT.md
- **Code issues?** → GitHub issues
- **Production issues?** → CloudWatch logs + AWS Console

---

**Status**: 🟢 READY TO DEPLOY  
**Last Updated**: June 22, 2026  
**Next Review**: After first deployment
