#!/bin/bash
# D'Agri Talk - Development Environment Script

set -e

echo "🚀 Starting D'Agri Talk Development Environment..."

# Load development environment
export $(cat .env.development | grep -v '#' | xargs)

# Start services
docker compose up --build -d

echo "✅ Development environment started!"
echo "🌐 Frontend: http://localhost:3000"
echo "🔧 Backend API: http://localhost:5001"
echo "🗄️ Database: localhost:5432"
echo "📊 Logs: npm run logs"