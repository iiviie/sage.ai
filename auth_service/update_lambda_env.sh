#!/bin/bash

# ============================================================================
# Update Lambda Environment Variables
# ============================================================================
# This script updates the DATABASE_URL to use the correct host IP
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
NC='\033[0m'

echo -e "${BLUE}🔧 Updating Lambda Environment Variables${NC}"
echo ""

# Try to detect host IP
echo -e "${YELLOW}Detecting host IP address...${NC}"

# Method 1: Try to get the Docker bridge IP (works in most cases)
DOCKER_BRIDGE_IP="172.17.0.1"

# Method 2: Try to get actual host IP
HOST_IP=$(ip route get 1.1.1.1 2>/dev/null | grep -oP 'src \K\S+' || echo "")

if [ -z "$HOST_IP" ]; then
    # Fallback: try hostname -I
    HOST_IP=$(hostname -I 2>/dev/null | awk '{print $1}' || echo "")
fi

echo ""
echo -e "${YELLOW}Available options:${NC}"
echo "  1. Use Docker bridge IP: $DOCKER_BRIDGE_IP (recommended for Docker)"
if [ -n "$HOST_IP" ]; then
    echo "  2. Use detected host IP: $HOST_IP"
fi
echo "  3. Enter custom IP address"
echo ""

read -p "Select option (1-3): " CHOICE

case $CHOICE in
    1)
        DB_HOST="$DOCKER_BRIDGE_IP"
        ;;
    2)
        if [ -n "$HOST_IP" ]; then
            DB_HOST="$HOST_IP"
        else
            echo "Could not detect host IP. Please enter manually."
            read -p "Enter PostgreSQL host IP: " DB_HOST
        fi
        ;;
    3)
        read -p "Enter PostgreSQL host IP: " DB_HOST
        ;;
    *)
        echo "Invalid choice. Using Docker bridge IP as default."
        DB_HOST="$DOCKER_BRIDGE_IP"
        ;;
esac

DATABASE_URL="postgresql://sage_user:sage_password@${DB_HOST}:5432/sage_auth_db"

echo ""
echo -e "${YELLOW}Updating Lambda environment variables...${NC}"
echo "   DATABASE_URL: $DATABASE_URL"

aws --profile "$AWS_PROFILE" lambda update-function-configuration \
    --function-name "$FUNCTION_NAME" \
    --environment "Variables={
        ENVIRONMENT=development,
        DEBUG=true,
        DATABASE_URL=${DATABASE_URL},
        SECRET_KEY=your-secret-key-change-this,
        GOOGLE_CLIENT_ID=dummy,
        GOOGLE_CLIENT_SECRET=dummy,
        GOOGLE_REDIRECT_URI=http://localhost:4566
    }" \
    --endpoint-url="$LOCALSTACK_ENDPOINT" \
    --region "$REGION" > /dev/null

echo -e "${GREEN}✅ Environment variables updated successfully!${NC}"
echo ""
echo "Test the database connection:"
echo "  ./test_lambda.sh"
