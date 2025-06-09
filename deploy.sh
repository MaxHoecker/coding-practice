#!/bin/bash

# Exit on any error
set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[INFO]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "Starting deployment..."

# Check if running as root or with sudo
if [[ $EUID -ne 0 ]]; then
    print_error "This script must be run as root or with sudo"
    exit 1
fi

# Verify required directories exist
if [[ ! -d "nginx" ]]; then
    print_error "nginx/ directory not found in current directory"
    exit 1
fi

if [[ ! -f "nginx/nginx.conf" ]]; then
    print_error "nginx/nginx.conf file not found"
    exit 1
fi

if [[ ! -d "frontend" ]]; then
    print_error "frontend/ directory not found in current directory"
    exit 1
fi

# Create conf.d directory if it doesn't exist
print_status "Ensuring /etc/nginx/conf.d/ directory exists..."
mkdir -p /etc/nginx/conf.d/

# Backup existing nginx config
print_status "Backing up existing nginx configuration..."
if [[ -f "/etc/nginx/conf.d/codingPractice.conf" ]]; then
    cp /etc/nginx/conf.d/codingPractice.conf /etc/nginx/conf.d/codingPractice.conf.backup.$(date +%Y%m%d_%H%M%S)
    print_status "Backup created: /etc/nginx/conf.d/codingPractice.conf.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Copy nginx configuration
print_status "Copying nginx configuration..."
cp nginx/nginx.conf /etc/nginx/conf.d/codingPractice.conf
print_status "Nginx configuration copied to /etc/nginx/conf.d/codingPractice.conf"

# Test nginx configuration
print_status "Testing nginx configuration..."
if nginx -t; then
    print_status "Nginx configuration test passed"
else
    print_error "Nginx configuration test failed"
    # Restore backup if it exists
    if [[ -f "/etc/nginx/conf.d/codingPractice.conf.backup.$(date +%Y%m%d_%H%M%S)" ]]; then
        print_warning "Restoring previous nginx configuration..."
        cp /etc/nginx/conf.d/codingPractice.conf.backup.$(date +%Y%m%d_%H%M%S) /etc/nginx/conf.d/codingPractice.conf
    fi
    exit 1
fi

# Create destination directory if it doesn't exist
print_status "Ensuring destination directory exists..."
mkdir -p /usr/share/nginx/frontend

# Backup existing frontend files
if [[ -d "/usr/share/nginx/frontend" ]] && [[ "$(ls -A /usr/share/nginx/frontend)" ]]; then
    print_status "Backing up existing frontend files..."
    mv /usr/share/nginx/frontend /usr/share/nginx/frontend.backup.$(date +%Y%m%d_%H%M%S)
    mkdir -p /usr/share/nginx/frontend
    print_status "Frontend backup created: /usr/share/nginx/frontend.backup.$(date +%Y%m%d_%H%M%S)"
fi

# Copy frontend files
print_status "Copying frontend files..."
cp -r frontend/* /usr/share/nginx/frontend/
print_status "Frontend files copied to /usr/share/nginx/frontend/"

# Set proper permissions
print_status "Setting proper permissions..."
chown -R nginx:nginx /usr/share/nginx/frontend/ 2>/dev/null || chown -R www-data:www-data /usr/share/nginx/frontend/ 2>/dev/null || true
chmod -R 755 /usr/share/nginx/frontend/

# Handle systemd service
SERVICE_SOURCE="/home/practice-app/coding-practice/backend/fastapi-backend.service"
SERVICE_DEST="/etc/systemd/system/fastapi-backend.service"

if [[ -f "$SERVICE_SOURCE" ]]; then
    print_status "Backing up existing systemd service file..."
    if [[ -f "$SERVICE_DEST" ]]; then
        cp "$SERVICE_DEST" "${SERVICE_DEST}.backup.$(date +%Y%m%d_%H%M%S)"
        print_status "Service backup created: ${SERVICE_DEST}.backup.$(date +%Y%m%d_%H%M%S)"
    fi

    print_status "Copying systemd service file..."
    cp "$SERVICE_SOURCE" "$SERVICE_DEST"
    print_status "Service file copied to $SERVICE_DEST"

    print_status "Reloading systemd daemon..."
    systemctl daemon-reload

    print_status "Restarting fastapi-backend service..."
    systemctl restart fastapi-backend

    print_status "Enabling fastapi-backend service for auto-start..."
    systemctl enable fastapi-backend

    # Check service status
    if systemctl is-active --quiet fastapi-backend; then
        print_status "FastAPI backend service is running"
    else
        print_warning "FastAPI backend service may not be running properly"
        systemctl status fastapi-backend --no-pager
    fi
else
    print_warning "SystemD service file not found at $SERVICE_SOURCE - skipping service deployment"
fi

# Reload nginx
print_status "Reloading nginx..."
if systemctl reload nginx; then
    print_status "Nginx reloaded successfully"
else
    print_error "Failed to reload nginx"
    exit 1
fi

# Verify nginx is running
if systemctl is-active --quiet nginx; then
    print_status "Nginx is running"
else
    print_warning "Nginx may not be running properly"
    systemctl status nginx
fi

print_status "Deployment completed successfully!"
print_status "Frontend files deployed to: /usr/share/nginx/frontend/"
print_status "Nginx configuration updated at: /etc/nginx/conf.d/codingPractice.conf"
print_status "FastAPI backend service deployed and started"