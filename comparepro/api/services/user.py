import uuid
from api.utils.redis_client import redis_client


def generate_user_id_util():
    """
    Generates a new user ID and initializes their comparison count.
    
    Returns:
        tuple: (user_id, available_comparisons)
    """
    user_id = str(uuid.uuid4())
    available_comparisons = 5
    redis_client.set(f'{user_id}:no_of_comparisons', available_comparisons)
    return user_id, available_comparisons


def get_remaining_comparisons(user_id):
    """
    Get the number of remaining comparisons for a user.
    
    Args:
        user_id (str): The user's ID
        
    Returns:
        int: Number of remaining comparisons, or 0 if user doesn't exist
    """
    if not user_id:
        return 0
    
    comparisons = redis_client.get(f'{user_id}:no_of_comparisons')
    return int(comparisons) if comparisons is not None else 0


def decrement_comparisons(user_id):
    """
    Decrements the user's remaining comparison count.
    
    Args:
        user_id (str): The user's ID
        
    Returns:
        int: New remaining comparison count
        
    Raises:
        ValueError: If user has no comparisons remaining
    """
    if not user_id:
        raise ValueError("User ID is required")
        
    key = f'{user_id}:no_of_comparisons'
    remaining = redis_client.get(key)
    
    if remaining is None:
        remaining = 5
    else:
        remaining = int(remaining)
        if remaining <= 0:
            raise ValueError("No comparisons remaining")
        remaining -= 1
    
    redis_client.set(key, remaining)
    return remaining
