from fuzzywuzzy import fuzz, process

def remove_redundant_features(features_list):
    """
    Remove redundant features from a list of product features.

    It uses fuzzy matching to find similar features and removes them from the list.

    Args:
        features_list (list): A list of product features.

    Returns:
        list: A list of product features with redundant features removed.
    """
    for pack in features_list:
        name = pack.split(": ")[0]
        # Get all features except the current one
        leftover = [f.split(': ')[0] for f in features_list]
        leftover.remove(name)

        # Find the best match using fuzzy matching
        best_match = process.extractOne(name, leftover)

        if best_match and best_match[1] > 89:
            # Remove the best match from the list
            for rem in features_list:
                if rem.split(": ")[0] == best_match[0]:
                    features_list.remove(rem)

    return features_list


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
    accuracy = 68

    features1 = remove_redundant_features(features1)
    features2 = remove_redundant_features(features2)

    # Iterate over the first list of features
    for feature1 in features1:
        # Split the feature name and value
        feature_name1, value1 = feature1.split(': ')

        # Use fuzzywuzzy to find the best match in the second list
        best_match = process.extractOne(feature_name1, [f.split(': ')[0] for f in features2])

        if best_match and best_match[1] > accuracy:  # Adjust the threshold to your liking
            # Get the index of the best match in the second list
            index = [f.split(': ')[0] for f in features2].index(best_match[0])

            # Add the feature to the dictionary with the values from both lists
            matched_features[feature_name1] = [value1, features2[index].split(': ')[1]]

            # Remove the best match from the second list so it doesn't get matched again
            features2.pop(index)
        else:
            # If no good match is found, add the feature to the dictionary with a '--' value
            matched_features[feature_name1] = [value1, '--']

    # Iterate over the second list of features to find any features that were not matched
    for feature2 in features2:
        # Split the feature name and value
        feature_name2, value2 = feature2.split(': ')

        # Use fuzzywuzzy to find the best match in the second list
        best_match = process.extractOne(feature_name1, [f.split(': ')[0] for f in features2])

        # Check if the feature is already in the dictionary
        if feature_name2 not in matched_features:
            # Add the feature to the dictionary with a '--' value
            matched_features[feature_name2] = ['--', value2]

    return matched_features