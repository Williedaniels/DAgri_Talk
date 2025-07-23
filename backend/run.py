import os
from app import create_app

config_name = os.getenv('FLASK_ENV', 'development')
app = create_app(config_name)

if __name__ == '__main__':
    PORT = int(os.getenv('PORT', 80))
    app.run(host='0.0.0.0', port=PORT, debug=True)
    print(f"Server is running on port {PORT}")