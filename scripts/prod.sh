#!/bin/bash
# D'Agri Talk - Production Environment Script

set -e

echo "🚀 Starting D'Agri Talk Production Environment..."

# Load production environment
export $(cat .env.production | grep -v '#' | xargs)

# Start production services
docker compose -f /Users/williedaniels/DAgri_Talk/docker-compose.prod.yml up -d

echo "✅ Production environment started!"
echo "🌐 Application: http://localhost"
echo "📊 Logs: npm run logs-prod"