"""Basic API tests for the Smart Lock System."""

import requests
import json

BASE_URL = "http://localhost:8001"

def test_health_check():
    """Test the health check endpoint."""
    response = requests.get(f"{BASE_URL}/health")
    print("Health Check Response:", response.json())
    assert response.status_code == 200

def test_root_endpoint():
    """Test the root endpoint."""
    response = requests.get(f"{BASE_URL}/")
    print("Root Endpoint Response:", response.json())
    assert response.status_code == 200

def test_report_types():
    """Test getting available report types (no auth required)."""
    # First try without auth - should fail
    response = requests.get(f"{BASE_URL}/reports/types")
    print("Report Types (no auth):", response.status_code)
    # This should return 403 or 401 because authentication is required

if __name__ == "__main__":
    print("Testing Smart Lock System API...")
    
    try:
        test_health_check()
        test_root_endpoint()
        test_report_types()
        print("✅ Basic API tests completed!")
    except Exception as e:
        print(f"❌ Test failed: {e}")
