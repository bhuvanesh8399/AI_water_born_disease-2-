import os
import sys
from pathlib import Path

import pytest
from fastapi.testclient import TestClient

ROOT_DIR = Path(__file__).resolve().parents[1]
if str(ROOT_DIR) not in sys.path:
    sys.path.append(str(ROOT_DIR))

os.environ["DATABASE_URL"] = "sqlite:///./test_ews.db"
os.environ["AUTH_ENABLED"] = "false"
os.environ["READ_ONLY_DEMO"] = "true"

from app.main import app


@pytest.fixture(scope="session")
def client():
    with TestClient(app) as test_client:
        yield test_client
