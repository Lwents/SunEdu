#!/bin/bash

# Script to deploy fix to EC2 server
# Run this from your local machine

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Deploy Fix to EC2 Server ===${NC}"
echo ""

# Check if SSH key and host are provided
if [ -z "$1" ] || [ -z "$2" ]; then
    echo -e "${RED}Usage: $0 <ssh-key-path> <ec2-host>${NC}"
    echo "Example: $0 ~/.ssh/my-key.pem ubuntu@ec2-xx-xx-xx-xx.compute.amazonaws.com"
    exit 1
fi

SSH_KEY="$1"
EC2_HOST="$2"
PROJECT_PATH="/home/ubuntu/SunEdu/backend"  # Adjust this path if needed

echo -e "${GREEN}Step 1: Connecting to EC2...${NC}"
ssh -i "$SSH_KEY" "$EC2_HOST" "cd $PROJECT_PATH && pwd"

if [ $? -ne 0 ]; then
    echo -e "${RED}Failed to connect to EC2. Please check your SSH key and host.${NC}"
    exit 1
fi

echo ""
echo -e "${GREEN}Step 2: Pulling latest code from develop branch...${NC}"
ssh -i "$SSH_KEY" "$EC2_HOST" "cd $PROJECT_PATH && git pull origin develop"

echo ""
echo -e "${GREEN}Step 3: Running fix script...${NC}"
ssh -i "$SSH_KEY" "$EC2_HOST" "cd $PROJECT_PATH && chmod +x fix_env_on_server.sh && ./fix_env_on_server.sh"

echo ""
echo -e "${GREEN}Step 4: Restarting Docker containers...${NC}"
ssh -i "$SSH_KEY" "$EC2_HOST" "cd $PROJECT_PATH && docker compose -f docker-compose.prod.yml down && docker compose -f docker-compose.prod.yml up -d"

echo ""
echo -e "${GREEN}Step 5: Waiting for containers to start (30 seconds)...${NC}"
sleep 30

echo ""
echo -e "${GREEN}Step 6: Checking container status...${NC}"
ssh -i "$SSH_KEY" "$EC2_HOST" "cd $PROJECT_PATH && docker compose -f docker-compose.prod.yml ps"

echo ""
echo -e "${GREEN}Step 7: Checking logs...${NC}"
ssh -i "$SSH_KEY" "$EC2_HOST" "cd $PROJECT_PATH && docker compose -f docker-compose.prod.yml logs --tail=50 web"

echo ""
echo -e "${GREEN}=== Deployment Complete! ===${NC}"
echo ""
echo "Please verify:"
echo "1. Visit https://api.smartedu.click/admin/ - should see Django admin login"
echo "2. Visit https://smartedu.click - should see your frontend"
echo ""
echo "If you still see errors, check logs with:"
echo "  ssh -i $SSH_KEY $EC2_HOST 'cd $PROJECT_PATH && docker compose -f docker-compose.prod.yml logs -f web'"

