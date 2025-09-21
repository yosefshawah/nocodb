import pytest
from config import BASE_URL, make_api_request

class TestServerHealth:
    """Test class for server health and availability checks"""
    
    def test_server_up(self):
        """Test that the server is running and responding"""
        response = make_api_request('GET', BASE_URL)
        assert response is not None, "Server is not responding"
        assert response.status_code in (200, 302), f"Expected 200 or 302, got {response.status_code}"
    
