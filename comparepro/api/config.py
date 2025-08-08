import os
from dotenv import load_dotenv

# Load environment variables from a .env file
load_dotenv()

class Config:
    """Base configuration settings."""
    # Secret key for session management
    SECRET_KEY = os.getenv('REDIS_SECRET_KEY', 'your-default-secret-key')

    # Flask-Session configuration
    SESSION_TYPE = 'redis'
    SESSION_PERMANENT = False

    # App-specific settings
    TEST_MODE = False
    DEBUG = False
    TESTING = False
    NEXTJS_API_ENDPOINT = "/api/python"

    # Upstash Redis credentials
    UPSTASH_REDIS_REST_URL = os.getenv('UPSTASH_REDIS_REST_URL')
    UPSTASH_REDIS_REST_TOKEN = os.getenv('UPSTASH_REDIS_REST_TOKEN')

    # Sentry DSN for error tracking
    SENTRY_DSN = os.getenv('SENTRY_DSN', 'https://eb65b450d62fe2bb96a37f0d8d5f71f4@o4508770057584640.ingest.us.sentry.io/4508770067021824')

    # External API Keys
    AMAZON_API_KEY = os.getenv('AMAZON_API_KEY')
    AMAZON_API_HOST = os.getenv('AMAZON_API_HOST')
    SERPI_API_KEY = os.getenv('SERPI_API_KEY')

class DevelopmentConfig(Config):
    """Development configuration."""
    DEBUG = True

class TestingConfig(Config):
    """Testing configuration."""
    TESTING = True
    TEST_MODE = True

class ProductionConfig(Config):
    """Production configuration."""
    pass

# Dictionary to map config names to their respective classes
config_by_name = {
    'development': DevelopmentConfig,
    'testing': TestingConfig,
    'production': ProductionConfig,
    'default': DevelopmentConfig
}
