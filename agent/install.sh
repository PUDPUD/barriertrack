#!/bin/bash

SERVICE_NAME=barriertrack_agent
APP_DIRECTORY="$(pwd)"
PYTHON_PATH="/usr/bin/python3"

cat <<EOF | sudo tee /etc/systemd/system/$SERVICE_NAME.service
[Unit]
Description=Flask API Service
After=network.target

[Service]
User=root
Group=root
WorkingDirectory=$APP_DIRECTORY
ExecStart=$PYTHON_PATH $APP_DIRECTORY/agent.py

[Install]
WantedBy=multi-user.target
EOF


sudo systemctl daemon-reload
sudo systemctl start $SERVICE_NAME
sudo systemctl enable $SERVICE_NAME
echo "Barriertrack Api is succesvol geinnstalleerd, bekijk de status met: systemctl status barriertrack_agent." 