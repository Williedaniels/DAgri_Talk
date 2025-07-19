#!/bin/bash

# A script to create CloudWatch Log Groups for ECS services and set a retention policy.
# This script is idempotent and can be run multiple times without causing errors.

# Exit immediately if a command exits with a non-zero status.
set -e

# --- Configuration ---
AWS_REGION="ap-southeast-2"
RETENTION_DAYS=7

LOG_GROUPS=(
  "/ecs/dagri-talk-backend-dev"
  "/ecs/dagri-talk-frontend-dev"
)

# --- Main Logic ---
echo "Ensuring CloudWatch Log Groups exist in region ${AWS_REGION}..."

for group in "${LOG_GROUPS[@]}"; do
  echo "--> Processing log group: ${group}"
  
  # Check if the log group already exists.
  if aws logs describe-log-groups --log-group-name-prefix "${group}" --region "${AWS_REGION}" | grep -q "\"logGroupName\": \"${group}\""; then
    echo "Log group '${group}' already exists. Skipping creation."
  else
    echo "Creating log group '${group}'..."
    aws logs create-log-group --log-group-name "${group}" --region "${AWS_REGION}"
  fi

  echo "Setting retention policy for '${group}' to ${RETENTION_DAYS} days..."
  aws logs put-retention-policy --log-group-name "${group}" --retention-in-days ${RETENTION_DAYS} --region "${AWS_REGION}"

done

echo "✅ CloudWatch Log Group setup complete."