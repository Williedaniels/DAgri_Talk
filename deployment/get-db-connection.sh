#!/bin/bash
# Get RDS database connection details

echo "🔍 Getting RDS database connection details..."

# --- Configuration ---
# The name of the secret in AWS Secrets Manager containing the DB credentials.
# This is assumed based on project naming conventions.
SECRET_NAME="dagri-talk-dev-db-credentials"
DB_NAME="dagri_talk_dev"

# Get RDS instance endpoint
DB_ENDPOINT=$(aws rds describe-db-instances \
    --db-instance-identifier dagri-talk-dev-db \
    --query 'DBInstances[0].Endpoint.Address' \
    --output text 2>/dev/null)

if [ "$DB_ENDPOINT" = "None" ] || [ -z "$DB_ENDPOINT" ]; then
    echo "❌ RDS instance not found. Checking for Aurora cluster..."

    # Try Aurora cluster
    DB_ENDPOINT=$(aws rds describe-db-clusters \
        --db-cluster-identifier dagri-talk-dev-cluster \
        --query 'DBClusters[0].Endpoint' \
        --output text 2>/dev/null)
fi

if [ "$DB_ENDPOINT" = "None" ] || [ -z "$DB_ENDPOINT" ]; then
    echo "❌ No RDS database found. Please check your Terraform deployment."
    echo "💡 Using fallback SQLite configuration for now..."
    export DATABASE_URL="sqlite:///dagri_talk_dev.db"
else
    echo "✅ Found RDS endpoint: $DB_ENDPOINT"

    echo "🔑 Retrieving credentials from AWS Secrets Manager..."
    # Note: This requires 'jq' to be installed (e.g., 'brew install jq' or 'sudo apt-get install jq')
    SECRET_JSON=$(aws secretsmanager get-secret-value --secret-id "$SECRET_NAME" --query SecretString --output text)

    if [ -z "$SECRET_JSON" ]; then
        echo "❌ Could not retrieve secret '$SECRET_NAME'. Please check the secret name and IAM permissions."
        exit 1
    fi

    # Parse credentials from the secret JSON
    DB_USER=$(echo "$SECRET_JSON" | jq -r .username)
    DB_PASSWORD=$(echo "$SECRET_JSON" | jq -r .password)

    echo "📝 Building database connection string..."
    export DATABASE_URL="postgresql://${DB_USER}:${DB_PASSWORD}@${DB_ENDPOINT}:5432/${DB_NAME}"

    # For security, we no longer print the full URL with the password to the console.
    echo "✅ Database connection string has been configured and exported as DATABASE_URL."
fi