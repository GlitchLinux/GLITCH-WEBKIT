#!/bin/bash

# Define variables
PROJECT_DIR="/home/x/flask_project"
APP_PATH="/home/x/glitch-webkit/app.py"
LOG_FILE="/home/x/flask_app.log"
VENV_PATH="$PROJECT_DIR/venv"

echo "[+] Installing system dependencies..."
sudo apt update && sudo apt install -y python3 python3-pip python3-venv

# Create project directory if it doesn't exist
if [ ! -d "$PROJECT_DIR" ]; then
    echo "[+] Creating project directory at $PROJECT_DIR"
    mkdir -p "$PROJECT_DIR"
fi

# Create virtual environment if it doesn't exist
if [ ! -d "$VENV_PATH" ]; then
    echo "[+] Creating virtual environment..."
    python3 -m venv "$VENV_PATH"
fi

# Activate virtualenv and install packages
echo "[+] Activating virtual environment and installing packages..."
source "$VENV_PATH/bin/activate"
pip install --upgrade pip
pip install Flask==2.3.2 Gunicorn==20.1.0
deactivate

cd /home/x/glitch-webkit/
git clone https://github.com/GlitchLinux/gLiTcH-ToolKit.git

# Clean up old log file if exists
if [ -f "$LOG_FILE" ]; then
    echo "[+] Removing old log file at $LOG_FILE"
    rm -f "$LOG_FILE"
fi

# Wait a moment if needed
sleep 2

# Start Python app independently (orphaned, detached)
echo "[+] Starting Python app independently..."
setsid "$VENV_PATH/bin/python" "$APP_PATH" >"$LOG_FILE" 2>&1 &

echo "[+] Bash script done — Python app continues running in background."
echo "[+] Log file: $LOG_FILE"

# Optional: prompt before exit
read -rp "Press [Enter] to close..."
