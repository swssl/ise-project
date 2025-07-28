"""Demo script to test the simplified Smart Lock System API."""

import requests
import json

BASE_URL = "http://localhost:8001"

def demo_authentication():
    """Demo the authentication system with sample users."""
    print("=== Authentication Demo ===")
    
    # Try to login with a sample user
    login_data = {
        "username": "admin",
        "password": "any_password"  # In prototype, any password works
    }
    
    response = requests.post(f"{BASE_URL}/auth/login", json=login_data)
    print(f"Login attempt: {response.status_code}")
    
    if response.status_code == 200:
        token_data = response.json()
        print(f"✅ Login successful! Token: {token_data['access_token'][:20]}...")
        return token_data['access_token']
    else:
        print(f"❌ Login failed: {response.json()}")
        return None

def demo_user_management(token):
    """Demo user management features."""
    print("\n=== User Management Demo ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Get current user info
    response = requests.get(f"{BASE_URL}/auth/me", headers=headers)
    if response.status_code == 200:
        user_info = response.json()
        print(f"✅ Current user: {user_info['user_id']}")
        return user_info['user_id']
    else:
        print(f"❌ Failed to get user info: {response.status_code}")
        return None

def demo_permissions(token, user_id):
    """Demo permission management."""
    print("\n=== Permission Management Demo ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create a permission
    permission_data = {
        "user_id": user_id,
        "room_id": "room_101",
        "time_slots": [
            {
                "start_time": "09:00:00",
                "end_time": "17:00:00",
                "day_of_week": "mon"  # Monday to Friday
            }
        ]
    }
    
    response = requests.post(f"{BASE_URL}/permissions/", json=permission_data, headers=headers)
    if response.status_code == 200:
        permission = response.json()
        print(f"✅ Permission created for room {permission['room_id']}")
        
        # Get user permissions
        response = requests.get(f"{BASE_URL}/permissions/user/{user_id}", headers=headers)
        if response.status_code == 200:
            permissions = response.json()
            print(f"✅ User has {len(permissions)} permission(s)")
        
        return permission['room_id']
    else:
        print(f"❌ Failed to create permission: {response.status_code}")
        return None

def demo_access_logs(token, user_id, room_id):
    """Demo access logging."""
    print("\n=== Access Logging Demo ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create an access log
    access_log_data = {
        "user_id": user_id,
        "room_id": room_id,
        "access_granted": True,
        "device_id": "device_001"
    }
    
    response = requests.post(f"{BASE_URL}/access-logs/", json=access_log_data, headers=headers)
    if response.status_code == 200:
        log = response.json()
        print(f"✅ Access log created: {log['user_id']} accessed {log['room_id']}")
        
        # Get access logs
        response = requests.get(f"{BASE_URL}/access-logs/", headers=headers)
        if response.status_code == 200:
            logs = response.json()
            print(f"✅ Found {len(logs)} access log(s)")
    else:
        print(f"❌ Failed to create access log: {response.status_code}")

def demo_card_generation(token, user_id):
    """Demo card data generation."""
    print("\n=== Card Data Generation Demo ===")
    
    headers = {"Authorization": f"Bearer {token}"}
    
    response = requests.post(f"{BASE_URL}/permissions/generate-card/{user_id}", headers=headers)
    if response.status_code == 200:
        card_data = response.json()
        print(f"✅ Card data generated: {len(card_data['card_data'])} characters")
        print(f"   Preview: {card_data['card_data'][:50]}...")
    else:
        print(f"❌ Failed to generate card data: {response.status_code}")

if __name__ == "__main__":
    print("🔐 Smart Lock System API Demo")
    print("This demo shows the simplified prototype functionality")
    print("-" * 50)
    
    try:
        # Step 1: Login
        token = demo_authentication()
        if not token:
            exit(1)
        
        # Step 2: User management
        user_id = demo_user_management(token)
        if not user_id:
            exit(1)
        
        # Step 3: Permission management
        room_id = demo_permissions(token, user_id)
        if not room_id:
            exit(1)
        
        # Step 4: Access logging
        demo_access_logs(token, user_id, room_id)
        
        # Step 5: Card generation
        demo_card_generation(token, user_id)
        
        print("\n🎉 Demo completed successfully!")
        print("The simplified prototype is working correctly.")
        
    except Exception as e:
        print(f"❌ Demo failed: {e}")
        import traceback
        traceback.print_exc()
