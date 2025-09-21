import pytest
from config import (
    get_auth_headers,
    Endpoints,
    make_api_request,
    get_response_data,
    get_department_id_by_name,
)

class TestTableRelation:
    """Test relationships between employees, departments, and roles tables"""

    @classmethod
    def setup_class(cls):
        cls.headers = get_auth_headers()

    def test_it_employees_match_department_count(self):
        """Test that number of IT employees matches the count in IT department record"""
        
        # 1. Fetch all employees
        employees_url = Endpoints.employees_records()
        employees_resp = make_api_request('GET', employees_url, headers=self.headers)
        assert employees_resp is not None, "No response from employees fetch"
        assert employees_resp.status_code == 200, f"Failed to fetch employees: {employees_resp.status_code}"
        
        employees_data = get_response_data(employees_resp)
        assert employees_data is not None, "No employees data received"
        
        # Handle different response formats
        if isinstance(employees_data, dict) and 'list' in employees_data:
            employees_list = employees_data['list']
        elif isinstance(employees_data, list):
            employees_list = employees_data
        else:
            assert False, f"Unexpected employees response format: {type(employees_data)}"
        
        # 2. Count employees in IT department
        it_dept_id = get_department_id_by_name("IT")
        it_employees_count = 0
        
        for employee in employees_list:
            if employee.get('nc_4p9k___departments_csv_id') == it_dept_id:
                it_employees_count += 1
        
        print(f"Found {it_employees_count} employees in IT department")
        
        # 3. Fetch IT department record to get its count
        it_dept_url = f"{Endpoints.employees_records().split('/tables/')[0]}/tables/mrlt1har4l0yifj/records"
        dept_resp = make_api_request('GET', it_dept_url, headers=self.headers)
        assert dept_resp is not None, "No response from department fetch"
        assert dept_resp.status_code == 200, f"Failed to fetch IT department: {dept_resp.status_code}"
        
        dept_data = get_response_data(dept_resp)
        assert dept_data is not None, "No department data received"
        
        # Handle department response format
        if isinstance(dept_data, dict) and 'list' in dept_data:
            dept_list = dept_data['list']
        elif isinstance(dept_data, list):
            dept_list = dept_data
        else:
            assert False, f"Unexpected department response format: {type(dept_data)}"
        
        # Find IT department in the list
        it_dept_record = None
        for dept in dept_list:
            if dept.get('department_name') == 'IT':
                it_dept_record = dept
                break
        
        assert it_dept_record is not None, "IT department not found in departments list"
        
        # Get the count from IT department record
        dept_employee_count = it_dept_record.get('employees', 0)
        print(f"IT department record shows {dept_employee_count} employees")
        
        # 4. Verify counts match
        assert it_employees_count == dept_employee_count, (
            f"IT department employee count ({it_employees_count}) does not match "
            f"department record count ({dept_employee_count})"
        )
        
        print(f"✅ Verified: {it_employees_count} employees match department record count")
