#!/bin/bash
# Script to optimize nginx configuration for image caching
# Run this on the EC2 server

NGINX_CONFIG="/etc/nginx/sites-enabled/api-smartedu"
BACKUP_FILE="/etc/nginx/sites-enabled/api-smartedu.backup.$(date +%Y%m%d_%H%M%S)"

echo "Backing up nginx config to $BACKUP_FILE"
sudo cp $NGINX_CONFIG $BACKUP_FILE

echo "Updating nginx config for image caching..."

# Create a temporary file with optimized config
sudo sed -i.tmp '/location \/media\/ {/,/}/ {
    /location \/media\/ {/a\
        expires 30d;\
        add_header Cache-Control "public, immutable";\
        access_log off;
}' $NGINX_CONFIG

# Test nginx configuration
echo "Testing nginx configuration..."
sudo nginx -t

if [ $? -eq 0 ]; then
    echo "Nginx config is valid. Reloading nginx..."
    sudo systemctl reload nginx
    echo "Done! Media files will now be cached for 30 days."
else
    echo "Error: Nginx config test failed. Restoring backup..."
    sudo cp $BACKUP_FILE $NGINX_CONFIG
    echo "Backup restored. Please check the config manually."
    exit 1
fi

