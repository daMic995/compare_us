import os
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration
from flask import Flask, g
from flask_cors import CORS
from upstash_redis import Redis
from api.config import config_by_name

def setup_sentry(dsn):
    """Initializes Sentry for error tracking."""
    sentry_sdk.init(
        dsn=dsn,
        send_default_pii=True,
        integrations=[LoggingIntegration(level=logging.INFO, event_level=logging.INFO)],
    )

def create_app(config_name: str = 'default') -> Flask:
    """
    Creates and configures a Flask application instance using the factory pattern.

    Args:
        config_name (str): The name of the configuration to use
                           (e.g., 'development', 'production').

    Returns:
        Flask: The configured Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration from the specified config object
    app.config.from_object(config_by_name[config_name])

    # Initialize Flask extensions
    CORS(app)

    # Set up Sentry if a DSN is provided in the configuration
    if app.config.get('SENTRY_DSN'):
        setup_sentry(app.config['SENTRY_DSN'])

    # Configure application logging
    logging.basicConfig(level=logging.INFO,
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Set up a context-bound Redis client
    @app.before_request
    def before_request():
        """
        Before each request, create a Redis client and store it in the 'g' object.
        This ensures that the Redis client is available for the duration of the request.
        """
        if 'redis_client' not in g:
            try:
                g.redis_client = Redis(
                    url=app.config['UPSTASH_REDIS_REST_URL'],
                    token=app.config['UPSTASH_REDIS_REST_TOKEN']
                )
            except Exception as e:
                logging.error(f"Failed to initialize Redis client: {e}")
                g.redis_client = None

    # Register blueprints to structure the routes
    from .routes.main import main as main_blueprint
    app.register_blueprint(main_blueprint, url_prefix='/api/python')

    # A simple health check endpoint to confirm the app is running
    @app.route('/health')
    def health_check():
        return "OK", 200

    app.logger.info("Application created successfully.")
    return app
