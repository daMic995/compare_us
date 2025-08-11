import os
from dotenv import load_dotenv
from flask import Flask
from flask_cors import CORS
import sentry_sdk
from sentry_sdk.integrations.flask import FlaskIntegration
from api.utils.redis_client import redis_client
from api.exceptions.exceptions import register_error_handlers


# Load environment variables from .env file
load_dotenv()

def create_app(test_config=None):
    """Create and configure the Flask application."""
    app = Flask(__name__, instance_relative_config=True)
    
    # Default configuration
    app.config.from_mapping(
        SECRET_KEY=os.getenv('SECRET_KEY', 'dev'),
        SESSION_TYPE='redis',
        SESSION_PERMANENT=False,
        TESTING=False
    )
    
    if test_config is None:
        # Load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # Load the test config if passed in
        app.config.from_mapping(test_config)
    
    # Ensure the instance folder exists
    try:
        os.makedirs(app.instance_path, exist_ok=True)
    except OSError:
        pass
    
    # Initialize Sentry
    if not app.testing and not app.debug:
        sentry_sdk.init(
            dsn=os.getenv('SENTRY_DSN'),
            integrations=[FlaskIntegration()],
            traces_sample_rate=1.0,
            environment=os.getenv('FLASK_ENV', 'production')
        )
    
    # Initialize CORS
    CORS(app)
    
    # Register blueprints
    from api.routes.api import api_bp
    app.register_blueprint(api_bp, url_prefix='/api')
    
    # Register error handlers
    register_error_handlers(app)
    
    # Simple route for health check
    @app.route('/health')
    def health_check():
        return {'status': 'healthy'}
    
    return app
