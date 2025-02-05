from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
from logging.handlers import RotatingFileHandler
import json

from api.compare import *
from api.features import match_product_features

app = Flask(__name__)
CORS(app)

TEST_MODE = True

def setup_logger():
    # Setup file handler
    file_handler = RotatingFileHandler(
        './tmp/logs/comparepro.log', 
        maxBytes=100000, backupCount=5)

    # Setup format for logs
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)

    # Setup application logger
    app.logger.addHandler(file_handler)
    app.logger.setLevel(logging.INFO)

# Initialize logger
setup_logger()

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

    if TEST_MODE:
        # Load test products data
        with open('./api/data/amazon/test_data2.json', 'r') as f:
            test_product1 = json.load(f)

        with open('./api/data/walmart/test_data2.json', 'r') as f:
            test_product2 = json.load(f)

        products = [test_product1, test_product2]

    else:
        # Load real products data
        products = [product1, product2]

        for p in products:
            if p == None:
                print('Invalid/Empty product URL!')
                return jsonify({"message": "Invalid product URL!", "status": 400})
                
            [store, url] = store_check(p)
                
            if store == 'amazon':
                # Get the product data from Amazon
                pro = amzn_get_product(url)
                
                if pro["status"] != 200:
                    app.logger.error(pro["message"])
                    return jsonify(pro)
                
                # Construct the valid product data for comparison
                pro = amzn_comparator(pro["product"])

                # Replace the original product URL with the product data
                products[products.index(p)] = pro

                app.logger.info("Product data received from Amazon API!")

            elif store == 'bestbuy':
                # Add support for Best Buy
                # Log action and return message
                app.logger.info("User tried to compare products from Best Buy")
                return jsonify({"message": "Best Buy not supported yet!", "status": 400})

            elif store == 'walmart':
                # Add support for Walmart
                # Log action and return message
                app.logger.info("User tried to compare products from Walmart")
                return jsonify({"message": "Walmart not supported yet!", "status": 400})
            else:
                # Unsupported store
                # Log action and return message
                app.logger.info(f"User tried to compare products from {store}")
                
                return jsonify({"message": "Store not supported yet!", "status": 400})
        
    # Group products by features
    matched_features = match_product_features(products[0]['details'], products[1]['details'])

    return jsonify({
        "product1": products[0], 
        "product2": products[1], 
        "matched_features": matched_features,
        "message": "Products compared successfully!",
        "status": 200})


@app.errorhandler(Exception)
def handle_exception(e):

    return jsonify({"message": "Internal server error!", "status": 500})

"""# Local Flask Development
if __name__ == "__main__":
    app.run(debug=True)"""