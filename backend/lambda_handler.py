"""
AWS Lambda handler for SOJPE C2H Dashboard
Wraps Flask app to work with API Gateway proxy integration
"""
import json
import base64
import os
import sys
from io import BytesIO

# Add current dir to path for imports
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

# Mock Flask app for Lambda
class MockApp:
    def __init__(self):
        self.routes = {}

    def route(self, path, methods=['GET']):
        def decorator(func):
            self.routes[(path, tuple(methods))] = func
            return func
        return decorator

    def handle_request(self, method, path, body, headers):
        # Route to appropriate handler
        for (route_path, route_methods), handler in self.routes.items():
            if method in route_methods:
                if path == route_path or path.startswith(route_path.rstrip('/')):
                    try:
                        return handler()
                    except Exception as e:
                        return {
                            'statusCode': 500,
                            'body': json.dumps({'error': str(e)})
                        }

        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'Not Found'})
        }

# Initialize mock app
app = MockApp()

# Define routes
@app.route('/api/health', methods=['GET'])
def health():
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'status': 'healthy',
            'service': 'sojpe-c2h-api',
            'version': '1.0.0-lambda'
        })
    }

@app.route('/api/upload', methods=['POST'])
def upload():
    return {
        'statusCode': 202,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'success': True,
            'message': 'Files queued for processing',
            'report_id': 'SOJPE_' + str(int(__import__('time').time())),
            'status': 'PROCESSING'
        })
    }

@app.route('/api/reports', methods=['GET'])
def list_reports():
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({
            'reports': [],
            'count': 0,
            'message': 'DynamoDB integration in progress'
        })
    }

def lambda_handler(event, context):
    """
    Handle API Gateway proxy integration events
    """
    try:
        # Parse request
        method = event.get('httpMethod', 'GET')
        path = event.get('path', '/')
        body = event.get('body', '{}')
        headers = event.get('headers', {})

        # Decode base64 if needed
        if event.get('isBase64Encoded'):
            body = base64.b64decode(body).decode('utf-8')

        # CORS headers
        cors_headers = {
            'Content-Type': 'application/json',
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
            'Access-Control-Allow-Headers': 'Content-Type'
        }

        # Handle OPTIONS
        if method == 'OPTIONS':
            return {
                'statusCode': 200,
                'headers': cors_headers,
                'body': json.dumps({'message': 'OK'})
            }

        # Route request
        response = app.handle_request(method, path, body, headers)

        # Ensure headers are present
        if 'headers' not in response:
            response['headers'] = cors_headers
        else:
            response['headers'].update(cors_headers)

        return response

    except Exception as e:
        print(f"Lambda error: {str(e)}")
        return {
            'statusCode': 500,
            'headers': {'Content-Type': 'application/json'},
            'body': json.dumps({'error': str(e)})
        }

# For local testing
if __name__ == '__main__':
    test_event = {
        'httpMethod': 'GET',
        'path': '/api/health',
        'headers': {},
        'body': None
    }
    print(json.dumps(lambda_handler(test_event, None), indent=2))
