import pytest
from config import get_auth_headers, Endpoints, make_api_request

class TestDeleteEmployee:
    @classmethod
    def setup_class(cls):
        cls.headers = get_auth_headers()

    def test_delete_employee_id(self):
        delete_url = Endpoints.employees_records()
        payload = {"Id": 2}  # Delete record with Id 2 (bob)

        # Perform DELETE with JSON body (matches your curl exactly)
        resp = make_api_request('DELETE', delete_url, data=payload, headers=self.headers)
        assert resp is not None, "No response from DELETE"
        assert resp.status_code in (200, 204), f"Unexpected status for delete: {resp.status_code} {resp.text}"

        # Verify it's gone by trying to fetch the SAME ID that was deleted
        get_url = Endpoints.employees_record(2)  # Check Id 2 (the one we deleted)
        get_resp = make_api_request('GET', get_url, headers=self.headers)
        # Depending on NocoDB behavior: could be 404, or 200 with empty/flag
        assert get_resp is not None
        assert get_resp.status_code in (200, 404), f"Unexpected fetch status after delete: {get_resp.status_code} {get_resp.text}"
        if get_resp.status_code == 200:
            # If 200, ensure body doesn't represent the same existing record
            try:
                data = get_resp.json()
            except Exception:
                data = None
            # Check that the record we deleted (Id 2) is not present
            assert not (isinstance(data, dict) and data.get("Id") == 2), "Record still present after delete"
