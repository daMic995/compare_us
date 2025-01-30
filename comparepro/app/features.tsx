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

export function searchFeatures(productFeature: string, matchedFeatures: { [key: string]: [string, string] }) {
    var productFeature = productFeature.toLowerCase();
    
    const searchMatch = ['product-details'];

    for (const feature in matchedFeatures) {
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