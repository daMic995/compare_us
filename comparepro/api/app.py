from api import create_app
import os

# Get the environment from env variable, default to 'development'
# In a production environment, you would set FLASK_ENV to 'production'
env_name = os.getenv('FLASK_ENV', 'development')

# Create the Flask app instance using the application factory
app = create_app(env_name)
