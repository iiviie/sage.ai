#!/bin/bash

# ============================================================================
# Test Sage Auth Service Lambda Function in LocalStack
# ============================================================================
# This script tests various endpoints of the deployed Lambda function
# without using API Gateway (direct Lambda invocations)
# ============================================================================

set -e

FUNCTION_NAME="sage-auth-service"
LOCALSTACK_ENDPOINT="http://localhost:4566"
REGION="us-east-1"
AWS_PROFILE="localstack"

# Colors
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
RED='\033[0;31m'
NC='\033[0m'

echo -e "${BLUE}🧪 Testing Sage Auth Service Lambda Function${NC}"
echo ""

# ============================================================================
# Test 1: Health Check
# ============================================================================
echo -e "${YELLOW}Test 1: Health Check Endpoint${NC}"
cat > /tmp/event.json <<EOF
{
  "version": "2.0",
  "routeKey": "GET /health",
  "rawPath": "/health",
  "rawQueryString": "",
  "headers": {
    "accept": "application/json"
  },
  "requestContext": {
    "accountId": "000000000000",
    "apiId": "test-api",
    "domainName": "test-api.localhost.localstack.cloud",
    "domainPrefix": "test-api",
    "http": {
      "method": "GET",
      "path": "/health",
      "protocol": "HTTP/1.1",
      "sourceIp": "127.0.0.1",
      "userAgent": "test"
    },
    "requestId": "test-request-id",
    "routeKey": "GET /health",
    "stage": "\$default",
    "time": "01/Jan/2024:00:00:00 +0000",
    "timeEpoch": 1704067200000
  },
  "isBase64Encoded": false
}
EOF

echo "   Invoking Lambda..."
aws --profile "$AWS_PROFILE" lambda invoke \
    --function-name "$FUNCTION_NAME" \
    --payload file:///tmp/event.json \
    --endpoint-url="$LOCALSTACK_ENDPOINT" \
    --region "$REGION" \
    /tmp/response.json > /dev/null

echo -e "   ${GREEN}Response:${NC}"
cat /tmp/response.json | jq '.'
echo ""

# ============================================================================
# Test 2: Root Endpoint
# ============================================================================
echo -e "${YELLOW}Test 2: Root Endpoint${NC}"
cat > /tmp/event.json <<EOF
{
  "version": "2.0",
  "routeKey": "GET /",
  "rawPath": "/",
  "rawQueryString": "",
  "headers": {
    "accept": "application/json"
  },
  "requestContext": {
    "accountId": "000000000000",
    "apiId": "test-api",
    "domainName": "test-api.localhost.localstack.cloud",
    "domainPrefix": "test-api",
    "http": {
      "method": "GET",
      "path": "/",
      "protocol": "HTTP/1.1",
      "sourceIp": "127.0.0.1",
      "userAgent": "test"
    },
    "requestId": "test-request-id",
    "routeKey": "GET /",
    "stage": "\$default",
    "time": "01/Jan/2024:00:00:00 +0000",
    "timeEpoch": 1704067200000
  },
  "isBase64Encoded": false
}
EOF

aws --profile "$AWS_PROFILE" lambda invoke \
    --function-name "$FUNCTION_NAME" \
    --payload file:///tmp/event.json \
    --endpoint-url="$LOCALSTACK_ENDPOINT" \
    --region "$REGION" \
    /tmp/response.json > /dev/null

echo -e "   ${GREEN}Response:${NC}"
cat /tmp/response.json | jq '.'
echo ""

# ============================================================================
# Test 3: Database Check
# ============================================================================
echo -e "${YELLOW}Test 3: Database Connection Check${NC}"
cat > /tmp/event.json <<EOF
{
  "version": "2.0",
  "routeKey": "GET /api/v1/test/db-check",
  "rawPath": "/api/v1/test/db-check",
  "rawQueryString": "",
  "headers": {
    "accept": "application/json"
  },
  "requestContext": {
    "accountId": "000000000000",
    "apiId": "test-api",
    "domainName": "test-api.localhost.localstack.cloud",
    "domainPrefix": "test-api",
    "http": {
      "method": "GET",
      "path": "/api/v1/test/db-check",
      "protocol": "HTTP/1.1",
      "sourceIp": "127.0.0.1",
      "userAgent": "test"
    },
    "requestId": "test-request-id",
    "routeKey": "GET /api/v1/test/db-check",
    "stage": "\$default",
    "time": "01/Jan/2024:00:00:00 +0000",
    "timeEpoch": 1704067200000
  },
  "isBase64Encoded": false
}
EOF

