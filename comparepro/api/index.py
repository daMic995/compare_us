from flask import Flask, jsonify, request
from flask_cors import CORS
import json

from api.compare import *
from api.features import match_product_features

app = Flask(__name__)
CORS(app)

@app.route("/api/python")
def hello_world():
    return "<p>Hello, World!</p>"

@app.route("/api/python/compare", methods=["POST"])
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

    product1 = data["product1url"]
    product2 = data["product2url"]

    if product1 and product2:
        print('Products URL Received!')

    """
    # Load test products data
    with open('api/data/test_products_data.json', 'r') as f:
        products = json.load(f)

    """
    products = [product1, product2]

    for p in products:
        if p == None:
            print('Invalid/Empty product URL!')
            return jsonify({"message": "Invalid product URL!", "status": 400})
            
        [check, url] = store_check(p)
            
        if check == 'a':
            # Get the product data from Amazon
            pro = amzn_get_product(url)
            
            if pro == None:
                print('Product data from Amazon returned None!')
                return jsonify({"message": "Amazon API response error!", "status": 400})
            
            # Construct the valid product data for comparison
            pro = comparator(pro)

            # Replace the original product URL with the product data
            products[products.index(p)] = pro

        elif check == 'b':
            # Add support for Best Buy
            pass
        else:
            # Invalid product URL
            print('Invalid product URL!')
            return jsonify({"message": "Invalid product URL!", "status": 400})
        
    matched_features = match_product_features(products[0]['details'], products[1]['details'])

    return jsonify({
        "product1": products[0], 
        "product2": products[1], 
        "matched_features": matched_features,
        "message": "Products compared successfully!",
        "status": 200})

"""# Local Flask Development
if __name__ == "__main__":
    app.run(debug=True)"""