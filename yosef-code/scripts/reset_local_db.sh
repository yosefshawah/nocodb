#!/bin/bash

# Local database reset script for NocoDB tests
# This script copies the backup database to restore clean state

set -e  # Exit on any error

# Configuration
DB_PATH="./nocodb/noco.db"
BACKUP_PATH="./nocodb/noco.db.bak"
CONTAINER_NAME="noco"

echo "🔄 Starting local database reset..."

# Check if backup file exists
if [ ! -f "$BACKUP_PATH" ]; then
    echo "❌ Error: Backup file not found at $BACKUP_PATH"
    echo "Please ensure noco.db.bak exists in the nocodb directory"
    exit 1
fi

# Check if Docker container is running
if ! docker ps --format 'table {{.Names}}' | grep -q "^${CONTAINER_NAME}$"; then
    echo "⚠️  Container $CONTAINER_NAME is not running. Starting it..."
    docker-compose up -d
    echo "⏳ Waiting for container to start..."
    sleep 3
else
    echo "📦 Container $CONTAINER_NAME is already running"
fi

# Stop the container temporarily to safely replace the database
echo "⏸️  Stopping container for database replacement..."
docker-compose stop noco

# Copy backup to main database
echo "📋 Copying backup database to active database..."
cp "$BACKUP_PATH" "$DB_PATH"

if [ $? -eq 0 ]; then
    echo "✅ Database backup restored successfully"
else
    echo "❌ Error: Failed to copy backup database"
    exit 1
fi

# Start the container again
echo "▶️  Starting container with fresh database..."
docker-compose start noco

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
