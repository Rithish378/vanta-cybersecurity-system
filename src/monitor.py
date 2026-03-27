import os
import time
import subprocess
from datetime import datetime
import RPi.GPIO as GPIO

# ---------------- CONFIG ---------------- #
PI_IP = "192.168.29.225"
ROUTER_IP = "192.168.29.1"
ALERT_COOLDOWN = 60  # seconds

known_devices = set()
last_alert_time = {}

# GPIO Setup
GPIO.setmode(GPIO.BCM)
RED = 17
GPIO.setup(RED, GPIO.OUT)
GPIO.output(RED, GPIO.LOW)

print("🛡️ VANTA Advanced Security Monitoring Started...")

# ---------------- ALERT FUNCTION ---------------- #
def send_alert(message):
    os.system(f'/home/vanta/vanta-env/bin/python /home/vanta/alert.py "{message}"')

def trigger_alert():
    GPIO.output(RED, GPIO.HIGH)
    time.sleep(2)
    GPIO.output(RED, GPIO.LOW)

# ---------------- RATE LIMIT ---------------- #
def can_alert(key):
    now = time.time()
    if key not in last_alert_time or (now - last_alert_time[key]) > ALERT_COOLDOWN:
        last_alert_time[key] = now
        return True
    return False

# ---------------- THREAT SCORING ---------------- #
def threat_score(keyword):
    scores = {
        "phishing": 9,
        "malware": 10,
        "crypto": 6,
        "tracking": 5,
        "adult": 4
    }
    return scores.get(keyword, 3)

# ---------------- DEVICE SCAN ---------------- #
def scan_devices():
    output = subprocess.getoutput("arp-scan --localnet")

    for line in output.split("\n"):
        if "192.168.29." in line:
            parts = line.split()
            if len(parts) >= 3:
                ip = parts[0]
                mac = parts[1]
                vendor = " ".join(parts[2:])

                if ip in [PI_IP, ROUTER_IP]:
                    continue

                if mac not in known_devices:
                    known_devices.add(mac)

                    message = (
                        f"🚨 NEW DEVICE DETECTED\n"
                        f"Time: {datetime.now()}\n"
                        f"IP: {ip}\n"
                        f"MAC: {mac}\n"
                        f"Vendor: {vendor}"
                    )

                    print(message)

                    if can_alert(mac):
                        send_alert(message)
                        trigger_alert()

# ---------------- DNS ATTACK DETECTION ---------------- #
def check_dns_attacks():
    try:
        log = subprocess.getoutput("tail -n 30 /var/log/pihole.log")

        suspicious_keywords = [
            "phishing",
            "malware",
            "crypto",
            "tracking",
            "adult",
            "bitcoin"
        ]

        for line in log.split("\n"):
            for keyword in suspicious_keywords:
                if keyword in line.lower():
                    key = f"dns_{keyword}"

                    if can_alert(key):
                        score = threat_score(keyword)

                        message = (
                            f"⚠️ THREAT DETECTED\n"
                            f"Risk Score: {score}/10\n"
                            f"Type: {keyword}\n"
                            f"Time: {datetime.now()}\n"
                            f"Log: {line.strip()}"
                        )

                        print(message)
                        send_alert(message)
                        trigger_alert()

    except Exception as e:
        print("DNS check error:", e)

# ---------------- TRAFFIC ANOMALY ---------------- #
def detect_traffic_spike():
    try:
        result = subprocess.getoutput("netstat -an | grep :53 | wc -l")
        connections = int(result)

        if connections > 50:
            key = "traffic_spike"

            if can_alert(key):
                message = (
                    f"⚠️ HIGH DNS TRAFFIC DETECTED\n"
                    f"Connections: {connections}\n"
                    f"Time: {datetime.now()}"
                )

                print(message)
                send_alert(message)
                trigger_alert()

    except:
        pass

# ---------------- MAIN LOOP ---------------- #
while True:
    scan_devices()
    check_dns_attacks()
    detect_traffic_spike()

    time.sleep(30)
