#!/bin/bash
set -e

echo "🚀 Starting deployment..."

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Check if .env exists
if [ ! -f .env ]; then
    echo -e "${RED}❌ Error: .env file not found!${NC}"
    echo -e "${YELLOW}Please copy .env.production.example to .env and configure it.${NC}"
    exit 1
fi

# Check if required env vars are set
if ! grep -q "SECRET_KEY=" .env || grep -q "your-super-secret-key" .env; then
    echo -e "${RED}❌ Error: SECRET_KEY not configured in .env${NC}"
    exit 1
fi

echo -e "${GREEN}✓ Environment file validated${NC}"

# Create required directories
echo "📁 Creating required directories..."
mkdir -p logs runtime_logs media staticfiles
chmod 777 logs runtime_logs media

echo -e "${GREEN}✓ Directories created${NC}"

# Pull latest code (if in git repo)
if [ -d .git ]; then
    echo "📥 Pulling latest code..."
    git stash
    git pull origin develop
    echo -e "${GREEN}✓ Code updated${NC}"
fi

# Stop existing containers
echo "🛑 Stopping existing containers..."
docker compose down

# Build new images
echo "🔨 Building Docker images..."
docker compose build --no-cache

# Start services
echo "🚀 Starting services..."
docker compose up -d

# Wait for services to be healthy
echo "⏳ Waiting for services to be ready..."
sleep 20

# Check if services are running
if docker compose ps | grep -q "Up"; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    echo ""
    echo "Services status:"
    docker compose ps
    echo ""
    echo "View logs with: docker compose logs -f web"
else
    echo -e "${RED}❌ Deployment failed! Check logs with: docker compose logs${NC}"
    exit 1
fi
