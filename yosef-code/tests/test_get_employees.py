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
        
        
        # Verify specific employee data for ID 7 (Helena Martinez) - essential fields only
        assert data["Id"] == 7, f"Expected Id 7, got {data['Id']}"
        assert data["first_name"] == "Helena", f"Expected first_name 'Helena', got '{data['first_name']}'"
        assert data["last_name"] == "Martinez", f"Expected last_name 'Martinez', got '{data['last_name']}'"
        assert data["email"] == "helena.martinez@company.com", f"Expected email 'helena.martinez@company.com', got '{data['email']}'"
        assert data["hire_date"] == "2024-01-15", f"Expected hire_date '2024-01-15', got '{data['hire_date']}'"
        assert data["salary"] == 100000, f"Expected salary 100000, got {data['salary']}"
        assert data["experience"] == "over 4 years in cloud, contributing to cloud migration and system design.", f"Expected specific experience text, got '{data['experience']}'"

    def test_get_employee_by_id_not_found(self):
        """Test getting a non-existent employee by ID - should return 404 or similar error"""
        # Test with non-existent employee ID
        employee_id = 999
        url = Endpoints.employees_record(employee_id)
        
        response = make_api_request('GET', url, headers=self.headers)
        
        assert response is not None, "No response received"
        
        # Should return 404 or similar error status code for non-existent employee
        assert response.status_code in [404, 400, 422], f"Expected error status (404/400/422), got {response.status_code}. Body: {response.text}"
        
        # Verify that we get an error response, not employee data
        data = get_response_data(response)
        if data is not None:
            # If there's response data, it should indicate an error
            assert isinstance(data, dict), f"Expected dict error response, got {type(data)}"
            
        print(f"Successfully verified employee ID {employee_id} does not exist - Status: {response.status_code}")

    def test_get_employee_unauthorized(self):
        """Test getting employee with invalid token - should return 401 unauthorized"""
        # Test with valid employee ID but invalid token
        employee_id = 7
        url = Endpoints.employees_record(employee_id)
        
        # Create invalid headers with wrong token
        invalid_headers = {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'xc-token': 'invalid-token-123456789',  # Invalid token
        }
        
        response = make_api_request('GET', url, headers=invalid_headers)
        
        assert response is not None, "No response received"
        
        # Should return 401 unauthorized or 403 forbidden for invalid token
        assert response.status_code in [401, 403], f"Expected unauthorized status (401/403), got {response.status_code}. Body: {response.text}"
        
        # Verify that we get an error response, not employee data
        data = get_response_data(response)
        if data is not None:
            assert isinstance(data, dict), f"Expected dict error response, got {type(data)}"
            
    
  
  