"""
D'Agri Talk Application Monitoring
Comprehensive monitoring and metrics collection
"""

import time
import logging
import json
from datetime import datetime, timedelta
from functools import wraps
from flask import request, g, current_app
import psutil
import boto3
from prometheus_client import Counter, Histogram, Gauge, generate_latest
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer()
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

# Prometheus Metrics
REQUEST_COUNT = Counter(
    'dagri_talk_requests_total',
    'Total number of HTTP requests',
    ['method', 'endpoint', 'status_code']
)

REQUEST_DURATION = Histogram(
    'dagri_talk_request_duration_seconds',
    'HTTP request duration in seconds',
    ['method', 'endpoint']
)

ACTIVE_USERS = Gauge(
    'dagri_talk_active_users',
    'Number of active users'
)

DATABASE_CONNECTIONS = Gauge(
    'dagri_talk_database_connections',
    'Number of active database connections'
)

KNOWLEDGE_ENTRIES = Gauge(
    'dagri_talk_knowledge_entries_total',
    'Total number of knowledge entries'
)

MARKET_LISTINGS = Gauge(
    'dagri_talk_market_listings_total',
    'Total number of market listings'
)

SYSTEM_CPU = Gauge(
    'dagri_talk_system_cpu_percent',
    'System CPU usage percentage'
)

SYSTEM_MEMORY = Gauge(
    'dagri_talk_system_memory_percent',
    'System memory usage percentage'
)

ERROR_COUNT = Counter(
    'dagri_talk_errors_total',
    'Total number of application errors',
    ['error_type', 'endpoint']
)

