from api.services.user import decrement_comparisons, get_remaining_comparisons
from api.utils.store_utils import store_check
from api.utils.feature_utils import match_product_features
from api.exceptions.exceptions import (
    InvalidProductURL, UnsupportedStore, ProductFetchError, ComparisonLimitExceeded
)

import json

# Import store-specific modules
from api.services.stores.amazon import get_amazon_product
from api.services.stores.walmart import get_walmart_product


def compare_products(product1_url: str, product2_url: str, user_id: str, test_mode: bool = False):
    """
    Compare two products from different stores.
    
    Args:
        product1_url: URL of the first product
        product2_url: URL of the second product
        user_id: ID of the user making the comparison
        test_mode: If True, use test data instead of making real API calls
        
    Returns:
        dict: Comparison results
        
    Raises:
        InvalidProductURL: If a product URL is invalid
        UnsupportedStore: If a store is not supported
        ProductFetchError: If there's an error fetching product data
        ComparisonLimitExceeded: If user has no comparisons remaining
    """

    if test_mode:
        # In test mode, use test data
        with open('./api/data/amazon/test_data2.json', 'r') as f:
            product1 = json.load(f)
        with open('./api/data/walmart/test_data2.json', 'r') as f:
            product2 = json.load(f)
    else:
        # Check remaining comparisons
        remaining = get_remaining_comparisons(user_id)
        if remaining <= 0:
            raise ComparisonLimitExceeded("You have exhausted your comparisons!")
        
        # Get store information
        store1, url1 = store_check(product1_url)
        store2, url2 = store_check(product2_url)
    
        # Check if both URLs are valid
        if not store1 or not store2:
            raise InvalidProductURL("One or both product URLs are invalid")
    
        # Fetch product data
        try:
                
            # Fetch product 1
            if store1 == 'amazon':
                product1 = get_amazon_product(url1)
            elif store1 == 'walmart':
                product1 = get_walmart_product(url1)
            else:
                raise UnsupportedStore(f"Store '{store1}' is not supported")
                
            # Fetch product 2
            if store2 == 'amazon':
                product2 = get_amazon_product(url2)
            elif store2 == 'walmart':
                product2 = get_walmart_product(url2)
            else:
                raise UnsupportedStore(f"Store '{store2}' is not supported")
        
        except Exception as e:
            # Re-raise known exceptions
            if isinstance(e, (InvalidProductURL, UnsupportedStore, ComparisonLimitExceeded)):
                raise
            # Wrap other exceptions in ProductFetchError
            raise ProductFetchError(f"Error comparing products: {str(e)}")

        # Decrement comparisons after making API calls
        decrement_comparisons(user_id)

    # Match features between products
    matched_features = match_product_features(
        product1.get('details', []),
        product2.get('details', [])
    )
        
    # Prepare response
    return {
        "status": 200,
        "products": [product1, product2],
        "matched_features": matched_features,
        "available_comparisons": get_remaining_comparisons(user_id)
    }