#!/usr/bin/env bash
set -euo pipefail

# Usage:
#   sudo bash deploy/setup_vps.sh
# Run from /var/www/hs/backend

APP_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$APP_DIR"

echo "[1/7] Installing system packages..."
sudo apt update
sudo apt install -y python3 python3-venv python3-pip nginx mysql-client

echo "[2/7] Creating virtual environment..."
python3 -m venv .venv
source .venv/bin/activate

echo "[3/7] Installing Python dependencies..."
pip install --upgrade pip setuptools wheel
pip install -r requirements.txt

echo "[4/7] Preparing .env file..."
if [ ! -f .env ]; then
  cp .env.example .env
  echo "Created .env from .env.example. Please edit it before continuing."
  exit 1
fi

echo "[5/7] Installing systemd service..."
sudo cp deploy/gunicorn.service /etc/systemd/system/hs.service
sudo systemctl daemon-reload
sudo systemctl enable hs
sudo systemctl restart hs

echo "[6/7] Installing nginx site config..."
sudo cp deploy/nginx.conf /etc/nginx/sites-available/hs
sudo ln -sf /etc/nginx/sites-available/hs /etc/nginx/sites-enabled/hs
sudo nginx -t
sudo systemctl restart nginx

echo "[7/7] Done."
echo "Check app health: curl http://127.0.0.1:8080/health"
echo "Check gunicorn logs: sudo journalctl -u hs -f"
