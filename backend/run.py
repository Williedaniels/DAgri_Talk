import os
from app import create_app

config_name = os.getenv('FLASK_ENV', 'default')
app = create_app(config_name)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5001)