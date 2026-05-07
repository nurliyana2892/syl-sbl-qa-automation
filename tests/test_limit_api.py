import requests

BASE_URL = "http://127.0.0.1:5000"

def test_api_low_yield_hold():
    response = requests.post(
        f"{BASE_URL}/api/evaluate",
        json={"yield_percent": 93.0, "bin_rate": 0.8}
    )

    assert response.status_code == 200
    assert response.json()["decision"] == "LOW_YIELD_HOLD"


def test_api_high_fail_rate_hold():
    response = requests.post(
        f"{BASE_URL}/api/evaluate",
        json={"yield_percent": 96.0, "bin_rate": 2.0}
    )

    assert response.status_code == 200
    assert response.json()["decision"] == "HIGH_FAIL_RATE_BIN_HOLD"


def test_api_release_good_lot():
    response = requests.post(
        f"{BASE_URL}/api/evaluate",
        json={"yield_percent": 96.0, "bin_rate": 0.8}
    )

    assert response.status_code == 200
    assert response.json()["decision"] == "RELEASE"