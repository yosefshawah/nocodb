import subprocess
import time
import os
import requests  # pyright: ignore[reportMissingModuleSource]
import pytest  # pyright: ignore[reportMissingImports]
from dotenv import load_dotenv
from config import BASE_URL

# Load environment variables from .env file
load_dotenv()

# Environment detection
IS_LOCAL = BASE_URL.startswith('http://localhost:') or BASE_URL.startswith('http://127.0.0.1:')

# Remote configuration (for CI/CD)
HOST = os.environ.get("HOST", "ec2-52-18-93-49.eu-west-1.compute.amazonaws.com")
USER = "ubuntu"
KEY_FILE = os.environ.get("KEY_FILE", "/Users/shawahyosef/Desktop/nocodb-final-project/nocodb-final-yosef.pem")
REMOTE_RESET_SCRIPT = "/home/ubuntu/app/scripts/reset_db.sh"

# Local configuration
LOCAL_RESET_SCRIPT = os.path.join(os.path.dirname(__file__), "..", "scripts", "reset_local_db.sh")

def _wait_healthy(url: str, timeout: int = 40):
    t0 = time.time()
    if not url.endswith('/'):
        url = url + '/'
    while time.time() - t0 < timeout:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code in (200, 302):
                return
        except Exception:
            pass
        time.sleep(0.5)
    raise TimeoutError("Service not healthy")

def reset_remote_db():
    """Reset database on remote EC2 instance"""
    subprocess.run([
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-i", KEY_FILE,
        f"{USER}@{HOST}",
        f"bash {REMOTE_RESET_SCRIPT}"
    ], check=True)

def reset_local_db():
    """Reset database locally using backup file"""
    script_path = os.path.abspath(LOCAL_RESET_SCRIPT)
    script_dir = os.path.dirname(os.path.dirname(script_path))  # Go up to yosef-code directory
    
    print(f"🔍 Script path: {script_path}")
    print(f"🔍 Working directory: {script_dir}")
    print(f"🔍 Script exists: {os.path.exists(script_path)}")
    
    if not os.path.exists(script_path):
        raise FileNotFoundError(f"Local reset script not found at: {script_path}")
    
    # Check if backup database exists
    backup_path = os.path.join(script_dir, "nocodb", "noco.db.bak")
    db_path = os.path.join(script_dir, "nocodb", "noco.db")
    print(f"🔍 Backup DB path: {backup_path}")
    print(f"🔍 Main DB path: {db_path}")
    print(f"🔍 Backup exists: {os.path.exists(backup_path)}")
    print(f"🔍 Main DB exists: {os.path.exists(db_path)}")
    
    # Run the script from the yosef-code directory with detailed output
    print("🔄 Executing local reset script...")
    result = subprocess.run([
        "bash", script_path
    ], cwd=script_dir, capture_output=True, text=True, check=False)
    
    print(f"🔍 Script exit code: {result.returncode}")
    if result.stdout:
        print(f"📝 Script stdout:\n{result.stdout}")
    if result.stderr:
        print(f"❌ Script stderr:\n{result.stderr}")
    
    if result.returncode != 0:
        raise subprocess.CalledProcessError(result.returncode, f"bash {script_path}", result.stdout, result.stderr)

def reset_database():
    """Reset database based on environment (local or remote)"""
    print(f"🔍 Environment detection: BASE_URL='{BASE_URL}'")
    print(f"🔍 IS_LOCAL={IS_LOCAL}")
    
    if IS_LOCAL:
        print("🏠 Running LOCAL database reset...")
        print(f"🔍 Local script path: {LOCAL_RESET_SCRIPT}")
        try:
            reset_local_db()
            print("✅ Local database reset completed successfully")
        except Exception as e:
            print(f"❌ Local database reset failed: {e}")
            raise
    else:
        print("☁️ Running REMOTE database reset...")
        try:
            reset_remote_db()
            print("✅ Remote database reset completed successfully")
        except Exception as e:
            print(f"❌ Remote database reset failed: {e}")
            raise

@pytest.fixture(scope="session", autouse=True)
def service_up():
    t0 = time.time()
    _wait_healthy(BASE_URL)
    print(f"[timing] Service health check: {time.time() - t0:.2f}s")
    yield

@pytest.fixture(autouse=True)
def reset_db_before_each_test(service_up, request: pytest.FixtureRequest):
    t_reset = time.time()
    
    # Use appropriate reset method based on environment
    reset_database()
    _wait_healthy(BASE_URL)
    
    environment_type = "LOCAL" if IS_LOCAL else "REMOTE"
    print(f"[timing] {request.node.nodeid} {environment_type} reset+health: {time.time() - t_reset:.2f}s")

    t_test = time.time()
    yield
    print(f"[timing] {request.node.nodeid} test duration: {time.time() - t_test:.2f}s")
