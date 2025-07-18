#!/bin/bash

# An idempotent script to create the necessary IAM roles and policies for the D'Agri Talk ECS deployment.

set -e

# --- Configuration ---
AWS_REGION="ap-southeast-2"
TASK_EXECUTION_ROLE_NAME="ecsTaskExecutionRole"
TASK_ROLE_NAME="ecsTaskRole"
POLICY_NAME="DAgriTalkSecretsAccess"
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
POLICY_ARN="arn:aws:iam::${ACCOUNT_ID}:policy/${POLICY_NAME}"

ASSUME_ROLE_POLICY_DOCUMENT='{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": { "Service": "ecs-tasks.amazonaws.com" },
            "Action": "sts:AssumeRole"
        }
    ]
}'

SECRETS_POLICY_DOCUMENT='{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": "secretsmanager:GetSecretValue",
            "Resource": "arn:aws:secretsmanager:'"${AWS_REGION}"':'"${ACCOUNT_ID}"':secret:dagri-talk-*"
        }
    ]
}'

# --- Function to create role if it doesn't exist ---
create_role_if_not_exists() {
    local role_name=$1
    echo "--> Checking for IAM role: ${role_name}"
    if aws iam get-role --role-name "${role_name}" >/dev/null 2>&1; then
        echo "Role '${role_name}' already exists. Skipping creation."
    else
        echo "Creating role '${role_name}'..."
        aws iam create-role --role-name "${role_name}" --assume-role-policy-document "${ASSUME_ROLE_POLICY_DOCUMENT}" >/dev/null
    fi
}

echo "🚀 Starting IAM Role and Policy setup..."

# --- 1. ECS Task Execution Role ---
# This role is used by the ECS agent to pull ECR images and send logs to CloudWatch.
create_role_if_not_exists "${TASK_EXECUTION_ROLE_NAME}"
echo "Attaching AmazonECSTaskExecutionRolePolicy to ${TASK_EXECUTION_ROLE_NAME}..."
aws iam attach-role-policy --role-name "${TASK_EXECUTION_ROLE_NAME}" --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# --- 2. ECS Task Role ---
# This role is used by the application containers themselves to access other AWS services.
create_role_if_not_exists "${TASK_ROLE_NAME}"

# --- 3. Custom Policy for Secrets Manager ---
echo "--> Checking for IAM policy: ${POLICY_NAME}"
if aws iam get-policy --policy-arn "${POLICY_ARN}" >/dev/null 2>&1; then
    echo "Policy '${POLICY_NAME}' already exists. Skipping creation."
else
    echo "Creating policy '${POLICY_NAME}'..."
    aws iam create-policy \
        --policy-name "${POLICY_NAME}" \
        --policy-document "${SECRETS_POLICY_DOCUMENT}"
fi

# --- 4. Attach Secrets Policy to the Task Role ---
# The application (backend) needs permission to get secrets, so we attach it to the Task Role.
echo "Attaching ${POLICY_NAME} policy to ${TASK_ROLE_NAME}..."
aws iam attach-role-policy --role-name "${TASK_ROLE_NAME}" --policy-arn "${POLICY_ARN}"

# Incorrect attachment from original script - attaching secrets access to the execution role is not needed.
# The line below is what you had, which should be corrected to the line above.
# aws iam attach-role-policy --role-name ecsTaskExecutionRole --policy-arn "${POLICY_ARN}"

echo "✅ IAM Role and Policy setup complete."