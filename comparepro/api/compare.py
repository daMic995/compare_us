import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Amazon API
X_RapidAPI_Key = os.getenv('AMAZON_API_KEY')
X_RapidAPI_Host = os.getenv('AMAZON_API_HOST')

COMPARISONS = ['title', 'currency', 'price', 'description', 'details', 'images',  'reviews', 'url']

def store_check(url):
    check = ''
    search_string = url.strip("https://")

    store_name = search_string.split('/')[0]

    if store_name == "www.amazon.com":
        check = 'a'
    elif store_name == "bestbuy.com":
        check = 'b'

    return check, url


def amzn_get_asin(url):
    """
    Extracts the Amazon Standard Identification Number (ASIN) from a given Amazon product URL.

    :param url: The URL of the Amazon product.
    :return: The ASIN extracted from the URL.
    """
    # Remove the "https://" prefix from the URL to get the search string
    search_string = url.strip("https://")

    # Split the search string by '/' and extract the ASIN, which is the fourth element
    asin = search_string.split('/')[3][:10]

    return asin
    

def amzn_get_product(product_url):
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

    # Perform the API request
    response = requests.get(api_url, headers=headers, params=querystring)

    # Extract the product data from the API response
    product = response.json()['results'][0]

    return product


def comparator(product):
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