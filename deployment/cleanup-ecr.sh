#!/bin/bash

# A script to forcefully delete ECR repositories matching a given prefix.
# This is useful for cleaning up environments where 'terraform destroy' fails
# because repositories still contain images and 'force_delete' was not set.

set -e

# --- 1. Input Validation ---
if [ -z "$1" ]; then
    echo "❌ Error: No repository prefix provided."
    echo "Usage: $0 <repository-prefix>"
    echo "Example: $0 dagri-talk-dev"
    exit 1
fi

REPO_PREFIX=$1

echo "🔍 Finding ECR repositories with prefix: ${REPO_PREFIX}"

# --- 2. Find Repositories ---
# The query filters repositories where the name starts with the provided prefix.
REPO_NAMES=$(aws ecr describe-repositories \
    --query "repositories[?starts_with(repositoryName, '${REPO_PREFIX}')].repositoryName" \
    --output text)

if [ -z "$REPO_NAMES" ]; then
    echo "✅ No ECR repositories found with the prefix '${REPO_PREFIX}'."
    exit 0
fi

echo "The following repositories will be deleted:"
echo "$REPO_NAMES"
echo
read -p "⚠️ This will permanently delete the repositories and all images within them. This action cannot be undone. Press Enter to continue or Ctrl+C to abort..."

# --- 3. Delete Repositories ---
for repo in $REPO_NAMES; do
    echo "--- Deleting repository: $repo ---"
    aws ecr delete-repository --repository-name "$repo" --force
    echo "✅ Successfully deleted repository: $repo"
done

echo "🎉 ECR cleanup complete."