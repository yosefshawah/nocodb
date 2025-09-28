import pytest
from config import get_auth_headers, Endpoints, make_api_request, get_response_data

class TestDeleteEmployee:
    @classmethod
    def setup_class(cls):
        cls.headers = get_auth_headers()

    def test_delete_employee_id(self):
        delete_url = Endpoints.employees_records()
        payload = {"Id": 2}  # Delete record with Id 2 (Rosa Rivera)

        # Perform DELETE with JSON body (matches your curl exactly)
        resp = make_api_request('DELETE', delete_url, data=payload, headers=self.headers)
        assert resp is not None, "No response from DELETE"
        assert resp.status_code in (200, 204), f"Unexpected status for delete: {resp.status_code} {resp.text}"

    def test_delete_employee_not_found(self):
        """Test deleting a non-existent employee - should return error status"""
        delete_url = Endpoints.employees_records()
        payload = {"Id": 999}  # Try to delete non-existent employee with ID 999

        # Perform DELETE with JSON body for non-existent employee
        resp = make_api_request('DELETE', delete_url, data=payload, headers=self.headers)
        assert resp is not None, "No response from DELETE"
        
        # Should return error status for non-existent employee
        # Common error codes: 404 (Not Found), 400 (Bad Request), 422 (Unprocessable Entity)
        assert resp.status_code in (404, 400, 422), f"Expected error status (404/400/422) for non-existent employee, got {resp.status_code}. Body: {resp.text}"
        
        # Should not contain success indicators for non-existent employe
        print(f"Successfully verified delete failed for non-existent employee ID 999 - Status: {resp.status_code}")
      
    