"""
Configuration file for NocoDB API tests
Contains common settings, API tokens, table IDs, and helper functions
"""

import requests
import os

# Base configuration - use environment variables with fallbacks
BASE_URL = os.getenv('NOCODB_URL', 'http://52.18.93.49:8080/')
# BASE_URL = "http://localhost:8080/"
API_TOKEN = os.getenv('API_TOKEN', 'xpkrixNKoiHqfwzsIDoNh7MLRjP4FLR48gV3QFgQ')
# Environment detection
ENVIRONMENT = os.getenv('ENVIRONMENT', 'production')

# Descriptive table ID for employees (if needed elsewhere)
EMPLOYEES_TABLE_ID = os.getenv('EMPLOYEES_TABLE_ID', 'm3jxshm3jce0b2v')

# ----- Department and Role mappings (adjust to match your DB snapshot) -----
# You can override any of these via env vars like DEPT_IT_ID, DEPT_HR_ID, DEPT_FINANCE_ID, ROLE_DEVELOPER_ID, etc.
DEPARTMENT_NAME_TO_ID = {
    'IT': int(os.getenv('DEPT_IT_ID', '1')),
    'Human Resources': int(os.getenv('DEPT_HR_ID', '2')),
    'Finance': int(os.getenv('DEPT_FINANCE_ID', '3')),
}

ROLE_NAME_TO_ID = {
    'Manager': int(os.getenv('Manager', '1')),
    'Developer': int(os.getenv('Developer', '2')),
    'HR Specialist': int(os.getenv('HR Specialist', '3')),
}

def get_department_id_by_name(name: str) -> int:
    return DEPARTMENT_NAME_TO_ID[name]

def get_role_id_by_name(name: str) -> int:
    return ROLE_NAME_TO_ID[name]

# Common headers for API requests
def get_auth_headers():
    """Get authentication headers for API requests"""
    return {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'xc-token': API_TOKEN
    }

# Sample request bodies for different test scenarios
class SampleData:
    """Sample data for testing different scenarios"""
    
    @staticmethod
    def valid_employee():
        """Get a valid employee record for testing"""
        return {
            "first_name": "John",
            "last_name": "Doe",
            "email": "john.doe@example.com",
            "hire_date": "2024-01-15",
            "salary": 75000
        }
    
    @staticmethod
    def employee_with_string_salary():
        """Get an employee record with salary as string"""
        return {
            "first_name": "Jane",
            "last_name": "Smith",
            "email": "jane.smith@example.com",
            "hire_date": "2024-02-20",
            "salary": "65000"  # Salary as string
        }
    
    @staticmethod
    def invalid_employee():
        """Get an employee record with invalid data for testing validation"""
        return {
            "first_name": "",  # Empty first name
            "last_name": "Test",
            "email": "invalid-email",  # Invalid email
            "hire_date": "invalid-date",  # Invalid date
            "salary": "not-a-number"  # Invalid salary
        }
    
    @staticmethod
    def partial_employee():
        """Get a partial employee record for testing required fields"""
        return {
            "first_name": "Test"
            # Missing other required fields
        }
    
    @staticmethod
    def salary_test_cases():
        """Get different salary format test cases"""
        return [
            {"salary": 75000, "description": "integer salary"},
            {"salary": "65000", "description": "string salary"},
            {"salary": 75000.50, "description": "float salary"},
            {"salary": "75000.50", "description": "string float salary"}
        ]

# API endpoint builders
class Endpoints:
    """Helper class for building API endpoints"""
    
    @staticmethod
    def employees_records():
        """Get the employees records endpoint"""
        return f"{BASE_URL}api/v2/tables/{EMPLOYEES_TABLE_ID}/records"
    
    @staticmethod
    def employees_record(record_id):
        """Get a specific employee record endpoint"""
        return f"{BASE_URL}api/v2/tables/{EMPLOYEES_TABLE_ID}/records/{record_id}"
    
    @staticmethod
    def table_columns():
        """Get the table columns endpoint"""
        return f"{BASE_URL}api/v1/tables/{EMPLOYEES_TABLE_ID}/columns"

# Helper functions for common operations
def make_api_request(method, url, data=None, headers=None):
    """Make an API request with proper error handling"""
    if headers is None:
        headers = get_auth_headers()
    
    try:
        if method.upper() == 'GET':
            response = requests.get(url, headers=headers, timeout=10)
        elif method.upper() == 'POST':
            response = requests.post(url, headers=headers, json=data, timeout=10)
        elif method.upper() == 'PUT':
            response = requests.put(url, headers=headers, json=data, timeout=10)
        elif method.upper() == 'PATCH':
            response = requests.patch(url, headers=headers, json=data, timeout=10)
        elif method.upper() == 'DELETE':
            response = requests.delete(url, headers=headers, json=data, timeout=10)
        else:
            raise ValueError(f"Unsupported HTTP method: {method}")
        
        return response
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
        return None

def is_success_response(response):
    """Check if the response indicates success"""
    return response and response.status_code in [200, 201]

def is_error_response(response):
    """Check if the response indicates an error"""
    return response and response.status_code >= 400

def get_response_data(response):
    """Safely get JSON data from response"""
    try:
        return response.json() if response else None
    except ValueError:
        return None
