from flask import Blueprint, jsonify, session, request
from api.services.compare import compare_products
from api.services.user import generate_user_id_util, get_remaining_comparisons
from api.exceptions.exceptions import (
    InvalidProductURL, UnsupportedStore, ProductFetchError,
    ComparisonLimitExceeded, InvalidRequestData
)

# Create a Blueprint for API routes
api_bp = Blueprint('api', __name__)

@api_bp.route("/python")
def index():
    """
    Root endpoint that returns a welcome message and the number of remaining comparisons.
    """
    remaining = get_remaining_comparisons(session.get('user_id'))
    return jsonify({
        "message": "Welcome to the ComparePro API!",
        "available": remaining,
        "status": 200
    })

@api_bp.route('/python/generate_user_id', methods=['GET'])
def generate_user_id():
    """
    Generates a unique user ID and assigns it to the session.
    Returns the user ID and initializes comparison count.
    """
    try:
        user_id, comparisons = generate_user_id_util()
        session['user_id'] = user_id
        return jsonify({
            'user_id': user_id,
            'available_comparisons': comparisons
        })
    except Exception as e:
        return jsonify({
            "message": "Failed to generate user ID",
            "error": str(e),
            "status": 500
        }), 500

@api_bp.route("/python/compare", methods=["POST"])
def compare():
    """
    Compares two products and returns the comparison data.
    
    Expected JSON payload:
    {
        "product1url": "url1",
        "product2url": "url2",
        "user_id": "user_id"
    }
    """
    try:
        data = request.get_json()
        if not data or 'product1url' not in data or 'product2url' not in data or 'user_id' not in data:
            print("Missing required fields: product1url, product2url, and user_id are required")
            raise InvalidRequestData("Missing required fields: product1url, product2url, and user_id are required")
        
        result = compare_products(
            product1_url=data['product1url'],
            product2_url=data['product2url'],
            user_id=data['user_id'],
            test_mode=False
        )
        return jsonify(result)
        
    except InvalidRequestData as e:
        return jsonify({"message": str(e), "status": 400}), 400
    except ComparisonLimitExceeded as e:
        return jsonify({
            "message": str(e), 
            "status": 403, 
            "available_comparisons": 0}), 403
    #except (InvalidProductURL, UnsupportedStore) as e:
    #    print('InvalidProductURL or UnsupportedStore')
    #    return jsonify({"message": str(e), "status": 400}), 400
    except ProductFetchError as e:
        return jsonify({"message": f"Error fetching product data: {str(e)}",     
        "status": 500}), 500
    except Exception as e:
        return jsonify({"message": "An unexpected error occurred",     
        "error": str(e),     
        "status": 500}), 500
