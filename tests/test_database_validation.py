import sqlite3
import requests

BASE_URL = "http://127.0.0.1:5000"

def test_api_result_saved_to_database():
    response = requests.post(
        f"{BASE_URL}/api/evaluate",
        json={"yield_percent": 93.0, "bin_rate": 0.8}
    )

    assert response.status_code == 200
    assert response.json()["decision"] == "LOW_YIELD_HOLD"

    conn = sqlite3.connect("lots.db")
    cursor = conn.cursor()

    cursor.execute("""
        SELECT decision
        FROM lot_results
        ORDER BY id DESC
        LIMIT 1
    """)

    latest_decision = cursor.fetchone()[0]
    conn.close()

    assert latest_decision == "LOW_YIELD_HOLD"