#!/usr/bin/env python3
"""
Quick test script to verify the TIBCO BW XPath Translator backend
"""

import requests
import json
import time

BASE_URL = "http://localhost:5000"

def test_health():
    """Test health check endpoint"""
    print("🔍 Testing health endpoint...")
    try:
        response = requests.get(f"{BASE_URL}/api/health", timeout=5)
        if response.status_code == 200:
            print(f"✅ Health check passed: {response.json()}")
            return True
        else:
            print(f"❌ Health check failed: {response.status_code}")
            return False
    except Exception as e:
        print(f"❌ Health check error: {e}")
        return False

def test_translate():
    """Test XPath translation endpoint"""
    print("\n🔍 Testing XPath translation...")
    test_cases = [
        {
            "xpath": "//Order/Customer/@id",
            "context": {}
        },
        {
            "xpath": "$orderData/Order/TotalAmount > 1000",
            "context": {"type": "condition"}
        },
        {
            "xpath": "count(//Items/Item)",
            "context": {}
        }
    ]
    
    for i, test_case in enumerate(test_cases, 1):
        try:
            response = requests.post(
                f"{BASE_URL}/api/translate",
                json=test_case,
                headers={"Content-Type": "application/json"},
                timeout=5
            )
            if response.status_code == 200:
                result = response.json()
                print(f"\n✅ Test {i} passed:")
                print(f"   XPath: {result['xpath']}")
                print(f"   Plain Language: {result['plain_language']}")
                print(f"   Confidence: {result['confidence']}")
            else:
                print(f"❌ Test {i} failed: {response.status_code}")
                print(f"   Response: {response.text}")
        except Exception as e:
            print(f"❌ Test {i} error: {e}")

def test_file_upload():
    """Test file upload with sample BW file"""
    print("\n🔍 Testing file upload...")
    try:
        with open('sample_bw_process.xml', 'rb') as f:
            files = {'file': ('sample_bw_process.xml', f, 'text/xml')}
            response = requests.post(
                f"{BASE_URL}/api/upload",
                files=files,
                timeout=10
            )
            
        if response.status_code == 200:
            result = response.json()
            print(f"✅ File upload passed:")
            print(f"   File ID: {result['file_id']}")
            print(f"   XPath Count: {result['xpath_count']}")
            print(f"   Process: {result['metadata'].get('process_name', 'N/A')}")
            return result['file_id']
        else:
            print(f"❌ File upload failed: {response.status_code}")
            print(f"   Response: {response.text}")
            return None
    except Exception as e:
        print(f"❌ File upload error: {e}")
        return None

def test_parse(file_id):
    """Test parsing and translating uploaded file"""
    if not file_id:
        print("\n⚠️  Skipping parse test (no file_id)")
        return
    
    print(f"\n🔍 Testing parse endpoint for file: {file_id}...")
    try:
        response = requests.get(
            f"{BASE_URL}/api/parse/{file_id}",
            timeout=15
        )
        
        if response.status_code == 200:
            result = response.json()
            print(f"✅ Parse test passed:")
            print(f"   Total Translations: {result['total_count']}")
            
            if result['translations']:
                first = result['translations'][0]
                print(f"\n   Sample Translation:")
                print(f"   XPath: {first['xpath']}")
                print(f"   Plain: {first['plain_language']}")
                print(f"   Location: {first['location']} - {first['activity']}")
        else:
            print(f"❌ Parse test failed: {response.status_code}")
            print(f"   Response: {response.text}")
    except Exception as e:
        print(f"❌ Parse test error: {e}")

if __name__ == "__main__":
    print("=" * 80)
    print("TIBCO BW XPath Translator - Backend Test Suite")
    print("=" * 80)
    
    # Wait for server to be ready
    print("\n⏳ Waiting for backend to start...")
    time.sleep(2)
    
    # Run tests
    if test_health():
        test_translate()
        file_id = test_file_upload()
        test_parse(file_id)
        
        print("\n" + "=" * 80)
        print("✅ All tests completed!")
        print("=" * 80)
    else:
        print("\n❌ Backend not available. Make sure Flask is running on port 5000")
