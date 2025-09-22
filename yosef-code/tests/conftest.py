import shutil
import subprocess
import time
import os
from pathlib import Path
import requests
import pytest
from config import BASE_URL  # uses localhost by default

# Compose dir and files
# Allow overriding deploy/compose directory via DEPLOY_DIR env (useful on EC2 where deploy is at /home/ubuntu/app)
DEPLOY_DIR = Path(os.getenv("DEPLOY_DIR", str(Path(__file__).resolve().parents[2] / "deploy")))
COMPOSE_DIR = DEPLOY_DIR
SERVICE_NAME = "app"  # service key in docker-compose.yml

# Data files mounted by compose: ./nocodb -> /usr/app/data/
# Allow overriding DB and snapshot paths via env; fall back to EC2 default if present
DEFAULT_DB = COMPOSE_DIR / "nocodb" / "noco.db"
DEFAULT_SNAPSHOT = COMPOSE_DIR / "nocodb" / "noco.db.bak"
EC2_DB = Path("/home/ubuntu/app/nocodb/noco.db")
EC2_SNAPSHOT = Path("/home/ubuntu/app/nocodb/noco.db.bak")

DB_FILE = Path(
    os.getenv(
        "NOCODB_DB_FILE",
        str(DEFAULT_DB if DEFAULT_DB.exists() else (EC2_DB if EC2_DB.exists() else DEFAULT_DB)),
    )
)
SNAPSHOT_FILE = Path(
    os.getenv(
        "NOCODB_DB_SNAPSHOT",
        str(
            DEFAULT_SNAPSHOT
            if DEFAULT_SNAPSHOT.exists()
            else (EC2_SNAPSHOT if EC2_SNAPSHOT.exists() else DEFAULT_SNAPSHOT)
        ),
    )
)

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
    print(f"[setup] Using compose dir: {COMPOSE_DIR}")
    _compose(["up", "-d", SERVICE_NAME])
    _wait_healthy(BASE_URL)
    yield
    _compose(["down", "--remove-orphans"])

@pytest.fixture(autouse=True)
def fresh_db(service_up):
    # Restore snapshot BEFORE each test; next test’s setup acts as teardown.
    if SNAPSHOT_FILE.exists():
        print(f"[setup] Restoring snapshot: {SNAPSHOT_FILE} -> {DB_FILE}")
        _compose(["stop", SERVICE_NAME])
        time.sleep(1)
        shutil.copy2(SNAPSHOT_FILE, DB_FILE)
        _compose(["start", SERVICE_NAME])
        _wait_healthy(BASE_URL)
        time.sleep(1)
    else:
        print(f"[setup] Snapshot not found: {SNAPSHOT_FILE}")
    yield
