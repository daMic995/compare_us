import os
import requests
from typing import Dict, Any
from dotenv import load_dotenv
from api.exceptions.exceptions import ProductFetchError
from api.utils.redis_client import redis_client
from api.utils.constants import COMPARISONS

# Load environment variables from .env file
load_dotenv()

# SerpAPI Configuration for Walmart
SERPAPI_KEY = os.getenv('SERPI_API_KEY')

def get_walmart_product(url: str) -> Dict[str, Any]:
    """
    Fetches product data from Walmart using the provided URL.
    
    Args:
        url: The Walmart product URL
        
    Returns:
        dict: Formatted product data
        
    Raises:
        ProductFetchError: If there's an error fetching the product data
    """
    try:
        # Extract product ID from URL
        product_id = extract_walmart_id(url)
        if not product_id:
            raise ProductFetchError("Invalid Walmart product URL")
        
        # Check cache first
        cache_key = f'walmart:{product_id}'
        cached_data = redis_client.get(cache_key)
        if cached_data:
            return cached_data
        
        # Use SerpAPI to get Walmart product data
        params = {
            'engine': 'walmart_product',
            'product_id': product_id,
            'api_key': SERPAPI_KEY
        }
        
        response = requests.get('https://serpapi.com/search', params=params)
        
        if response.status_code != 200:
            raise ProductFetchError(f"Failed to fetch product data: {response.text}")
        
        product_data = response.json()
        
        # Format the product data
        formatted_product = format_walmart_product(product_data)
        
        # Cache the result for future use (24 hours)
        redis_client.set(cache_key, formatted_product, ex=86400)
        
        return formatted_product
        
    except Exception as e:
        raise ProductFetchError(f"Error fetching Walmart product: {str(e)}")

def extract_walmart_id(url: str) -> str:
    """Extracts product ID from Walmart URL."""
    # Remove protocol and split by /
    parts = url.replace('https://', '').replace('http://', '').split('/')
    
    # Look for product ID in the URL
    for part in parts:
        if part.isdigit() and len(part) > 5:  # Walmart product IDs are numeric and at least 6 digits
            return part
    
    return ''

def format_walmart_product(data: Dict[str, Any]) -> Dict[str, Any]:
    """Formats Walmart product data into a standardized format."""
    try:
        # Extract price information
        price_data : Dict[str, Any] = data.get('price', {})
        current_price = price_data.get('current_price')
        original_price = price_data.get('was_price')
        
        # Extract review information
        reviews = data.get('reviews', {})
        
        return {
            'title': data.get('title', ''),
            'price': current_price,
            'original_price': original_price,
            'currency': 'USD',  # Assuming USD for Walmart US
            'images': [img.get('url', '') for img in data.get('images', []) if 'url' in img],
            'description': data.get('description', ''),
            'details': _extract_walmart_details(data),
            'url': data.get('product_url', ''),
            'store': 'walmart',
            'reviews': {
                'rating': reviews.get('rating'),
                'count': reviews.get('total')
            }
        }
    except Exception as e:
        raise ProductFetchError(f"Error formatting Walmart product data: {str(e)}")

def _extract_walmart_details(data: Dict[str, Any]) -> list:
    """Extracts and formats product details from Walmart data."""
    details = []
    
    # Add specifications if available
    if 'specifications' in data:
        for spec in data['specifications']:
            if 'name' in spec and 'value' in spec:
                details.append(f"{spec['name']}: {spec['value']}")
    
    # Add additional product information
    if 'about_item' in data:
        for item in data['about_item']:
            if isinstance(item, str):
                details.append(item)
    
    return details
