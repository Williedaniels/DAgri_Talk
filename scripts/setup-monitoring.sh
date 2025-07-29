#!/bin/bash

# D'Agri Talk - Complete Monitoring Setup Script
# This script sets up comprehensive monitoring and observability

set -e

echo "🚀 Setting up D'Agri Talk Monitoring & Observability..."

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}✅ $1${NC}"
}

print_warning() {
    echo -e "${YELLOW}⚠️ $1${NC}"
}

print_error() {
    echo -e "${RED}❌ $1${NC}"
}

# Check prerequisites
echo "Checking prerequisites..."

if ! command -v aws &> /dev/null; then
    print_error "AWS CLI not found. Please install AWS CLI."
    exit 1
fi

if ! command -v python3 &> /dev/null; then
    print_error "Python 3 not found. Please install Python 3."
    exit 1
fi

print_status "Prerequisites check passed"

# Install Python dependencies
echo "Installing Python dependencies..."
pip3 install boto3 requests psutil prometheus-client structlog --quiet
print_status "Python dependencies installed"

# Create monitoring directories
echo "Creating monitoring directories..."
mkdir -p monitoring/dashboards
mkdir -p monitoring/alerts
mkdir -p logs
print_status "Monitoring directories created"

# Setup CloudWatch
echo "Setting up CloudWatch monitoring..."
python3 monitoring/cloudwatch_setup.py
print_status "CloudWatch setup completed"

# Create log groups
echo "Creating CloudWatch log groups..."
aws logs create-log-group --log-group-name "/aws/ecs/dagri-talk-backend" --region us-east-1 2>/dev/null || true
aws logs create-log-group --log-group-name "/aws/ecs/dagri-talk-frontend" --region us-east-1 2>/dev/null || true
aws logs create-log-group --log-group-name "/dagri-talk/application" --region us-east-1 2>/dev/null || true
aws logs create-log-group --log-group-name "/dagri-talk/security" --region us-east-1 2>/dev/null || true
print_status "CloudWatch log groups created"

# Setup SNS topic for alerts
echo "Setting up SNS topic for alerts..."
SNS_TOPIC_ARN=$(aws sns create-topic --name dagri-talk-alerts --region us-east-1 --query 'TopicArn' --output text)
print_status "SNS topic created: $SNS_TOPIC_ARN"

# Subscribe email to SNS topic (optional)
read -p "Enter email address for alerts (or press Enter to skip): " email
if [ ! -z "$email" ]; then
    aws sns subscribe --topic-arn "$SNS_TOPIC_ARN" --protocol email --notification-endpoint "$email" --region us-east-1
    print_status "Email subscription added to SNS topic"
fi

# Create monitoring configuration file
echo "Creating monitoring configuration..."
cat > monitoring/config.json << EOF
{
  "cloudwatch": {
    "region": "us-east-1",
    "namespace": "DAgriTalk/Application"
  },
  "alerts": {
    "response_time_threshold": 2.0,
    "error_rate_threshold": 0.05,
    "cpu_threshold": 80,
    "memory_threshold": 80,
    "sns_topic_arn": "$SNS_TOPIC_ARN"
  },
  "dashboards": {
    "grafana_url": "http://localhost:3000",
    "cloudwatch_dashboard": "DAgriTalk-Production-Dashboard"
  },
  "log_groups": [
    "/aws/ecs/dagri-talk-backend",
    "/aws/ecs/dagri-talk-frontend",
    "/dagri-talk/application",
    "/dagri-talk/security"
  ]
}
EOF
print_status "Monitoring configuration created"

# Test monitoring setup
echo "Testing monitoring setup..."
python3 << 'EOF'
import boto3
import json

try:
    # Test CloudWatch connection
    cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
    cloudwatch.list_metrics(Namespace='AWS/ApplicationELB')
    print("✅ CloudWatch connection successful")
    
    # Test SNS connection
    sns = boto3.client('sns', region_name='us-east-1')
    sns.list_topics()
    print("✅ SNS connection successful")
    
    # Test logs connection
    logs = boto3.client('logs', region_name='us-east-1')
    logs.describe_log_groups()
    print("✅ CloudWatch Logs connection successful")
    
except Exception as e:
    print(f"❌ Monitoring test failed: {e}")
    exit(1)
EOF

print_status "Monitoring setup test passed"

# Create monitoring dashboard URL
ALB_DNS=$(aws elbv2 describe-load-balancers --names dagri-talk-dev-alb --query 'LoadBalancers[0].DNSName' --output text 2>/dev/null || echo "Not deployed yet")

echo ""
echo "🎉 Monitoring & Observability Setup Complete!"
echo ""
echo "📊 Monitoring Resources:"
echo "   • CloudWatch Dashboard: https://console.aws.amazon.com/cloudwatch/home?region=us-east-1#dashboards:name=DAgriTalk-Production-Dashboard"
echo "   • Application URL: https://$ALB_DNS"
echo "   • Health Check: https://$ALB_DNS/api/health"
echo "   • Metrics Endpoint: https://$ALB_DNS/metrics"
echo "   • SNS Topic: $SNS_TOPIC_ARN"
echo ""
echo "🔔 Alert Channels:"
echo "   • SNS Topic: $SNS_TOPIC_ARN"
echo "   • Email: ${email:-"Not configured"}"
echo ""
echo "📋 Next Steps:"
echo "   1. Configure Grafana dashboard (optional)"
echo "   2. Set up Slack webhook for alerts"
echo "   3. Test alert notifications"
echo "   4. Review monitoring configuration in monitoring/config.json"
echo ""
print_status "Setup completed successfully!"