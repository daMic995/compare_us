import os
from dotenv import load_dotenv
from upstash_redis import Redis

# Load environment variables from .env file
load_dotenv()

# Get Redis configuration from environment variables
redis_url = os.getenv('UPSTASH_REDIS_REST_URL')
redis_token = os.getenv('UPSTASH_REDIS_REST_TOKEN')

if not redis_url or not redis_token:
    raise ValueError("Redis configuration is missing. Please set UPSTASH_REDIS_REST_URL and UPSTASH_REDIS_REST_TOKEN environment variables.")

# Initialize Redis client
redis_client = Redis(url=redis_url, token=redis_token)

def get_redis_client() -> Redis:
    """
    Returns the Redis client instance.
    
    Returns:
        Redis: The Redis client instance
    """
    return redis_client
