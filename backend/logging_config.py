"""
Comprehensive logging configuration for D'Agri Talk
"""

import os
import logging
import logging.config
from datetime import datetime
from flask import Flask, jsonify, redirect, url_for, request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import config
from app.extensions import jwt
from app.monitoring import monitor

# Logging configuration
LOGGING_CONFIG = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'detailed': {
            'format': '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        },
        'json': {
            'format': '{"timestamp": "%(asctime)s", "logger": "%(name)s", "level": "%(levelname)s", "message": "%(message)s", "module": "%(module)s", "function": "%(funcName)s", "line": %(lineno)d}'
        },
        'simple': {
            'format': '%(levelname)s - %(message)s'
        }
    },
    'handlers': {
        'console': {
            'class': 'logging.StreamHandler',
            'level': 'INFO',
            'formatter': 'json',
            'stream': 'ext://sys.stdout'
        },
        'file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'DEBUG',
            'formatter': 'detailed',
            'filename': 'logs/dagri_talk.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        },
        'error_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'ERROR',
            'formatter': 'detailed',
            'filename': 'logs/dagri_talk_errors.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 5
        },
        'security_file': {
            'class': 'logging.handlers.RotatingFileHandler',
            'level': 'WARNING',
            'formatter': 'json',
            'filename': 'logs/dagri_talk_security.log',
            'maxBytes': 10485760,  # 10MB
            'backupCount': 10
        }
    },
    'loggers': {
        '': {  # Root logger
            'handlers': ['console', 'file'],
            'level': 'INFO',
            'propagate': False
        },
        'dagri_talk': {
            'handlers': ['console', 'file', 'error_file'],
            'level': 'DEBUG',
            'propagate': False
        },
        'dagri_talk.security': {
            'handlers': ['console', 'security_file'],
            'level': 'WARNING',
            'propagate': False
        },
        'werkzeug': {
            'handlers': ['file'],
            'level': 'WARNING',
            'propagate': False
        }
    }
}

def setup_logging():
    """Setup logging configuration"""
    # Create logs directory if it doesn't exist
    os.makedirs('logs', exist_ok=True)
    
    # Apply logging configuration
    logging.config.dictConfig(LOGGING_CONFIG)
    
    # Log startup message
    logger = logging.getLogger('dagri_talk')
    logger.info(f"Logging initialized at {datetime.now().isoformat()}")
    
    return logger

def create_app(config_name=os.getenv('FLASK_ENV', 'default')):
    app = Flask(__name__)
    CORS(app, resources={r"/*": {"origins": "*"}}, supports_credentials=True)
    
    # Load configuration
    app.config.from_object(config[config_name])
    
    # Initialize monitoring
    monitor.init_app(app)
    
    # Initialize direct MongoDB connection
    from app import database
    database.init_app(app)
    
    jwt.init_app(app)
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.knowledge import knowledge_bp
    from app.routes.market import market_bp
    from app.routes.api_root import api_root_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(knowledge_bp, url_prefix='/api/knowledge')
    app.register_blueprint(market_bp, url_prefix='/api/market')
    app.register_blueprint(api_root_bp, url_prefix='/api')
    
    # Root route
    @app.route('/')
    def index():
        return redirect(url_for('api_root.index'))
    
    # Health check route with monitoring
    @app.route('/api/health')
    def health_check():
        health_status = monitor.get_health_status()
        status_code = 200 if health_status['status'] == 'healthy' else 503
        return jsonify(health_status), status_code
    
    @app.route('/api/test-cors', methods=['GET', 'OPTIONS'])
    def test_cors():
        return jsonify({'message': 'CORS is working!'}), 200

    return app