# Usurper ReLoaded - Linux Install Guide (Web Edition)

A complete guide for installing and running the web version of Usurper ReLoaded on Linux.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start](#quick-start)
3. [Detailed Installation](#detailed-installation)
   - [Debian / Ubuntu](#debian--ubuntu)
   - [Fedora / RHEL / CentOS / AlmaLinux](#fedora--rhel--centos--almalinux)
   - [Arch Linux / Manjaro](#arch-linux--manjaro)
   - [openSUSE](#opensuse)
4. [Python Dependencies](#python-dependencies)
5. [Running the Game](#running-the-game)
6. [Enabling SSL/HTTPS](#enabling-sslhttps)
7. [Running as a systemd Service](#running-as-a-systemd-service)
8. [Production Deployment with Gunicorn](#production-deployment-with-gunicorn)
9. [Reverse Proxy with Nginx](#reverse-proxy-with-nginx)
10. [Firewall Configuration](#firewall-configuration)
11. [First-Time Setup](#first-time-setup)
12. [Updating](#updating)
13. [Troubleshooting](#troubleshooting)

---

## System Requirements

| Component       | Requirement                   |
|-----------------|-------------------------------|
| **OS**          | Any modern Linux distribution |
| **Python**      | 3.8 or higher                 |
| **RAM**         | 512 MB minimum, 1 GB recommended |
| **Disk**        | 200 MB (application + database) |
| **Network**     | Port 5000 (default) open for web access |

### Required System Packages

- `python3` (3.8+)
- `python3-pip`
- `python3-venv` (recommended)
- `git`

### Python Dependencies

These are installed automatically via `pip` from `requirements.txt`:

| Package              | Version  | Purpose                                    |
|----------------------|----------|--------------------------------------------|
| `flask`              | >= 3.0   | Web framework                              |
| `flask-sqlalchemy`   | >= 3.1   | Database ORM (SQLite)                      |
| `flask-login`        | >= 0.6   | User authentication and session management |
| `flask-wtf`          | >= 1.2   | Form handling and CSRF protection          |
| `werkzeug`           | >= 3.0   | Password hashing and security utilities    |
| `apscheduler`        | >= 3.10  | Background task scheduling (NPC AI engine) |
| `pyopenssl`          | >= 23.0  | *Optional* -- only needed for SSL_ADHOC mode |

The database engine is **SQLite**, which is included with Python -- no separate database server is needed.

---

## Quick Start

If you already have Python 3.8+ and pip installed:

```bash
git clone https://github.com/faustus1005/UsurperReloaded.git
cd UsurperReloaded/web
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
python app.py
```

The game will be available at `http://localhost:5000`.

> **Tip**: Keep this `web/venv` as your permanent virtual environment for updates and service commands. Reuse it instead of creating a new venv each time.

---

## Detailed Installation

### Debian / Ubuntu

Tested on Debian 11/12, Ubuntu 20.04/22.04/24.04, and derivatives (Linux Mint, Pop!_OS, etc.).

```bash
# Update package lists
sudo apt update

# Install Python 3, pip, venv, and git
sudo apt install -y python3 python3-pip python3-venv git

# Verify Python version (must be 3.8+)
python3 --version

# Clone the repository
git clone https://github.com/faustus1005/UsurperReloaded.git
cd UsurperReloaded/web

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run the game
python app.py
```

### Fedora / RHEL / CentOS / AlmaLinux

```bash
# Install Python 3, pip, and git
sudo dnf install -y python3 python3-pip git

# Verify Python version
python3 --version

# Clone the repository
git clone https://github.com/faustus1005/UsurperReloaded.git
cd UsurperReloaded/web

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run the game
python app.py
```

> **Note for RHEL/CentOS 7**: Python 3.8+ is not available in default repos. Use the `python39` or `python311` package from EPEL, or install via `pyenv`.

### Arch Linux / Manjaro

```bash
# Install Python and git
sudo pacman -S python python-pip git

# Clone the repository
git clone https://github.com/faustus1005/UsurperReloaded.git
cd UsurperReloaded/web

# Create and activate a virtual environment
python -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run the game
python app.py
```

### openSUSE

```bash
# Install Python 3, pip, and git
sudo zypper install -y python3 python3-pip git

# Clone the repository
git clone https://github.com/faustus1005/UsurperReloaded.git
cd UsurperReloaded/web

# Create and activate a virtual environment
python3 -m venv venv
source venv/bin/activate

# Install Python dependencies
pip install -r requirements.txt

# Run the game
python app.py
```

---

## Python Dependencies

All Python dependencies are listed in `web/requirements.txt` and installed with a single command:

```bash
pip install -r requirements.txt
```

This installs:

- **Flask 3.0+** -- the web framework that serves the game
- **Flask-SQLAlchemy 3.1+** -- ORM layer for the SQLite database
- **Flask-Login 0.6+** -- handles user login sessions
- **Flask-WTF 1.2+** -- provides form validation and CSRF protection
- **Werkzeug 3.0+** -- password hashing (used by Flask-Login)
- **APScheduler 3.10+** -- runs the NPC AI engine on a background timer
- **PyOpenSSL 23.0+** -- *(optional)* only required if you use `SSL_ADHOC=1` mode

---

## Running the Game

### Development Mode (Built-in Flask Server)

```bash
cd UsurperReloaded/web
source venv/bin/activate
python app.py
```

The game starts at `http://localhost:5000`. The SQLite database (`usurper.db`) is automatically created and seeded with monsters, items, NPCs, gods, and default configuration on first run.

### Changing the Port

```bash
PORT=8080 python app.py
```

### Binding to All Interfaces

By default Flask binds to `0.0.0.0`, making the game accessible from other machines on the network. Access it at `http://<your-ip>:5000`.

---

## Enabling SSL/HTTPS

### Option 1 -- Your Own Certificate (Recommended for Production)

```bash
SSL_CERT=/path/to/cert.pem SSL_KEY=/path/to/privkey.pem python app.py
```

### Option 2 -- Quick Self-Signed Certificate (Development/Testing)

```bash
pip install pyopenssl
SSL_ADHOC=1 python app.py
```

### Option 3 -- Generate a Self-Signed Certificate with OpenSSL

```bash
# Install OpenSSL if not already present
# Debian/Ubuntu: sudo apt install openssl
# Fedora/RHEL:   sudo dnf install openssl
# Arch:          sudo pacman -S openssl

# Generate certificate
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"

# Run with the generated certificate
SSL_CERT=cert.pem SSL_KEY=key.pem python app.py
```

When SSL is active, the server listens on `https://localhost:5000` and session cookies are automatically marked `Secure` + `HttpOnly`.

---

## Running as a systemd Service

To keep Usurper running in the background and auto-start on boot:

1. Create a dedicated system user (optional but recommended):

```bash
sudo useradd -r -s /bin/false usurper
sudo chown -R usurper:usurper /opt/UsurperReloaded
```

2. Install Gunicorn into your permanent virtual environment:

```bash
cd /opt/UsurperReloaded/web
source venv/bin/activate
pip install gunicorn
```

3. Create the service file:

```bash
sudo tee /etc/systemd/system/usurper.service > /dev/null << 'EOF'
[Unit]
Description=Usurper ReLoaded Web Game
After=network.target

[Service]
Type=simple
User=usurper
Group=usurper
WorkingDirectory=/opt/UsurperReloaded/web
Environment=PATH=/opt/UsurperReloaded/web/venv/bin:/usr/bin
ExecStart=/opt/UsurperReloaded/web/venv/bin/gunicorn --preload -w 4 -b 0.0.0.0:5000 app:app
Restart=on-failure
RestartSec=5

[Install]
WantedBy=multi-user.target
EOF
```

> **Note**: Adjust `WorkingDirectory` and `ExecStart` paths to match your installation location.

4. Enable and start the service:

```bash
sudo systemctl daemon-reload
sudo systemctl enable usurper
sudo systemctl start usurper
```

5. Check status:

```bash
sudo systemctl status usurper
```

6. View logs:

```bash
sudo journalctl -u usurper -f
```

---

## Production Deployment with Gunicorn

For production use, serve with Gunicorn instead of the built-in Flask development server:

```bash
# Run with Gunicorn (4 workers) from the web directory
cd /path/to/UsurperReloaded/web
source venv/bin/activate
gunicorn --preload -w 4 -b 0.0.0.0:5000 app:app
```

> **Note**: The systemd service example above already uses Gunicorn and the permanent `web/venv` environment.

---

## Reverse Proxy with Nginx

To serve Usurper behind Nginx with SSL termination:

1. Install Nginx:

```bash
# Debian/Ubuntu
sudo apt install -y nginx

# Fedora/RHEL
sudo dnf install -y nginx

# Arch
sudo pacman -S nginx
```

2. Create a site configuration:

```bash
sudo tee /etc/nginx/sites-available/usurper > /dev/null << 'EOF'
server {
    listen 80;
    server_name your-domain.com;
    return 301 https://$server_name$request_uri;
}

server {
    listen 443 ssl;
    server_name your-domain.com;

    ssl_certificate     /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;

    location / {
        proxy_pass http://127.0.0.1:5000;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
EOF
```

3. Enable the site and restart Nginx:

```bash
# Debian/Ubuntu (sites-available/sites-enabled pattern)
sudo ln -s /etc/nginx/sites-available/usurper /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl restart nginx

# Fedora/Arch (drop config in conf.d)
# sudo cp usurper.conf /etc/nginx/conf.d/
# sudo nginx -t
# sudo systemctl restart nginx
```

> **Tip**: Use [Certbot](https://certbot.eff.org/) to obtain free SSL certificates from Let's Encrypt.

---

## Firewall Configuration

### UFW (Debian/Ubuntu)

```bash
sudo ufw allow 5000/tcp    # Direct access
sudo ufw allow 80/tcp      # HTTP (if using Nginx)
sudo ufw allow 443/tcp     # HTTPS (if using Nginx)
```

### firewalld (Fedora/RHEL)

```bash
sudo firewall-cmd --permanent --add-port=5000/tcp
sudo firewall-cmd --reload
```

### iptables

```bash
sudo iptables -A INPUT -p tcp --dport 5000 -j ACCEPT
```

---

## First-Time Setup

1. Open your browser and navigate to `http://<your-server-ip>:5000`
2. Click **Register** and create a new account
3. The **first registered user** automatically becomes the admin
4. Create your character -- choose a name, race, class, and sex
5. Access the **Admin Panel** from the main menu or the "Admin" link in the header
6. Configure game settings via the **Configuration** editor (70+ settings available)

---

## Updating

To update to the latest version:

```bash
cd /opt/UsurperReloaded
git pull origin master

# Reactivate venv and update dependencies
cd web
source venv/bin/activate
pip install -r requirements.txt

# Restart the service
sudo systemctl restart usurper
```

---

## Troubleshooting

### "python3: command not found"

Install Python 3 using your distribution's package manager (see [Detailed Installation](#detailed-installation) above).

### "pip: command not found"

```bash
# Debian/Ubuntu
sudo apt install python3-pip

# Fedora/RHEL
sudo dnf install python3-pip
```

### "No module named venv"

```bash
# Debian/Ubuntu
sudo apt install python3-venv
```

### Python version is below 3.8

Use `pyenv` to install a newer version:

```bash
curl https://pyenv.run | bash
# Follow the instructions to add pyenv to your shell
pyenv install 3.12.0
pyenv global 3.12.0
```

### Port 5000 is already in use

Change the port:

```bash
PORT=8080 python app.py
```

### Permission denied on usurper.db

Ensure the user running the app has write permissions to the `web/` directory:

```bash
chmod 755 /opt/UsurperReloaded/web
chmod 644 /opt/UsurperReloaded/web/usurper.db
```

### NPC actions are not running

The APScheduler background scheduler starts automatically with the app. Check the logs for scheduler errors:

```bash
sudo journalctl -u usurper | grep -i scheduler
```

### Game is slow or unresponsive

- Use Gunicorn instead of the Flask development server (see [Production Deployment](#production-deployment-with-gunicorn))
- Increase the number of Gunicorn workers: `-w 4` (adjust based on CPU cores)
- Place Nginx in front as a reverse proxy for static file serving

### SSL certificate errors in browser

Self-signed certificates will show a browser warning. This is expected -- click "Advanced" and proceed. For production, use Let's Encrypt with Certbot for trusted certificates.
