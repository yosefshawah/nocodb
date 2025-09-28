#!/usr/bin/env python3
"""
Debug script to check environment detection for local vs remote testing
Run this to see what environment is detected: python debug_env.py
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

print("🔍 Environment Debug Information")
print("=" * 50)

# Check BASE_URL
BASE_URL = os.getenv('NOCODB_URL', 'http://localhost:8080/')
print(f"BASE_URL: '{BASE_URL}'")

# Environment detection logic (same as conftest.py)
IS_LOCAL = BASE_URL.startswith('http://localhost:') or BASE_URL.startswith('http://127.0.0.1:')
print(f"IS_LOCAL: {IS_LOCAL}")

# Show environment detection logic
print(f"Starts with localhost: {BASE_URL.startswith('http://localhost:')}")
print(f"Starts with 127.0.0.1: {BASE_URL.startswith('http://127.0.0.1:')}")

# Check .env file
env_file = '.env'
print(f".env file exists: {os.path.exists(env_file)}")

if os.path.exists(env_file):
    print(f".env file contents:")
    with open(env_file, 'r') as f:
        for line_num, line in enumerate(f, 1):
            if line.strip() and not line.strip().startswith('#'):
                print(f"  {line_num}: {line.strip()}")

# Check all relevant environment variables
env_vars = [
    'NOCODB_URL', 'API_TOKEN', 'NC_ADMIN_EMAIL', 'NC_ADMIN_PASSWORD',
    'ENVIRONMENT', 'EMPLOYEES_TABLE_ID'
]

print("\nEnvironment Variables:")
for var in env_vars:
    value = os.getenv(var)
    if value:
        # Hide sensitive values
        if 'TOKEN' in var or 'PASSWORD' in var:
            display_value = value[:10] + "..." if len(value) > 10 else value
        else:
            display_value = value
        print(f"  {var}: {display_value}")
    else:
        print(f"  {var}: NOT SET")

print("\nFile structure check:")
script_dir = os.path.dirname(os.path.abspath(__file__))
print(f"Current directory: {script_dir}")

# Check important files/directories
important_paths = [
    'scripts/reset_local_db.sh',
    'nocodb/noco.db',
    'nocodb/noco.db.bak',
    'docker-compose.yml'
]

for path in important_paths:
    full_path = os.path.join(script_dir, path)
    exists = os.path.exists(full_path)
    print(f"  {path}: {'✅ EXISTS' if exists else '❌ MISSING'}")

print("\nTo run tests locally, ensure:")
print("1. NOCODB_URL starts with http://localhost: or http://127.0.0.1:")
print("2. noco.db.bak exists in nocodb/ directory")
print("3. reset_local_db.sh exists and is executable")
print("4. docker-compose.yml exists")
