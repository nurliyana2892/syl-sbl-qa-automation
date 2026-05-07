from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)
def save_lot_result(yield_percent, bin_rate, decision):
    conn = sqlite3.connect("lots.db")
    cursor = conn.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS lot_results (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            yield_percent REAL,
            bin_rate REAL,
            decision TEXT
        )
    """)

    cursor.execute("""
        INSERT INTO lot_results (yield_percent, bin_rate, decision)
        VALUES (?, ?, ?)
    """, (yield_percent, bin_rate, decision))

    conn.commit()
    conn.close()

@app.route("/")
def home():
    return """
    <h1>SYL/SBL QA Automation Portal</h1>

    <form action="/evaluate" method="post">
        <label>Yield %</label><br>
        <input name="yield_percent" data-testid="yield"><br><br>

        <label>Fail Bin %</label><br>
        <input name="bin_rate" data-testid="bin"><br><br>

        <button type="submit" data-testid="evaluate-btn">
            Evaluate Lot
        </button>
    </form>
    """

@app.route("/evaluate", methods=["POST"])
def evaluate():
    yield_percent = float(request.form["yield_percent"])
    bin_rate = float(request.form["bin_rate"])

    syl = 94.0
    sbl = 1.6

    if yield_percent < syl:
        decision = "LOW_YIELD_HOLD"
    elif bin_rate > sbl:
        decision = "HIGH_FAIL_RATE_BIN_HOLD"
    else:
        decision = "RELEASE"

        save_lot_result(yield_percent, bin_rate, decision)

    return f"""
    <h1 data-testid="decision">{decision}</h1>
    """
@app.route("/api/evaluate", methods=["POST"])
def api_evaluate():
    data = request.get_json()

    yield_percent = float(data["yield_percent"])
    bin_rate = float(data["bin_rate"])

    syl = 94.0
    sbl = 1.6

    if yield_percent < syl:
        decision = "LOW_YIELD_HOLD"
    elif bin_rate > sbl:
        decision = "HIGH_FAIL_RATE_BIN_HOLD"
    else:
        decision = "RELEASE"

    save_lot_result(yield_percent, bin_rate, decision)

    return jsonify({"decision": decision})
    
if __name__ == "__main__":
    app.run(debug=True, port=5000)
