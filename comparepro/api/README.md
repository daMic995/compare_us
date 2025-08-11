# ComparePro API

This is the backend API for the ComparePro application, which allows users to compare products from different e-commerce platforms.

## Project Structure

```
api/
├── __init__.py          # Application factory and main package initialization
├── index.py             # Entry point for the application
├── requirements.txt     # Project dependencies
├── .env.example        # Example environment variables
├── services/           # Business logic and service layer
│   ├── __init__.py
│   ├── compare_service.py  # Product comparison logic
│   ├── user_service.py     # User-related operations
│   └── stores/            # Store-specific implementations
│       ├── __init__.py
│       ├── amazon.py      # Amazon product data fetching
│       └── walmart.py     # Walmart product data fetching
├── routes/             # API routes and request handlers
│   ├── __init__.py
│   └── api.py          # API endpoints
└── utils/              # Utility functions and helpers
    ├── __init__.py
    ├── exceptions.py   # Custom exceptions
    ├── feature_utils.py # Feature matching utilities
    ├── redis_client.py # Redis client configuration
    └── store_utils.py  # Store-related utilities
```

## Setup Instructions

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd comparepro
   ```

2. **Create and activate a virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Set up environment variables**
   - Copy `.env.example` to `.env`
   - Update the values in `.env` with your actual API keys and configuration

5. **Run the development server**
   ```bash
   python -m api.index
   ```

   Or for production:
   ```bash
   gunicorn wsgi:application
   ```

## Environment Variables

Create a `.env` file in the project root with the following variables:

```
# Redis Configuration
UPSTASH_REDIS_REST_URL=your_redis_url
UPSTASH_REDIS_REST_TOKEN=your_redis_token

# Amazon API
AMAZON_API_KEY=your_amazon_api_key
AMAZON_API_HOST=your_amazon_api_host

# SerpAPI (for Walmart)
SERPI_API_KEY=your_serpapi_key

# Sentry
SENTRY_DSN=your_sentry_dsn

# Flask
FLASK_ENV=development
SECRET_KEY=your_secret_key
```

## API Endpoints

### `GET /api/python`
- **Description**: Welcome endpoint that returns the API status
- **Response**: 
  ```json
  {
    "message": "Welcome to the ComparePro API!",
    "available": 5,
    "status": 200
  }
  ```

### `GET /api/python/generate_user_id`
- **Description**: Generates a new user ID and initializes their comparison count
- **Response**: 
  ```json
  {
    "user_id": "550e8400-e29b-41d4-a716-446655440000",
    "available_comparisons": 5
  }
  ```

### `POST /api/python/compare`
- **Description**: Compares two products
- **Request Body**:
  ```json
  {
    "product1url": "https://www.amazon.com/...",
    "product2url": "https://www.walmart.com/...",
    "user_id": "550e8400-e29b-41d4-a716-446655440000"
  }
  ```
- **Response**:
  ```json
  {
    "status": 200,
    "products": [...],
    "matched_features": {...},
    "available_comparisons": 4
  }
  ```

## Error Handling

The API uses standard HTTP status codes and provides JSON error responses with the following format:

```json
{
  "message": "Error description",
  "status": 400
}
```

Common error status codes:
- `400`: Bad Request - Invalid input or missing required fields
- `401`: Unauthorized - Authentication required
- `403`: Forbidden - Insufficient permissions or rate limit exceeded
- `404`: Not Found - Resource not found
- `500`: Internal Server Error - Something went wrong on the server

## Testing

To run the test suite:

```bash
pytest
```

## Deployment

For production deployment, it's recommended to use a production-ready WSGI server like Gunicorn:

```bash
gunicorn wsgi:application -w 4 -b 0.0.0.0:5000
```

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.
