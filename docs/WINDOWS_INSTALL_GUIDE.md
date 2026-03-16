# Usurper ReLoaded - Windows Install Guide (Web Edition)

A complete guide for installing and running the web version of Usurper ReLoaded on Windows.

---

## Table of Contents

1. [System Requirements](#system-requirements)
2. [Quick Start](#quick-start)
3. [Detailed Installation](#detailed-installation)
   - [Installing Python](#installing-python)
   - [Installing Git (Optional)](#installing-git-optional)
   - [Downloading the Game](#downloading-the-game)
   - [Setting Up a Virtual Environment](#setting-up-a-virtual-environment)
   - [Installing Dependencies](#installing-dependencies)
4. [Running the Game](#running-the-game)
5. [Enabling SSL/HTTPS](#enabling-sslhttps)
6. [Running as a Windows Service](#running-as-a-windows-service)
   - [Using NSSM](#using-nssm)
   - [Using Task Scheduler](#using-task-scheduler)
7. [Production Deployment with Waitress](#production-deployment-with-waitress)
8. [Reverse Proxy with IIS](#reverse-proxy-with-iis)
9. [Windows Firewall Configuration](#windows-firewall-configuration)
10. [First-Time Setup](#first-time-setup)
11. [Updating](#updating)
12. [Troubleshooting](#troubleshooting)

---

## System Requirements

| Component       | Requirement                              |
|-----------------|------------------------------------------|
| **OS**          | Windows 10 or later (Windows 7/8 may work but are unsupported) |
| **Python**      | 3.8 or higher                            |
| **RAM**         | 512 MB minimum, 1 GB recommended         |
| **Disk**        | 200 MB (application + database)          |
| **Network**     | Port 5000 (default) available for web access |

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

If you already have Python 3.8+ installed and on your PATH:

### Command Prompt

```cmd
git clone https://github.com/faustus1005/UsurperReloaded.git
cd UsurperReloaded\web
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python app.py
```

### PowerShell

```powershell
git clone https://github.com/faustus1005/UsurperReloaded.git
cd UsurperReloaded\web
python -m venv venv
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
python app.py
```

The game will be available at `http://localhost:5000`.

---

## Detailed Installation

### Installing Python

1. Download the latest Python 3 installer from [python.org/downloads](https://www.python.org/downloads/).
2. Run the installer.
3. **Important**: Check the box that says **"Add python.exe to PATH"** on the first screen of the installer. This ensures you can run `python` and `pip` from any terminal.
4. Click **"Install Now"** for the default installation, or choose **"Customize installation"** if you want to change the install location.
5. Verify the installation by opening a new Command Prompt or PowerShell window:

```cmd
python --version
```

You should see output like `Python 3.12.x` (any version 3.8 or higher is fine).

> **Note**: On some systems, Python may be available as `py` instead of `python`. You can use `py` in place of `python` throughout this guide. Run `py --version` to check.

### Installing Git (Optional)

Git is recommended for cloning the repository and pulling updates, but you can also download the source as a ZIP file.

1. Download Git for Windows from [git-scm.com/downloads/win](https://git-scm.com/downloads/win).
2. Run the installer with the default options (the defaults are fine for most users).
3. Verify the installation:

```cmd
git --version
```

> **Tip**: Git for Windows includes Git Bash, a Linux-like terminal that some users prefer. It also includes OpenSSL, which is useful for generating SSL certificates.

### Downloading the Game

#### Option A -- Clone with Git (Recommended)

```cmd
git clone https://github.com/faustus1005/UsurperReloaded.git
cd UsurperReloaded
```

#### Option B -- Download as ZIP

1. Go to [github.com/faustus1005/UsurperReloaded](https://github.com/faustus1005/UsurperReloaded).
2. Click the green **"Code"** button, then click **"Download ZIP"**.
3. Extract the ZIP file to a folder of your choice (e.g., `C:\Games\UsurperReloaded`).
4. Open a terminal and navigate to the extracted folder:

```cmd
cd C:\Games\UsurperReloaded
```

### Setting Up a Permanent Virtual Environment

A virtual environment keeps the game's Python dependencies isolated from other Python projects. On Windows, you should create it once in the `web` folder and keep it as the **permanent** runtime for updates, Task Scheduler, and NSSM service commands.

#### Command Prompt

```cmd
cd web
python -m venv venv
venv\Scripts\activate
```

When the virtual environment is active, you will see `(venv)` at the beginning of your prompt.

#### PowerShell

```powershell
cd web
python -m venv venv
.\venv\Scripts\Activate.ps1
```

> **PowerShell Execution Policy**: If you get an error about running scripts being disabled, run this command first and then try again:
> ```powershell
> Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
> ```

To deactivate the virtual environment later, simply type `deactivate`.

> **Important**: Do **not** create a new virtual environment every time you start the game. Keep using `C:\Games\UsurperReloaded\web\venv` (or your chosen install path) so service and startup commands always point to the same Python and installed packages.

### Installing Dependencies

With the virtual environment active (or without one, if you prefer a system-wide install):

```cmd
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

#### Command Prompt

```cmd
cd UsurperReloaded\web
venv\Scripts\activate
python app.py
```

#### PowerShell

```powershell
cd UsurperReloaded\web
.\venv\Scripts\Activate.ps1
python app.py
```

The game starts at `http://localhost:5000`. The SQLite database (`usurper.db`) is automatically created and seeded with monsters, items, NPCs, gods, and default configuration on first run.

### Changing the Port

#### Command Prompt

```cmd
set PORT=8080
python app.py
```

#### PowerShell

```powershell
$env:PORT = "8080"
python app.py
```

### Accessing from Other Devices

By default Flask binds to `0.0.0.0`, making the game accessible from other machines on the network. Access it at `http://<your-ip>:5000` from other devices on the same network (you may need to allow the port through Windows Firewall -- see [Windows Firewall Configuration](#windows-firewall-configuration)).

---

## Enabling SSL/HTTPS

### Option 1 -- Your Own Certificate (Recommended for Production)

#### Command Prompt

```cmd
set SSL_CERT=C:\path\to\cert.pem
set SSL_KEY=C:\path\to\privkey.pem
python app.py
```

#### PowerShell

```powershell
$env:SSL_CERT = "C:\path\to\cert.pem"
$env:SSL_KEY = "C:\path\to\privkey.pem"
python app.py
```

### Option 2 -- Quick Self-Signed Certificate (Development/Testing)

```cmd
pip install pyopenssl
```

#### Command Prompt

```cmd
set SSL_ADHOC=1
python app.py
```

#### PowerShell

```powershell
$env:SSL_ADHOC = "1"
python app.py
```

### Option 3 -- Generate a Self-Signed Certificate with OpenSSL

Git for Windows includes OpenSSL. You can also install it with [Chocolatey](https://chocolatey.org/): `choco install openssl`.

Open **Git Bash** or any terminal with OpenSSL available:

```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
```

Then run with the generated files:

#### Command Prompt

```cmd
set SSL_CERT=cert.pem
set SSL_KEY=key.pem
python app.py
```

#### PowerShell

```powershell
$env:SSL_CERT = "cert.pem"
$env:SSL_KEY = "key.pem"
python app.py
```

When SSL is active, the server listens on `https://localhost:5000` and session cookies are automatically marked `Secure` + `HttpOnly`.

---

## Running as a Windows Service

To keep Usurper running in the background and auto-start on boot, you have two main options on Windows.

### Using NSSM

[NSSM (Non-Sucking Service Manager)](https://nssm.cc/) is a free tool that wraps any executable as a Windows service.

1. Download NSSM from [nssm.cc/download](https://nssm.cc/download) and extract it somewhere on your PATH (e.g., `C:\Tools\nssm.exe`), or install with Chocolatey:

```cmd
choco install nssm
```

2. Install Waitress into your permanent virtual environment:

```cmd
cd C:\Games\UsurperReloaded\web
venv\Scripts\activate
pip install waitress
```

3. Install the service (run as Administrator) and point NSSM to Waitress:

```cmd
nssm install UsurperReloaded "C:\Games\UsurperReloaded\web\venv\Scripts\python.exe" "-m waitress --host=0.0.0.0 --port=5000 --threads=4 app:app"
nssm set UsurperReloaded AppDirectory "C:\Games\UsurperReloaded\web"
nssm set UsurperReloaded DisplayName "Usurper ReLoaded Web Game"
nssm set UsurperReloaded Description "Usurper ReLoaded - Web Edition fantasy RPG game server"
nssm set UsurperReloaded Start SERVICE_AUTO_START
```

> **Note**: Adjust the paths above to match your actual installation location.

4. Optionally set environment variables:

```cmd
nssm set UsurperReloaded AppEnvironmentExtra PORT=5000
```

5. Start the service:

```cmd
nssm start UsurperReloaded
```

6. Manage the service:

```cmd
nssm status UsurperReloaded
nssm stop UsurperReloaded
nssm restart UsurperReloaded
nssm remove UsurperReloaded confirm
```

7. View logs -- configure NSSM to write stdout/stderr to log files:

```cmd
nssm set UsurperReloaded AppStdout "C:\Games\UsurperReloaded\web\logs\service.log"
nssm set UsurperReloaded AppStderr "C:\Games\UsurperReloaded\web\logs\error.log"
nssm set UsurperReloaded AppRotateFiles 1
nssm set UsurperReloaded AppRotateBytes 1048576
```

> **Note**: Create the `logs` directory first: `mkdir C:\Games\UsurperReloaded\web\logs`

### Using Task Scheduler

Windows Task Scheduler can start the game at boot without installing third-party software.

1. Open **Task Scheduler** (search for it in the Start menu).
2. Click **Create Task** (not "Create Basic Task").
3. **General** tab:
   - Name: `Usurper ReLoaded`
   - Check **"Run whether user is logged on or not"**
   - Check **"Run with highest privileges"**
4. **Triggers** tab:
   - Click **New**, choose **"At startup"**, click OK.
5. **Actions** tab:
   - Click **New**
   - Action: **"Start a program"**
   - Program/script: `C:\Games\UsurperReloaded\web\venv\Scripts\python.exe`
   - Add arguments: `-m waitress --host=0.0.0.0 --port=5000 --threads=4 app:app`
   - Start in: `C:\Games\UsurperReloaded\web`
   - Click OK.
6. **Settings** tab:
   - Uncheck **"Stop the task if it runs longer than"**
   - Check **"If the task fails, restart every"** and set to 1 minute, up to 3 times.
   - Click OK.
7. Enter your Windows password when prompted.

The game will now start automatically whenever the computer boots.

---

## Production Deployment with Waitress

For production use on Windows, use [Waitress](https://docs.pylonsproject.org/projects/waitress/) instead of the built-in Flask development server. Waitress is a pure-Python WSGI server that runs natively on Windows (unlike Gunicorn, which is Linux-only).

```cmd
:: Install Waitress inside your virtual environment
venv\Scripts\activate
pip install waitress

:: Run with Waitress (4 threads) from the web directory
cd C:\Games\UsurperReloaded\web
python -m waitress --host=0.0.0.0 --port=5000 --threads=4 app:app
```

PowerShell equivalent:

```powershell
.\venv\Scripts\Activate.ps1
pip install waitress
python -m waitress --host=0.0.0.0 --port=5000 --threads=4 app:app
```

> **Note**: When using Waitress as a Windows service with NSSM, update the program and arguments:
> ```cmd
> nssm set UsurperReloaded Application "C:\Games\UsurperReloaded\web\venv\Scripts\python.exe"
> nssm set UsurperReloaded AppParameters "-m waitress --host=0.0.0.0 --port=5000 --threads=4 app:app"
> ```
>
> If you followed the NSSM steps in this guide, these values are already configured.

---

## Reverse Proxy with IIS

If you want to serve Usurper behind IIS (Internet Information Services) with SSL termination:

### Prerequisites

1. Enable IIS via **Turn Windows features on or off** (search in Start menu):
   - Check **Internet Information Services**
   - Under **World Wide Web Services > Application Development Features**, check **WebSocket Protocol**
2. Install the [URL Rewrite](https://www.iis.net/downloads/microsoft/url-rewrite) module.
3. Install the [Application Request Routing (ARR)](https://www.iis.net/downloads/microsoft/application-request-routing) module.

### Configuration

1. Open **IIS Manager**.
2. Select the server node, open **Application Request Routing Cache**, click **Server Proxy Settings**, and check **Enable proxy**.
3. Create a new website or use the Default Web Site.
4. Open **URL Rewrite** and add an inbound rule:

| Setting             | Value                                    |
|---------------------|------------------------------------------|
| **Match URL**       | Pattern: `(.*)` using Regular Expressions |
| **Action Type**     | Rewrite                                  |
| **Rewrite URL**     | `http://localhost:5000/{R:1}`            |

5. For SSL, bind an SSL certificate to the site in **Site Bindings** and add an HTTPS binding on port 443.

> **Tip**: For simpler setups or home use, you may not need a reverse proxy at all. The built-in Flask server or Waitress can serve the game directly.

---

## Windows Firewall Configuration

If you want other devices on your network to access the game, you need to allow the port through Windows Firewall.

### Using the GUI

1. Open **Windows Defender Firewall with Advanced Security** (search in Start menu).
2. Click **Inbound Rules** in the left panel.
3. Click **New Rule** in the right panel.
4. Select **Port**, click Next.
5. Select **TCP**, enter **5000** (or your custom port), click Next.
6. Select **Allow the connection**, click Next.
7. Check all profiles (Domain, Private, Public) or only the ones you need, click Next.
8. Name the rule **"Usurper ReLoaded"**, click Finish.

### Using the Command Line (Run as Administrator)

#### Command Prompt

```cmd
netsh advfirewall firewall add rule name="Usurper ReLoaded" dir=in action=allow protocol=tcp localport=5000
```

#### PowerShell

```powershell
New-NetFirewallRule -DisplayName "Usurper ReLoaded" -Direction Inbound -Action Allow -Protocol TCP -LocalPort 5000
```

To remove the rule later:

```cmd
netsh advfirewall firewall delete rule name="Usurper ReLoaded"
```

---

## First-Time Setup

1. Open your browser and navigate to `http://localhost:5000`
2. Click **Register** and create a new account
3. The **first registered user** automatically becomes the admin
4. Create your character -- choose a name, race, class, and sex
5. Access the **Admin Panel** from the main menu or the "Admin" link in the header
6. Configure game settings via the **Configuration** editor (70+ settings available)

---

## Updating

To update to the latest version:

### If You Cloned with Git

#### Command Prompt

```cmd
cd C:\Games\UsurperReloaded
git pull origin master

cd web
venv\Scripts\activate
pip install -r requirements.txt
```

#### PowerShell

```powershell
cd C:\Games\UsurperReloaded
git pull origin master

cd web
.\venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Then restart the game (or restart the Windows service if you set one up).

### If You Downloaded as ZIP

1. Download the latest ZIP from GitHub.
2. Extract it to a temporary folder.
3. Copy the new files over your existing installation, **but do not overwrite** `usurper.db` (your game database) or `.secret_key` (your session key).
4. Re-run `pip install -r requirements.txt` to update dependencies.
5. Restart the game.

---

## Troubleshooting

### "python is not recognized as an internal or external command"

Python is not on your PATH. Either:
- Reinstall Python and check **"Add python.exe to PATH"** during installation.
- Or use the full path to Python, e.g., `C:\Users\YourName\AppData\Local\Programs\Python\Python312\python.exe`.
- Or try `py` instead of `python` (the Python Launcher is usually installed separately).

### "pip is not recognized as an internal or external command"

Use `python -m pip` instead of `pip`:

```cmd
python -m pip install -r requirements.txt
```

### PowerShell script execution is disabled

If you see an error like `cannot be loaded because running scripts is disabled`, run:

```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

Then try activating the virtual environment again.

### Python version is below 3.8

Download and install a newer version from [python.org/downloads](https://www.python.org/downloads/). You can have multiple Python versions installed side-by-side on Windows. Use the Python Launcher to select a specific version:

```cmd
py -3.12 -m venv venv
```

### Port 5000 is already in use

Change the port:

#### Command Prompt

```cmd
set PORT=8080
python app.py
```

#### PowerShell

```powershell
$env:PORT = "8080"
python app.py
```

To find what is using port 5000:

```cmd
netstat -ano | findstr :5000
```

Then look up the process ID (last column) with:

```cmd
tasklist /FI "PID eq <pid>"
```

### Permission denied on usurper.db

Ensure the game's `web\` folder is not in a read-only or restricted location (e.g., `C:\Program Files`). Install the game in a user-writable location such as `C:\Games\UsurperReloaded` or your home folder.

### Antivirus blocks the application

Some antivirus software may flag Flask's development server or Python network activity. Add the game folder and Python executable to your antivirus exclusion list if you encounter issues.

### NPC actions are not running

The APScheduler background scheduler starts automatically with the app. If NPCs are not performing actions:
- Check the terminal output for scheduler-related errors.
- Ensure the "Enable NPC Engine" option is turned on in the admin panel Configuration page.
- Verify the NPC action interval setting in Configuration.

### Game is slow or unresponsive

- Use Waitress instead of the Flask development server (see [Production Deployment with Waitress](#production-deployment-with-waitress)).
- Increase the number of Waitress threads: `--threads=8` (adjust based on your CPU).
- Close other applications consuming system resources.

### SSL certificate errors in browser

Self-signed certificates will show a browser warning. This is expected -- click "Advanced" and then "Proceed" (or "Continue to localhost" in some browsers). For production, obtain a trusted certificate from a Certificate Authority or use Let's Encrypt.

### "ModuleNotFoundError: No module named 'flask'"

You are running Python outside the virtual environment. Activate it first:

#### Command Prompt

```cmd
venv\Scripts\activate
```

#### PowerShell

```powershell
.\venv\Scripts\Activate.ps1
```

Then run `python app.py` again.
