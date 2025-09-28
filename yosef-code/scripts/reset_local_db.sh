#!/bin/bash

# Local database reset script for NocoDB tests
# This script copies the backup database to restore clean state

set -e  # Exit on any error

# Configuration
DB_PATH="./nocodb/noco.db"
BACKUP_PATH="./nocodb/noco.db.bak"
CONTAINER_NAME="noco"

echo "🔄 Starting local database reset..."
echo "📍 Working directory: $(pwd)"
echo "📍 Script location: $(dirname "$0")"
echo "📍 Target DB path: $(realpath "$DB_PATH" 2>/dev/null || echo "$DB_PATH")"
echo "📍 Backup DB path: $(realpath "$BACKUP_PATH" 2>/dev/null || echo "$BACKUP_PATH")"

# Check if backup file exists
if [ ! -f "$BACKUP_PATH" ]; then
    echo "❌ Error: Backup file not found at $BACKUP_PATH"
    echo "Current directory contents:"
    ls -la ./ || true
    echo "Nocodb directory contents:"
    ls -la ./nocodb/ || true
    echo "Please ensure noco.db.bak exists in the nocodb directory"
    exit 1
fi

# Check if docker-compose is available
if command -v docker-compose >/dev/null 2>&1; then
    DOCKER_COMPOSE="docker-compose"
    echo "🐳 Using docker-compose command"
elif command -v docker >/dev/null 2>&1 && docker compose version >/dev/null 2>&1; then
    DOCKER_COMPOSE="docker compose"
    echo "🐳 Using docker compose command"
else
    echo "❌ Error: Neither docker-compose nor docker compose is available"
    exit 1
fi

# Check Docker status
echo "🔍 Checking Docker status..."
if ! docker ps >/dev/null 2>&1; then
    echo "❌ Error: Docker is not running or not accessible"
    exit 1
fi

# Check if our container exists (running or stopped)
if docker ps -a --format 'table {{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "📦 Container $CONTAINER_NAME exists"
else
    echo "📦 Container $CONTAINER_NAME doesn't exist, will be created"
fi

# Stop and remove containers completely to avoid conflicts
echo "⏸️  Stopping and removing containers for database replacement..."
$DOCKER_COMPOSE down --remove-orphans

# Remove any leftover containers with the same name
echo "🧹 Cleaning up any leftover containers..."
docker rm -f "$CONTAINER_NAME" 2>/dev/null || true

# Copy backup to main database
echo "📋 Copying backup database to active database..."
cp "$BACKUP_PATH" "$DB_PATH"

if [ $? -eq 0 ]; then
    echo "✅ Database backup restored successfully"
else
    echo "❌ Error: Failed to copy backup database"
    exit 1
fi

# Start the container stack again with clean state
echo "▶️  Starting containers with fresh database..."
$DOCKER_COMPOSE up -d --force-recreate

# Wait for the service to be healthy
echo "⏳ Waiting for NocoDB to be ready..."
sleep 5

# Health check loop
for i in {1..30}; do
    if curl -sSf -o /dev/null http://localhost:8080/ 2>/dev/null; then
        echo "✅ NocoDB is ready and responding"
        break
    fi
    if [ $i -eq 30 ]; then
        echo "❌ Error: NocoDB failed to start within 60 seconds"
        exit 1
    fi
    echo "⏳ Waiting for NocoDB... ($i/30)"
    sleep 2
done

echo "🎉 Local database reset completed successfully!"
