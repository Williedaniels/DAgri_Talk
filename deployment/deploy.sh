#!/bin/bash
set -e

echo "🚀 Starting D'Agri Talk Manual Deployment..."

# Get Terraform outputs
cd terraform/environments/dev
export VPC_ID=$(terraform output -raw vpc_id)
export PUBLIC_SUBNET_IDS=$(terraform output -json public_subnet_ids | jq -r '.[]' | tr '\n' ',' | sed 's/,$//')
export PRIVATE_SUBNET_IDS=$(terraform output -json private_subnet_ids | jq -r '.[]' | tr '\n' ',' | sed 's/,$//')
export ECS_SECURITY_GROUP_ID=$(terraform output -raw ecs_security_group_id)
export ALB_SECURITY_GROUP_ID=$(terraform output -raw alb_security_group_id)
export BACKEND_ECR_URL=$(terraform output -raw backend_ecr_repository_url)
export FRONTEND_ECR_URL=$(terraform output -raw frontend_ecr_repository_url)
export DB_SECRET_ARN=$(terraform output -raw database_credentials_secret_arn)
export AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

cd ../../..

# --- Validate Terraform Outputs ---
if [ -z "$VPC_ID" ] || [ -z "$PUBLIC_SUBNET_IDS" ] || [ -z "$ECS_SECURITY_GROUP_ID" ] || [ -z "$BACKEND_ECR_URL" ] || [ -z "$FRONTEND_ECR_URL" ] || [ -z "$DB_SECRET_ARN" ]; then
    echo "❌ Error: Failed to retrieve one or more required Terraform outputs."
    echo "Please ensure all required outputs are defined in your root Terraform configuration (e.g., 'terraform/environments/dev/outputs.tf')"
    echo "and that you have run 'terraform apply' to update the state file."
    exit 1
fi

echo "📋 Infrastructure Details:"
echo "VPC ID: $VPC_ID"
echo "Public Subnets: $PUBLIC_SUBNET_IDS"
echo "Private Subnets: $PRIVATE_SUBNET_IDS"
echo "Backend ECR: $BACKEND_ECR_URL"
echo "Frontend ECR: $FRONTEND_ECR_URL"

# 1. Create ECS Cluster
echo "🏗️ Creating ECS Cluster..."
aws ecs create-cluster --cluster-name dagri-talk-dev-cluster

# 2. Create Application Load Balancer
echo "🔗 Creating Application Load Balancer..."
ALB_ARN=$(aws elbv2 create-load-balancer \
    --name dagri-talk-dev-alb \
    --subnets $(echo $PUBLIC_SUBNET_IDS | tr ',' ' ') \
    --security-groups $ALB_SECURITY_GROUP_ID \
    --scheme internet-facing \
    --type application \
    --ip-address-type ipv4 \
    --tags Key=Project,Value="DAgri Talk" Key=Environment,Value=dev \
    --query 'LoadBalancers[0].LoadBalancerArn' --output text)

# Get ALB DNS name
ALB_DNS_NAME=$(aws elbv2 describe-load-balancers --load-balancer-arns $ALB_ARN --query 'LoadBalancers[0].DNSName' --output text)
echo "🌐 ALB DNS Name: $ALB_DNS_NAME"

# 3. Create Target Groups
echo "🎯 Creating Target Groups..."
BACKEND_TG_ARN=$(aws elbv2 create-target-group \
    --name dagri-talk-backend-dev-tg \
    --protocol HTTP \
    --port 5000 \
    --vpc-id $VPC_ID \
    --target-type ip \
    --health-check-path /api/health \
    --health-check-interval-seconds 30 \
    --health-check-timeout-seconds 5 \
    --healthy-threshold-count 2 \
    --unhealthy-threshold-count 3 \
    --query 'TargetGroups[0].TargetGroupArn' --output text)

