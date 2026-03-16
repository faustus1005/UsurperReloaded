# Usurper Reloaded - Web Edition

A web-based reimplementation of the classic BBS door game **Usurper** by Jakob Dangarden. Fight monsters, battle other players, become king, ascend to godhood, or fall in love and have children -- all from your browser.

## About

Usurper was originally a multi-player BBS door game created by Jakob Dangarden, known for its deep fantasy RPG mechanics, social systems, and chaotic player interactions. Players explore a vast dungeon, fight monsters and each other, join teams, get married, run for king, and even ascend to godhood. This web edition faithfully recreates the full game as a modern Flask web application with a dark fantasy theme, bringing the classic BBS experience to the browser while preserving the spirit and depth of the original.

## Features

### Character System
- **13 Races**: Human, Hobbit, Elf, Half-Elf, Dwarf, Troll, Orc, Gnome, Gnoll, Mutant, Tiefling, Dragonborn, Fae -- each with unique stat bonuses
- **14 Classes**: Alchemist, Assassin, Barbarian, Bard, Cleric, Jester, Magician, Monk, Necromancer, Paladin, Ranger, Sage, Warrior, Witch Hunter
- **7 Core Stats**: Strength, Defence, Stamina, Agility, Charisma, Dexterity, Wisdom
- **100 Levels** of character progression with scaling XP requirements
- **Alignment System**: Chivalry vs Darkness -- your actions shape your path (Good, Neutral, or Evil)
- **Mental Health & Addiction**: Track mental stability and drug addiction with gameplay consequences

### Combat
- **Dungeon Exploration**: Fight monsters across 100 dungeon levels with daily fight limits
- **50+ Monster Types**: From Giant Rats and Goblins to Ancient Dragons, Demon Princes, and The Usurper -- each with unique abilities, organized across 10 tiers (Beginner through Cosmic)
- **Player vs Player (PvP)**: Challenge other players in the Dormitory
- **Tavern Brawls**: Bar fights for fun and gold
- **Drinking Contests**: Compete against opponents in a drinking competition at Bob's Tavern
- **Spell System**: 99 spells across attack, heal, buff, cure, and freeze types for spellcasting classes (Alchemist, Cleric, Magician, Monk, Necromancer, Paladin, Sage, Witch Hunter)
- **Poisonous and diseased enemies** that inflict status effects

### Dungeon Events
- **20+ Single-Step Events**: Random encounters including wounded strangers, dungeon merchants, magic fountains, trapped chests, ghostly warriors, dragon hoards, enchanted armories, gambling demons, harassed travelers, and more
- **5 Multi-Step Branching Events**: Complex storylines with multiple choices at each step:
  - **The Captive Princess**: Rescue a noblewoman from orc guards through stealth, combat, or distraction -- then choose how to handle the reward
  - **The Necromancer's Laboratory**: Ambush, negotiate, or steal from a dark mage -- fight skeletal warriors, make deals, or claim forbidden knowledge
  - **The Abandoned Dwarven Forge**: Solve rune puzzles, relight an ancient forge, battle a stone golem, and loot a dwarven vault
  - **The Cursed Mirror**: Face your shadow clone, resist dark temptation, or free a trapped wizard's soul from an enchanted mirror
  - **The Underground Arena**: Fight gladiatorial challengers, face an undefeated minotaur champion, bet on fights, or sneak backstage

### Equipment & Economy
- **16 Equipment Slots**: Weapon (Right), Weapon (Left), Shield, Head, Body, Arms, Hands, Legs, Feet, Waist, Neck 1, Neck 2, Face, Around Body, Ring 1, Ring 2
- **100+ Items**: Weapons, armor, accessories, potions, class-specific gear, and unique dungeon-only treasures
- **Multiple Shops**: Weapon Shop, Armor Shop, Magic Shop, Healing Hut, General Store, and specialized shops
- **The Dark Alley**: A hub of illicit commerce including the Shady Dealer, Drug Palace, Steroid Shop, and Alchemist's Heaven
- **Drug Palace**: 10 mind-expanding substances (Incense to Transactor) with XP gains, addiction risk, and 10% overdose chance
- **Steroid Shop**: 10 strength-boosting compounds (Teddy Bears to D.E.M.O.N.) trading mental stability for raw power
- **Alchemist's Heaven**: 9 poisons of increasing potency for the Alchemist class (Snake Bite to Devil's Cure)
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
- **Castle Defense**: Hire moat creatures and royal bodyguards to protect your throne
- **Royal Guard Salaries**: Guards receive daily pay from the treasury -- unpaid guards are automatically dismissed
- **Royal Proclamations**: The monarch can issue proclamations to all subjects

