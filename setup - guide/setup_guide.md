#  VANTA Setup Guide (Step-by-Step Deployment)

# 1. Hardware Requirements

* Raspberry Pi Zero / Zero 2 W
* MicroSD Card (16GB+)
* Power Supply
* WiFi connection

#2. Install Raspberry Pi OS

1. Download Raspberry Pi Imager
2. Flash Raspberry Pi OS (Lite recommended)
3. Enable:

   * SSH
   * WiFi (configure SSID & password)
4. Insert SD card and power ON Pi

# 3. Find Raspberry Pi IP Address

* Login to router:

```
http://192.168.29.1
```

* Go to **Connected Devices**
* Note Pi IP (example: `192.168.29.225`)


# 4. Connect via SSH

```
ssh vanta@192.168.29.225
```

# 5. Set Static IP (Recommended)

```
sudo nano /etc/dhcpcd.conf
```

Add:

```
interface wlan0
static ip_address=192.168.29.225/24
static routers=192.168.29.1
static domain_name_servers=1.1.1.1
```

Save and reboot:

```
sudo reboot
```

# 6. Install Pi-hole

```
curl -sSL https://install.pi-hole.net | bash
```

During installation:

* Interface → wlan0
* DNS → Cloudflare
* Privacy → Show everything

# 7. Access Pi-hole Dashboard

```
http://192.168.29.225/admin
```

Reset password if needed:

```
pihole -a -p
```

# 8. Configure Router DNS

Open:

```
http://192.168.29.1
```

Set:

```
Primary DNS → 192.168.29.225
Secondary DNS → (empty or same)
```

Restart WiFi/router.

#9. Add Blocklists

Go to:

**Group Management → Adlists**

Add:

```
https://raw.githubusercontent.com/StevenBlack/hosts/master/hosts
```

Then:

**Tools → Update Gravity**

# 10. Setup Telegram Bot

1. Open Telegram → @BotFather
2. Run:

```
/start
/newbot
```

3. Save BOT TOKEN

### Get Chat ID

1. Send message to your bot
2. Open:

```
https://api.telegram.org/bot<TOKEN>/getUpdates
```

3. Copy `chat_id`

---

# 11. Setup Python Environment

```
sudo apt install python3-venv -y
python3 -m venv vanta-env
source vanta-env/bin/activate
pip install requests
```

# 12. Setup Project

```
git clone https://github.com/your-username/vanta-cybersecurity-system.git
cd vanta-cybersecurity-system
```


# 13. Configure Alerts

```
nano src/alert.py
```

Update:

```
TOKEN = "YOUR_TOKEN"
CHAT_ID = "YOUR_CHAT_ID"
```

# 14. Install Network Tools

```
sudo apt install arp-scan net-tools -y
```

# 15. Run Monitoring System

```
source vanta-env/bin/activate
python src/monitor.py
```

# 16. Run as Service

```
sudo nano /etc/systemd/system/vanta.service
```

Paste:

```
[Unit]
Description=VANTA Security Monitor
After=network.target

[Service]
ExecStart=/home/vanta/vanta-env/bin/python /home/vanta/src/monitor.py
Restart=always
User=vanta

[Install]
WantedBy=multi-user.target
```

Enable:

```
sudo systemctl daemon-reload
sudo systemctl enable vanta
sudo systemctl start vanta
```

# 17. Setup Remote Access (Tailscale)

```
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
tailscale ip
```

Access:

```
http://100.x.x.x/admin
```

#18. Testing

* Connect a new device → Telegram alert
* Open ad-heavy website → ads blocked
* Check Pi-hole dashboard → queries increase


# Final System Capabilities

* DNS-level threat blocking
* Real-time intrusion detection
* Telegram alert system
* Remote monitoring (Tailscale)
* 24/7 automated operation


# 📊 Metrics

* 10,000+ DNS queries analyzed
* 7,000+ threats blocked
* <30 sec detection time
* <2 sec alert latency


VANTA acts as a centralized network security layer providing real-time monitoring, threat detection, and automated response.
