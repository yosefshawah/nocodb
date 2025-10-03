#!/usr/bin/env python3
"""
Quick test script to validate local testing setup
Run this to check if everything is working: python test_local_setup.py
"""
# testing the key
import os
import sys
import subprocess
import requests
import time
from dotenv import load_dotenv

def main():
    print("🧪 Testing Local NocoDB Setup")
    print("=" * 50)
    
    # Load environment
    load_dotenv()
    
    # Check environment
    base_url = os.getenv('NOCODB_URL', 'http://localhost:8080/')
    print(f"📍 Target URL: {base_url}")
    
    # Check if it's detected as local
    is_local = base_url.startswith('http://localhost:') or base_url.startswith('http://127.0.0.1:')
    print(f"🏠 Detected as local: {is_local}")
    
    if not is_local:
        print("❌ URL is not detected as local. Please check your .env file")
        return False
    
    # Check required files
    required_files = [
        'scripts/reset_local_db.sh',
        'nocodb/noco.db.bak',
        'docker-compose.yml'
    ]
    
    print("\n📂 Checking required files:")
    for file_path in required_files:
        exists = os.path.exists(file_path)
        status = "✅" if exists else "❌"
        print(f"  {status} {file_path}")
        if not exists:
            print(f"     Missing: {file_path}")
            return False
    
    # Test database reset
    print("\n🔄 Testing database reset...")
    try:
        result = subprocess.run([
            'bash', 'scripts/reset_local_db.sh'
        ], capture_output=True, text=True, timeout=60)
        
        if result.returncode == 0:
            print("✅ Database reset successful")
        else:
            print("❌ Database reset failed")
            print(f"Error: {result.stderr}")
            return False
            
    except subprocess.TimeoutExpired:
        print("❌ Database reset timed out")
        return False
    except Exception as e:
        print(f"❌ Database reset error: {e}")
        return False
    
    # Test service connectivity
    print("\n🌐 Testing service connectivity...")
    max_attempts = 30
    for attempt in range(max_attempts):
        try:
            response = requests.get(f"{base_url}", timeout=2)
            if response.status_code in [200, 302]:
                print("✅ Service is responding")
                break
        except requests.exceptions.RequestException:
            pass
        
        if attempt == max_attempts - 1:
            print("❌ Service is not responding after 60 seconds")
            return False
        
        print(f"⏳ Waiting for service... ({attempt + 1}/{max_attempts})")
        time.sleep(2)
    
    # Test basic API
    print("\n🔌 Testing basic API...")
    try:
        api_url = f"{base_url}api/v1/health"
        response = requests.get(api_url, timeout=5)
        if response.status_code == 200:
            print("✅ API health check passed")
        else:
            print(f"⚠️  API health check returned {response.status_code}")
    except Exception as e:
        print(f"⚠️  API health check failed: {e}")
        # This is not critical for basic setup
    
    print("\n🎉 Local setup test completed successfully!")
    print("\n📋 Next steps:")
    print("1. Create .env file: cp env.local.example .env")
    print("2. Edit .env with your settings if needed")
    print("3. Run tests: pytest tests/ -v")
    
    return True

if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
