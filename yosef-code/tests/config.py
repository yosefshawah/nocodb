"""
Configuration file for NocoDB API tests
Contains common settings, API tokens, table IDs, and helper functions
"""

import os
import requests

# Base configuration - use environment variables with fallbacks
BASE_URL = os.getenv('NOCODB_URL', 'http://52.18.93.49:8080/')
API_TOKEN = os.getenv('API_TOKEN', 'xpkrixNKoiHqfwzsIDoNh7MLRjP4FLR48gV3QFgQ')  # no fallback; token varies per instance
NC_ADMIN_EMAIL = os.getenv('NC_ADMIN_EMAIL', 'admin@example.com')
NC_ADMIN_PASSWORD = os.getenv('NC_ADMIN_PASSWORD', '12341234')
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
    if API_TOKEN:
        return {
            'accept': 'application/json',
            'Content-Type': 'application/json',
            'xc-token': API_TOKEN,
        }
    # Fallback: login to get session token
    r = requests.post(
        f"{BASE_URL}api/v1/auth/user/signin",
        json={'email': NC_ADMIN_EMAIL, 'password': NC_ADMIN_PASSWORD},
        timeout=10,
    )
    r.raise_for_status()
    token = r.json()['token']
    return {
        'accept': 'application/json',
        'Content-Type': 'application/json',
        'xc-auth': token,
    }

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
