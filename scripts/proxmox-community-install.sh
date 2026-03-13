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
REPO_URL="${REPO_URL:-https://github.com/<your-org>/UsurperReloaded.git}"
REPO_REF="${REPO_REF:-main}"

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

if [[ "${REPO_URL}" == *"<your-org>"* ]]; then
  echo "Update REPO_URL before running (or export REPO_URL)."
  exit 1
fi

echo "[1/6] Creating LXC ${CTID} (${HOSTNAME})"
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

echo "[2/6] Starting container"
pct start "${CTID}"

echo "[3/6] Installing base dependencies"
pct exec "${CTID}" -- bash -lc "apt-get update && apt-get install -y git python3 python3-venv python3-pip sqlite3"

echo "[4/6] Deploying application"
pct exec "${CTID}" -- bash -lc "id -u ${APP_USER} >/dev/null 2>&1 || useradd -m -s /bin/bash ${APP_USER}"
pct exec "${CTID}" -- bash -lc "rm -rf ${APP_DIR} && git clone --depth 1 --branch ${REPO_REF} ${REPO_URL} ${APP_DIR}"
pct exec "${CTID}" -- bash -lc "python3 -m venv ${APP_DIR}/web/.venv"
pct exec "${CTID}" -- bash -lc "${APP_DIR}/web/.venv/bin/pip install --upgrade pip && ${APP_DIR}/web/.venv/bin/pip install -r ${APP_DIR}/web/requirements.txt gunicorn"
pct exec "${CTID}" -- bash -lc "chown -R ${APP_USER}:${APP_USER} ${APP_DIR}"

echo "[5/6] Creating systemd service"
pct exec "${CTID}" -- bash -lc "cat > /etc/systemd/system/usurperreloaded.service <<'SERVICE'\n[Unit]\nDescription=Usurper ReLoaded Flask App\nAfter=network.target\n\n[Service]\nUser=${APP_USER}\nGroup=${APP_USER}\nWorkingDirectory=${APP_DIR}/web\nEnvironment=FLASK_ENV=production\nEnvironment=PORT=${APP_PORT}\nExecStart=${APP_DIR}/web/.venv/bin/gunicorn --bind 0.0.0.0:${APP_PORT} app:app\nRestart=always\nRestartSec=5\n\n[Install]\nWantedBy=multi-user.target\nSERVICE"

pct exec "${CTID}" -- bash -lc "systemctl daemon-reload && systemctl enable --now usurperreloaded"

echo "[6/6] Done"
pct exec "${CTID}" -- bash -lc "systemctl --no-pager --full status usurperreloaded | sed -n '1,12p'"
echo "Container ${CTID} is running Usurper ReLoaded on port ${APP_PORT}."
echo "Find container IP: pct exec ${CTID} -- hostname -I"
