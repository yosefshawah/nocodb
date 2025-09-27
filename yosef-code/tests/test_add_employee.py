import pytest
import os
from config import (
    get_auth_headers,
    Endpoints,
    make_api_request,
    is_success_response,
    get_response_data,
)


class TestAddEmployee:
    """Create an employee with the updated API structure."""
    
    @classmethod
    def setup_class(cls):
        cls.headers = get_auth_headers()

    def test_add_employee_minimal_data(self):
        """Test adding an employee with minimal required data."""
        
        payload = {
            "first_name": "John",
            "last_name": "Smith", 
            "email": "john.smith@example.com",
            "hire_date": "2024-01-15",
            "salary": 75000,
            "experience": "5 years of experience in frontend development"
        }
        
        create_url = Endpoints.employees_records()
        create_resp = make_api_request('POST', create_url, data=payload, headers=self.headers)
        
        assert create_resp is not None, "No response from create employee request"
        assert is_success_response(create_resp), f"Create failed: {create_resp.status_code} {create_resp.text}"
        
        create_data = get_response_data(create_resp)
        record_id = create_data.get("Id") or create_data.get("id") or create_data.get("ID")
        assert record_id is not None, "Create response missing Id field"