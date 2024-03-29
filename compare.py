import requests
#from bs4 import BeautifulSoup
#import numpy as np
#import matplotlib.pyplot as plt

def amzn_get_asin(url):
    """
    Retrieves the product ID from an Amazon URL.

    Parameters:
        url (str): The Amazon URL.

    Returns:
        str: The ASIN extracted from the URL.
    """

    # Extract the search string from the URL by removing the first 8 characters
    search_string = url.strip("https://")

    # Split the search string by '/' and get the product ID; the first ten digits at index 3
    name = search_string.split('/')[0]
    asin = search_string.split('/')[3][:10]

    print(f"Amazon Standard Indentification Number [ASIN]: {asin}")
    return {"asin":asin, "name":name}


def amzn_get_details_from_url(url):
    """
    Retrieves the product details from an Amazon URL.

    Parameters:
        url (str): The Amazon URL.

    Returns:
        dict: The product details extracted from the ASIN from the URL.
    """
    results = amzn_get_asin(url)
    product_id = results["asin"]

    querystring = {"asin":f"{product_id}","country":"US"}

    headers = {
        "X-RapidAPI-Key": "df8135b716msh69f7a613d181ab6p1b7f84jsn8a60b3f71c2d",
        "X-RapidAPI-Host": "amazon23.p.rapidapi.com"
    }

    # Need New Amazon API
    base_url = "https://amazon23.p.rapidapi.com/product-details"
    response = requests.get(base_url, headers=headers, params=querystring, timeout=10)

    print(f"Troubleshoot : {response.json if response.json else 'Nothing returned'}")

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code) + " ")
        return None


def amzn_get_product_details(details_dict):
    """
    Retrieves the product details from an Amazon result json.
    """

    title = details_dict["result"][0]["title"]
    desc = details_dict["result"][0]["description"]
    price = details_dict["result"][0]["price"]["symbol"] + str(details_dict["result"][0]["price"]["current_price"])
    rating = details_dict["result"][0]["reviews"]["rating"]
    no_of_reviews = details_dict["result"][0]["reviews"]["total_reviews"]
    images = details_dict["result"][0]["images"]

    return {"title":title, "desc":desc, "price":price, "rating":rating,
            "no_of_reviews":no_of_reviews, "images":images}
        