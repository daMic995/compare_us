import os
import requests
from dotenv import load_dotenv
from serpapi import GoogleSearch

load_dotenv()

# Amazon API
X_RapidAPI_Key = os.getenv('AMAZON_API_KEY')
X_RapidAPI_Host = os.getenv('AMAZON_API_HOST')

# Google API (SerpAPI) - Walmart
SERPI_API_KEY = os.getenv('SERPI_API_KEY')

# List of fields to compare
COMPARISONS = ['title', 'currency', 'price', 'description', 'details', 'images',  'reviews', 'url']

def store_check(url: str) -> tuple:

    if not url.startswith("https"):
        return None, url
    
    store = url.strip("https://").split("/")[0].split(".")[1]

    return store, url


def amzn_get_asin(url: str) -> str:
    """
    Extracts the Amazon Standard Identification Number (ASIN) from a given Amazon product URL.

    :param url: The URL of the Amazon product.
    :return: The ASIN extracted from the URL.
    """
    # Remove the "https://" prefix from the URL to get the search string
    search_string = url.strip("https://")

    # Split the search string by '/' and extract the ASIN, which is the fourth element
    isdp = 'dp' == search_string.split('/')[2]

    if isdp:
        asin = search_string.split('/')[3][:10]
    else:
        asin = search_string.split('/')[2][:10]

    return asin
    

def amzn_get_product(product_url : str):
    """
    Retrieves product data from Amazon using the provided product URL.

    :param product_url: The URL of the Amazon product.
    :return: A dictionary containing product details.
    """
    # Extract the ASIN from the product URL
    asin = amzn_get_asin(product_url)

    # Define the API endpoint for fetching product data
    api_url = "https://amazon-online-data-api.p.rapidapi.com/product"

    # Set the query parameters with the ASIN and geographical location
    querystring = {"asins": asin, "geo": "US"}

    # Set the necessary headers for the API request
    headers = {
        "x-rapidapi-key": X_RapidAPI_Key,
        "x-rapidapi-host": X_RapidAPI_Host
    }

    try:
        # Perform the API request
        response = requests.get(api_url, headers=headers, params=querystring)

        # Check if the request was successful
        if response.json():
            # Check if the API quota has been reached
            if not response.json().get('results'):
                return {"message": "API quota reached", "status": 429}
            
            # Extract the product data from the API response
            product = response.json()['results'][0]
            return {"message": "API request successful", "status": response.status_code,  
                    "product": product}

        else:
            return {"message": "API request failed", "status": response.status_code}

    except requests.exceptions.RequestException as e:
        return {"message": f"Error fetching product data: {e}", "status": 500}


def amzn_comparator(product):
    """
    Compares the product data to the comparison criteria and 
    constructs a dictionary with the valid comparisons.

    Args:
        product (dict): The product data.

    Returns:
        dict: A dictionary with the valid product data.
    """
    valid = {}
    for c in COMPARISONS:
        for p, v in product.items():
            if c in p:
                # Construct the valid dictionary with the comparison
                # criteria as the keys and the product data as the values
                valid[f'{c}'] = v

    return valid


def wlmrt_get_pid(url: str) -> str:
    """
    Extracts the Walmart product ID from a given URL.

    Args:
        url (str): The URL of the Walmart product.

    Returns:
        str: The product ID of the Walmart product.
    """
    # Remove the "https://" prefix from the URL to get the search string
    search_string = url.strip("https://")

    # Split the search string by '/' and extract the product ID, which is the third element
    product_id = search_string.split('/')[3].split('?')[0]
    return product_id
    

def wlmrt_get_product(product_url: str) -> dict:
    """
    Retrieves the product data from the Walmart API using the provided product URL.

    Args:
        product_url (str): The URL of the Walmart product.

    Returns:
        dict: A dictionary containing the product data and a status message.
    """
    # Extract the Walmart product ID from the provided URL
    wlmrt_pid = wlmrt_get_pid(product_url)

    # Construct the API request parameters
    params = {
        "engine": "walmart_product",
        "product_id": wlmrt_pid,
        "api_key": SERPI_API_KEY
    }

    try:
        # Perform the API request
        search = GoogleSearch(params)
        results = search.get_dict()
        
        # Check if the request was successful
        if results['search_metadata']['status'] != 'Success':
            return {"message": "API request failed", "status": 500}

        # Return the product data and a success message
        return {"message": "API request successful", "status": 200,  
                "product": results['product_result']}
    
    except Exception as e:
        # Return an error message and a 500 status code if an error occurred
        return {"message": f"Error fetching product data: {e}", "status": 500}


def wlmrt_comparator(product):
    """
    Compares the product data to the comparison criteria and 
    constructs a dictionary with the valid comparisons.

    Args:
        product (dict): The product data.

    Returns:
        dict: A dictionary with the valid product data.
    """
    # Initialize the valid dictionary with an empty details list
    valid = {"details": []}

    # Iterate over the product data
    for key, value in product.items():
        # Check if the key is in the comparison criteria
        if key in COMPARISONS:
            # Handle the reviews key separately to structure its content
            if key == "reviews":
                valid[key] = {
                    'count': value,
                    'rating': product["rating"] if product.get("rating") else 0
                }
                continue
            # Add the value to the valid dictionary for matched keys
            valid[key] = value

        # Handle the short_description_html key
        elif key == "short_description_html":
            # Populate the description field in the valid dictionary
            valid['description'] = value

        # Handle the specification_highlights key
        elif key == "specification_highlights":
            # Add each specification to the details list with formatted text
            for spec in value:
                valid['details'].append(f"{spec['key']}: {spec['value'].replace(':', '-')}")

        # Handle the price_map key
        elif key == "price_map":
            # Extract currency and price information
            valid['currency'] = value["currency"]
            valid['price'] = value["price"]

        # Handle the product_page_url key
        elif key == "product_page_url":
            # Store the product URL
            valid['url'] = value

    # Return the constructed dictionary with valid product data
    return valid
