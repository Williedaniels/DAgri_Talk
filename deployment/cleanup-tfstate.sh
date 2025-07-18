#!/bin/bash

# A script to remove manually-deleted resources from the Terraform state.
# This is a crucial step after using cleanup scripts like cleanup-vpc.sh or
# cleanup-ecr.sh to resolve a failed 'terraform destroy'.

set -e

echo "🧹 Starting Terraform state cleanup..."
echo "This script will run 'terraform state rm' for resources that are commonly"
echo "stuck after a manual cleanup."
echo

# --- Configuration ---
# The directory where your terraform state is managed.
TERRAFORM_DIR="terraform/environments/dev"

# List of resources to remove from the state.
# These should correspond to resources you've already deleted from AWS manually.
RESOURCES_TO_REMOVE=(
    "module.ecr.aws_ecr_repository.backend"
    "module.ecr.aws_ecr_repository.frontend"
    "module.ecr.aws_ecr_lifecycle_policy.backend"
    "module.ecr.aws_ecr_lifecycle_policy.frontend"
    "module.ecr.aws_ecr_repository_policy.backend"
    "module.ecr.aws_ecr_repository_policy.frontend"
    "module.networking.aws_vpc.main"
)

echo "Navigating to ${TERRAFORM_DIR}..."
cd "${TERRAFORM_DIR}"

for resource in "${RESOURCES_TO_REMOVE[@]}"; do
    echo "--- Removing: ${resource} ---"
    # Redirect stderr to /dev/null to suppress the "Invalid target address" error block from Terraform.
    terraform state rm "${resource}" 2>/dev/null || echo "--> INFO: Resource ${resource} not found in state, skipping."
done

echo
echo "✅ Terraform state cleanup complete."
echo "You can now run 'terraform destroy' again to remove any remaining infrastructure."