FRONTEND_TG_ARN=$(aws elbv2 create-target-group \
    --name dagri-talk-frontend-dev-tg \
    --protocol HTTP \
    --port 80 \
    --vpc-id $VPC_ID \
    --target-type ip \
    --health-check-path /health \
    --health-check-interval-seconds 30 \
    --health-check-timeout-seconds 5 \
    --healthy-threshold-count 2 \
    --unhealthy-threshold-count 3 \
    --query 'TargetGroups[0].TargetGroupArn' --output text)

# 4. Create ALB Listeners
echo "👂 Creating ALB Listeners..."
aws elbv2 create-listener \
    --load-balancer-arn $ALB_ARN \
    --protocol HTTP \
    --port 80 \
    --default-actions Type=forward,TargetGroupArn=$FRONTEND_TG_ARN

# Create listener rule for API traffic
aws elbv2 create-rule \
    --listener-arn $(aws elbv2 describe-listeners --load-balancer-arn $ALB_ARN --query 'Listeners[0].ListenerArn' --output text) \
    --priority 100 \
    --conditions Field=path-pattern,Values="/api/*" \
    --actions Type=forward,TargetGroupArn=$BACKEND_TG_ARN

# 5. Update task definitions with actual values
echo "📝 Updating Task Definitions..."
sed -i '' "s/ACCOUNT_ID/$AWS_ACCOUNT_ID/g" deployment/backend-task-definition.json
sed -i '' "s|BACKEND_ECR_URL|$BACKEND_ECR_URL|g" deployment/backend-task-definition.json
sed -i '' "s|DATABASE_CREDENTIALS_SECRET_ARN|$DB_SECRET_ARN|g" deployment/backend-task-definition.json

sed -i '' "s/ACCOUNT_ID/$AWS_ACCOUNT_ID/g" deployment/frontend-task-definition.json
sed -i '' "s|FRONTEND_ECR_URL|$FRONTEND_ECR_URL|g" deployment/frontend-task-definition.json
sed -i '' "s|ALB_DNS_NAME|$ALB_DNS_NAME|g" deployment/frontend-task-definition.json

# 6. Register Task Definitions
echo "📋 Registering Task Definitions..."
BACKEND_TASK_DEF_ARN=$(aws ecs register-task-definition --cli-input-json file://deployment/backend-task-definition.json --query 'taskDefinition.taskDefinitionArn' --output text)
FRONTEND_TASK_DEF_ARN=$(aws ecs register-task-definition --cli-input-json file://deployment/frontend-task-definition.json --query 'taskDefinition.taskDefinitionArn' --output text)

# 7. Create ECS Services
echo "🚀 Creating ECS Services..."
aws ecs create-service \
    --cluster dagri-talk-dev-cluster \
    --service-name dagri-talk-backend-dev \
    --task-definition $BACKEND_TASK_DEF_ARN \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[$PRIVATE_SUBNET_IDS],securityGroups=[$ECS_SECURITY_GROUP_ID],assignPublicIp=DISABLED}" \
    --load-balancers targetGroupArn=$BACKEND_TG_ARN,containerName=dagri-talk-backend,containerPort=5000

aws ecs create-service \
    --cluster dagri-talk-dev-cluster \
    --service-name dagri-talk-frontend-dev \
    --task-definition $FRONTEND_TASK_DEF_ARN \
    --desired-count 1 \
    --launch-type FARGATE \
    --network-configuration "awsvpcConfiguration={subnets=[$PRIVATE_SUBNET_IDS],securityGroups=[$ECS_SECURITY_GROUP_ID],assignPublicIp=DISABLED}" \
    --load-balancers targetGroupArn=$FRONTEND_TG_ARN,containerName=dagri-talk-frontend,containerPort=80

echo "✅ Deployment Complete!"
echo "🌐 Your D'Agri Talk application will be available at: http://$ALB_DNS_NAME"
echo "📊 Monitor deployment status in AWS ECS Console"
echo "📝 Check logs in CloudWatch: /ecs/dagri-talk-backend-dev and /ecs/dagri-talk-frontend-dev"