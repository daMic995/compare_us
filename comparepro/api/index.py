from flask import Flask, jsonify, request
from flask_cors import CORS
import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

import json

from api.compare import *
from api.features import match_product_features


app = Flask(__name__)
CORS(app)

TEST_MODE = False

def setup_logger() -> None:
    """
    Sets up the logger for the application.

    It sets the logging level to INFO and configures Sentry to capture
    errors and exceptions.
    """
    logging.basicConfig(level=logging.INFO, 
                        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')

    # Initialize Sentry
    sentry_sdk.init(
        dsn="https://eb65b450d62fe2bb96a37f0d8d5f71f4@o4508770057584640.ingest.us.sentry.io/4508770067021824",
        # Add data like request headers and IP for users,
        # see https://docs.sentry.io/platforms/python/data-management/data-collected/ for more info
        send_default_pii=True,
        integrations=[LoggingIntegration(level=logging.INFO,
                                        event_level=logging.INFO)],
    )

# Initialize logger and Sentry
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
                    logging.error(pro["message"])
                    return jsonify(pro)
                
                # Construct the valid product data for comparison
                pro = amzn_comparator(pro["product"])

                # Replace the original product URL with the product data
                products[products.index(p)] = pro

            elif store == 'bestbuy':
                # Add support for Best Buy
                # Log action and return message
                logging.info("User tried to compare products from Best Buy")
                return jsonify({"message": "Best Buy not supported yet!", "status": 400})

            elif store == 'walmart':
                # Get the product data from Walmart
                pro = wlmrt_get_product(url)
                
                if pro["status"] != 200:
                    logging.error(pro["message"])
                    return jsonify(pro)
                
                # Construct the valid product data for comparison
                pro = wlmrt_comparator(pro["product"])

                # Replace the original product URL with the product data
                products[products.index(p)] = pro
            
            elif store == None:
                # Invalid URL
                # Return message
                return jsonify({"message": "Invalid URL!", "status": 400})
            else:
                # Unsupported store
                # Log action and return message
                logging.info(f"User tried to compare products from {store}")
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
    print(e)
    logging.error(e)
    return jsonify({"message": "Internal server error!", "status": 500})

"""# Local Flask Development
if __name__ == "__main__":
    app.run(debug=True)"""