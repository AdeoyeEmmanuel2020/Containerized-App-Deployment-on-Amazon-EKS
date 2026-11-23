import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parents[1] / "src"))

from app import create_app


def test_index_exposes_expected_contract():
    response = create_app().test_client().get("/")
    assert response.status_code == 200
    assert response.get_json()["application"] == "eks-reference-service"


def test_liveness():
    response = create_app().test_client().get("/health/live")
    assert response.status_code == 200
    assert response.get_json() == {"status": "alive"}


def test_readiness():
    response = create_app().test_client().get("/health/ready")
    assert response.status_code == 200
    assert response.get_json() == {"status": "ready"}
