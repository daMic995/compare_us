import pytest
from api import create_app

@pytest.fixture
def app():
    """Create and configure a new app instance for each test."""
    app = create_app('testing')
    yield app

@pytest.fixture
def client(app):
    """A test client for the app."""
    return app.test_client()

def test_health_check(client):
    """
    GIVEN a Flask application configured for testing
    WHEN the '/health' endpoint is requested (GET)
    THEN check that the response is valid and returns 200 OK.
    """
    response = client.get('/health')
    assert response.status_code == 200
    assert response.data == b'OK'

def test_index_route_without_session(client):
    """
    GIVEN a Flask application
    WHEN the index route ('/api/python/') is accessed without a user session
    THEN the global error handler should catch the resulting KeyError
    and return a 500 Internal Server Error.
    """
    response = client.get('/api/python/')
    # Check that the response status code is 500
    assert response.status_code == 500

    # Check that the response contains the expected error message
    json_data = response.get_json()
    assert json_data['status'] == 500
    assert json_data['message'] == 'An internal server error occurred.'
