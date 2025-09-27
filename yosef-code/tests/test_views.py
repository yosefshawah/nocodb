import pytest
from config import (
    get_auth_headers,
    make_api_request,
    is_success_response,
    get_response_data,
    BASE_URL,
    EMPLOYEES_TABLE_ID
)

class TestViews:
    """Test class for view-related API operations"""
    
    @classmethod
    def setup_class(cls):
        cls.headers = get_auth_headers()

    def test_get_table_views(self):
        """Test getting table views - matches GET /api/v2/meta/tables/{tableId}/views"""
        # Use the employees table ID
        table_id = EMPLOYEES_TABLE_ID  # m3jxshm3jce0b2v
        url = f"{BASE_URL}api/v2/meta/tables/{table_id}/views"
        
        response = make_api_request('GET', url, headers=self.headers)
        
        assert response is not None, "No response received"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Body: {response.text}"
        
        data = get_response_data(response)
        assert data is not None, "Expected JSON body"
        
        # Response should be a paginated object with 'list' key (like other endpoints)
        assert isinstance(data, dict), f"Expected dict response, got {type(data)}"
        assert "list" in data, "Missing 'list' key in response"
        
        views_list = data["list"]
        assert isinstance(views_list, list), f"Expected list in 'list' key, got {type(views_list)}"
        
        # Tables should have at least one default view, but handle empty case
        if len(views_list) > 0:
            # Test first view in the list
            first_view = views_list[0]
            assert isinstance(first_view, dict), f"Expected dict view object, got {type(first_view)}"
            
            # Verify essential view fields are present
            assert "id" in first_view, "Missing view id field"
            assert "title" in first_view, "Missing view title field"
            assert "type" in first_view, "Missing view type field"
            assert "fk_model_id" in first_view, "Missing fk_model_id field"
            
            # Verify the fk_model_id matches the table ID
            assert first_view["fk_model_id"] == table_id, f"Expected fk_model_id {table_id}, got {first_view['fk_model_id']}"
            
            # Verify field types
            assert isinstance(first_view["id"], str), "View id should be string"
            assert isinstance(first_view["title"], str), "View title should be string"
            assert isinstance(first_view["type"], (str, int)), "View type should be string or int"
            assert isinstance(first_view["fk_model_id"], str), "fk_model_id should be string"
            
            # Verify non-empty values
            assert len(first_view["id"]) > 0, "View id should not be empty"
            assert len(first_view["title"]) > 0, "View title should not be empty"
            assert len(first_view["fk_model_id"]) > 0, "fk_model_id should not be empty"
            
            # Check for common view metadata fields
            optional_fields = ["alias", "is_default", "order", "password", "lock_type", "uuid", "description", "show", "created_at", "updated_at"]
            found_optional = []
            for field in optional_fields:
                if field in first_view:
                    found_optional.append(field)
            
            print(f"Found {len(views_list)} views for table {table_id}")
            print(f"First view - Title: {first_view.get('title')}, ID: {first_view.get('id')}, Type: {first_view.get('type')}")
            if found_optional:
                print(f"Optional fields found: {', '.join(found_optional)}")
        else:
            print(f"No views found for table {table_id}")

    def test_create_grid_view(self):
        """Test creating a new grid view - matches POST /api/v2/meta/tables/{tableId}/grids"""
        # Use the roles table ID
        table_id = "m4eqrc006ipf58h"
        url = f"{BASE_URL}api/v2/meta/tables/{table_id}/grids"
        
        # Create payload for grid view
        payload = {
            "title": "Test Grid View Created by API",
            "type": 3  # Grid view type (3 = Grid)
        }
        
        response = make_api_request('POST', url, data=payload, headers=self.headers)
        
        assert response is not None, "No response received"
        assert is_success_response(response), f"Create failed: {response.status_code} {response.text}"
        
        data = get_response_data(response)
        assert data is not None, "Expected JSON body"
        assert isinstance(data, dict), f"Expected dict response, got {type(data)}"
        
        # Verify essential fields in the created view response
        assert "id" in data, "Missing view id field in response"
        assert "title" in data, "Missing view title field in response"
        assert "type" in data, "Missing view type field in response"
        assert "fk_model_id" in data, "Missing fk_model_id field in response"
        
        # Verify the created view has the correct properties
        assert data["title"] == payload["title"], f"Expected title '{payload['title']}', got '{data.get('title')}'"
        assert data["type"] == payload["type"], f"Expected type {payload['type']}, got {data.get('type')}"
        assert data["fk_model_id"] == table_id, f"Expected fk_model_id {table_id}, got {data.get('fk_model_id')}"
        
        # Verify field types
        assert isinstance(data["id"], str), "View id should be string"
        assert isinstance(data["title"], str), "View title should be string"
        assert isinstance(data["type"], int), "View type should be integer"
        assert isinstance(data["fk_model_id"], str), "fk_model_id should be string"
        
        # Verify non-empty values
        assert len(data["id"]) > 0, "View id should not be empty"
        assert len(data["title"]) > 0, "View title should not be empty"
        assert len(data["fk_model_id"]) > 0, "fk_model_id should not be empty"
        
        # Check for additional view properties that might be set
        if "is_default" in data:
            # is_default can be boolean or None
            assert isinstance(data["is_default"], (bool, type(None))), "is_default should be boolean or None"
        
        if "order" in data:
            assert isinstance(data["order"], (int, float, type(None))), "order should be numeric or None"
        
        created_view_id = data["id"]
        print(f"Successfully created grid view - Title: {data.get('title')}, ID: {created_view_id}, Type: {data.get('type')}")
        print(f"View belongs to table: {data.get('fk_model_id')}")

    def test_get_form_view_metadata(self):
        """Test getting form view metadata - matches GET /api/v2/meta/forms/{formViewId}"""
        # Extract form view ID from the URL: vwkt5maum1ztaxkk
        form_view_id = "vwkt5maum1ztaxkk"
        url = f"{BASE_URL}api/v2/meta/forms/{form_view_id}"
        
        response = make_api_request('GET', url, headers=self.headers)
        
        assert response is not None, "No response received"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Body: {response.text}"
        
        data = get_response_data(response)
        assert data is not None, "Expected JSON body"
        assert isinstance(data, dict), f"Expected dict response, got {type(data)}"
        
        # Verify essential form metadata fields are present
        # The response has base_id instead of id field
        assert "base_id" in data, "Missing base_id field"
        assert "columns" in data, "Missing columns field"
        assert "created_at" in data, "Missing created_at field"
        
        # Verify field types for essential fields
        assert isinstance(data["base_id"], str), "base_id should be string"
        assert len(data["base_id"]) > 0, "base_id should not be empty"
        assert isinstance(data["created_at"], str), "created_at should be string"
        
    
        if "columns" in data:
            # columns should be an array of form column objects
            columns = data["columns"]
            assert isinstance(columns, list), "columns should be a list"
            print(f"Form has {len(columns)} columns configured")
            
            # If there are columns, validate the structure of the first one
            if len(columns) > 0:
                first_column = columns[0]
                assert isinstance(first_column, dict), "Form column should be a dict"
                # Common form column fields might include: id, label, help, required, etc.
                if "id" in first_column:
                    assert isinstance(first_column["id"], str), "Column id should be string"
        
        # Check for other common form metadata fields
        form_fields = ["title", "heading", "subheading", "success_msg", "redirect_url", "redirect_after_secs", "email", "submit_another_form", "show_blank_form"]
        found_fields = []
        for field in form_fields:
            if field in data:
                found_fields.append(field)
                # Basic type validation for known fields
                if field in ["title", "heading", "subheading", "success_msg", "redirect_url", "email"]:
                    if data[field] is not None:
                        assert isinstance(data[field], str), f"{field} should be string or None"
                elif field in ["redirect_after_secs"]:
                    if data[field] is not None:
                        assert isinstance(data[field], (int, float)), f"{field} should be numeric or None"
                elif field in ["submit_another_form", "show_blank_form"]:
                    if data[field] is not None:
                        # These fields can be boolean or integer (0/1)
                        assert isinstance(data[field], (bool, int)), f"{field} should be boolean, integer, or None"
                        if isinstance(data[field], int):
                            assert data[field] in [0, 1], f"{field} integer value should be 0 or 1"
        
        print(f"Form view metadata - Base ID: {data.get('base_id')}")
        print(f"Form view ID (requested): {form_view_id}")
        if "title" in data:
            print(f"Form title: {data.get('title')}")
        if found_fields:
            print(f"Found form fields: {', '.join(found_fields)}")
        if "columns" in data:
            print(f"Form columns count: {len(data['columns'])}")
        
 