import os
from flask import Flask
from .api.routes import api

def create_app():
    """Create and configure the Flask application"""
    app = Flask(__name__)
    
    # Register blueprints
    app.register_blueprint(api, url_prefix='/api')
    
    return app

if __name__ == "__main__":
    # Get port from environment variable or use default
    port = int(os.environ.get('PORT', 5001))
    # Get host from environment variable or use default
    host = os.environ.get('HOST', '0.0.0.0')
    # Get debug mode from environment variable or use default
    debug = os.environ.get('FLASK_DEBUG', 'True').lower() == 'true'
    
    print(f"Starting server on {host}:{port} (debug={debug})")
    app = create_app()
    app.run(debug=debug, port=port, host=host) 