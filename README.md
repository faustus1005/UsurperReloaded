# Usurper ReLoaded - Web Edition

A web-based reimplementation of the classic BBS door game **Usurper** by Jakob Dangarden. Fight monsters, battle other players, become king, ascend to godhood, or fall in love and have children -- all from your browser.

## About

Usurper was originally a multi-player BBS door game known for its deep fantasy RPG mechanics, social systems, and chaotic player interactions. This web edition faithfully recreates the game as a modern Flask web application with a dark fantasy theme, while preserving the spirit of the original.

## Features

### Character System
- **10 Races**: Human, Hobbit, Elf, Half-Elf, Dwarf, Troll, Orc, Gnome, Gnoll, Mutant -- each with unique stat bonuses
- **11 Classes**: Alchemist, Assassin, Barbarian, Bard, Cleric, Jester, Magician, Paladin, Ranger, Sage, Warrior
- **7 Core Stats**: Strength, Defence, Stamina, Agility, Charisma, Dexterity, Wisdom
- **30 Levels** of character progression with scaling XP requirements
- **Alignment System**: Chivalry vs Darkness -- your actions shape your path (Good, Neutral, or Evil)

### Combat
- **Dungeon Exploration**: Fight monsters across multiple dungeon levels with daily fight limits
- **24 Monster Types**: From Giant Rats to Ancient Dragons and Demon Princes, each with unique abilities
- **Player vs Player (PvP)**: Challenge other players in the Dormitory
- **Tavern Brawls**: Bar fights for fun and gold
- **Spell System**: 12 spells across attack, heal, buff, and cure types for spellcasting classes
- **Poisonous and diseased enemies** that inflict status effects

### Equipment & Economy
- **15 Equipment Slots**: Weapon, Shield, Head, Body, Arms, Hands, Fingers, Legs, Feet, Waist, Neck, Face, Around Body, plus consumables
- **60+ Items**: Weapons, armor, accessories, potions, and unique dungeon-only treasures
- **Multiple Shops**: Weapon Shop, Armor Shop, Magic Shop, Healing Hut, General Store, Dark Alley (shady dealer), Alchemist
- **Banking System**: Deposit gold for safekeeping with interest
- **Cursed, unique, class-restricted, and alignment-locked items**

### Social Systems
- **Marriage & Romance**: Court other players at the Love Corner, get married, have children
- **Children System**: Pregnancy, childbirth, and family management
- **Teams/Gangs**: Create or join teams, participate in gang wars for town control
- **Inter-player Mail**: Send messages to other players
- **Bounty Board**: Place bounties on your enemies
- **Daily News**: A newspaper tracking all notable events in the realm

### Governance
- **Throne System**: Fight your way to become King/Queen by defeating castle guards
- **Royal Quests**: The monarch can issue quests for other players
- **Tax Collection**: The king collects taxes from the realm
- **Castle Defense**: Set moat guards to protect your throne

### Religion & Godhood
- **Temple System**: Worship deities for blessings and divine favor
- **8 Gods**: Tyr, Freya, Hel, Silvanus, Oghma, Talos, Lathander, Shar -- each with unique domains
- **Ascension**: Players can eventually ascend to godhood themselves

### NPC System
- **Autonomous NPCs**: Computer-controlled characters that live in the world
- **NPC AI Engine**: NPCs explore dungeons, buy equipment, join teams, fight other players, usurp the throne, and even get married
- **Background Scheduler**: NPCs act on a configurable timer interval (default: every 5 minutes)
- **Configurable Behavior**: Control NPC population, combat frequency, and social interactions

### Web Admin Panel (Game Editor)

A comprehensive admin panel inspired by the original Usurper editor, accessible at `/admin` for designated admin users.

#### Admin Features
- **Dashboard**: Overview of game state with player counts, NPC counts, items, monsters, teams, active bounties, and current monarch
- **Game Configuration**: Edit 50+ game settings organized into categories:
  - General settings (game name, town name, dungeon name, NPC names)
  - Combat & daily limits (fights per day, dungeon difficulty, XP loss rates)
  - Throne & governance (level required to usurp, attack rules)
  - NPC behavior (enable/disable, action intervals, social permissions)
  - Economy (bank interest, starting gold, max players)
  - Location names (inn, shops, dungeon)
- **Item Editor**: Create, edit, and delete items with full control over stats, bonuses, shop availability, level ranges, class restrictions, and alignment requirements
- **Monster Editor**: Create, edit, and delete monsters with control over stats, dungeon levels, rewards, special abilities (poison, disease, magic), and aggression
- **Player Editor**: View and modify any player's stats, level, gold, alignment, status effects, and flags (king, imprisoned, god). Separate views for human players and NPCs
- **God Editor**: Create, edit, and delete deities with control over domain, alignment, level, divine power, and active status
- **User Management**: Grant/revoke admin privileges, reset passwords, view account details
- **Quick Actions**: Run daily maintenance for all players, clear news entries

#### Admin Designation
- The **first user** to register automatically receives admin privileges
- Additional admins can be designated by existing admins via the User Management page
- Admin access is protected by a decorator that returns 403 for non-admin users

## Technical Stack

