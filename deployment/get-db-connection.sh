#!/bin/bash
# Get RDS database connection details

echo "🔍 Getting RDS database connection details..."

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
    echo "📝 Database connection string:"
    export DATABASE_URL="postgresql://dagri_user:your_db_password@$DB_ENDPOINT:5432/dagri_talk_dev"
    echo "$DATABASE_URL"
fi

echo ""
echo "🔧 Update your task definition with this DATABASE_URL:"
echo "\"name\": \"DATABASE_URL\","
echo "\"value\": \"$DATABASE_URL\""