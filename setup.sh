#!/bin/bash

echo "Installing dependencies..."

sudo apt update
sudo apt install arp-scan net-tools python3-venv -y

python3 -m venv vanta-env
source vanta-env/bin/activate

pip install -r requirements.txt

echo "Setup complete!"