aws --profile "$AWS_PROFILE" lambda invoke \
    --function-name "$FUNCTION_NAME" \
    --payload file:///tmp/event.json \
    --endpoint-url="$LOCALSTACK_ENDPOINT" \
    --region "$REGION" \
    /tmp/response.json > /dev/null

echo -e "   ${GREEN}Response:${NC}"
cat /tmp/response.json | jq '.'
echo ""

# ============================================================================
# Test 4: Create Test Item
# ============================================================================
echo -e "${YELLOW}Test 4: Create Test Item (POST)${NC}"
cat > /tmp/event.json <<EOF
{
  "version": "2.0",
  "routeKey": "POST /api/v1/test/items",
  "rawPath": "/api/v1/test/items",
  "rawQueryString": "",
  "headers": {
    "accept": "application/json",
    "content-type": "application/json"
  },
  "requestContext": {
    "accountId": "000000000000",
    "apiId": "test-api",
    "domainName": "test-api.localhost.localstack.cloud",
    "domainPrefix": "test-api",
    "http": {
      "method": "POST",
      "path": "/api/v1/test/items",
      "protocol": "HTTP/1.1",
      "sourceIp": "127.0.0.1",
      "userAgent": "test"
    },
    "requestId": "test-request-id",
    "routeKey": "POST /api/v1/test/items",
    "stage": "\$default",
    "time": "01/Jan/2024:00:00:00 +0000",
    "timeEpoch": 1704067200000
  },
  "body": "{\"title\": \"Lambda Test Item\", \"description\": \"Testing from LocalStack Lambda\", \"is_active\": true}",
  "isBase64Encoded": false
}
EOF

aws --profile "$AWS_PROFILE" lambda invoke \
    --function-name "$FUNCTION_NAME" \
    --payload file:///tmp/event.json \
    --endpoint-url="$LOCALSTACK_ENDPOINT" \
    --region "$REGION" \
    /tmp/response.json > /dev/null

echo -e "   ${GREEN}Response:${NC}"
cat /tmp/response.json | jq '.'
echo ""

# ============================================================================
# Test 5: Get All Test Items
# ============================================================================
echo -e "${YELLOW}Test 5: Get All Test Items${NC}"
cat > /tmp/event.json <<EOF
{
  "version": "2.0",
  "routeKey": "GET /api/v1/test/items",
  "rawPath": "/api/v1/test/items",
  "rawQueryString": "skip=0&limit=10",
  "headers": {
    "accept": "application/json"
  },
  "queryStringParameters": {
    "skip": "0",
    "limit": "10"
  },
  "requestContext": {
    "accountId": "000000000000",
    "apiId": "test-api",
    "domainName": "test-api.localhost.localstack.cloud",
    "domainPrefix": "test-api",
    "http": {
      "method": "GET",
      "path": "/api/v1/test/items",
      "protocol": "HTTP/1.1",
      "sourceIp": "127.0.0.1",
      "userAgent": "test"
    },
    "requestId": "test-request-id",
    "routeKey": "GET /api/v1/test/items",
    "stage": "\$default",
    "time": "01/Jan/2024:00:00:00 +0000",
    "timeEpoch": 1704067200000
  },
  "isBase64Encoded": false
}
EOF

aws --profile "$AWS_PROFILE" lambda invoke \
    --function-name "$FUNCTION_NAME" \
    --payload file:///tmp/event.json \
    --endpoint-url="$LOCALSTACK_ENDPOINT" \
    --region "$REGION" \
    /tmp/response.json > /dev/null

echo -e "   ${GREEN}Response:${NC}"
cat /tmp/response.json | jq '.'
echo ""

echo -e "${GREEN}✅ All tests complete!${NC}"
echo ""
echo "💡 Tips:"
echo "   - View Lambda logs: aws --profile $AWS_PROFILE logs tail /aws/lambda/$FUNCTION_NAME --follow --endpoint-url=$LOCALSTACK_ENDPOINT"
echo "   - Invoke custom event: aws --profile $AWS_PROFILE lambda invoke --function-name $FUNCTION_NAME --payload file://your-event.json --endpoint-url=$LOCALSTACK_ENDPOINT response.json"
