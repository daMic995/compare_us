#!/usr/bin/env python3
"""
Main entry point for the ComparePro API.
"""
import os
from dotenv import load_dotenv
from api import create_app

# Load environment variables from .env file
load_dotenv()

# Create the Flask application
app = create_app()

if __name__ == "__main__":
    # Run the application
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))