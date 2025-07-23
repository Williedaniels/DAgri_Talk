import pymongo
import certifi
import os
from flask import g

def get_db_client():
    """
    Returns a MongoDB client, reusing existing connection if available
    """
    if 'mongo_client' not in g:
        mongo_uri = os.environ.get('MONGO_URI')
        g.mongo_client = pymongo.MongoClient(
            mongo_uri,
            tlsCAFile=certifi.where()
        )
    return g.mongo_client

def get_db():
    """
    Returns the database object, extracting DB name from the URI
    """
    client = get_db_client()
    
    # Extract database name from URI or use default
    mongo_uri = os.environ.get('MONGO_URI')
    db_name = "dagri_talk"  # default name
    
    # Try to extract database name from URI
    if mongo_uri and '/' in mongo_uri:
        parts = mongo_uri.split('/')
        if len(parts) >= 4:
            potential_db = parts[3].split('?')[0]
            if potential_db:
                db_name = potential_db
    
    return client[db_name]

def close_db(e=None):
    """
    Close the MongoDB connection when the request is finished
    """
    mongo_client = g.pop('mongo_client', None)
    
    if mongo_client is not None:
        mongo_client.close()

def init_app(app):
    """
    Register database functions with the Flask app
    """
    app.teardown_appcontext(close_db)