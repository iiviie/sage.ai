# Serverless Lambda Setup Guide

This guide walks you through deploying and testing the Sage Auth Service as an AWS Lambda function using LocalStack.

## 🎯 Architecture Overview

- **FastAPI App** → Wrapped with Mangum adapter → **AWS Lambda**
- **PostgreSQL** → Running in Docker (port 5432)
- **LocalStack** → Running locally (port 4566)
- **AWS CLI** → Configured for LocalStack

## 📋 Prerequisites

### 1. LocalStack Running
Ensure LocalStack is running locally on port 4566:
```bash
# Check if LocalStack is running
curl http://localhost:4566/_localstack/health
```

### 2. PostgreSQL Running
Start PostgreSQL via Docker Compose:
```bash
cd /path/to/sage.ai
docker-compose up -d postgres
```

Verify it's running:
```bash
docker ps | grep sage_postgres
```

### 3. AWS CLI Configured for LocalStack
Your AWS CLI should be configured to point to LocalStack. Verify:
```bash
aws --profile localstack --endpoint-url=http://localhost:4566 lambda list-functions
```

## 🚀 Deployment Steps

### Step 1: Install Dependencies
```bash
cd auth_service
pip install -r requirements.txt
```

This installs FastAPI, SQLAlchemy, Mangum, and all dependencies.

### Step 2: Make Scripts Executable
```bash
chmod +x deploy_lambda.sh test_lambda.sh
```

### Step 3: Deploy to LocalStack Lambda
```bash
./deploy_lambda.sh
```

This script will:
1. ✅ Create a deployment package (ZIP file)
2. ✅ Install all dependencies
3. ✅ Deploy Lambda function to LocalStack
4. ✅ Configure environment variables

**Expected Output:**
```
🚀 Deploying Sage Auth Service to LocalStack Lambda...
📦 Step 1: Creating deployment package...
   ✅ Package created: lambda-deployment.zip
📋 Step 2: Checking if Lambda function exists...
   ✅ Lambda function created
🔍 Step 3: Verifying deployment...
✅ Deployment complete!
```

### Step 4: Test the Lambda Function
```bash
./test_lambda.sh
```

This will run 5 tests:
1. Health check endpoint
2. Root endpoint
3. Database connection check
4. Create a test item (POST)
5. Get all test items (GET)

## 🧪 Manual Testing

### Invoke Lambda Directly (AWS CLI)

Create a test event file:
```bash
cat > event.json <<EOF
{
  "httpMethod": "GET",
  "path": "/health",
  "headers": {},
  "body": null,
  "isBase64Encoded": false
}
EOF
```

Invoke the Lambda:
```bash
aws --profile localstack lambda invoke \
  --function-name sage-auth-service \
  --payload file://event.json \
  --endpoint-url=http://localhost:4566 \
  response.json

cat response.json | jq '.'
```

### Test POST Request

```bash
cat > event-post.json <<EOF
{
  "httpMethod": "POST",
  "path": "/api/v1/test/items",
  "headers": {
    "Content-Type": "application/json"
  },
  "body": "{\"title\": \"My Test\", \"description\": \"Testing Lambda\", \"is_active\": true}",
  "isBase64Encoded": false
}
EOF

aws --profile localstack lambda invoke \
  --function-name sage-auth-service \
  --payload file://event-post.json \
  --endpoint-url=http://localhost:4566 \
  response.json
```

## 📊 Database Connection

### Important: Database URL for Lambda

Lambda functions in LocalStack run inside LocalStack's Docker container. To connect to PostgreSQL running in a separate Docker container, use:

```
DATABASE_URL=postgresql://sage_user:sage_password@host.docker.internal:5432/sage_auth_db
```

This is already configured in `deploy_lambda.sh`.

### Verify Database Connection

1. Check if PostgreSQL is accessible from host:
```bash
psql -h localhost -U sage_user -d sage_auth_db -c "SELECT 1;"
```

2. Test database endpoint via Lambda:
```bash
aws --profile localstack lambda invoke \
  --function-name sage-auth-service \
  --payload '{"httpMethod":"GET","path":"/api/v1/test/db-check"}' \
  --endpoint-url=http://localhost:4566 \
  response.json

cat response.json
```

## 🔍 Debugging

### View Lambda Logs
```bash
aws --profile localstack logs tail /aws/lambda/sage-auth-service \
  --follow \
  --endpoint-url=http://localhost:4566
```

### List Lambda Functions
```bash
aws --profile localstack lambda list-functions \
  --endpoint-url=http://localhost:4566 \
  --query 'Functions[*].[FunctionName,Runtime,Handler]' \
  --output table
```

### Get Lambda Configuration
```bash
aws --profile localstack lambda get-function-configuration \
  --function-name sage-auth-service \
  --endpoint-url=http://localhost:4566
```

### Update Environment Variables
```bash
aws --profile localstack lambda update-function-configuration \
  --function-name sage-auth-service \
  --environment "Variables={DATABASE_URL=postgresql://...}" \
  --endpoint-url=http://localhost:4566
```

### Delete Lambda Function
```bash
aws --profile localstack lambda delete-function \
  --function-name sage-auth-service \
  --endpoint-url=http://localhost:4566
```

## 🔧 Troubleshooting

### Issue: Database Connection Failed

**Symptom:** Lambda can't connect to PostgreSQL

**Solutions:**
1. Check if PostgreSQL is running: `docker ps | grep postgres`
2. Try using actual host IP instead of `host.docker.internal`:
   ```bash
   # Get your IP
   ifconfig | grep "inet "

   # Update DATABASE_URL in deploy_lambda.sh
   DATABASE_URL=postgresql://sage_user:sage_password@YOUR_IP:5432/sage_auth_db
   ```

### Issue: Lambda Package Too Large

**Symptom:** Deployment fails due to package size

**Solution:** Use Lambda Layers or Docker-based Lambda (future enhancement)

### Issue: Module Import Errors

**Symptom:** `ModuleNotFoundError` when invoking Lambda

**Solution:**
1. Ensure all dependencies are in requirements.txt
2. Re-run deployment: `./deploy_lambda.sh`

## 📝 Available Endpoints

Once deployed, your Lambda function supports these endpoints:

| Method | Path | Description |
|--------|------|-------------|
| GET | `/` | Root endpoint - service info |
| GET | `/health` | Health check with DB status |
| GET | `/api/v1/test/db-check` | Database connectivity test |
| POST | `/api/v1/test/items` | Create test item |
| GET | `/api/v1/test/items` | List all test items |
| GET | `/api/v1/test/items/{id}` | Get specific test item |
| DELETE | `/api/v1/test/items/{id}` | Delete test item |

## 🔮 Next Steps

### 1. Add API Gateway (Optional)
Create an HTTP API in LocalStack for easier testing:
```bash
# Create API Gateway
aws --profile localstack apigatewayv2 create-api \
  --name sage-auth-api \
  --protocol-type HTTP \
  --endpoint-url=http://localhost:4566

# Create integration with Lambda
# Create routes
# ... (detailed steps can be added later)
```

### 2. Add More Endpoints
- User authentication endpoints
- OAuth2 flow
- Token management

### 3. Production Deployment
- Deploy to real AWS Lambda
- Use RDS for PostgreSQL
- Set up proper IAM roles
- Configure VPC for database access

## 📚 Resources

- [Mangum Documentation](https://mangum.io/)
- [LocalStack Lambda Docs](https://docs.localstack.cloud/user-guide/aws/lambda/)
- [FastAPI with Lambda](https://fastapi.tiangolo.com/deployment/serverless/)
