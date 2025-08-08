import requests
import logging
from fuzzywuzzy import fuzz, process
from serpapi import GoogleSearch
from flask import current_app

# --- Feature Matching Logic (from features.py) ---

def _remove_redundant_features(features_list):
    """Internal helper to remove redundant features from a list."""
    # This is a simplified version of the original logic for clarity
    unique_features = []
    seen_names = set()
    for feature in features_list:
        name = feature.split(": ")[0]
        if name.lower() not in seen_names:
            unique_features.append(feature)
            seen_names.add(name.lower())
    return unique_features

def match_features(features1: list, features2: list) -> dict:
    """Compares two lists of product features using fuzzy matching."""
    matched = {}
    accuracy_threshold = 68

    features1 = _remove_redundant_features(features1)
    features2 = _remove_redundant_features(features2)

    for f1 in features1:
        name1, val1 = f1.split(': ', 1)
        best_match = process.extractOne(name1, [f.split(': ', 1)[0] for f in features2])

        if best_match and best_match[1] > accuracy_threshold:
            idx = [f.split(': ', 1)[0] for f in features2].index(best_match[0])
            _, val2 = features2.pop(idx).split(': ', 1)
            matched[name1] = [val1, val2]
        else:
            matched[name1] = [val1, '--']

    for f2 in features2:
        name2, val2 = f2.split(': ', 1)
        matched[name2] = ['--', val2]

    return matched

# --- Product Comparison Logic (from compare.py) ---

def _get_store_from_url(url: str) -> str:
    """Determines the store from a product URL."""
    if not url.startswith("https"):
        return None
    try:
        return url.strip("https://").split("/")[0].split(".")[1]
    except IndexError:
        return None

def _amzn_get_product(url: str):
    """Fetches product data from Amazon."""
    # ... (logic from amzn_get_product and amzn_comparator)
    return {"message": "Amazon support not fully implemented in this refactor.", "status": 400}

def _wlmrt_get_product(url: str):
    """Fetches product data from Walmart."""
    # ... (logic from wlmrt_get_product and wlmrt_comparator)
    return {"message": "Walmart support not fully implemented in this refactor.", "status": 400}

# --- Main Service Function ---

def process_comparison(user_id: str, url1: str, url2: str, redis_client):
    """
    Main service function to handle the comparison logic.
    Checks user's available comparisons, fetches product data, and decrements count.
    """
    try:
        available_str = redis_client.get(f'{user_id}:no_of_comparisons')
        if not available_str:
            # If user has no count, initialize it.
            redis_client.set(f'{user_id}:no_of_comparisons', 5)
            available = 5
        else:
            available = int(available_str)

        if available <= 0:
            return {"message": "You have exhausted your comparisons!", "available": 0, "status": 403}

        # This is a placeholder for the full product fetching logic.
        # In a real scenario, you would call the specific store functions.
        product1_data = {"details": ["FeatureA: Value1", "FeatureB: Value2"], "price": "100"}
        product2_data = {"details": ["FeatureA: ValueA", "FeatureC: Value3"], "price": "120"}

        # Decrement the count after successful processing
        redis_client.set(f'{user_id}:no_of_comparisons', available - 1)

        return {
            "products": [product1_data, product2_data],
            "available": available - 1,
            "status": 200
        }

    except Exception as e:
        logging.error(f"Error in comparison service: {e}")
        return {"message": "An error occurred during comparison.", "status": 500}
