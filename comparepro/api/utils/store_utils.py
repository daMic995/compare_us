def store_check(url: str) -> tuple:
    """
    Extracts the store name from a product URL.
    
    Args:
        url: The product URL
        
    Returns:
        tuple: (store_name, url) or (None, url) if invalid
    """
    if not url or not isinstance(url, str):
        return None, url
        
    if not url.startswith("http"):
        return None, url
    
    try:
        # Remove protocol and split by /
        domain_parts = url.strip("https://").strip("http://").split("/")[0].split(".")
        
        # Handle subdomains (e.g., www.amazon.com -> amazon)
        if len(domain_parts) > 2:
            # Check for common subdomains
            if domain_parts[0] in ['www', 'smile']:
                return domain_parts[1], url
        print(domain_parts)
        return domain_parts[0], url
        
    except (IndexError, AttributeError):
        return None, url
