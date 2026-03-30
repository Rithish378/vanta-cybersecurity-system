import sqlite3
import matplotlib.pyplot as plt
import datetime
from alert import send_photo

DB_PATH = "/etc/pihole/pihole-FTL.db"

try:
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
except Exception as e:
    print("Database error:", e)
    exit()

cursor.execute("SELECT COUNT(*) FROM queries;")
total = cursor.fetchone()[0]

cursor.execute("SELECT COUNT(*) FROM queries WHERE status = 1;")
blocked = cursor.fetchone()[0]

allowed = total - blocked

if total == 0:
    print("No data yet")
    exit()

blocked_percent = (blocked / total) * 100
current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

labels = ["Blocked", "Allowed"]
values = [blocked, allowed]

plt.style.use("dark_background")
plt.figure(figsize=(10,5))

plt.subplot(1,2,1)
plt.bar(labels, values, color=["#ff4c4c", "#00ff9c"])
plt.title("Traffic Overview")

for i, v in enumerate(values):
    plt.text(i, v + (total * 0.01), str(v), ha='center', color="white")

plt.subplot(1,2,2)
plt.pie(values, labels=labels, autopct='%1.1f%%',
        colors=["#ff4c4c", "#00ff9c"])

plt.suptitle("VANTA Security Dashboard")

summary = (
    f"Time: {current_time}\n"
    f"Total: {total}\n"
    f"Blocked: {blocked}\n"
    f"Allowed: {allowed}\n"
    f"Block Rate: {blocked_percent:.1f}%"
)

plt.figtext(0.5, -0.08, summary, ha="center", color="white")

file_name = "vanta_dashboard.png"
plt.tight_layout()
plt.savefig(file_name, facecolor="#121212")

print("Dashboard generated")

send_photo(file_name, f"VANTA Report\n{current_time}")