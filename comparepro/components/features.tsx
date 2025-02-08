/**
 * Scrolls smoothly to a specific feature element on the page.
 * Adjusts for the height of the navbar and an additional offset.
 *
 * @param {string} productFeature - The ID of the feature element to scroll to.
 */
export function scrollToFeature(productFeature: string) {
    // Get the height of the navbar, default to 0 if not found
    const navbarHeight = document.querySelector("nav")?.clientHeight || 0;

    // Get the DOM element with the given feature ID
    const element = document.getElementById(productFeature);
    if (element) {
        // Scroll the window to the feature element, adjusting for the navbar and additional offset
        window.scrollTo({ 
            behavior: 'smooth',
            top: element.getBoundingClientRect().top + window.pageYOffset - navbarHeight - 242
        });
    }
}

/**
 * Searches for a specific feature in the matched features object and scrolls to it.
 *
 * @param {string} productFeature - The feature to search for.
 * @param {Object} matchedFeatures - The object containing the matched features.
 */
export function searchFeatures(productFeature: string, matchedFeatures: { [key: string]: [string, string] }): string[] {
    const searchMatch = []; // Initialize the search match array with the product details ID
    
    // Iterate over the matched features object
    for (const feature in matchedFeatures) {
        // Check if the feature name (lowercased) includes the product feature (lowercased)
        if (feature.toLowerCase().includes(productFeature.toLowerCase())) {
            // Add the feature ID to the search match array
            searchMatch.push(feature.toLowerCase());
        }
    }
    
    // Check if the feature ID exists in the DOM
    if (document.getElementById(searchMatch[1])) {
        // Scroll to the feature element using the scrollToFeature function
        scrollToFeature(searchMatch[1]);
    }
    else {
        console.log("Feature not found!");
    }

    return searchMatch;
}