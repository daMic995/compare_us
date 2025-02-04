import os
import requests
from dotenv import load_dotenv

load_dotenv()

# Amazon API
X_RapidAPI_Key = os.getenv('AMAZON_API_KEY')
X_RapidAPI_Host = os.getenv('AMAZON_API_HOST')

COMPARISONS = ['title', 'currency', 'price', 'description', 'details', 'images',  'reviews', 'url']

def store_check(url: str) -> tuple:
    check = ''

    if not url.startswith("https"):
        print("URL does not start with https!")
        return None, url
    
    if url.startswith("https://www.amazon.com"):
        check = 'a'
    elif url.startswith("https://www.bestbuy.com"):
        check = 'b'
    elif url.startswith("https://www.walmart.com"):
        check = 'w'

    return check, url


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

    print(asin)

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

        if response.json():
            if not response.json()['results']:
                return {"message": "API quota reached", "status": 429}
            
            # Extract the product data from the API response
            product = response.json()['results'][0]

            return {"message": "API request successful", "status": response.status_code,  "product": product}

        else:
            {"message": "API request failed", "status": response.status_code}
            return None

    except requests.exceptions.RequestException as e:
        print(f"Error fetching product data: {e}")
        return {"message": f"Error fetching product data: {e}", "status": 500}


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