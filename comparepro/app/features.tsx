/**
 * Compares two arrays of product features and returns an object with the matched features.
 * @param product1Features - Array of features for the first product.
 * @param product2Features - Array of features for the second product.
 * @returns An object with the feature names as keys and an array of two values as the value.
 *          The first value is the feature value for the first product and the second value
 *          is the feature value for the second product.
 */
export function pfeatures(product1Features: string[], product2Features: string[]): { [key: string]: [string, string] } {
    /**
     * An object to store the matched features.
     * The key is the feature name and the value is an array of two values.
     * The first value is the feature value for the first product and the second value
     * is the feature value for the second product.
     */
    const matchedFeatures: { [key: string]: [string, string] } = {};

    // Iterate over the features of the first product
    for (const feature1 of product1Features) {
        // Split the feature into name and value
        const [featureName1, featureValue1] = feature1.split(': ');

        // Iterate over the features of the second product
        for (const feature2 of product2Features) {
            // Split the feature into name and value
            const [featureName2, featureValue2] = feature2.split(': ');

            // If the feature name matches, add it to the matchedFeatures object
            if (featureName1 === featureName2) {
                matchedFeatures[featureName1] = [featureValue1, featureValue2];
                break;
            // If the feature name does not match, add it to the matchedFeatures object with a value of '--'
            } else if (!matchedFeatures[featureName2]) {
                matchedFeatures[featureName2] = ['--', featureValue2];
            }
        }

        // If the feature name does not match any of the features of the second product, add it to the matchedFeatures object with a value of '--'
        if (!matchedFeatures[featureName1]) {
            matchedFeatures[featureName1] = [featureValue1, '--'];
        }
    }

    return matchedFeatures;
}


export function scrollToFeature(productFeature: string) {
    const navbarHeight = document.querySelector("nav")?.clientHeight || 0;

    const element = document.getElementById(productFeature);
    if (element) {
        window.scrollTo({ 
            behavior: 'smooth',
            top: element.getBoundingClientRect().top + window.pageYOffset - navbarHeight - 8
         });
    }
}

export function searchFeatures(productFeature: string, product1Details: string[], product2Details: string[]) {
    var productFeature = productFeature.toLowerCase();
    
    const existingFeatures = pfeatures(product1Details, product2Details);
    const searchMatch = ['product-details'];

    for (const feature in existingFeatures) {
        if (feature.toLowerCase().includes(productFeature)) {
            searchMatch.push(feature.toLowerCase());
        }
    }
    console.log(searchMatch);
    if (document.getElementById(searchMatch[1])) {
        scrollToFeature(searchMatch[1]);
    }
    else {
        console.log("Feature not found!")
    }

}