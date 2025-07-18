#!/bin/bash

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
AWS_ACCOUNT_ID="103670753244"
AWS_REGION="ap-southeast-2"
BACKEND_REPO_NAME="dagri-talk-dev-backend"
FRONTEND_REPO_NAME="dagri-talk-dev-frontend"

# Construct the full ECR URLs
BACKEND_ECR_URL="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${BACKEND_REPO_NAME}"
FRONTEND_ECR_URL="${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com/${FRONTEND_REPO_NAME}"

# --- Authenticate with AWS ECR ---
echo "Authenticating Docker with Amazon ECR in region ${AWS_REGION}..."
aws ecr get-login-password --region "${AWS_REGION}" | docker login --username AWS --password-stdin "${AWS_ACCOUNT_ID}.dkr.ecr.${AWS_REGION}.amazonaws.com"
echo "Authentication successful."

# --- Build Docker Images ---
echo "Building backend Docker image..."
docker build -t dagri-talk-backend:latest ./backend

echo "Building frontend Docker image..."
docker build -t dagri-talk-frontend:latest ./frontend

# --- Backend Deployment ---
echo "--- Deploying Backend ---"
BACKEND_TAG="dev-$(date +%Y%m%d-%H%M%S)"
echo "Tagging backend image with: latest and ${BACKEND_TAG}"
docker tag dagri-talk-backend:latest "${BACKEND_ECR_URL}:latest"
docker tag dagri-talk-backend:latest "${BACKEND_ECR_URL}:${BACKEND_TAG}"

echo "Pushing backend images to ECR..."
docker push "${BACKEND_ECR_URL}:latest"
docker push "${BACKEND_ECR_URL}:${BACKEND_TAG}"

# --- Frontend Deployment ---
echo "--- Deploying Frontend ---"
FRONTEND_TAG="dev-$(date +%Y%m%d-%H%M%S)"
echo "Tagging frontend image with: latest and ${FRONTEND_TAG}"
docker tag dagri-talk-frontend:latest "${FRONTEND_ECR_URL}:latest"
docker tag dagri-talk-frontend:latest "${FRONTEND_ECR_URL}:${FRONTEND_TAG}"

echo "Pushing frontend images to ECR..."
docker push "${FRONTEND_ECR_URL}:latest"
docker push "${FRONTEND_ECR_URL}:${FRONTEND_TAG}"

echo "✅ Deployment to ECR complete!"