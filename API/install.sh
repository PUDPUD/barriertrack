#!/bin/bash

# Definieer de naam van de service
SERVICE_NAME=barriertrack_api

# Pad naar de directory van je Flask app
APP_DIRECTORY="$(pwd)"

# Pad naar de Python interpreter, pas deze aan naar jouw omgeving
PYTHON_PATH="/usr/bin/python3"

# Maak het systemd service bestand
cat <<EOF | sudo tee /etc/systemd/system/$SERVICE_NAME.service
[Unit]
Description=Flask API Service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=$APP_DIRECTORY
ExecStart=$PYTHON_PATH $APP_DIRECTORY/api.py

[Install]
WantedBy=multi-user.target
EOF

# Herlaad systemd om de nieuwe service te herkennen
sudo systemctl daemon-reload

# Start de service
sudo systemctl start $SERVICE_NAME

# Schakel de service in om automatisch te starten bij het opstarten
sudo systemctl enable $SERVICE_NAME

echo "Flask API service is geïnstalleerd en gestart."