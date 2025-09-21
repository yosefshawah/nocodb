import shutil
import subprocess
import time
from pathlib import Path
import pytest

# Paths
REPO_ROOT = Path(__file__).resolve().parents[1]
DB_FILE = REPO_ROOT / "nocodb" / "noco.db"
SNAPSHOT_FILE = REPO_ROOT / "nocodb" / "noco.db.bak"

SERVICE_NAME = "noco"  # as defined in docker-compose.yml

@pytest.fixture(autouse=True)
def reset_db():
    """Restore DB snapshot after each test run.

    Stops the docker service to release file locks, restores the DB file
    from the snapshot, then starts the service again.
    """
    yield

    # Basic sanity checks
    if not SNAPSHOT_FILE.exists():
        print(f"[teardown] Snapshot not found: {SNAPSHOT_FILE}")
        return
    if not DB_FILE.exists():
        print(f"[teardown] DB file not found (will be created): {DB_FILE}")

    # Stop service (best-effort)
    try:
        subprocess.run(["docker", "compose", "stop", SERVICE_NAME], cwd=REPO_ROOT, check=False, capture_output=True)
    except Exception as e:
        print(f"[teardown] Warning stopping service: {e}")

    # Small delay to ensure locks are released
    time.sleep(1)

    # Restore DB
    shutil.copy2(SNAPSHOT_FILE, DB_FILE)

    # Start service (best-effort)
    try:
        subprocess.run(["docker", "compose", "start", SERVICE_NAME], cwd=REPO_ROOT, check=False, capture_output=True)
    except Exception as e:
        print(f"[teardown] Warning starting service: {e}")

    # Give the service a moment to come back up
    time.sleep(2)
