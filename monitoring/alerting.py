"""
Advanced Alerting System for D'Agri Talk
"""

import smtplib
import json
import requests
import boto3
from email.mime.text import MimeText
from email.mime.multipart import MimeMultipart
from datetime import datetime, timedelta
import logging

logger = logging.getLogger(__name__)

class AlertManager:
    def __init__(self):
        self.sns = boto3.client('sns', region_name='us-east-1')
        self.cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
    
    def send_slack_alert(self, webhook_url, message, severity="warning"):
        """Send alert to Slack"""
        colors = {
            "info": "#36a64f",
            "warning": "#ff9500", 
            "error": "#ff0000",
            "critical": "#8B0000"
        }
        
        payload = {
            "attachments": [
                {
                    "color": colors.get(severity, "#ff9500"),
                    "fields": [
                        {
                            "title": f"D'Agri Talk Alert - {severity.upper()}",
                            "value": message,
                            "short": False
                        },
                        {
                            "title": "Timestamp",
                            "value": datetime.now().strftime("%Y-%m-%d %H:%M:%S UTC"),
                            "short": True
                        }
                    ]
                }
            ]
        }
        
        try:
            response = requests.post(webhook_url, json=payload, timeout=10)
            response.raise_for_status()
            logger.info("Slack alert sent successfully")
        except Exception as e:
            logger.error(f"Failed to send Slack alert: {e}")
    
    def send_email_alert(self, smtp_config, to_emails, subject, message):
        """Send email alert"""
        try:
            msg = MimeMultipart()
            msg['From'] = smtp_config['from_email']
            msg['To'] = ', '.join(to_emails)
            msg['Subject'] = f"[D'Agri Talk Alert] {subject}"
            
            body = f"""
            D'Agri Talk Monitoring Alert
            
            Time: {datetime.now().strftime('%Y-%m-%d %H:%M:%S UTC')}
            
            Message:
            {message}
            
            Please investigate immediately.
            
            ---
            D'Agri Talk Monitoring System
            """
            
            msg.attach(MimeText(body, 'plain'))
            
            server = smtplib.SMTP(smtp_config['smtp_server'], smtp_config['smtp_port'])
            server.starttls()
            server.login(smtp_config['username'], smtp_config['password'])
            server.send_message(msg)
            server.quit()
            
            logger.info(f"Email alert sent to {to_emails}")
        except Exception as e:
            logger.error(f"Failed to send email alert: {e}")
    
    def send_sns_alert(self, topic_arn, message, subject):
        """Send SNS alert"""
        try:
            self.sns.publish(
                TopicArn=topic_arn,
                Message=message,
                Subject=f"[D'Agri Talk] {subject}"
            )
            logger.info("SNS alert sent successfully")
        except Exception as e:
            logger.error(f"Failed to send SNS alert: {e}")
    
    def check_and_alert(self, alert_config):
        """Check metrics and send alerts if thresholds exceeded"""
        alerts_triggered = []
        
        # Check response time
        if self._check_response_time_threshold(alert_config.get('response_time_threshold', 2.0)):
            alerts_triggered.append("High response time detected")
        
        # Check error rate
        if self._check_error_rate_threshold(alert_config.get('error_rate_threshold', 0.05)):
            alerts_triggered.append("High error rate detected")
        
        # Check system resources
        if self._check_system_resources(alert_config.get('cpu_threshold', 80), alert_config.get('memory_threshold', 80)):
            alerts_triggered.append("High system resource usage")
        
        # Send alerts if any triggered
        if alerts_triggered:
            message = "The following issues were detected:\n" + "\n".join(f"- {alert}" for alert in alerts_triggered)
            
            # Send to all configured channels
            if 'slack_webhook' in alert_config:
                self.send_slack_alert(alert_config['slack_webhook'], message, "error")
            
            if 'email_config' in alert_config:
                self.send_email_alert(
                    alert_config['email_config'],
                    alert_config.get('email_recipients', []),
                    "System Alert",
                    message
                )
            
            if 'sns_topic_arn' in alert_config:
                self.send_sns_alert(alert_config['sns_topic_arn'], message, "System Alert")
    
    def _check_response_time_threshold(self, threshold):
        """Check if response time exceeds threshold"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=15)
            
            response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/ApplicationELB',
                MetricName='TargetResponseTime',
                Dimensions=[
                    {
                        'Name': 'LoadBalancer',
                        'Value': 'dagri-talk-dev-alb'
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Average']
            )
            
            if response['Datapoints']:
                avg_response_time = sum(dp['Average'] for dp in response['Datapoints']) / len(response['Datapoints'])
                return avg_response_time > threshold
            
        except Exception as e:
            logger.error(f"Error checking response time: {e}")
        
        return False
    
    def _check_error_rate_threshold(self, threshold):
        """Check if error rate exceeds threshold"""
        try:
            end_time = datetime.utcnow()
            start_time = end_time - timedelta(minutes=15)
            
            # Get total requests
            total_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/ApplicationELB',
                MetricName='RequestCount',
                Dimensions=[
                    {
                        'Name': 'LoadBalancer',
                        'Value': 'dagri-talk-dev-alb'
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Sum']
            )
            
            # Get error requests
            error_response = self.cloudwatch.get_metric_statistics(
                Namespace='AWS/ApplicationELB',
                MetricName='HTTPCode_Target_5XX_Count',
                Dimensions=[
                    {
                        'Name': 'LoadBalancer',
                        'Value': 'dagri-talk-dev-alb'
                    }
                ],
                StartTime=start_time,
                EndTime=end_time,
                Period=300,
                Statistics=['Sum']
            )
            
            if total_response['Datapoints'] and error_response['Datapoints']:
                total_requests = sum(dp['Sum'] for dp in total_response['Datapoints'])
                error_requests = sum(dp['Sum'] for dp in error_response['Datapoints'])
                
                if total_requests > 0:
                    error_rate = error_requests / total_requests
                    return error_rate > threshold
            
        except Exception as e:
            logger.error(f"Error checking error rate: {e}")
        
        return False
    
    def _check_system_resources(self, cpu_threshold, memory_threshold):
        """Check system resource usage"""
        # This would typically check ECS service metrics
        # Implementation depends on your specific monitoring setup
        return False

# Example usage configuration
ALERT_CONFIG = {
    'response_time_threshold': 2.0,  # seconds
    'error_rate_threshold': 0.05,   # 5%
    'cpu_threshold': 80,            # 80%
    'memory_threshold': 80,         # 80%
    'slack_webhook': 'https://hooks.slack.com/services/YOUR/SLACK/WEBHOOK',
    'email_config': {
        'smtp_server': 'smtp.gmail.com',
        'smtp_port': 587,
        'from_email': 'alerts@dagritalk.com',
        'username': 'your-email@gmail.com',
        'password': 'your-app-password'
    },
    'email_recipients': ['admin@dagritalk.com', 'devops@dagritalk.com'],
    'sns_topic_arn': 'arn:aws:sns:us-east-1:123456789012:dagri-talk-alerts'
}

if __name__ == "__main__":
    alert_manager = AlertManager()
    alert_manager.check_and_alert(ALERT_CONFIG)