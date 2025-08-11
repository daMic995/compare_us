from flask import jsonify

class BaseAPIError(Exception):
    """Base exception for all API-related errors."""
    status_code = 500
    message = "An unexpected error occurred"
    
    def __init__(self, message=None, status_code=None, payload=None):
        super().__init__()
        if message is not None:
            self.message = message
        if status_code is not None:
            self.status_code = status_code
        self.payload = payload
    
    def to_dict(self):
        rv = dict(self.payload or ())
        rv['message'] = self.message
        rv['status'] = self.status_code
        return rv

class InvalidRequestData(BaseAPIError):
    """Raised when the request data is invalid or missing required fields."""
    status_code = 400
    message = "Invalid request data"

class UnauthorizedError(BaseAPIError):
    """Raised when a user is not authorized to access a resource."""
    status_code = 401
    message = "Unauthorized access"

class ForbiddenError(BaseAPIError):
    """Raised when a user doesn't have permission to access a resource."""
    status_code = 403
    message = "Forbidden"

class NotFoundError(BaseAPIError):
    """Raised when a requested resource is not found."""
    status_code = 404
    message = "Resource not found"

class InvalidProductURL(BaseAPIError):
    """Raised when a product URL is invalid or malformed."""
    status_code = 400
    message = "Invalid product URL"

class UnsupportedStore(BaseAPIError):
    """Raised when trying to process a product from an unsupported store."""
    status_code = 400
    message = "Store not supported"

class ProductFetchError(BaseAPIError):
    """Raised when there's an error fetching product data from a store."""
    status_code = 500
    message = "Error fetching product data"

class ComparisonLimitExceeded(BaseAPIError):
    """Raised when a user has exceeded their comparison limit."""
    status_code = 403
    message = "Comparison limit exceeded"

class RateLimitExceeded(BaseAPIError):
    """Raised when the rate limit is exceeded."""
    status_code = 429
    message = "Rate limit exceeded"

class ExternalServiceError(BaseAPIError):
    """Raised when an external service fails."""
    status_code = 502
    message = "External service error"

class DatabaseError(BaseAPIError):
    """Raised when there's a database-related error."""
    status_code = 500
    message = "Database error"

def register_error_handlers(app):
    """Register error handlers for the Flask app."""
    @app.errorhandler(BaseAPIError)
    def handle_api_error(error):
        response = jsonify(error.to_dict())
        response.status_code = error.status_code
        return response
    
    @app.errorhandler(404)
    def not_found_error(error):
        return jsonify({
            'status': 404,
            'message': 'The requested resource was not found.'
        }), 404
    
    @app.errorhandler(500)
    def internal_error(error):
        return jsonify({
            'status': 500,
            'message': 'An internal server error occurred.'
        }), 500
