#!/bin/bash

# A script to destroy the application resources created by deploy.sh
# and provide instructions for the final terraform destroy command.

set -e

echo "🔥 Starting D'Agri Talk Manual Destruction..."

# --- Configuration (should match deploy.sh and your environment) ---
CLUSTER_NAME="dagri-talk-dev-cluster"
ALB_NAME="dagri-talk-dev-alb"
BACKEND_SERVICE_NAME="dagri-talk-backend-dev"
FRONTEND_SERVICE_NAME="dagri-talk-frontend-dev"
BACKEND_TG_NAME="dagri-talk-backend-dev-tg"
FRONTEND_TG_NAME="dagri-talk-frontend-dev-tg"

# --- 1. Delete ECS Services ---
# We must scale down services to 0 and wait for them to drain before deleting.
echo
echo "--- Deleting ECS Services ---"
echo "Scaling down and deleting service: $BACKEND_SERVICE_NAME"
aws ecs update-service --cluster $CLUSTER_NAME --service $BACKEND_SERVICE_NAME --desired-count 0 >/dev/null || echo "Service $BACKEND_SERVICE_NAME not found."

echo "Scaling down and deleting service: $FRONTEND_SERVICE_NAME"
aws ecs update-service --cluster $CLUSTER_NAME --service $FRONTEND_SERVICE_NAME --desired-count 0 >/dev/null || echo "Service $FRONTEND_SERVICE_NAME not found."

echo "Waiting for services to become inactive..."
aws ecs wait services-inactive --cluster $CLUSTER_NAME --services $BACKEND_SERVICE_NAME $FRONTEND_SERVICE_NAME

aws ecs delete-service --cluster $CLUSTER_NAME --service $BACKEND_SERVICE_NAME --force >/dev/null || echo "Service $BACKEND_SERVICE_NAME already deleted."
aws ecs delete-service --cluster $CLUSTER_NAME --service $FRONTEND_SERVICE_NAME --force >/dev/null || echo "Service $FRONTEND_SERVICE_NAME already deleted."
echo "Services deleted."

# --- 2. Delete Application Load Balancer ---
echo
echo "--- Deleting Application Load Balancer ---"
ALB_ARN=$(aws elbv2 describe-load-balancers --names $ALB_NAME --query 'LoadBalancers[0].LoadBalancerArn' --output text 2>/dev/null || true)
if [ -n "$ALB_ARN" ] && [ "$ALB_ARN" != "None" ]; then
    echo "Deleting ALB: $ALB_NAME ($ALB_ARN)"
    aws elbv2 delete-load-balancer --load-balancer-arn $ALB_ARN
    echo "Waiting for ALB to be deleted..."
    aws elbv2 wait load-balancers-deleted --load-balancer-arns "$ALB_ARN"
else
    echo "ALB $ALB_NAME not found."
fi

# --- 3. Delete Target Groups ---
echo
echo "--- Deleting Target Groups ---"
BACKEND_TG_ARN=$(aws elbv2 describe-target-groups --names $BACKEND_TG_NAME --query 'TargetGroups[0].TargetGroupArn' --output text 2>/dev/null || true)
if [ -n "$BACKEND_TG_ARN" ] && [ "$BACKEND_TG_ARN" != "None" ]; then
    echo "Deleting Target Group: $BACKEND_TG_NAME"
    aws elbv2 delete-target-group --target-group-arn $BACKEND_TG_ARN
else
    echo "Target Group $BACKEND_TG_NAME not found."
fi

FRONTEND_TG_ARN=$(aws elbv2 describe-target-groups --names $FRONTEND_TG_NAME --query 'TargetGroups[0].TargetGroupArn' --output text 2>/dev/null || true)
if [ -n "$FRONTEND_TG_ARN" ] && [ "$FRONTEND_TG_ARN" != "None" ]; then
    echo "Deleting Target Group: $FRONTEND_TG_NAME"
    aws elbv2 delete-target-group --target-group-arn $FRONTEND_TG_ARN
else
    echo "Target Group $FRONTEND_TG_NAME not found."
fi

# --- 4. Delete ECS Cluster ---
echo
echo "--- Deleting ECS Cluster ---"
if aws ecs describe-clusters --clusters $CLUSTER_NAME --query 'clusters[?status==`ACTIVE`]' --output text | grep -q $CLUSTER_NAME; then
    echo "Deleting ECS Cluster: $CLUSTER_NAME"
    aws ecs delete-cluster --cluster $CLUSTER_NAME >/dev/null
else
    echo "ECS Cluster $CLUSTER_NAME not found or already inactive."
fi

echo
echo "✅ Manual application resource cleanup complete."
echo "You can now destroy the underlying infrastructure managed by Terraform."
echo "Navigate to 'terraform/environments/dev' and run: terraform destroy"
echo
echo "⚠️ If 'terraform destroy' fails on ECR repositories, run 'deployment/cleanup-ecr.sh dagri-talk-dev' to fix it."