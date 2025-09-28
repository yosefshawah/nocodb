import pytest
from config import (
    get_auth_headers,
    Endpoints,
    make_api_request,
    is_success_response,
    get_response_data,
    BASE_URL
)

class TestBaseOperations:
    """Test class for base-related API operations"""
    
    @classmethod
    def setup_class(cls):
        cls.headers = get_auth_headers()

    def test_get_base_meta(self):
        """Test getting base metadata - matches GET /api/v2/meta/bases/{baseId}"""
        # Use the provided base ID
        base_id = "pce1khaxfq6n1pz"
        url = f"{BASE_URL}api/v2/meta/bases/{base_id}"
        
        response = make_api_request('GET', url, headers=self.headers)
        
        assert response is not None, "No response received"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Body: {response.text}"
        
        data = get_response_data(response)
        assert data is not None, "Expected JSON body"
        assert isinstance(data, dict), f"Expected dict response, got {type(data)}"
        
        # Verify essential base metadata fields are present
        assert "id" in data, "Missing base id field"
        assert "title" in data, "Missing base title field"
        
        # Verify the base ID matches what we requested
        assert data["id"] == base_id, f"Expected base ID {base_id}, got {data.get('id')}"
        
        # Verify specific base title
        assert data["title"] == "company-x", f"Expected base title 'company-x', got '{data.get('title')}'"
        
        # Optional: Check for other common base metadata fields
        print(f"Base title: {data.get('title')}")
        print(f"Base ID: {data.get('id')}")

    def test_get_all_bases(self):
        """Test getting all bases - matches GET /api/v2/meta/bases/"""
        url = f"{BASE_URL}api/v2/meta/bases/"
        
        response = make_api_request('GET', url, headers=self.headers)
        
        assert response is not None, "No response received"
        assert response.status_code == 200, f"Expected 200, got {response.status_code}. Body: {response.text}"
        
        data = get_response_data(response)
        assert data is not None, "Expected JSON body"
        
        # Response should be a paginated object with 'list' key
        assert isinstance(data, dict), f"Expected dict response, got {type(data)}"
        assert "list" in data, "Missing 'list' key in response"
        assert "pageInfo" in data, "Missing 'pageInfo' key in response"
        
        bases_list = data["list"]
        assert isinstance(bases_list, list), f"Expected list in 'list' key, got {type(bases_list)}"
        
        # Verify pageInfo structure
        page_info = data["pageInfo"]
        assert isinstance(page_info, dict), "pageInfo should be a dict"
        
        # List can be empty, but if it has bases, validate the structure
        if len(bases_list) > 0:
            # Test first base in the list
            first_base = bases_list[0]
            assert isinstance(first_base, dict), f"Expected dict base object, got {type(first_base)}"
            
            # Verify essential fields are present
            assert "id" in first_base, "Missing base id field"
            assert "title" in first_base, "Missing base title field"
            
            # Verify field types
            assert isinstance(first_base["id"], str), "Base id should be string"
            assert isinstance(first_base["title"], str), "Base title should be string"
            
            # Verify non-empty values
            assert len(first_base["id"]) > 0, "Base id should not be empty"
            assert len(first_base["title"]) > 0, "Base title should not be empty"
            
            print(f"Found {len(bases_list)} bases. First base - Title: {first_base.get('title')}, ID: {first_base.get('id')}")
        else:
            print("No bases found in the response")

    def test_create_base(self):
        """Test creating a new base - matches POST /api/v2/meta/bases/"""
        url = f"{BASE_URL}api/v2/meta/bases/"
        
        # Create payload with required and optional fields
        payload = {
            "title": "Test Base Created by API",
            "description": "This is a test base created via API testing",
            "meta": {}
        }
        
        response = make_api_request('POST', url, data=payload, headers=self.headers)
        
        assert response is not None, "No response received"
        assert is_success_response(response), f"Create failed: {response.status_code} {response.text}"
        
        data = get_response_data(response)
        assert data is not None, "Expected JSON body"
        assert isinstance(data, dict), f"Expected dict response, got {type(data)}"
        
        # Verify essential fields in the created base response
        assert "id" in data, "Missing base id field in response"
        assert "title" in data, "Missing base title field in response"
        
        # Verify the created base has the correct title
        assert data["title"] == payload["title"], f"Expected title '{payload['title']}', got '{data.get('title')}'"
        
        # Verify field types
        assert isinstance(data["id"], str), "Base id should be string"
        assert isinstance(data["title"], str), "Base title should be string"
        
        # Verify non-empty values
        assert len(data["id"]) > 0, "Base id should not be empty"
        assert len(data["title"]) > 0, "Base title should not be empty"
        
        # Check if description was set (optional field)
        if "description" in data:
            assert data["description"] == payload["description"], f"Expected description '{payload['description']}', got '{data.get('description')}'"
        
        created_base_id = data["id"]
        print(f"Successfully created base - Title: {data.get('title')}, ID: {created_base_id}")
      

    

    