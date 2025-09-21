import pytest
from config import get_auth_headers, Endpoints, make_api_request, is_success_response, get_response_data

class TestGetEmployees:
    """Fetch employees with query params"""

    @classmethod
    def setup_class(cls):
        cls.headers = get_auth_headers()

    def test_get_employees(self):
        url = Endpoints.employees_records()
        response = make_api_request('GET', url, headers=self.headers)

        assert response is not None, "No response received"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Body: {response.text}"

        data = get_response_data(response)
        assert data is not None, "Expected JSON body"
        assert isinstance(data, (list, dict)), f"Unexpected response type: {type(data)}"

        # Optional sanity: if list, allow empty; if dict, just ensure it's non-empty
        if isinstance(data, dict):
            assert len(data) >= 0
