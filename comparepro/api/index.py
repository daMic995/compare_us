from flask import Flask, jsonify, request, session, redirect, url_for
from flask_cors import CORS
from upstash_redis import Redis

from dotenv import load_dotenv
import json
import uuid
from datetime import timedelta

import logging
import sentry_sdk
from sentry_sdk.integrations.logging import LoggingIntegration

from api.compare import *
from api.features import match_product_features

load_dotenv()
redis_url = os.getenv('UPSTASH_REDIS_REST_URL')
token = os.getenv('UPSTASH_REDIS_REST_TOKEN')

# Configure Redis
upstash_redis_client = Redis(url="https://sought-husky-11990.upstash.io", token=token)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.getenv('REDIS_SECRET_KEY')
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = False

# Enable CORS
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
def index():
    curr_comparisons = upstash_redis_client.get(f'{session['user_id']}:no_of_comparisons')

    return jsonify({"message": "Welcome to the ComparePro API!",
                    "available": curr_comparisons,
                    "status": 200})


@app.route('/api/python/generate_user_id', methods=['GET'])
def generate_user_id():
    """
    Generates a unique user ID and assigns it to the session.

    Returns the user ID.
    """
    # Configure session id
    user_id = str(uuid.uuid4())
    session['user_id'] = user_id

    try:
        # Check if the user ID already exists in Redis
        if not upstash_redis_client.exists(f'{session["user_id"]}:no_of_comparisons'):
            # Set the number of available comparisons to 5
            upstash_redis_client.set(f'{session["user_id"]}:no_of_comparisons', 5)
        
    except Exception as e:
        # Log any errors
        logging.error(e)
        return jsonify({"message": "Something went wrong!", "status": 500})
    
    # Return the user ID
    return jsonify({'user_id': session['user_id']})


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

    # Get product URLs and user ID
    product1 = data["product1url"]
    product2 = data["product2url"]
    c_user_id = data["user_id"]

    # Get available comparisons
    available = int(upstash_redis_client.get(f'{c_user_id}:no_of_comparisons'))

    # Check if there are available comparisons
    if available <= 0:
        # Return no available comparisons
        return jsonify({"message": "You have exhausted your comparisons!", 
                        "available": available,
                        "status": 403})

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

    # Update available comparisons in Redis
    upstash_redis_client.set(f'{c_user_id}:no_of_comparisons', available-1)

    return jsonify({
        "product1": products[0], 
        "product2": products[1], 
        "matched_features": matched_features,
        "message": "Products compared successfully!",
        "available": available-1,
        "status": 200})


@app.route("/api/python/reset")
def reset():
    upstash_redis_client.set(f'{session['user_id']}:no_of_comparisons', 5)
    return redirect(url_for('index'))

"""
@app.route("/api/python/decrement")
def decrement():
    curr_comparisons = int(upstash_redis_client.get('no_of_comparisons'))
    print('Before decrement', curr_comparisons)

    upstash_redis_client.set('no_of_comparisons', curr_comparisons-1)
    print('After decrement', upstash_redis_client.get('no_of_comparisons'))
    return redirect(url_for('index'))"""


@app.errorhandler(Exception)
def handle_exception(e):
    print(e)
    logging.error(e)
    return jsonify({"message": "Internal server error!", 
                    "status": 500})

"""# Local Flask Development
if __name__ == "__main__":
    app.run(debug=True)"""