from flask import Flask, send_file, render_template_string
import sqlite3
import matplotlib.pyplot as plt
import datetime

app = Flask(__name__)

DB_PATH = "/etc/pihole/pihole-FTL.db"

def detect_anomaly(current, history):
    if len(history) < 3:
        return False
    avg = sum(history) / len(history)
    return current > avg * 1.5

def generate_graph():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    cursor.execute("""
        SELECT timestamp, COUNT(*) 
        FROM queries 
        WHERE timestamp > strftime('%s','now','-10 minutes')
        GROUP BY (timestamp/60)
    """)

    data = cursor.fetchall()

    times = []
    counts = []

    for row in data:
        times.append(datetime.datetime.fromtimestamp(row[0]).strftime('%H:%M'))
        counts.append(row[1])

    if not counts:
        return None, False

    anomaly = detect_anomaly(counts[-1], counts[:-1])

    plt.style.use("dark_background")
    plt.figure(figsize=(10,5))

    plt.plot(times, counts, marker='o', color="#00ffcc")
    plt.title("Traffic (Last 10 mins)")

    file_name = "dashboard_live.png"
    plt.savefig(file_name, facecolor="#121212")
    plt.close()

    return file_name, anomaly

@app.route("/")
def home():
    file, anomaly = generate_graph()

    alert = ""
    if anomaly:
        alert = "<h2 style='color:red;'>⚠️ Anomaly Detected</h2>"

    html = f"""
    <html>
    <head>
        <meta http-equiv="refresh" content="10">
        <style>
            body {{
                background:#0d1117;
                color:#00ffcc;
                text-align:center;
                font-family:Arial;
            }}
            img {{
                width:80%;
                border:2px solid #00ffcc;
            }}
        </style>
    </head>
    <body>
        <h1>VANTA LIVE DASHBOARD</h1>
        {alert}
        <img src="/graph">
    </body>
    </html>
    """

    return render_template_string(html)

@app.route("/graph")
def graph():
    file, _ = generate_graph()
    return send_file(file, mimetype="image/png")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)