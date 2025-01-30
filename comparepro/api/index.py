from flask import Flask, jsonify, request
from flask_cors import CORS

from api.compare import *
from api.test import test_products_data

app = Flask(__name__)
CORS(app)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"


@app.route("/api/compare", methods=["POST"])
def compare():
    """
    Compares two products and returns the comparison data.

    Args:
        product1 (str): The URL of the first product.
        product2 (str): The URL of the second product.

    Returns:
        dict: The comparison data.
    """
    data = request.json

    product1 = data["product1"]
    product2 = data["product2"]

    if product1 and product2:
        print('Products URL Received!')

    products = test_products_data

    """products = [product1, product2]
    
    for p in products:
        [check, url] = store_check(p)
        if check == 'a':
            # Get the product data from Amazon
            pro = amzn_get_product(url)
            # Construct the valid product data for comparison
            pro = comparator(pro)

            # Replace the original product URL with the product data
            products[products.index(p)] = pro
        elif check == 'b':
            # Add support for Best Buy
            pass"""
    
    return jsonify({"product1": products[0], "product2": products[1], "status": 200})