- **Backend**: Python 3 with Flask
- **Database**: SQLite via Flask-SQLAlchemy
- **Authentication**: Flask-Login with password hashing (Werkzeug)
- **Scheduling**: APScheduler for background NPC actions
- **Frontend**: Server-rendered Jinja2 templates with a dark fantasy CSS theme
- **No JavaScript frameworks required** -- pure HTML forms with minimal inline JS for confirmations

## Getting Started

### Requirements
- Python 3.8+
- pip

### Installation

#### Linux / macOS

```bash
cd web
pip install -r requirements.txt
python app.py
```

#### Windows (Command Prompt)

```cmd
cd web
pip install -r requirements.txt
python app.py
```

#### Windows (PowerShell)

```powershell
cd web
pip install -r requirements.txt
python app.py
```

The game will be available at `http://localhost:5000`.

The database is automatically created and seeded with monsters, items, NPCs, gods, and default configuration on first run.

### Proxmox VE (LXC Community Script)

This repository includes a host-side script that creates and provisions an LXC container on a Proxmox VE node:

```bash
scripts/proxmox-community-install.sh
```

Example usage:

```bash
chmod +x scripts/proxmox-community-install.sh
CTID=120 HOSTNAME=usurper \
REPO_URL=https://github.com/<your-org>/UsurperReloaded.git \
PASSWORD='use-a-strong-root-password' \
bash scripts/proxmox-community-install.sh
```

Notes:
- Run it on the **Proxmox host** as root (not inside a container).
- Update `REPO_URL` to your actual Git repository before running.
- Override defaults via environment variables (`CTID`, `MEMORY`, `DISK`, `BRIDGE`, `APP_PORT`, etc.).

### Enabling SSL (HTTPS)

To protect passwords in transit, you can enable SSL in one of two ways:

**Option 1 -- Your own certificate** (recommended for production):

Linux / macOS:
```bash
SSL_CERT=/path/to/cert.pem SSL_KEY=/path/to/privkey.pem python app.py
```

Windows (Command Prompt):
```cmd
set SSL_CERT=C:\path\to\cert.pem
set SSL_KEY=C:\path\to\privkey.pem
python app.py
```

Windows (PowerShell):
```powershell
$env:SSL_CERT = "C:\path\to\cert.pem"
$env:SSL_KEY = "C:\path\to\privkey.pem"
python app.py
```

**Option 2 -- Quick self-signed certificate** (for development/testing):

Linux / macOS:
```bash
pip install pyopenssl
SSL_ADHOC=1 python app.py
```

Windows (Command Prompt):
```cmd
pip install pyopenssl
set SSL_ADHOC=1
python app.py
```

Windows (PowerShell):
```powershell
pip install pyopenssl
$env:SSL_ADHOC = "1"
python app.py
```

**Option 3 -- Generate a self-signed certificate with OpenSSL** (works on all platforms):

If you have OpenSSL installed (comes with Git for Windows, or install via `choco install openssl`):

```bash
openssl req -x509 -newkey rsa:2048 -keyout key.pem -out cert.pem -days 365 -nodes -subj "/CN=localhost"
```

Then run with the generated files:

Linux / macOS:
```bash
SSL_CERT=cert.pem SSL_KEY=key.pem python app.py
```

Windows (Command Prompt):
```cmd
set SSL_CERT=cert.pem
set SSL_KEY=key.pem
python app.py
```

Windows (PowerShell):
```powershell
$env:SSL_CERT = "cert.pem"
$env:SSL_KEY = "key.pem"
python app.py
```

When SSL is active the server listens on `https://localhost:5000` and session cookies are automatically marked `Secure` + `HttpOnly`.

You can also set the `PORT` environment variable to change the listening port (default `5000`).

Windows (Command Prompt): `set PORT=8443` | Windows (PowerShell): `$env:PORT = "8443"` | Linux/macOS: `PORT=8443 python app.py`

### First-Time Setup

1. Navigate to the game in your browser
2. Register a new account -- the first account automatically becomes the admin
3. Create your character (choose name, race, class, and sex)
4. Access the admin panel from the main menu or the "Admin" link in the header
5. Configure game settings to your liking via the Configuration editor

## Project Structure

```
web/
  app.py           - Flask application with all routes
  models.py        - SQLAlchemy database models
  game.py          - Core game logic (combat, leveling, maintenance)
  npc_engine.py    - NPC AI and autonomous behavior
  seed.py          - Database seeding (monsters, items, config, NPCs, gods)
  requirements.txt - Python dependencies
  static/
    css/style.css  - Dark fantasy theme stylesheet
  templates/
    base.html      - Base layout template
    admin/         - Admin panel templates (dashboard, editors, user management)
    *.html         - Game page templates (dungeon, shops, combat, etc.)
SOURCE/
  EDITOR/          - Original Pascal editor source code (reference)
```

## Credits

- **Original Game**: Copyright 2009 Jakob Dangarden
- **Pascal Port**: [Rick Parrish](https://github.com/rickparrish)
- **Bug Fixes**: [Dan Zingaro](https://github.com/dan1982code)
- **Web Edition**: [Faustus1005](https://github.com/faustus1005)

## License

Usurper is free software; you can redistribute it and/or modify it under the terms of the GNU General Public License as published by the Free Software Foundation; either version 2 of the License, or (at your option) any later version.

Usurper is distributed in the hope that it will be useful, but WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the GNU General Public License for more details.
