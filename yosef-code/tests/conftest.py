import shutil
import subprocess
import time
from pathlib import Path
import requests
import pytest
from config import BASE_URL  # uses localhost by default

# Compose dir and files
COMPOSE_DIR = Path(__file__).resolve().parents[2] / "deploy"
SERVICE_NAME = "app"  # service key in docker-compose.yml

# Data files mounted by compose: ./nocodb -> /usr/app/data/
DB_FILE = COMPOSE_DIR / "nocodb" / "noco.db"
SNAPSHOT_FILE = COMPOSE_DIR / "nocodb" / "noco.db.bak"

def _compose(args):
    subprocess.run(["docker", "compose", *args], cwd=COMPOSE_DIR, check=False, capture_output=True)

def _wait_healthy(url: str, timeout: int = 40):
    t0 = time.time()
    while time.time() - t0 < timeout:
        try:
            r = requests.get(url, timeout=2)
            if r.status_code in (200, 302):
                return
        except Exception:
            pass
        time.sleep(0.5)
    raise TimeoutError("Service not healthy")

@pytest.fixture(scope="session", autouse=True)
def service_up():
    _compose(["up", "-d", SERVICE_NAME])
    _wait_healthy(BASE_URL)
    yield
    _compose(["down", "--remove-orphans"])

@pytest.fixture(autouse=True)
def fresh_db(service_up):
    # Restore snapshot BEFORE each test; next test’s setup acts as teardown.
    if SNAPSHOT_FILE.exists():
        _compose(["stop", SERVICE_NAME])
        time.sleep(1)
        shutil.copy2(SNAPSHOT_FILE, DB_FILE)
        _compose(["start", SERVICE_NAME])
        _wait_healthy(BASE_URL)
        time.sleep(1)
    else:
        print(f"[setup] Snapshot not found: {SNAPSHOT_FILE}")
    yield
