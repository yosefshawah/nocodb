# NocoDB API Tests

This directory contains comprehensive tests for the NocoDB API, organized with a shared configuration system for maintainability and reusability.

## 📁 File Structure

```
tests/
├── config.py                    # Shared configuration and utilities
├── conftest.py                  # Pytest fixtures and teardown
├── test_server_health.py        # Server health and availability tests
├── test_add_employee.py         # Employee record creation tests
├── test_get_employees.py        # Employee record retrieval tests
├── test_delete_employee.py      # Employee record deletion tests
└── README.md                    # This file
```

## 🔧 Configuration System (`config.py`)

The `config.py` file contains all shared configuration and utilities:

### **Environment Variables Setup**

1. **Create a `.env` file** in the project root:

```bash
# NocoDB Configuration
NOCODB_BASE_URL=http://52.18.93.49:8080/
NOCODB_API_TOKEN=xpkrixNKoiHqfwzsIDoNh7MLRjP4FLR48gV3QFgQ
EMPLOYEES_TABLE_ID=m3jxshm3jce0b2v
ENVIRONMENT=production
```

2. **Install python-dotenv**:

```bash
pip install python-dotenv
```

3. **Environment Variables**:

- `NOCODB_BASE_URL`: NocoDB server URL
- `NOCODB_API_TOKEN`: Authentication token
- `EMPLOYEES_TABLE_ID`: Descriptive table ID for employees
- `ENVIRONMENT`: Current environment (production/development/test)

### **Base Configuration**

The configuration automatically loads from environment variables with fallbacks:

- `BASE_URL`: NocoDB server URL
- `API_TOKEN`: Authentication token
- `EMPLOYEES_TABLE_ID`: Descriptive table ID for employees

### **Helper Functions**

- `get_auth_headers()`: Returns authentication headers
- `make_api_request()`: Makes HTTP requests with error handling
- `is_success_response()`: Checks if response indicates success
- `is_error_response()`: Checks if response indicates error
- `get_response_data()`: Safely extracts JSON data from response

### **Department and Role Mappings**

- `DEPARTMENT_NAME_TO_ID`: Maps department names to IDs (IT, Human Resources, Finance)
- `ROLE_NAME_TO_ID`: Maps role names to IDs (Manager, Developer, HR Specialist)
- `get_department_id_by_name()`: Helper to get department ID by name
- `get_role_id_by_name()`: Helper to get role ID by name

### **API Endpoints (`Endpoints` class)**

- `employees_records()`: Employees table records endpoint
- `employees_record(record_id)`: Specific employee record endpoint
- `table_columns()`: Table schema endpoint

## 🧪 Test Files

### **`test_server_health.py`**

Tests server availability and basic connectivity:

- `test_server_up()`: Basic server response
- `test_server_accessible()`: Network accessibility

### **`test_add_employee.py`**

Employee record creation tests:

- `test_add_employee_and_fetch()`: Creates employee with IT department and Developer role, then fetches and verifies

### **`test_get_employees.py`**

Employee record retrieval tests:

- `test_get_employees_schema()`: Validates GET employees response schema with pagination

### **`test_delete_employee.py`**

Employee record deletion tests:

- `test_delete_employee_id()`: Deletes employee with Id 2 and verifies it's removed

## 🚀 Usage

### **Setup Environment**

1. **Copy environment variables**:

```bash
cp .env.example .env
# Edit .env with your values
```

2. **Install dependencies**:

```bash
pip install -r requirements.txt
```

### **Run All Tests**

```bash
pytest tests/ -v
```

### **Run Specific Test Files**

```bash
# Server health tests only
pytest tests/test_server_health.py -v

# Employee tests only
pytest tests/test_add_employee.py -v
```

### **Run Specific Test Classes**

```bash
# Only server health tests
pytest tests/test_server_health.py::TestServerHealth -v

# Only employee creation tests
pytest tests/test_add_employee.py::TestAddEmployee -v

# Only employee retrieval tests
pytest tests/test_get_employees.py::TestGetEmployees -v

# Only employee deletion tests
pytest tests/test_delete_employee.py::TestDeleteEmployee -v
```

### **Run Specific Test Methods**

```bash
# Single test method
pytest tests/test_add_employee.py::TestAddEmployee::test_add_employee_and_fetch -v
```

## 🔄 Adding New Tests

### **1. Create New Test File**

```python
import pytest
from config import (
    get_auth_headers,
    SampleData,
    Endpoints,
    make_api_request,
    is_success_response,
    is_error_response,
    get_response_data
)

class TestNewFeature:
    """Test class for new feature"""

    @classmethod
    def setup_class(cls):
        cls.headers = get_auth_headers()

    def test_new_functionality(self):
        # Your test logic here
        pass
```

### **2. Add New Sample Data**

In `config.py`, add to the `SampleData` class:

```python
@staticmethod
def new_test_data():
    """Get test data for new feature"""
    return {
        "field1": "value1",
        "field2": "value2"
    }
```

### **3. Add New Endpoints**

In `config.py`, add to the `Endpoints` class:

```python
@staticmethod
def new_feature_endpoint():
    """Get the new feature endpoint"""
    return f"{BASE_URL}api/v2/tables/{NEW_TABLE_ID}/records"
```

## 🎯 Benefits of This Structure

- **DRY Principle**: No code duplication across test files
- **Maintainability**: Single source of truth for configuration
- **Consistency**: All tests use the same patterns and utilities
- **Scalability**: Easy to add new test files and features
- **Readability**: Clear separation of concerns
- **Reusability**: Shared utilities can be used across all tests
- **Security**: Sensitive data stored in environment variables

## 🔐 Security Notes

- API tokens are stored in environment variables (`.env` file)
- `.env` file should be added to `.gitignore`
- Never commit sensitive tokens to version control
- Use different tokens for different environments
- Consider using secrets management for production

## 🌍 Environment Management

### **Production**

```bash
ENVIRONMENT=production
NOCODB_BASE_URL=http://52.18.93.49:8080/
```

### **Development**

```bash
ENVIRONMENT=development
NOCODB_BASE_URL=http://localhost:8080/
```

### **Testing**

```bash
ENVIRONMENT=test
NOCODB_BASE_URL=http://test-server:8080/
```
