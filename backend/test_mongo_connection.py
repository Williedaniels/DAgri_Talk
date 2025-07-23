from flask import Flask
from flask_pymongo import PyMongo
import pymongo
import os
import certifi
from dotenv import load_dotenv
import sys

load_dotenv()

app = Flask(__name__)
mongo_uri = os.environ.get('MONGO_URI')

# Basic validation of the URI
if not mongo_uri:
    print("ERROR: No MongoDB URI found in environment variables.")
    sys.exit(1)

# Add database name if not present
if "/?" in mongo_uri or (mongo_uri.count("/") == 2 and mongo_uri[-1] != "/"):
    parts = mongo_uri.split("?", 1)
    base_uri = parts[0]
    params = parts[1] if len(parts) > 1 else ""
    
    # Add the database name before parameters
    if base_uri.endswith("/"):
        base_uri += "dagri_talk"
    else:
        base_uri += "/dagri_talk"
    
    # Reconstruct the URI
    mongo_uri = f"{base_uri}?{params}" if params else base_uri

print(f"Using certifi certificate path: {certifi.where()}")
print(f"Attempting to connect using URI: {mongo_uri.replace(mongo_uri.split('@')[0].split('://')[1], '****')}")

# Try direct PyMongo connection with SSL certificate
try:
    print("\nTesting direct PyMongo connection...")
    client = pymongo.MongoClient(
        mongo_uri, 
        serverSelectionTimeoutMS=5000,
        tlsCAFile=certifi.where()  # Use certifi's certificate store
    )
    client.admin.command('ping')
    print("✅ Direct PyMongo connection successful!")
    print("\nAvailable databases:")
    for db_name in client.list_database_names():
        print(f"- {db_name}")
except Exception as e:
    print(f"❌ Direct PyMongo connection failed: {str(e)}")

# Now try Flask-PyMongo
try:
    print("\nTesting Flask-PyMongo connection...")
    app.config["MONGO_URI"] = mongo_uri
    app.config["MONGO_TLS"] = True
    app.config["MONGO_TLSCAFILE"] = certifi.where()
    
    mongo_flask = PyMongo(app)
    
    # Check if connection works
    mongo_flask.db.command('ping')
    print("✅ Flask-PyMongo connection successful!")
    print("\nAvailable collections:")
    collections = mongo_flask.db.list_collection_names()
    for collection in collections:
        print(f"- {collection}")
except Exception as e:
    print(f"❌ Flask-PyMongo connection failed: {str(e)}")

# Alternative method if both methods above fail
if "--allow-invalid-cert" in sys.argv:
    print("\nTesting with certificate validation disabled (INSECURE)...")
    try:
        # Try with certificate validation disabled
        client_insecure = pymongo.MongoClient(
            mongo_uri,
            serverSelectionTimeoutMS=5000,
            tlsAllowInvalidCertificates=True
        )
        client_insecure.admin.command('ping')
        print("✅ Connection successful with certificate validation disabled")
        print("  This is INSECURE and should not be used in production!")
        print("\nAvailable databases:")
        for db_name in client_insecure.list_database_names():
            print(f"- {db_name}")
    except Exception as e:
        print(f"❌ Connection failed even with certificate validation disabled: {str(e)}")

print("\nTesting complete.")