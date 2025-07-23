from flask_pymongo import PyMongo
from flask_jwt_extended import JWTManager

# Initialize extensions
mongo = PyMongo()
jwt = JWTManager()