from fuzzywuzzy import fuzz, process
from typing import List, Dict, Any

def remove_redundant_features(features_list: List[str]) -> List[str]:
    """
    Remove redundant features from a list of product features.

    It uses fuzzy matching to find similar features and removes them from the list.

    Args:
        features_list: A list of product features.

    Returns:
        A list of product features with redundant features removed.
    """
    if not features_list:
        return []
        
    # Convert to list in case it's not
    features_list = list(features_list)
    
    # Make a copy to avoid modifying the original list during iteration
    features_copy = features_list.copy()
    
    for feature in features_copy:
        if not feature or ':' not in feature:
            continue
            
        name = feature.split(": ")[0].strip()
        
        # Get all other features for comparison
        other_features = [
            f.split(': ')[0].strip() 
            for f in features_list 
            if f != feature and ':' in f
        ]
        
        if not other_features:
            continue
            
        # Find the best match using fuzzy matching
        best_match = process.extractOne(name, other_features, scorer=fuzz.ratio)
        
        # If we found a very similar feature, remove the current one
        if best_match and best_match[1] > 89:  # 90% similarity threshold
            try:
                features_list.remove(feature)
            except ValueError:
                # Feature might have been removed already
                pass
    
    return features_list

def match_product_features(features1: List[str], features2: List[str]) -> Dict[str, List[Any]]:
    """
    Compare two lists of product features and return a dictionary with the matched features.

    Args:
        features1: The first list of product features.
        features2: The second list of product features.

    Returns:
        A dictionary with the matched features. The keys are the feature names and 
        the values are lists of two elements: the first element is the value of the 
        feature from the first list, and the second element is the value of the 
        feature from the second list. If a feature is not present in one of the 
        lists, the corresponding value is '--'.
    """
    matched_features = {}
    accuracy_threshold = 68  # Fuzzy matching threshold (0-100)

    # Remove redundant features from both lists
    features1 = remove_redundant_features(features1) if features1 else []
    features2 = remove_redundant_features(features2) if features2 else []
    
    # Create dictionaries of feature name-value pairs
    features1_dict = {}
    for feature in features1:
        if ':' in feature:
            name, value = feature.split(':', 1)
            features1_dict[name.strip()] = value.strip()
    
    features2_dict = {}
    for feature in features2:
        if ':' in feature:
            name, value = feature.split(':', 1)
            features2_dict[name.strip()] = value.strip()
    
    # Find matching features between the two products
    for name1 in features1_dict:
        # Try exact match first
        if name1 in features2_dict:
            matched_features[name1] = [features1_dict[name1], features2_dict[name1]]
            continue
            
        # Try fuzzy matching if no exact match
        best_match = process.extractOne(
            name1, 
            features2_dict.keys(), 
            scorer=fuzz.ratio
        )
        
        if best_match and best_match[1] >= accuracy_threshold:
            matched_name = best_match[0]
            matched_features[name1] = [
                features1_dict[name1], 
                features2_dict[matched_name]
            ]
            # Remove matched feature to prevent duplicate matching
            if matched_name in features2_dict:
                del features2_dict[matched_name]
        else:
            # No match found in features2
            matched_features[name1] = [features1_dict[name1], "--"]
    
    # Add remaining features from features2 that weren't matched
    for name2 in features2_dict:
        matched_features[name2] = ["--", features2_dict[name2]]
    
    return matched_features
