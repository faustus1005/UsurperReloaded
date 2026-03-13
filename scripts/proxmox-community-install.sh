#!/usr/bin/env bash
set -euo pipefail

# Usurper ReLoaded - Proxmox LXC installer
# Run on a Proxmox VE host as root.

CTID="${CTID:-120}"
HOSTNAME="${HOSTNAME:-usurperreloaded}"
CORES="${CORES:-2}"
MEMORY="${MEMORY:-2048}"
SWAP="${SWAP:-512}"
DISK="${DISK:-8}"
BRIDGE="${BRIDGE:-vmbr0}"
OSTEMPLATE="${OSTEMPLATE:-local:vztmpl/debian-12-standard_12.7-1_amd64.tar.zst}"
STORAGE="${STORAGE:-local-lvm}"
PASSWORD="${PASSWORD:-change-me-now}"
IPCFG="${IPCFG:-dhcp}"
APP_DIR="/opt/usurperreloaded"
APP_USER="usurper"
APP_PORT="${APP_PORT:-5000}"
REPO_URL="${REPO_URL:-https://github.com/faustus1005/UsurperReloaded.git}"
REPO_REF="${REPO_REF:-main}"

# Generate a stable secret key for Flask session management
SECRET_KEY="${SECRET_KEY:-$(openssl rand -hex 32)}"

if [[ "${EUID}" -ne 0 ]]; then
  echo "This script must run as root on a Proxmox host."
  exit 1
fi

if ! command -v pct >/dev/null 2>&1; then
  echo "pct command not found. Run this on a Proxmox VE host."
  exit 1
fi

if pct status "${CTID}" >/dev/null 2>&1; then
  echo "Container ${CTID} already exists. Choose a different CTID."
  exit 1
fi

echo "[1/7] Creating LXC ${CTID} (${HOSTNAME})"
pct create "${CTID}" "${OSTEMPLATE}" \
  --hostname "${HOSTNAME}" \
  --password "${PASSWORD}" \
  --cores "${CORES}" \
  --memory "${MEMORY}" \
  --swap "${SWAP}" \
  --rootfs "${STORAGE}:${DISK}" \
  --features nesting=1 \
  --net0 "name=eth0,bridge=${BRIDGE},ip=${IPCFG}" \
  --unprivileged 1

echo "[2/7] Starting container"
pct start "${CTID}"

# Brief pause to let the container network come up
sleep 3

echo "[3/7] Installing base dependencies"
pct exec "${CTID}" -- bash -lc "apt-get update && apt-get install -y git curl python3 python3-venv python3-pip sqlite3"

echo "[4/7] Deploying application"
pct exec "${CTID}" -- bash -lc "id -u ${APP_USER} >/dev/null 2>&1 || useradd -m -s /bin/bash ${APP_USER}"
pct exec "${CTID}" -- bash -lc "rm -rf ${APP_DIR} && git clone --depth 1 --branch ${REPO_REF} ${REPO_URL} ${APP_DIR}"
pct exec "${CTID}" -- bash -lc "python3 -m venv ${APP_DIR}/web/.venv"
pct exec "${CTID}" -- bash -lc "${APP_DIR}/web/.venv/bin/pip install --upgrade pip && ${APP_DIR}/web/.venv/bin/pip install -r ${APP_DIR}/web/requirements.txt gunicorn"
pct exec "${CTID}" -- bash -lc "chown -R ${APP_USER}:${APP_USER} ${APP_DIR}"

echo "[5/7] Initializing database"
pct exec "${CTID}" -- bash -lc "cd ${APP_DIR}/web && sudo -u ${APP_USER} ${APP_DIR}/web/.venv/bin/python -c 'from app import app, init_db; init_db()'"

echo "[6/7] Creating systemd service"
pct exec "${CTID}" -- bash -lc "cat > /etc/systemd/system/usurperreloaded.service <<SERVICE
[Unit]
Description=Usurper ReLoaded Flask App
After=network.target

[Service]
User=${APP_USER}
Group=${APP_USER}
WorkingDirectory=${APP_DIR}/web
Environment=SECRET_KEY=${SECRET_KEY}
Environment=PORT=${APP_PORT}
ExecStart=${APP_DIR}/web/.venv/bin/gunicorn --bind 0.0.0.0:${APP_PORT} --preload --workers 1 app:app
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
SERVICE"

pct exec "${CTID}" -- bash -lc "systemctl daemon-reload && systemctl enable --now usurperreloaded"

echo "[7/7] Done"
pct exec "${CTID}" -- bash -lc "systemctl --no-pager --full status usurperreloaded | sed -n '1,12p'"
echo ""
echo "Container ${CTID} is running Usurper ReLoaded on port ${APP_PORT}."
echo "Find container IP: pct exec ${CTID} -- hostname -I"
echo "SECRET_KEY: ${SECRET_KEY}"
echo "Save this key if you ever need to recreate the container."
