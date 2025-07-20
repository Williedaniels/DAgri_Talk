#!/bin/bash
set -e

echo "🚀 Fixing D'Agri Talk 503 Service Unavailable Error..."

# Get current directory
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_DIR="$(dirname "$SCRIPT_DIR")"

echo "📁 Project directory: $PROJECT_DIR"
echo "📁 Deployment directory: $SCRIPT_DIR"

# Step 1: Get database connection details
echo ""
echo "🔍 Step 1: Getting database connection details..."
chmod +x "$SCRIPT_DIR/get-db-connection.sh"
source "$SCRIPT_DIR/get-db-connection.sh"

# Step 2: Update task definitions with correct database URL
echo ""
echo "🔧 Step 2: Updating task definitions..."

# Backup original files
cp "$SCRIPT_DIR/backend-task-definition.json" "$SCRIPT_DIR/backend-task-definition.json.backup"
cp "$SCRIPT_DIR/frontend-task-definition.json" "$SCRIPT_DIR/frontend-task-definition.json.backup"

# Update backend task definition with correct database URL
if [ ! -z "$DATABASE_URL" ]; then
    echo "📝 Updating backend task definition with database URL..."
    sed -i '' "s|sqlite:///dagri_talk_dev.db|$DATABASE_URL|g" "$SCRIPT_DIR/backend-task-definition.json"
fi

# Step 3: Stop current services
echo ""
echo "🛑 Step 3: Stopping current ECS services..."
aws ecs update-service \
    --cluster dagri-talk-dev-cluster \
    --service dagri-talk-backend-dev \
    --desired-count 0 || echo "⚠️ Backend service not found or already stopped"

aws ecs update-service \
    --cluster dagri-talk-dev-cluster \
    --service dagri-talk-frontend-dev \
    --desired-count 0 || echo "⚠️ Frontend service not found or already stopped"

echo "⏳ Waiting for services to stop..."
sleep 30

# Step 4: Register new task definitions
echo ""
echo "📋 Step 4: Registering updated task definitions..."

BACKEND_TASK_DEF_ARN=$(aws ecs register-task-definition \
    --cli-input-json file://"$SCRIPT_DIR/backend-task-definition.json" \
    --query 'taskDefinition.taskDefinitionArn' \
    --output text)

FRONTEND_TASK_DEF_ARN=$(aws ecs register-task-definition \
    --cli-input-json file://"$SCRIPT_DIR/frontend-task-definition.json" \
    --query 'taskDefinition.taskDefinitionArn' \
    --output text)

echo "✅ Backend task definition: $BACKEND_TASK_DEF_ARN"
echo "✅ Frontend task definition: $FRONTEND_TASK_DEF_ARN"

# Step 5: Update services with new task definitions
echo ""
echo "🔄 Step 5: Updating ECS services with new task definitions..."

aws ecs update-service \
    --cluster dagri-talk-dev-cluster \
    --service dagri-talk-backend-dev \
    --task-definition "$BACKEND_TASK_DEF_ARN" \
    --desired-count 1

aws ecs update-service \
    --cluster dagri-talk-dev-cluster \
    --service dagri-talk-frontend-dev \
    --task-definition "$FRONTEND_TASK_DEF_ARN" \
    --desired-count 1

# Step 6: Wait for services to stabilize
echo ""
echo "⏳ Step 6: Waiting for services to stabilize..."
echo "This may take 3-5 minutes..."

aws ecs wait services-stable \
    --cluster dagri-talk-dev-cluster \
    --services dagri-talk-backend-dev dagri-talk-frontend-dev

# Step 7: Check service health
echo ""
echo "🏥 Step 7: Checking service health..."

# Get ALB DNS name
ALB_DNS="dagri-talk-dev-alb-403835578.us-east-1.elb.amazonaws.com"

echo "🌐 Testing application endpoints..."
echo "Frontend: http://$ALB_DNS"
echo "Backend Health: http://$ALB_DNS/api/health"

# Test health endpoint
echo ""
echo "🔍 Testing backend health endpoint..."
for i in {1..10}; do
    if curl -f -s "http://$ALB_DNS/api/health" > /dev/null; then
        echo "✅ Backend health check passed!"
        break
    else
        echo "⏳ Attempt $i/10: Backend not ready yet, waiting 30 seconds..."
        sleep 30
    fi
done

# Test frontend
echo ""
echo "🔍 Testing frontend..."
for i in {1..5}; do
    if curl -f -s "http://$ALB_DNS" > /dev/null; then
        echo "✅ Frontend is responding!"
        break
    else
        echo "⏳ Attempt $i/5: Frontend not ready yet, waiting 30 seconds..."
        sleep 30
    fi
done

echo ""
echo "🎉 Deployment fix complete!"
echo "🌐 Your application should now be available at: http://$ALB_DNS"
echo ""
echo "📊 To monitor the deployment:"
echo "aws ecs describe-services --cluster dagri-talk-dev-cluster --services dagri-talk-backend-dev dagri-talk-frontend-dev"
echo ""
echo "📝 To check logs:"
echo "aws logs tail /ecs/dagri-talk-backend-dev --follow"
echo "aws logs tail /ecs/dagri-talk-frontend-dev --follow"