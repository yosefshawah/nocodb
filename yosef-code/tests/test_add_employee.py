import pytest
from config import (
    get_auth_headers,
    Endpoints,
    make_api_request,
    is_success_response,
    get_response_data,
    get_department_id_by_name,
    get_role_id_by_name,
)

class TestAddEmployee:
    """Create an employee (IT, Developer), then fetch it and verify it exists."""
# Test case 1: Add an employee with valid values
    @classmethod
    def setup_class(cls):
        cls.headers = get_auth_headers()

    def test_add_employee_and_fetch(self):
        # Fixed simple values
        first_name = "Alice"
        email = "alice@example.com"
        salary = 55000

        # Fixed department/role
        dept_id = get_department_id_by_name("IT")
        role_id = get_role_id_by_name("Developer")

        # Create employee (POST)
        create_url = Endpoints.employees_records()
        payload = {
            "first_name": first_name,
            "last_name": "Tester",
            "email": email,
            "hire_date": "2024-01-15",
            "salary": salary,
            "nc_4p9k___departments_csv_id": dept_id,
            "nc_4p9k___roles_id": role_id,
        }
        create_resp = make_api_request('POST', create_url, data=payload, headers=self.headers)
        assert create_resp is not None, "No response from create"
        assert is_success_response(create_resp), f"Create failed: {create_resp.status_code} {create_resp.text}"

        create_data = get_response_data(create_resp)
        assert create_data is not None and ("Id" in create_data or "id" in create_data), "Create response missing Id"
        record_id = create_data.get("Id") or create_data.get("id")
        assert isinstance(record_id, int), f"Id must be int, got {type(record_id)}"

        # Fetch employee (GET by ID)
        get_url = Endpoints.employees_record(record_id)
        get_resp = make_api_request('GET', get_url, headers=self.headers)
        assert get_resp is not None, "No response from fetch"
        assert get_resp.status_code == 200, f"Fetch failed: {get_resp.status_code} {get_resp.text}"

        fetched = get_response_data(get_resp)
        assert isinstance(fetched, dict), f"Unexpected fetch payload: {type(fetched)}"

        # Verify key fields
        assert fetched.get("Id") == record_id, "Fetched record Id mismatch"
        assert fetched.get("first_name") == first_name, "first_name mismatch"
        assert fetched.get("salary") == salary, "salary mismatch (must be non-zero)"
        assert fetched.get("nc_4p9k___departments_csv_id") == dept_id, "department id mismatch"
        assert fetched.get("nc_4p9k___roles_id") == role_id, "role id mismatch"