class ApplicationMonitor:
    def __init__(self, app=None):
        self.app = app
        self.cloudwatch = None
        
        if app is not None:
            self.init_app(app)
    
    def init_app(self, app):
        """Initialize monitoring for Flask app"""
        self.app = app
        
        # Initialize CloudWatch client
        try:
            self.cloudwatch = boto3.client('cloudwatch', region_name='us-east-1')
        except Exception as e:
            logger.warning("CloudWatch client initialization failed", error=str(e))
        
        # Register monitoring hooks
        app.before_request(self.before_request)
        app.after_request(self.after_request)
        app.teardown_appcontext(self.teardown_request)
        
        # Register metrics endpoint
        app.add_url_rule('/metrics', 'metrics', self.metrics_endpoint)
        
        # Start background monitoring
        self.start_background_monitoring()
    
    def before_request(self):
        """Record request start time"""
        g.start_time = time.time()
        g.request_id = f"{int(time.time())}-{hash(request.remote_addr) % 10000}"
        
        logger.info(
            "Request started",
            request_id=g.request_id,
            method=request.method,
            path=request.path,
            remote_addr=request.remote_addr,
            user_agent=request.headers.get('User-Agent', '')
        )
    
    def after_request(self, response):
        """Record request completion and metrics"""
        if hasattr(g, 'start_time'):
            duration = time.time() - g.start_time
            
            # Record Prometheus metrics
            REQUEST_COUNT.labels(
                method=request.method,
                endpoint=request.endpoint or 'unknown',
                status_code=response.status_code
            ).inc()
            
            REQUEST_DURATION.labels(
                method=request.method,
                endpoint=request.endpoint or 'unknown'
            ).observe(duration)
            
            # Log request completion
            logger.info(
                "Request completed",
                request_id=getattr(g, 'request_id', 'unknown'),
                method=request.method,
                path=request.path,
                status_code=response.status_code,
                duration=duration,
                response_size=len(response.get_data())
            )
            
            # Send metrics to CloudWatch
            self.send_cloudwatch_metrics(duration, response.status_code)
        
        return response
    
    def teardown_request(self, exception):
        """Handle request errors"""
        if exception:
            ERROR_COUNT.labels(
                error_type=type(exception).__name__,
                endpoint=request.endpoint or 'unknown'
            ).inc()
            
            logger.error(
                "Request error",
                request_id=getattr(g, 'request_id', 'unknown'),
                error=str(exception),
                error_type=type(exception).__name__,
                method=request.method,
                path=request.path
            )
    
    def send_cloudwatch_metrics(self, duration, status_code):
        """Send custom metrics to CloudWatch"""
        if not self.cloudwatch:
            return
        
        try:
            self.cloudwatch.put_metric_data(
                Namespace='DAgriTalk/Application',
                MetricData=[
                    {
                        'MetricName': 'RequestDuration',
                        'Value': duration,
                        'Unit': 'Seconds',
                        'Dimensions': [
                            {
                                'Name': 'Environment',
                                'Value': current_app.config.get('ENV', 'development')
                            }
                        ]
                    },
                    {
                        'MetricName': 'RequestCount',
                        'Value': 1,
                        'Unit': 'Count',
                        'Dimensions': [
                            {
                                'Name': 'StatusCode',
                                'Value': str(status_code)
                            },
                            {
                                'Name': 'Environment',
                                'Value': current_app.config.get('ENV', 'development')
                            }
                        ]
                    }
                ]
            )
        except Exception as e:
            logger.warning("Failed to send CloudWatch metrics", error=str(e))
    
    def start_background_monitoring(self):
        """Start background system monitoring"""
        import threading
        
        def monitor_system():
            while True:
                try:
                    # System metrics
                    cpu_percent = psutil.cpu_percent(interval=1)
                    memory_percent = psutil.virtual_memory().percent
                    
                    SYSTEM_CPU.set(cpu_percent)
                    SYSTEM_MEMORY.set(memory_percent)
                    
                    # Application metrics (would require database connection)
                    # KNOWLEDGE_ENTRIES.set(get_knowledge_count())
                    # MARKET_LISTINGS.set(get_market_listings_count())
                    
                    logger.debug(
                        "System metrics updated",
                        cpu_percent=cpu_percent,
                        memory_percent=memory_percent
                    )
                    
                    time.sleep(30)  # Update every 30 seconds
                    
                except Exception as e:
                    logger.error("Background monitoring error", error=str(e))
                    time.sleep(60)  # Wait longer on error
        
        thread = threading.Thread(target=monitor_system, daemon=True)
        thread.start()
    
    def metrics_endpoint(self):
        """Prometheus metrics endpoint"""
        return generate_latest(), 200, {'Content-Type': 'text/plain'}
    
    def get_health_status(self):
        """Get comprehensive health status"""
        health_data = {
            'status': 'healthy',
            'timestamp': datetime.utcnow().isoformat(),
            'version': current_app.config.get('VERSION', '1.0.0'),
            'environment': current_app.config.get('ENV', 'development'),
            'checks': {}
        }
        
        # Database health check
        try:
            # Add your database health check here
            health_data['checks']['database'] = {
                'status': 'healthy',
                'response_time': 0.05
            }
        except Exception as e:
            health_data['checks']['database'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
            health_data['status'] = 'degraded'
        
        # System health check
        try:
            cpu_percent = psutil.cpu_percent()
            memory_percent = psutil.virtual_memory().percent
            
            health_data['checks']['system'] = {
                'status': 'healthy' if cpu_percent < 80 and memory_percent < 80 else 'warning',
                'cpu_percent': cpu_percent,
                'memory_percent': memory_percent
            }
            
            if cpu_percent > 90 or memory_percent > 90:
                health_data['status'] = 'unhealthy'
        except Exception as e:
            health_data['checks']['system'] = {
                'status': 'unhealthy',
                'error': str(e)
            }
        
        return health_data

# Monitoring decorators
def monitor_endpoint(func):
    """Decorator to monitor specific endpoints"""
    @wraps(func)
    def wrapper(*args, **kwargs):
        start_time = time.time()
        
        try:
            result = func(*args, **kwargs)
            
            # Log successful execution
            logger.info(
                "Endpoint executed successfully",
                endpoint=func.__name__,
                duration=time.time() - start_time
            )
            
            return result
            
        except Exception as e:
            # Log endpoint error
            logger.error(
                "Endpoint execution failed",
                endpoint=func.__name__,
                error=str(e),
                duration=time.time() - start_time
            )
            raise
    
    return wrapper

def monitor_database_operation(operation_name):
    """Decorator to monitor database operations"""
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            start_time = time.time()
            
            try:
                result = func(*args, **kwargs)
                
                logger.info(
                    "Database operation completed",
                    operation=operation_name,
                    duration=time.time() - start_time
                )
                
                return result
                
            except Exception as e:
                logger.error(
                    "Database operation failed",
                    operation=operation_name,
                    error=str(e),
                    duration=time.time() - start_time
                )
                raise
        
        return wrapper
    return decorator

# Initialize global monitor instance
monitor = ApplicationMonitor()