#!/bin/bash

# ============================================================================
# Deploy Auth Service to LocalStack Lambda
# ============================================================================
# This script packages the FastAPI application and deploys it to LocalStack
# Prerequisites:
#   - LocalStack running on localhost:4566
#   - AWS CLI configured for LocalStack
# ============================================================================

set -e  # Exit on error

echo "🚀 Deploying Sage Auth Service to LocalStack Lambda..."

# Configuration
FUNCTION_NAME="sage-auth-service"
HANDLER="lambda_handler.lambda_handler"
RUNTIME="python3.11"
ROLE="arn:aws:iam::000000000000:role/lambda-role"
LOCALSTACK_ENDPOINT="http://localhost:4566"
REGION="us-east-1"
AWS_PROFILE="localstack"

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}📦 Step 1: Creating deployment package...${NC}"

# Create a temporary directory for the package
TEMP_DIR=$(mktemp -d)
echo "   Temporary directory: $TEMP_DIR"

# Copy application code to temp directory
echo "   Copying application code..."
cp -r app "$TEMP_DIR/"
cp lambda_handler.py "$TEMP_DIR/"
cp requirements.txt "$TEMP_DIR/"

# Install dependencies in temp directory
echo "   Installing dependencies..."
pip install -r requirements.txt -t "$TEMP_DIR/" \
    --platform manylinux2014_x86_64 \
    --implementation cp \
    --python-version 3.11 \
    --only-binary=:all: \
    --upgrade \
    --quiet

# Fix permissions for all files (Lambda needs read permissions)
echo "   Setting file permissions..."
chmod -R 755 "$TEMP_DIR"
find "$TEMP_DIR" -type f -exec chmod 644 {} \;

# Create ZIP file
DEPLOYMENT_PACKAGE="lambda-deployment.zip"
echo "   Creating ZIP package..."
cd "$TEMP_DIR"
zip -r -q "$DEPLOYMENT_PACKAGE" .
cd -

# Move ZIP to current directory
mv "$TEMP_DIR/$DEPLOYMENT_PACKAGE" .
echo -e "${GREEN}   ✅ Package created: $DEPLOYMENT_PACKAGE${NC}"

# Clean up temp directory
rm -rf "$TEMP_DIR"

# Check if function already exists
echo -e "${YELLOW}📋 Step 2: Checking if Lambda function exists...${NC}"
if aws --profile "$AWS_PROFILE" lambda get-function \
    --function-name "$FUNCTION_NAME" \
    --endpoint-url="$LOCALSTACK_ENDPOINT" \
    --region "$REGION" \
    2>/dev/null; then

    echo "   Function exists, updating code..."
    aws --profile "$AWS_PROFILE" lambda update-function-code \
        --function-name "$FUNCTION_NAME" \
        --zip-file "fileb://$DEPLOYMENT_PACKAGE" \
        --endpoint-url="$LOCALSTACK_ENDPOINT" \
        --region "$REGION" > /dev/null

    echo -e "${GREEN}   ✅ Lambda function updated${NC}"
else
    echo "   Function doesn't exist, creating new function..."
    aws --profile "$AWS_PROFILE" lambda create-function \
        --function-name "$FUNCTION_NAME" \
        --runtime "$RUNTIME" \
        --handler "$HANDLER" \
        --role "$ROLE" \
        --zip-file "fileb://$DEPLOYMENT_PACKAGE" \
        --timeout 30 \
        --memory-size 512 \
        --environment "Variables={
            ENVIRONMENT=development,
            DEBUG=true,
            DATABASE_URL=postgresql://sage_user:sage_password@host.docker.internal:5432/sage_auth_db,
            SECRET_KEY=your-secret-key-change-this,
            GOOGLE_CLIENT_ID=dummy,
            GOOGLE_CLIENT_SECRET=dummy,
            GOOGLE_REDIRECT_URI=http://localhost:4566
        }" \
        --endpoint-url="$LOCALSTACK_ENDPOINT" \
        --region "$REGION" > /dev/null

    echo -e "${GREEN}   ✅ Lambda function created${NC}"
fi

echo -e "${YELLOW}🔍 Step 3: Verifying deployment...${NC}"
aws --profile "$AWS_PROFILE" lambda get-function \
    --function-name "$FUNCTION_NAME" \
    --endpoint-url="$LOCALSTACK_ENDPOINT" \
    --region "$REGION" \
    --query 'Configuration.[FunctionName,Runtime,Handler,LastModified]' \
    --output table

echo ""
echo -e "${GREEN}✅ Deployment complete!${NC}"
echo ""
echo "📝 Next steps:"
echo "   1. Test the Lambda function:"
echo "      ./test_lambda.sh"
echo ""
echo "   2. View Lambda logs:"
echo "      aws --profile $AWS_PROFILE logs tail /aws/lambda/$FUNCTION_NAME --follow --endpoint-url=$LOCALSTACK_ENDPOINT"
echo ""
echo "   3. Delete function (if needed):"
echo "      aws --profile $AWS_PROFILE lambda delete-function --function-name $FUNCTION_NAME --endpoint-url=$LOCALSTACK_ENDPOINT"
