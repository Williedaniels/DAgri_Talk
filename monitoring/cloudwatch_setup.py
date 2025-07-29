"""
CloudWatch Dashboard and Alarms Setup
"""

import boto3
import json

class CloudWatchSetup:
    def __init__(self, region='us-east-1'):
        self.cloudwatch = boto3.client('cloudwatch', region_name=region)
        self.logs_client = boto3.client('logs', region_name=region)
    
    def create_log_groups(self):
        """Create CloudWatch log groups"""
        log_groups = [
            '/aws/ecs/dagri-talk-backend',
            '/aws/ecs/dagri-talk-frontend',
            '/dagri-talk/application',
            '/dagri-talk/security',
            '/dagri-talk/performance'
        ]
        
        for log_group in log_groups:
            try:
                self.logs_client.create_log_group(
                    logGroupName=log_group,
                    retentionInDays=30
                )
                print(f"Created log group: {log_group}")
            except self.logs_client.exceptions.ResourceAlreadyExistsException:
                print(f"Log group already exists: {log_group}")
    
    def create_dashboard(self):
        """Create comprehensive CloudWatch dashboard"""
        dashboard_body = {
            "widgets": [
                {
                    "type": "metric",
                    "x": 0,
                    "y": 0,
                    "width": 12,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", "dagri-talk-dev-alb"],
                            [".", "TargetResponseTime", ".", "."],
                            [".", "HTTPCode_Target_2XX_Count", ".", "."],
                            [".", "HTTPCode_Target_4XX_Count", ".", "."],
                            [".", "HTTPCode_Target_5XX_Count", ".", "."]
                        ],
                        "view": "timeSeries",
                        "stacked": False,
                        "region": "us-east-1",
                        "title": "Application Load Balancer Metrics",
                        "period": 300
                    }
                },
                {
                    "type": "metric",
                    "x": 12,
                    "y": 0,
                    "width": 12,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/ECS", "CPUUtilization", "ServiceName", "dagri-talk-backend-dev", "ClusterName", "dagri-talk-dev-cluster"],
                            [".", "MemoryUtilization", ".", ".", ".", "."],
                            [".", "CPUUtilization", "ServiceName", "dagri-talk-frontend-dev", "ClusterName", "dagri-talk-dev-cluster"],
                            [".", "MemoryUtilization", ".", ".", ".", "."]
                        ],
                        "view": "timeSeries",
                        "stacked": False,
                        "region": "us-east-1",
                        "title": "ECS Service Metrics",
                        "period": 300
                    }
                },
                {
                    "type": "metric",
                    "x": 0,
                    "y": 6,
                    "width": 8,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            ["DAgriTalk/Application", "RequestDuration", "Environment", "production"],
                            [".", "RequestCount", ".", "."]
                        ],
                        "view": "timeSeries",
                        "stacked": False,
                        "region": "us-east-1",
                        "title": "Application Performance",
                        "period": 300
                    }
                },
                {
                    "type": "log",
                    "x": 8,
                    "y": 6,
                    "width": 16,
                    "height": 6,
                    "properties": {
                        "query": "SOURCE '/aws/ecs/dagri-talk-backend' | fields @timestamp, @message\n| filter @message like /ERROR/\n| sort @timestamp desc\n| limit 20",
                        "region": "us-east-1",
                        "title": "Recent Application Errors",
                        "view": "table"
                    }
                },
                {
                    "type": "metric",
                    "x": 0,
                    "y": 12,
                    "width": 12,
                    "height": 6,
                    "properties": {
                        "metrics": [
                            ["AWS/RDS", "CPUUtilization", "DBInstanceIdentifier", "dagri-talk-dev-db"],
                            [".", "DatabaseConnections", ".", "."],
                            [".", "ReadLatency", ".", "."],
                            [".", "WriteLatency", ".", "."]
                        ],
                        "view": "timeSeries",
                        "stacked": False,
                        "region": "us-east-1",
                        "title": "Database Performance",
                        "period": 300
                    }
                },
                {
                    "type": "number",
                    "x": 12,
                    "y": 12,
                    "width": 6,
                    "height": 3,
                    "properties": {
                        "metrics": [
                            ["AWS/ApplicationELB", "HealthyHostCount", "LoadBalancer", "dagri-talk-dev-alb"]
                        ],
                        "view": "singleValue",
                        "region": "us-east-1",
                        "title": "Healthy Hosts"
                    }
                },
                {
                    "type": "number",
                    "x": 18,
                    "y": 12,
                    "width": 6,
                    "height": 3,
                    "properties": {
                        "metrics": [
                            ["AWS/ApplicationELB", "RequestCount", "LoadBalancer", "dagri-talk-dev-alb"]
                        ],
                        "view": "singleValue",
                        "region": "us-east-1",
                        "title": "Total Requests (5min)",
                        "period": 300,
                        "stat": "Sum"
                    }
                }
            ]
        }
        
        try:
            self.cloudwatch.put_dashboard(
                DashboardName='DAgriTalk-Production-Dashboard',
                DashboardBody=json.dumps(dashboard_body)
            )
            print("Dashboard created successfully")
        except Exception as e:
            print(f"Error creating dashboard: {e}")
    
    def create_alarms(self):
        """Create CloudWatch alarms"""
        alarms = [
            {
                'AlarmName': 'DAgriTalk-High-Error-Rate',
                'ComparisonOperator': 'GreaterThanThreshold',
                'EvaluationPeriods': 2,
                'MetricName': 'HTTPCode_Target_5XX_Count',
                'Namespace': 'AWS/ApplicationELB',
                'Period': 300,
                'Statistic': 'Sum',
                'Threshold': 10.0,
                'ActionsEnabled': True,
                'AlarmDescription': 'High error rate detected',
                'Dimensions': [
                    {
                        'Name': 'LoadBalancer',
                        'Value': 'dagri-talk-dev-alb'
                    }
                ],
                'Unit': 'Count'
            },
            {
                'AlarmName': 'DAgriTalk-High-Response-Time',
                'ComparisonOperator': 'GreaterThanThreshold',
                'EvaluationPeriods': 3,
                'MetricName': 'TargetResponseTime',
                'Namespace': 'AWS/ApplicationELB',
                'Period': 300,
                'Statistic': 'Average',
                'Threshold': 2.0,
                'ActionsEnabled': True,
                'AlarmDescription': 'High response time detected',
                'Dimensions': [
                    {
                        'Name': 'LoadBalancer',
                        'Value': 'dagri-talk-dev-alb'
                    }
                ],
                'Unit': 'Seconds'
            },
            {
                'AlarmName': 'DAgriTalk-Low-Healthy-Hosts',
                'ComparisonOperator': 'LessThanThreshold',
                'EvaluationPeriods': 1,
                'MetricName': 'HealthyHostCount',
                'Namespace': 'AWS/ApplicationELB',
                'Period': 300,
                'Statistic': 'Average',
                'Threshold': 1.0,
                'ActionsEnabled': True,
                'AlarmDescription': 'Low number of healthy hosts',
                'Dimensions': [
                    {
                        'Name': 'LoadBalancer',
                        'Value': 'dagri-talk-dev-alb'
                    }
                ],
                'Unit': 'Count'
            },
            {
                'AlarmName': 'DAgriTalk-High-CPU-Backend',
                'ComparisonOperator': 'GreaterThanThreshold',
                'EvaluationPeriods': 3,
                'MetricName': 'CPUUtilization',
                'Namespace': 'AWS/ECS',
                'Period': 300,
                'Statistic': 'Average',
                'Threshold': 80.0,
                'ActionsEnabled': True,
                'AlarmDescription': 'High CPU utilization on backend service',
                'Dimensions': [
                    {
                        'Name': 'ServiceName',
                        'Value': 'dagri-talk-backend-dev'
                    },
                    {
                        'Name': 'ClusterName',
                        'Value': 'dagri-talk-dev-cluster'
                    }
                ],
                'Unit': 'Percent'
            }
        ]
        
        for alarm in alarms:
            try:
                self.cloudwatch.put_metric_alarm(**alarm)
                print(f"Created alarm: {alarm['AlarmName']}")
            except Exception as e:
                print(f"Error creating alarm {alarm['AlarmName']}: {e}")

def setup_monitoring():
    """Setup complete monitoring infrastructure"""
    setup = CloudWatchSetup()
    
    print("Setting up CloudWatch monitoring...")
    setup.create_log_groups()
    setup.create_dashboard()
    setup.create_alarms()
    print("Monitoring setup complete!")

if __name__ == "__main__":
    setup_monitoring()