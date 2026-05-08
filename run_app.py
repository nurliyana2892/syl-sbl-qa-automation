from flask import Flask, request, jsonify
import sqlite3

app = Flask(__name__)

SYL = 94.0
SBL = 1.6


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


def evaluate_decision(yield_percent, bin_rate):
    if yield_percent < SYL:
        return "LOW_YIELD_HOLD"
    elif bin_rate > SBL:
        return "HIGH_FAIL_RATE_BIN_HOLD"
    return "RELEASE"


@app.route("/")
def home():
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>SYL/SBL QA Automation Portal</title>
        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #0f172a, #1e3a8a);
                color: #111827;
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .container {{
                width: 900px;
                background: #ffffff;
                border-radius: 24px;
                padding: 40px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.25);
            }}

            .header {{
                margin-bottom: 30px;
            }}

            .header h1 {{
                margin: 0;
                font-size: 36px;
                color: #0f172a;
            }}

            .header p {{
                color: #64748b;
                font-size: 16px;
            }}

            .grid {{
                display: grid;
                grid-template-columns: 1fr 1fr;
                gap: 24px;
            }}

            .card {{
                background: #f8fafc;
                border: 1px solid #e2e8f0;
                border-radius: 18px;
                padding: 24px;
            }}

            .metric {{
                font-size: 34px;
                font-weight: bold;
                color: #1d4ed8;
            }}

            label {{
                display: block;
                font-weight: bold;
                margin-top: 16px;
                color: #334155;
            }}

            input {{
                width: 100%;
                padding: 14px;
                margin-top: 8px;
                border-radius: 12px;
                border: 1px solid #cbd5e1;
                font-size: 16px;
                box-sizing: border-box;
            }}

            button {{
                margin-top: 24px;
                width: 100%;
                padding: 14px;
                border: none;
                border-radius: 12px;
                background: #2563eb;
                color: white;
                font-size: 16px;
                font-weight: bold;
                cursor: pointer;
            }}

            button:hover {{
                background: #1d4ed8;
            }}

            .footer {{
                margin-top: 28px;
                color: #64748b;
                font-size: 14px;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>SYL/SBL QA Automation Portal</h1>
                <p>Manufacturing yield monitoring and automated lot hold validation</p>
            </div>

            <div class="grid">
                <div class="card">
                    <h3>Current Statistical Limits</h3>
                    <p>SYL Threshold</p>
                    <div class="metric">{SYL}%</div>
                    <p>SBL Threshold</p>
                    <div class="metric">{SBL}%</div>
                </div>

                <div class="card">
                    <h3>Evaluate Production Lot</h3>
                    <form action="/evaluate" method="post">
                        <label>Yield %</label>
                        <input name="yield_percent" data-testid="yield" placeholder="Example: 96.5" required>

                        <label>Fail Bin %</label>
                        <input name="bin_rate" data-testid="bin" placeholder="Example: 0.8" required>

                        <button type="submit" data-testid="evaluate-btn">
                            Evaluate Lot
                        </button>
                    </form>
                </div>
            </div>

            <div class="footer">
                Built with Python, Flask, Playwright, Pytest, SQL validation and GitHub Actions CI/CD.
            </div>
        </div>
    </body>
    </html>
    """


@app.route("/evaluate", methods=["POST"])
def evaluate():
    yield_percent = float(request.form["yield_percent"])
    bin_rate = float(request.form["bin_rate"])

    decision = evaluate_decision(yield_percent, bin_rate)
    save_lot_result(yield_percent, bin_rate, decision)

    color = "#16a34a" if decision == "RELEASE" else "#dc2626"

    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Evaluation Result</title>
        <style>
            body {{
                margin: 0;
                font-family: Arial, sans-serif;
                background: linear-gradient(135deg, #0f172a, #1e3a8a);
                min-height: 100vh;
                display: flex;
                align-items: center;
                justify-content: center;
            }}

            .result-card {{
                background: white;
                padding: 48px;
                border-radius: 24px;
                width: 600px;
                text-align: center;
                box-shadow: 0 20px 60px rgba(0,0,0,0.25);
            }}

            .badge {{
                display: inline-block;
                padding: 16px 28px;
                border-radius: 999px;
                background: {color};
                color: white;
                font-size: 28px;
                font-weight: bold;
                margin: 20px 0;
            }}

            a {{
                display: inline-block;
                margin-top: 24px;
                color: #2563eb;
                text-decoration: none;
                font-weight: bold;
            }}
        </style>
    </head>
    <body>
        <div class="result-card">
            <h1>Lot Evaluation Result</h1>
            <div class="badge" data-testid="decision">{decision}</div>
            <p>Yield: {yield_percent}% | Fail Bin: {bin_rate}%</p>
            <a href="/">Evaluate another lot</a>
        </div>
    </body>
    </html>
    """


@app.route("/api/evaluate", methods=["POST"])
def api_evaluate():
    data = request.get_json()

    yield_percent = float(data["yield_percent"])
    bin_rate = float(data["bin_rate"])

    decision = evaluate_decision(yield_percent, bin_rate)
    save_lot_result(yield_percent, bin_rate, decision)

    return jsonify({"decision": decision})


if __name__ == "__main__":
    app.run(debug=True, port=5000)
