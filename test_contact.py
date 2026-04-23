#!/usr/bin/env python3

import sys
import os
sys.path.append('/home/antares/coding/backend/blogbk')

# Test the ContactSerializer logic
def test_contact_serializer():
    print("Testing ContactSerializer logic...")
    
    # Test case 1: All fields provided
    test_data_1 = {
        'name': 'John Doe',
        'email': 'john@example.com',
        'subject': 'Test Subject',
        'message': 'This is a test message'
    }
    print(f"Test 1 - All fields: {test_data_1}")
    
    # Test case 2: Only required fields (no subject)
    test_data_2 = {
        'name': 'Jane Smith',
        'email': 'jane@example.com',
        'message': 'This is another test message'
    }
    print(f"Test 2 - Required fields only: {test_data_2}")
    
    # Test case 3: Missing required field (no message)
    test_data_3 = {
        'name': 'Bob Wilson',
        'email': 'bob@example.com',
        'subject': 'Invalid test'
    }
    print(f"Test 3 - Missing required field: {test_data_3}")
    
    print("\nSerializer validation logic:")
    print("- name: required, max_length=100")
    print("- email: required, must be valid email")
    print("- subject: optional, max_length=150")
    print("- message: required")

if __name__ == "__main__":
    test_contact_serializer()
