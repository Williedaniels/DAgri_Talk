import os
from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from app.config import config

db = SQLAlchemy()
jwt = JWTManager()
migrate = Migrate()

def create_app(config_name=os.getenv('FLASK_ENV', 'default')):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    
    # Initialize extensions
    db.init_app(app)
    migrate.init_app(app, db)
    CORS(app, origins=['http://localhost:3000'])  # React dev server
    jwt.init_app(app)
    
    # Configure JWT to work with string identities
    
    # Register blueprints
    from app.routes.auth import auth_bp
    from app.routes.knowledge import knowledge_bp
    from app.routes.market import market_bp
    
    app.register_blueprint(auth_bp, url_prefix='/api/auth')
    app.register_blueprint(knowledge_bp, url_prefix='/api/knowledge')
    app.register_blueprint(market_bp, url_prefix='/api/market')
    
    # Health check endpoint for Docker
    @app.route('/api/health')
    def health():
        try:
            # A simple query to check database connectivity
            db.session.execute('SELECT 1')
            return jsonify({"status": "healthy", "service": "dagri-talk-backend"}), 200
        except Exception as e:
            # Log the error for debugging purposes if needed
            return jsonify({"status": "unhealthy", "reason": str(e)}), 500
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    return app