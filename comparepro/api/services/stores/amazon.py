import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from api.exceptions.exceptions import ProductFetchError
from api.utils.redis_client import redis_client
from api.utils.constants import COMPARISONS

# Load environment variables from .env file
load_dotenv()

# Amazon API Configuration
AMAZON_API_KEY = os.getenv('AMAZON_API_KEY')
AMAZON_API_HOST = os.getenv('AMAZON_API_HOST')

def get_amazon_product(url: str) -> Dict[str, Any]:
    """
    Fetches product data from Amazon using the provided URL.
    
    Args:
        url: The Amazon product URL
        
    Returns:
        dict: Formatted product data
        
    Raises:
        ProductFetchError: If there's an error fetching the product data
    """
    try:
        # Extract ASIN from URL
        asin = extract_asin(url)
        if not asin:
            raise ProductFetchError("Invalid Amazon product URL")
        
        # Check cache first
        cache_key = f'amazon:{asin}'
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return cached_data
        
        # Make API request to Amazon API
        headers = {
            'X-RapidAPI-Key': AMAZON_API_KEY,
            'X-RapidAPI-Host': AMAZON_API_HOST
        }
        
        params = {
            'asin': asin,
            'country': 'US'
        }
        
        response = requests.get(
            'https://' + AMAZON_API_HOST + '/product',
            headers=headers,
            params=params
        )
        
        if response.status_code != 200:
            print('Here', response.text)
            raise ProductFetchError(f"Failed to fetch product data: {response.text}")
        
        product_data = response.json()
        
        # Format the product data
        formatted_product = format_amazon_product(product_data)
        
        # Cache the result for future use (24 hours)
        redis_client.set(cache_key, formatted_product, ex=86400)
        
        return formatted_product
        
    except Exception as e:
        raise ProductFetchError(f"Error fetching Amazon product: {str(e)}")

def extract_asin(url: str) -> str:
    """Extracts ASIN from Amazon product URL."""
    # Remove protocol and split by /
    parts = url.replace('https://', '').replace('http://', '').split('/')
    
    # Look for 'dp' in the URL path
    try:
        dp_index = parts.index('dp')
        if dp_index + 1 < len(parts):
            # Get the ASIN (first 10 characters after 'dp/')
            return parts[dp_index + 1][:10]
    except ValueError:
        pass
    
    # If 'dp' not found, look for ASIN directly in the URL
    for part in parts:
        if len(part) == 10 and part.isalnum():
            return part
    
    return ''

def format_amazon_product(data: Dict[str, Any]) -> Dict[str, Any]:
    """Formats Amazon product data into a standardized format."""
    try:
        return {
            'title': data.get('title', ''),
            'price': data.get('price', {}).get('current_price'),
            'original_price': data.get('price', {}).get('before_price'),
            'currency': 'USD',  # Assuming USD for Amazon US
            'images': data.get('images', []),
            'description': data.get('description', ''),
            'details': _extract_amazon_details(data),
            'url': data.get('url', ''),
            'store': 'amazon',
            'reviews': {
                'rating': data.get('reviews', {}).get('rating'),
                'count': data.get('reviews', {}).get('total_reviews')
            }
        }
    except Exception as e:
        raise ProductFetchError(f"Error formatting Amazon product data: {str(e)}")

def _extract_amazon_details(data: Dict[str, Any]) -> list:
    """Extracts and formats product details from Amazon data."""
    details = []
    
    # Add key specifications
    if 'key_specs' in data:
        for spec in data['key_specs']:
            if 'name' in spec and 'value' in spec:
                details.append(f"{spec['name']}: {spec['value']}")
    
    # Add additional details
    if 'details' in data:
        for section in data['details']:
            if 'title' in section and 'items' in section:
                for item in section['items']:
                    if 'name' in item and 'value' in item:
                        details.append(f"{item['name']}: {item['value']}")
    
    return details
