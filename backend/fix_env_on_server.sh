#!/bin/bash

# Script to fix .env file on EC2 server
# This fixes the typo in ALLOWED_HOSTS and removes duplicate domains

echo "Fixing .env file on server..."

# Backup current .env
cp .env .env.backup.$(date +%Y%m%d_%H%M%S)

# Fix ALLOWED_HOSTS - remove typo 'api.smarledu.click'
sed -i 's/ALLOWED_HOSTS=127.0.0.1,localhost,api.smartedu.click,api.smarledu.click/ALLOWED_HOSTS=127.0.0.1,localhost,api.smartedu.click/' .env

# Fix CSRF_TRUSTED_ORIGINS - remove typo domains
sed -i 's|CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://api.smarledu.click,https://www.smarledu.click,https://smartedu.click|CSRF_TRUSTED_ORIGINS=http://localhost:8000,http://localhost:5173,http://127.0.0.1:5173,https://api.smartedu.click,https://smartedu.click,https://www.smartedu.click|' .env

# Fix CORS_ALLOWED_ORIGINS - remove typo domains
sed -i 's|CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173,https://smartedu.click,https://www.smartedu.click,https://smarledu.click,https://www.smarledu.click|CORS_ALLOWED_ORIGINS=http://localhost:3000,http://localhost:5173,http://127.0.0.1:5173,https://smartedu.click,https://www.smartedu.click|' .env

echo "✅ .env file has been fixed!"
echo ""
echo "Changes made:"
echo "1. Removed 'api.smarledu.click' from ALLOWED_HOSTS"
echo "2. Removed 'api.smarledu.click' and 'www.smarledu.click' from CSRF_TRUSTED_ORIGINS"
echo "3. Removed 'smarledu.click' and 'www.smarledu.click' from CORS_ALLOWED_ORIGINS"
echo ""
echo "Now restart Docker containers:"
echo "  docker compose -f docker-compose.prod.yml down"
echo "  docker compose -f docker-compose.prod.yml up -d"

