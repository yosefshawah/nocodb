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

    def test_get_employee_by_id(self):
        """Test getting a specific employee by ID - matches curl GET request"""
        # Test with employee ID 1 (as shown in curl example)
        employee_id = 7
        url = Endpoints.employees_record(employee_id)
        
        response = make_api_request('GET', url, headers=self.headers)
        
        assert response is not None, "No response received"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Body: {response.text}"
        
        data = get_response_data(response)
        assert data is not None, "Expected JSON body"
        assert isinstance(data, dict), f"Expected dict response, got {type(data)}"
        
        # Verify the response contains the expected employee ID
        record_id = data.get("Id") or data.get("id") or data.get("ID")
        assert record_id == employee_id, f"Expected employee ID {employee_id}, got {record_id}"
        
        # Verify essential employee fields are present
        assert "first_name" in data, "Missing first_name field"
        assert "last_name" in data, "Missing last_name field" 
        assert "email" in data, "Missing email field"
        assert "hire_date" in data, "Missing hire_date field"
        assert "salary" in data, "Missing salary field"
        assert "experience" in data, "Missing experience field"
        
        # Verify field types and values are reasonable
        assert isinstance(data["first_name"], str), "first_name should be string"
        assert isinstance(data["last_name"], str), "last_name should be string"
        assert isinstance(data["email"], str), "email should be string"
        assert isinstance(data["hire_date"], str), "hire_date should be string"
        assert isinstance(data["salary"], (int, float)), "salary should be numeric"
        assert isinstance(data["experience"], str), "experience should be string"
        
        # Verify non-empty values
        assert len(data["first_name"]) > 0, "first_name should not be empty"
        assert len(data["last_name"]) > 0, "last_name should not be empty"
        assert "@" in data["email"], "email should contain @ symbol"
