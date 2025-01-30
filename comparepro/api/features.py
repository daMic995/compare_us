def match_product_features(features1: list, features2: list) -> dict:
    """
    Compare two lists of product features and return a dictionary with the matched features.

    Args:
        features1 (list): The first list of product features.
        features2 (list): The second list of product features.

    Returns:
        dict: A dictionary with the matched features. The keys are the feature names and the values are lists of two elements, the first element is the value of the feature from the first list, and the second element is the value of the feature from the second list. If a feature is not present in one of the lists, the value is '--'.
    """
    matched_features = {}

    # Iterate over the first list of features
    for feature1 in features1:
        # Split the feature name and value
        feature_name1, value1 = feature1.split(': ')

        # Iterate over the second list of features
        for feature2 in features2:
            # Split the feature name and value
            feature_name2, value2 = feature2.split(': ')

            # Check if the feature names are the same
            if feature_name1 == feature_name2:
                # Add the feature to the dictionary with the values from both lists
                matched_features[feature_name1] = [value1, value2]
                break
            # If the feature is not present in the second list, add it to the dictionary with a '--' value
            elif feature_name2 not in matched_features:
                matched_features[feature_name2] = ['--', value2]

        # If the feature is not present in the second list, add it to the dictionary with a '--' value
        if feature_name1 not in matched_features:
            matched_features[feature_name1] = [value1, '--']

    return matched_features