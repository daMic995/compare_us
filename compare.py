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
    # Split the search string by '/' and get the product ID at index 3
    asin = search_string.split('/')[3]
    return asin


def amzn_get_details_from_url(url):
    """
    Retrieves the product details from an Amazon URL.

    Parameters:
        url (str): The Amazon URL.

    Returns:
        dict: The product details extracted from the ASIN from the URL.
    """

    product_id = amzn_get_asin(url)

    querystring = {"asin":f"{product_id}","country":"US"}

    headers = {
        "X-RapidAPI-Key": "df8135b716msh69f7a613d181ab6p1b7f84jsn8a60b3f71c2d",
        "X-RapidAPI-Host": "amazon23.p.rapidapi.com"
    }

    base_url = "https://amazon23.p.rapidapi.com/product-details"
    response = requests.get(base_url, headers=headers, params=querystring, timeout=18)

    if response.status_code == 200:
        return response.json()
    else:
        print("Error: " + str(response.status_code) + " ")
        return None


def amzn_get_product_details(details_dict):
    """
    Retrieves the product details from a Amazon result json.
    """

    title = details_dict["result"][0]["title"]
    desc = details_dict["result"][0]["description"]
    price = details_dict["result"][0]["price"]["symbol"] + str(details_dict["result"][0]["price"]["current_price"])
    rating = details_dict["result"][0]["reviews"]["rating"]
    no_of_reviews = details_dict["result"][0]["reviews"]["total_reviews"]
    images = details_dict["result"][0]["images"]
    return {"title":title, "desc":desc, "price":price, "rating":rating,
            "no_of_reviews":no_of_reviews, "images":images}


# Start from here
print("Compare Stuff".center(50, "-"))
cmp_items = int(input("How many items do you want to compare? "))

urls = []

for i in range(cmp_items):
    url = input(f"Enter the Amazon URL [{i+1}]: ")
    urls.append(url)
    print("\n")

# Get the product details from Amazon
product_details = [amzn_get_details_from_url(url) for url in urls]

# Print the product details
for details, i in zip(product_details, range(1, cmp_items + 1)):
    if details is not None:
        print(f"""
Product Details [{i}] ->
Title: {amzn_get_product_details(details)["title"]}
Description: {amzn_get_product_details(details)["desc"]}
Price: {amzn_get_product_details(details)["price"]}
Rating: {amzn_get_product_details(details)["rating"]}
No. of Reviews: {amzn_get_product_details(details)["no_of_reviews"]}\n""")
    else:
        print(f"""Error ->
Product Details [{i}] not found.\n""")
        