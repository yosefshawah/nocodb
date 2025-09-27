import pytest
from config import (
    get_auth_headers,
    make_api_request,
    is_success_response,
    get_response_data,
    BASE_URL,
    EMPLOYEES_TABLE_ID
)

class TestTableOperations:
    """Test class for table-related API operations"""
    
    @classmethod
    def setup_class(cls):
        cls.headers = get_auth_headers()

    def test_get_base_tables(self):
        """Test getting tables from a base - matches GET /api/v2/meta/bases/{baseId}/tables"""
        # Use the known base ID
        base_id = "pce1khaxfq6n1pz"
        url = f"{BASE_URL}api/v2/meta/bases/{base_id}/tables"
        
        response = make_api_request('GET', url, headers=self.headers)
        
        assert response is not None, "No response received"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Body: {response.text}"
        
        data = get_response_data(response)
        assert data is not None, "Expected JSON body"
        
        # Response should be a paginated object with 'list' key (similar to bases)
        assert isinstance(data, dict), f"Expected dict response, got {type(data)}"
        assert "list" in data, "Missing 'list' key in response"
        
        tables_list = data["list"]
        assert isinstance(tables_list, list), f"Expected list in 'list' key, got {type(tables_list)}"
        
        # List can be empty, but if it has tables, validate the structure
        if len(tables_list) > 0:
            # Test first table in the list
            first_table = tables_list[0]
            assert isinstance(first_table, dict), f"Expected dict table object, got {type(first_table)}"
            
            # Verify essential table fields are present
            assert "id" in first_table, "Missing table id field"
            assert "title" in first_table, "Missing table title field"
            assert "table_name" in first_table, "Missing table_name field"
            assert "base_id" in first_table, "Missing base_id field"
            
            # Verify field types
            assert isinstance(first_table["id"], str), "Table id should be string"
            assert isinstance(first_table["title"], str), "Table title should be string"
            assert isinstance(first_table["table_name"], str), "Table name should be string"
            assert isinstance(first_table["base_id"], str), "Base id should be string"
            
            # Verify non-empty values
            assert len(first_table["id"]) > 0, "Table id should not be empty"
            assert len(first_table["title"]) > 0, "Table title should not be empty"
            assert len(first_table["table_name"]) > 0, "Table name should not be empty"
            
            # Verify the base_id matches the requested base
            assert first_table["base_id"] == base_id, f"Expected base_id {base_id}, got {first_table['base_id']}"
            
            print(f"Found {len(tables_list)} tables in base {base_id}")
            print(f"First table - Title: {first_table.get('title')}, ID: {first_table.get('id')}, Table Name: {first_table.get('table_name')}")
        else:
            print(f"No tables found in base {base_id}")

    def test_get_table_metadata(self):
        """Test getting table metadata - matches GET /api/v2/meta/tables/{tableId}"""
        # Use the employees table ID
        table_id = EMPLOYEES_TABLE_ID  # m3jxshm3jce0b2v
        url = f"{BASE_URL}api/v2/meta/tables/{table_id}"
        
        response = make_api_request('GET', url, headers=self.headers)
        
        assert response is not None, "No response received"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Body: {response.text}"
        
        data = get_response_data(response)
        assert data is not None, "Expected JSON body"
        assert isinstance(data, dict), f"Expected dict response, got {type(data)}"
        
        # Verify essential table metadata fields are present
        assert "id" in data, "Missing table id field"
        assert "title" in data, "Missing table title field"
        assert "table_name" in data, "Missing table_name field"
        assert "base_id" in data, "Missing base_id field"
        
        # Verify the table ID matches what we requested
        assert data["id"] == table_id, f"Expected table ID {table_id}, got {data.get('id')}"
        
        # Verify field types
        assert isinstance(data["id"], str), "Table id should be string"
        assert isinstance(data["title"], str), "Table title should be string"
        assert isinstance(data["table_name"], str), "Table name should be string"
        assert isinstance(data["base_id"], str), "Base id should be string"
        
        # Verify non-empty values
        assert len(data["id"]) > 0, "Table id should not be empty"
        assert len(data["title"]) > 0, "Table title should not be empty"
        assert len(data["table_name"]) > 0, "Table name should not be empty"
        assert len(data["base_id"]) > 0, "Base id should not be empty"
        
        # Check for columns metadata if present
        if "columns" in data:
            assert isinstance(data["columns"], list), "Columns should be a list"
            print(f"Table has {len(data['columns'])} columns")
        
        # Optional metadata fields that might be present
        optional_fields = ["type", "meta", "schema", "enabled", "mm", "tags", "pinned", "deleted", "order", "created_at", "updated_at"]
        for field in optional_fields:
            if field in data:
                print(f"Found optional field '{field}': {type(data[field])}")
        
        print(f"Table metadata - Title: {data.get('title')}, ID: {data.get('id')}, Table Name: {data.get('table_name')}, Base ID: {data.get('base_id')}")
