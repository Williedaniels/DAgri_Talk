#!/bin/bash
# D'Agri Talk - Build Script for Containerization

set -e

echo "🚀 Building D'Agri Talk Containers..."

# Build all services with docker-compose
echo "📦 Building all services with docker-compose..."
docker compose --env-file .env.development build --no-cache


echo "✅ Build completed successfully!"
echo "🎯 Next steps:"
echo "   - Run 'npm run dev' to start development environment"
echo "   - Run 'npm run prod' to start production environment"