import json
import uuid
import logging
from flask import Blueprint, jsonify, request, session, redirect, url_for, g, current_app
from api.services import comparison_service as comp_service

main = Blueprint('main', __name__)

@main.route("/")
def index():
    """
    Welcome endpoint, shows number of comparisons available for the user.
    """
    # The redis_client is now accessed via the application context 'g'
    curr_comparisons = g.redis_client.get(f'{session["user_id"]}:no_of_comparisons')

    return jsonify({
        "message": "Welcome to the ComparePro API!",
        "available": curr_comparisons,
        "status": 200
    })

@main.route('/generate_user_id', methods=['GET'])
def generate_user_id():
    """
    Generates a unique user ID, stores it in the session, and initializes
    their comparison count in Redis.
    """
    user_id = str(uuid.uuid4())
    session['user_id'] = user_id

    try:
        if not g.redis_client.exists(f'{session["user_id"]}:no_of_comparisons'):
            g.redis_client.set(f'{session["user_id"]}:no_of_comparisons', 5)
    except Exception as e:
        logging.error(f"Error initializing user in Redis: {e}")
        return jsonify({"message": "Could not initialize user session.", "status": 500})

    return jsonify({'user_id': session['user_id']})

@main.route("/compare", methods=["POST"])
def compare():
    """
    Compares two products by their URLs.
    """
    data = request.json
    product1_url = data["product1url"]
    product2_url = data["product2url"]
    user_id = data["user_id"]

    # Configuration is now accessed via current_app
    if current_app.config['TEST_MODE']:
        with open('./api/data/amazon/test_data2.json', 'r') as f:
            product1_data = json.load(f)
        with open('./api/data/walmart/test_data2.json', 'r') as f:
            product2_data = json.load(f)
        products = [product1_data, product2_data]
        available = 5
    else:
        # Business logic is moved to the comparison_service
        result = comp_service.process_comparison(user_id, product1_url, product2_url, g.redis_client)
        if result.get("status") != 200:
            return jsonify(result), result.get("status")

        products = result["products"]
        available = result["available"]

    # Feature matching logic is also in the service
    matched_features = comp_service.match_features(products[0]['details'], products[1]['details'])

    return jsonify({
        "product1": products[0],
        "product2": products[1],
        "matched_features": matched_features,
        "message": "Products compared successfully!",
        "available": available,
        "status": 200
    })

@main.route("/reset")
def reset():
    """Resets the number of available comparisons for the user."""
    g.redis_client.set(f'{session["user_id"]}:no_of_comparisons', 5)
    # Redirect to the main index route within this blueprint
    return redirect(url_for('main.index'))

# Note: The /decrement route from the original file seemed like a debug route
# and has been removed for this refactoring to simplify the API. A similar
# function can be achieved via the /compare endpoint.

@main.app_errorhandler(Exception)
def handle_exception(e):
    """Global exception handler for the blueprint."""
    logging.error(f"An unhandled exception occurred: {e}", exc_info=True)
    return jsonify({
        "message": "An internal server error occurred.",
        "status": 500
    }), 500
