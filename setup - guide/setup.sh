#!/bin/bash

echo "Starting VANTA setup..."

# Update system
sudo apt update -y

# Install required packages
sudo apt install -y python3 python3-pip python3-matplotlib python3-flask python3-requests sqlite3

# Create project directory if it doesn't exist
mkdir -p /home/vanta/VANTA
cd /home/vanta/VANTA

# Create files if missing
touch app.py stats.py alert.py monitor.py requirements.txt

# Give execute permission to python files
chmod +x *.py

echo ""
echo "Setup complete."

echo "Next steps:"
echo "1. Open alert.py and add your Telegram bot token and chat ID"
echo "2. Make sure Pi-hole is installed and running"
echo "3. Test the setup using: sudo python3 stats.py"
