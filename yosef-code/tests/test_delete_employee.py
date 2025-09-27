import pytest
from config import get_auth_headers, Endpoints, make_api_request

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

   