### Player Market
- **Buy & Sell**: Player-to-player item marketplace run by Ugly Joe
- **Pricing**: Sellers set their own prices (up to 1,000,000,000 gold)
- **Private Listings**: Mark items as private (specific buyer) or team-only
- **Auto-Expiration**: Unsold items are automatically removed after a configurable number of days
- **Mail Notifications**: Sellers are notified by mail when their items sell

### Uman Cave
- **Indian Wrestling**: Challenge NPCs in a power-based wrestling mini-game with press, power moves, and rest actions -- 7 NPC opponents from Scrawny Steve to The Dragon
- **Bear Taming**: Tame a wild bear companion in a 7-round mood-based mini-game using fruit or whip strategies -- risk death if the bear gets too angry
- **High & Low Gambling**: Bet gold on whether the next card is high or low (max 15,000 gold per bet)

### Bard Songs
- **Class Feature**: Bards can perform songs with gameplay effects (3 performances per day)
- **6 Songs**: War Song (team attack buff), Lullaby (enemy debuff), Ballad of Healing, Merchant's Tune (shop discounts), Thief's Requiem (theft bonus), Hymn of Warding (defense buff)
- **Audience Scaling**: Song power increases with the number of players present
- **Experience & News**: Earn XP for performances with results posted to the daily news

### Beggars Wall
- **Give Alms**: Donate gold to beggars for chivalry points (up to 5 good deeds per day)
- **Attack Beggars**: Commit dark deeds for darkness points -- 5 attack methods (strangle, bash, wring neck, stab, cut throat)
- **16 Beggar Phrases**: Randomized pleas from the desperate poor

### Bank & Economy
- **Banking System**: Deposit gold for safekeeping with daily interest
- **Bank Guard Duty**: Apply as a bank guard for a daily salary based on level and strength
- **Wage Accrual**: Guard wages accumulate daily and are collected on bank visits

### Religion & Godhood
- **Temple System**: Worship deities for blessings and divine favor
- **8 Gods**: Tyr, Freya, Hel, Silvanus, Oghma, Talos, Lathander, Shar -- each with unique domains
- **Ascension**: Players can eventually ascend to godhood themselves

### NPC System
- **Autonomous NPCs**: Computer-controlled characters that live in the world
- **NPC AI Engine**: NPCs explore dungeons, buy equipment, join teams, fight other players, usurp the throne, and even get married
- **Background Scheduler**: NPCs act on a configurable timer interval (default: every 5 minutes)
- **Configurable Behavior**: Control NPC population, combat frequency, and social interactions

### Location Images
- **Configurable Images**: Every location (town, dungeon, shops, inn, tavern, bank, castle, temple, dark alley, beauty nest, love corner, home, dormitory, bounty board, level master, teams) supports an optional image
- **Easy Setup**: Drop images into `web/static/images/` and set the path in the admin panel under Location Images
- **Responsive Display**: Images scale to fit with a 300px max height, using cover fit with dark border styling

### Scrolling Text Window (Town Crier)
- **Persistent News Ticker**: A fixed panel at the bottom of every game page showing recent news and admin announcements
- **Admin-Configurable Text**: Set custom announcements via the "Scrolling News Text" field in admin configuration
- **Recent News Feed**: Automatically displays the 15 most recent news entries (combat, social, governance events)
- **Collapsible**: Click to collapse/expand; state is remembered across page loads via localStorage

### Web Admin Panel (Game Editor)

A comprehensive admin panel inspired by the original Usurper editor, accessible at `/admin` for designated admin users.

#### Admin Features
- **Dashboard**: Overview of game state with player counts, NPC counts, items, monsters, teams, active bounties, and current monarch
- **Game Configuration**: Edit 70+ game settings organized into categories:
  - General settings (game name, town name, dungeon name, scrolling news text)
  - Combat & daily limits (fights per day, dungeon difficulty, XP loss rates)
  - Throne & governance (level required to usurp, attack rules)
  - NPC behavior (enable/disable, action intervals, social permissions)
  - Economy (bank interest, starting gold, max players)
  - Beauty Nest settings (name, proprietress, visits per day, disease chance, enable/disable)
  - NPC names (all shop owners, trainers, and characters are renameable)
  - Location names (inn, shops, tavern, dark alley, temple, castle, love corner, dungeon)
  - Location images (20 configurable image paths for every game location)
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

For detailed installation instructions, see the platform-specific guides:

- **[Linux / macOS Install Guide](docs/LINUX_INSTALL_GUIDE.md)**
- **[Windows Install Guide](docs/WINDOWS_INSTALL_GUIDE.md)**

The database is automatically created and seeded with monsters, items, NPCs, gods, and default configuration on first run. The first user to register automatically becomes the admin.

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
    images/        - Location and character images (admin-configurable)
      locations/   - Location-specific images (e.g. inn.png, tavern.png)
  templates/
    base.html      - Base layout with scrolling text window (Town Crier)
    macros.html    - Reusable Jinja macros (location_img)
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
