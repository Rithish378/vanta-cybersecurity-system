import requests
import sys

TOKEN = "YOUR_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"

msg = " ".join(sys.argv[1:]) if len(sys.argv) > 1 else "VANTA Alert"

url = f"https://api.telegram.org/bot{TOKEN}/sendMessage"
requests.post(url, data={"chat_id": CHAT_ID, "text": msg})
