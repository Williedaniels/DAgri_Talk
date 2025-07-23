import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'dev-secret-key-dagri-talk'
    MONGO_URI = os.environ.get('MONGO_URI') or 'mongodb://localhost:27017/dagri_talk'
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY') or 'jwt-secret-dagri-talk'

class DevelopmentConfig(Config):
    DEBUG = True

class TestingConfig(Config):
    TESTING = True
    # Use a separate database for testing
    MONGO_URI = os.environ.get('MONGO_URI_TEST') or 'mongodb://localhost:27017/dagri_talk_test'

class ProductionConfig(Config):
    DEBUG = False
    TESTING = False
    # In production, no default fallback for security keys
    SECRET_KEY = os.environ.get('SECRET_KEY')
    JWT_SECRET_KEY = os.environ.get('JWT_SECRET_KEY')
    MONGO_URI = os.environ.get('MONGO_URI')

config = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}