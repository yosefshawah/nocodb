import subprocess
import time
import requests  # pyright: ignore[reportMissingModuleSource]
import pytest  # pyright: ignore[reportMissingImports]
from config import BASE_URL

HOST = "ec2-52-18-93-49.eu-west-1.compute.amazonaws.com"
USER = "ubuntu"
KEY_FILE = "/Users/shawahyosef/Desktop/nocodb-final-project/nocodb-final-yosef.pem"
RESET_SCRIPT = "/home/ubuntu/app/scripts/reset_db.sh"

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
    subprocess.run([
        "ssh",
        "-o", "StrictHostKeyChecking=no",
        "-o", "UserKnownHostsFile=/dev/null",
        "-i", KEY_FILE,
        f"{USER}@{HOST}",
        f"bash {RESET_SCRIPT}"
    ], check=True)

@pytest.fixture(scope="session", autouse=True)
def service_up():
    t0 = time.time()
    _wait_healthy(BASE_URL)
    print(f"[timing] Service health check: {time.time() - t0:.2f}s")
    yield

@pytest.fixture(autouse=True)
def reset_db_before_each_test(service_up, request: pytest.FixtureRequest):
    t_reset = time.time()
    reset_remote_db()
    _wait_healthy(BASE_URL)
    print(f"[timing] {request.node.nodeid} reset+health: {time.time() - t_reset:.2f}s")

    t_test = time.time()
    yield
    print(f"[timing] {request.node.nodeid} test duration: {time.time() - t_test:.2f}s")
