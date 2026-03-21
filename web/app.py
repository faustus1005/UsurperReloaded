"""Usurper ReLoaded - Web Edition

A fantasy RPG game, converted from BBS door game to web application.
Original by Jakob Dangarden, web conversion for modern access.
"""

import os
import ssl
import random
import logging
import time
from logging.handlers import RotatingFileHandler
from functools import wraps
from datetime import datetime, timezone

from flask import (Flask, render_template, redirect, url_for, flash, request,
                   session, jsonify, abort)
from flask_login import (LoginManager, login_user, logout_user, login_required,
                          current_user)
from werkzeug.security import generate_password_hash
from flask_wtf.csrf import CSRFProtect

from models import (
    db, User, Player, Item, InventoryItem, Monster, Mail, NewsEntry,
    GameConfig, Team, TeamMember, KingRecord, Bounty, Relationship,
    Child, RoyalQuest, God, TeamRecord, HomeChestItem,
    MoatCreature, RoyalGuard, DoorGuard, Drink, MarketListing,
    InnChat, BarrelLiftRecord, EquipmentSwapOffer,
    RACES, CLASSES, RACE_BONUSES, CLASS_BONUSES,
    SPELLCASTER_CLASSES, SPELLS, LEVEL_XP, EQUIPMENT_SLOTS, EQUIPMENT_SLOT_LABELS,
    ITEM_TYPES, DRINK_INGREDIENTS,
    CLOSE_COMBAT_MOVES, COMBAT_SKILL_RANKS, HIT_INTENSITY,
    GIGOLOS, POISON_LEVELS, DISEASES, FATAL_DRINK_COMBOS,
    DRINK_STAT_EFFECTS, MONSTER_SPELLS,
    TRAINING_MASTERS, HORSE_TYPES, FAIRY_ENCOUNTERS
)
import game as game_logic
from seed import seed_all
import npc_engine

logger = logging.getLogger(__name__)

# --- Logging configuration ---
_log_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'logs')
os.makedirs(_log_dir, exist_ok=True)

# General access log – every request/response
_access_handler = RotatingFileHandler(
    os.path.join(_log_dir, 'server.log'),
    maxBytes=10 * 1024 * 1024,  # 10 MB
    backupCount=10,
)
_access_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))
_access_handler.setLevel(logging.INFO)

# Security log – auth events (login, register, failures)
_security_handler = RotatingFileHandler(
    os.path.join(_log_dir, 'security.log'),
    maxBytes=10 * 1024 * 1024,
    backupCount=10,
)
_security_handler.setFormatter(logging.Formatter(
    '%(asctime)s %(levelname)s %(message)s', datefmt='%Y-%m-%d %H:%M:%S'
))
_security_handler.setLevel(logging.INFO)

access_logger = logging.getLogger('usurper.access')
access_logger.setLevel(logging.INFO)
access_logger.addHandler(_access_handler)

security_logger = logging.getLogger('usurper.security')
security_logger.setLevel(logging.INFO)
security_logger.addHandler(_security_handler)

# Also send module-level logger output to server.log
logger.addHandler(_access_handler)
logger.setLevel(logging.INFO)

app = Flask(__name__)

def _get_secret_key():
    """Return a stable secret key for session signing.

    Uses the SECRET_KEY environment variable if set.  Otherwise generates a
    random key and persists it to a file next to the database so that every
    Gunicorn worker (and future restarts) shares the same key.
    """
    env_key = os.environ.get('SECRET_KEY')
    if env_key:
        return env_key
    key_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), '.secret_key')
    try:
        with open(key_path, 'r') as f:
            return f.read().strip()
    except FileNotFoundError:
        key = os.urandom(32).hex()
        with open(key_path, 'w') as f:
            f.write(key)
        os.chmod(key_path, 0o600)
        return key

app.config['SECRET_KEY'] = _get_secret_key()
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'usurper.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SSL configuration via environment variables
SSL_CERT = os.environ.get('SSL_CERT')
SSL_KEY = os.environ.get('SSL_KEY')
SSL_ADHOC = os.environ.get('SSL_ADHOC', '').lower() in ('1', 'true', 'yes')

app.config['SESSION_COOKIE_HTTPONLY'] = True
app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'
if SSL_CERT or SSL_ADHOC:
    app.config['SESSION_COOKIE_SECURE'] = True

db.init_app(app)
csrf = CSRFProtect(app)

# Initialize database tables and seed data on first load.
# This ensures tables exist whether the app is run directly (python app.py)
# or via a WSGI server like Gunicorn (gunicorn app:app).
with app.app_context():
    db.create_all()
    # Add finger equipment columns if missing (for existing databases).
    # Wrapped in try/except so concurrent workers don't crash if another
    # worker already added the column between the inspect and the ALTER.
    from sqlalchemy import text as _sa_text
    from sqlalchemy.exc import OperationalError as _SAOpError
    # Add new columns for existing databases
    _new_player_cols = [
        ('equipped_finger1', 'INTEGER REFERENCES items(id)'),
        ('equipped_finger2', 'INTEGER REFERENCES items(id)'),
        ('equipped_weapon2', 'INTEGER REFERENCES items(id)'),
        ('equipped_neck2', 'INTEGER REFERENCES items(id)'),
        ('has_smallpox', 'BOOLEAN DEFAULT 0'),
        ('has_measles', 'BOOLEAN DEFAULT 0'),
        ('has_leprosy', 'BOOLEAN DEFAULT 0'),
        ('is_haunted', 'INTEGER DEFAULT 0'),
        ('dark_deeds_remaining', 'INTEGER DEFAULT 3'),
        ('good_deeds_remaining', 'INTEGER DEFAULT 3'),
        ('gym_sessions', 'INTEGER DEFAULT 4'),
        ('massage_visits', 'INTEGER DEFAULT 3'),
        ('barrel_lift_record', 'INTEGER DEFAULT 0'),
        ('close_combat_skills', 'TEXT DEFAULT "{}"'),
        ('poison_level', 'INTEGER DEFAULT 0'),
        ('prayers_remaining', 'INTEGER DEFAULT 3'),
        # Door guards
        ('door_guard_id', 'INTEGER REFERENCES door_guards(id)'),
        ('door_guard_count', 'INTEGER DEFAULT 0'),
        # Prison escape
        ('prison_days', 'INTEGER DEFAULT 0'),
        ('escape_attempts', 'INTEGER DEFAULT 0'),
        # Player Market
        ('market_listings', 'INTEGER DEFAULT 0'),
        # Wrestling
        ('wrestling_wins', 'INTEGER DEFAULT 0'),
        ('wrestling_losses', 'INTEGER DEFAULT 0'),
        ('wrestling_matches', 'INTEGER DEFAULT 2'),
        # Bear Taming
        ('has_tamed_bear', 'BOOLEAN DEFAULT 0'),
        ('bear_name', 'VARCHAR(30) DEFAULT ""'),
        ('bear_strength', 'INTEGER DEFAULT 0'),
        # Bard performances
        ('performances_remaining', 'INTEGER DEFAULT 3'),
        # Horse/Mount system
        ('has_horse', 'BOOLEAN DEFAULT 0'),
        ('horse_name', 'VARCHAR(30) DEFAULT ""'),
        ('horse_type', 'VARCHAR(30) DEFAULT ""'),
        ('horse_bonus_fights', 'INTEGER DEFAULT 0'),
        # Fairy encounter tracking
        ('fairy_dust', 'INTEGER DEFAULT 0'),
        # God/religion
        ('god_name', 'VARCHAR(30) DEFAULT ""'),
        ('is_god', 'BOOLEAN DEFAULT 0'),
        # Family
        ('is_pregnant', 'BOOLEAN DEFAULT 0'),
        ('pregnancy_days', 'INTEGER DEFAULT 0'),
        ('children_count', 'INTEGER DEFAULT 0'),
    ]
    for _col, _type in _new_player_cols:
        try:
            db.session.execute(_sa_text(
                f'ALTER TABLE players ADD COLUMN {_col} {_type}'
            ))
            db.session.commit()
        except _SAOpError:
            db.session.rollback()
    # Add new monster columns
    for _col, _type in [('mana', 'INTEGER DEFAULT 0'), ('max_mana', 'INTEGER DEFAULT 0'),
                         ('spells_known', 'VARCHAR(30) DEFAULT ""'),
                         ('dungeon_area', 'VARCHAR(20) DEFAULT "dungeon"')]:
        try:
            db.session.execute(_sa_text(
                f'ALTER TABLE monsters ADD COLUMN {_col} {_type}'
            ))
            db.session.commit()
        except _SAOpError:
            db.session.rollback()
    seed_all()
    # Load custom level XP table from admin config if set
    try:
        import json as _json
        _custom_xp = GameConfig.get('level_xp_table')
        if _custom_xp:
            _data = _json.loads(_custom_xp)
            for _k, _v in _data.items():
                LEVEL_XP[int(_k)] = int(_v)
    except Exception:
        pass

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


# --- Request / response logging ---
@app.before_request
def _log_request_start():
    request._start_time = time.time()


@app.after_request
def _log_request(response):
    duration_ms = 0
    start = getattr(request, '_start_time', None)
    if start:
        duration_ms = int((time.time() - start) * 1000)

    user_id = current_user.get_id() if current_user.is_authenticated else '-'
    access_logger.info(
        '%s %s %s %s %dms user=%s',
        request.remote_addr,
        request.method,
        request.path,
        response.status_code,
        duration_ms,
        user_id,
    )
    return response


def safe_int(value, default=0):
    """Safely convert a form value to int, returning default on failure."""
    try:
        return int(value) if value is not None else default
    except (ValueError, TypeError):
        return default


def get_player():
    """Get the current user's player character."""
    if not current_user.is_authenticated:
        return None
    return Player.query.filter_by(user_id=current_user.id).first()


def is_shop_open(shop_key):
    """Check if an establishment is open (not closed by royal decree)."""
    _, king_record = game_logic.get_current_king()
    if not king_record:
        return True  # No king = all shops open
    return getattr(king_record, shop_key, True)


def admin_required(f):
    """Decorator that requires the current user to be an admin."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            security_logger.warning(
                'ADMIN_DENIED ip=%s username=%s user_id=%s path=%s',
                request.remote_addr, current_user.username, current_user.get_id(), request.path,
            )
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


# --- Context processor for templates ---
@app.context_processor
def inject_game_data():
    player = get_player() if current_user.is_authenticated else None
    town_name = GameConfig.get('town_name', 'Dolingen')
    scrolling_text = ''
    recent_scroll_news = []
    if current_user.is_authenticated and player:
        scrolling_text = GameConfig.get('scrolling_text', '')
        recent_scroll_news = NewsEntry.query.order_by(
            NewsEntry.created_at.desc()).limit(15).all()
    return {
        'player': player,
        'town_name': town_name,
        'is_admin': current_user.is_admin if current_user.is_authenticated else False,
        'RACES': RACES,
        'CLASSES': CLASSES,
        'SPELLS': SPELLS,
        'scrolling_text': scrolling_text,
        'recent_scroll_news': recent_scroll_news,
        'get_location_image': lambda key: GameConfig.get(f'image_{key}', ''),
        'config': GameConfig,
    }


# ==================== AUTH ROUTES ====================

@app.route('/')
def index():
    if current_user.is_authenticated:
        player = get_player()
        if player:
            return redirect(url_for('main_menu'))
        return redirect(url_for('create_character'))
    return render_template('index.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')
        confirm = request.form.get('confirm', '')

        if not username or len(username) < 3 or len(username) > 30:
            flash('Username must be 3-30 characters.', 'error')
        elif not password or len(password) < 4:
            flash('Password must be at least 4 characters.', 'error')
        elif password != confirm:
            flash('Passwords do not match.', 'error')
        elif User.query.filter(User.username.ilike(username)).first():
            security_logger.warning('REGISTER_DUPLICATE ip=%s username=%s', request.remote_addr, username)
            flash('Username already taken.', 'error')
        else:
            user = User(username=username.lower())
            user.set_password(password)
            # First user becomes admin automatically
            if User.query.count() == 0 and GameConfig.get('auto_promote_first_admin', 'true').lower() == 'true':
                user.is_admin = True
            db.session.add(user)
            db.session.commit()
            login_user(user)
            security_logger.info('REGISTER_OK ip=%s username=%s user_id=%d', request.remote_addr, user.username, user.id)
            if user.is_admin:
                flash('Account created! You are the first user and have been granted admin privileges.', 'success')
            else:
                flash('Account created! Now create your character.', 'success')
            return redirect(url_for('create_character'))

    return render_template('register.html')


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))

    if request.method == 'POST':
        username = request.form.get('username', '').strip()
        password = request.form.get('password', '')

        user = User.query.filter(User.username.ilike(username)).first()
        if user and user.check_password(password):
            user.last_login = datetime.now(timezone.utc)
            db.session.commit()
            login_user(user)
            security_logger.info('LOGIN_OK ip=%s username=%s user_id=%d', request.remote_addr, user.username, user.id)

            # Run daily maintenance
            player = get_player()
            if player:
                if game_logic.daily_maintenance(player):
                    db.session.commit()
                    flash('A new day dawns. Your daily actions have been refreshed!', 'info')

            return redirect(url_for('index'))
        # Log failed attempt – distinguish unknown user vs wrong password
        if user:
            security_logger.warning('LOGIN_FAIL_PASSWORD ip=%s username=%s user_id=%d', request.remote_addr, username, user.id)
        else:
            security_logger.warning('LOGIN_FAIL_NOUSER ip=%s username=%s', request.remote_addr, username)
        flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    # Clear encounter state so it cannot leak to the next login
    session.pop('combat_monster', None)
    session.pop('combat_log', None)
    session.pop('combat_result', None)
    session.pop('dungeon_event', None)
    session.pop('encounter_player_id', None)
    _user_id = current_user.get_id()
    _username = current_user.username if hasattr(current_user, 'username') else '?'
    logout_user()
    security_logger.info('LOGOUT ip=%s username=%s user_id=%s', request.remote_addr, _username, _user_id)
    flash('You have left the realm.', 'info')
    return redirect(url_for('index'))


# ==================== CHARACTER CREATION ====================

@app.route('/create', methods=['GET', 'POST'])
@login_required
def create_character():
    if get_player():
        return redirect(url_for('main_menu'))

    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        race = request.form.get('race', '')
        player_class = request.form.get('player_class', '')
        try:
            sex = int(request.form.get('sex', 1))
        except (ValueError, TypeError):
            sex = 1

        errors = []
        if not name or len(name) < 2 or len(name) > 30:
            errors.append('Character name must be 2-30 characters.')
        if race not in RACES:
            errors.append('Invalid race.')
        if player_class not in CLASSES:
            errors.append('Invalid class.')
        if sex not in [1, 2]:
            errors.append('Invalid sex selection.')
        if Player.query.filter(Player.name.ilike(name)).first():
            errors.append('That character name is already taken.')

        if errors:
            for e in errors:
                flash(e, 'error')
        else:
            player = Player(user_id=current_user.id)
            game_logic.create_character(player, name, race, player_class, sex)
            db.session.add(player)
            db.session.commit()

            news = NewsEntry(
                player_id=player.id,
                category='social',
                message=f"{name} the {race} {player_class} has entered the realm!"
            )
            db.session.add(news)
            db.session.commit()

            flash(f'Welcome to the realm, {name}!', 'success')
            return redirect(url_for('main_menu'))

    return render_template('create_character.html',
                           race_bonuses=RACE_BONUSES,
                           class_bonuses=CLASS_BONUSES)


# ==================== MAIN GAME ====================

@app.route('/game')
@login_required
def main_menu():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    # Only honour encounter state that belongs to the current player.
    # Stale keys from a previous login (e.g. logout mid-fight, then
    # log in as a different user in the same browser) are discarded.
    _enc_owner = session.get('encounter_player_id')
    if _enc_owner and _enc_owner != player.id:
        session.pop('combat_monster', None)
        session.pop('combat_log', None)
        session.pop('combat_result', None)
        session.pop('dungeon_event', None)
        session.pop('encounter_player_id', None)

    if session.get('combat_monster'):
        flash("You cannot return to town while in combat!", 'error')
        return redirect(url_for('combat'))

    if session.get('dungeon_event'):
        flash("You cannot return to town during an event!", 'error')
        return redirect(url_for('dungeon_event'))

    player.last_played = datetime.now(timezone.utc)
    db.session.commit()

    unread_mail = Mail.query.filter_by(receiver_id=player.id, is_read=False).count()
    recent_news = NewsEntry.query.order_by(NewsEntry.created_at.desc()).limit(5).all()

    return render_template('main_menu.html', unread_mail=unread_mail,
                           recent_news=recent_news)


@app.route('/status')
@login_required
def status():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    equipped = {}
    for slot in EQUIPMENT_SLOTS:
        item_id = getattr(player, f'equipped_{slot}', None)
        if item_id:
            equipped[slot] = db.session.get(Item, item_id)
        else:
            equipped[slot] = None

    xp_next = player.xp_for_next_level()
    return render_template('status.html', equipped=equipped, xp_next=xp_next,
                           LEVEL_XP=LEVEL_XP, EQUIPMENT_SLOTS=EQUIPMENT_SLOTS,
                           EQUIPMENT_SLOT_LABELS=EQUIPMENT_SLOT_LABELS)


# ==================== PLAYER SEARCH API ====================

@app.route('/api/player_search')
@login_required
def player_search():
    """Search for players/NPCs by name prefix. Min 3 chars required.

    Returns JSON list of matching players for autocomplete fields.
    """
    q = request.args.get('q', '').strip()
    if len(q) < 3:
        return jsonify([])

    matches = Player.query.filter(
        Player.name.ilike(f'%{q}%')
    ).order_by(Player.name).limit(15).all()

    results = []
    for p in matches:
        results.append({
            'id': p.id,
            'name': p.name,
            'level': p.level,
            'race': p.race,
            'player_class': p.player_class,
            'is_npc': p.is_npc,
            'sex': 'M' if p.sex == 1 else 'F',
        })
    return jsonify(results)


# ==================== DUNGEON ====================

@app.route('/dungeon')
@login_required
def dungeon():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if player.is_imprisoned:
        flash("You cannot enter the dungeon while imprisoned.", 'error')
        return redirect(url_for('main_menu'))

    if player.hp <= 0:
        flash("You are too wounded to enter the dungeon. Rest at the inn first.", 'error')
        return redirect(url_for('main_menu'))

    dungeon_name = GameConfig.get('dungeon_name', 'The Dungeon Complex')
    min_level = max(1, player.level - 5)
    max_level = min(100, player.level + 5)
    # Validate dungeon level is within allowed range for current player level
    if not player.dungeon_level or player.dungeon_level < min_level or player.dungeon_level > max_level:
        player.dungeon_level = max(min_level, min(player.level, max_level))
        db.session.commit()
    return render_template('dungeon.html', dungeon_name=dungeon_name,
                           min_dungeon_level=min_level, max_dungeon_level=max_level)


@app.route('/dungeon/explore', methods=['POST'])
@login_required
def dungeon_explore():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if player.is_imprisoned:
        flash("You cannot enter the dungeon while imprisoned.", 'error')
        return redirect(url_for('main_menu'))

    if player.fights_remaining <= 0:
        flash("You have no dungeon fights remaining today.", 'warning')
        return redirect(url_for('dungeon'))

    if player.hp <= 0:
        flash("You are too wounded to fight.", 'error')
        return redirect(url_for('main_menu'))

    dungeon_level = player.dungeon_level if player.dungeon_level else min(player.level, 100)

    # 8% chance of fairy encounter (LORD-inspired)
    if random.randint(1, 100) <= 8:
        result = game_logic.fairy_encounter(player, dungeon_level)
        db.session.commit()
        session['fairy_encounter'] = result
        return redirect(url_for('fairy_encounter_page'))

    # 30% chance of non-combat event
    if random.randint(1, 100) <= 30:
        # 50% chance of new interactive event vs old simple event
        if random.randint(1, 2) == 1:
            event = game_logic.get_random_dungeon_event()
            session['dungeon_event'] = event
            session['encounter_player_id'] = player.id
            return redirect(url_for('dungeon_event'))
        else:
            event = game_logic.dungeon_event(player, dungeon_level)
            db.session.commit()
            flash(event['message'], 'info')
            return redirect(url_for('dungeon'))

    # Combat encounter
    monster = game_logic.get_dungeon_monster(dungeon_level)
    if not monster:
        flash("The dungeon is eerily empty...", 'info')
        return redirect(url_for('dungeon'))

    player.fights_remaining -= 1
    session['combat_monster'] = monster
    session['combat_log'] = [
        f"You encounter a {monster['name']}!",
        f'"{monster["phrase"]}"' if monster['phrase'] else '',
    ]
    session['encounter_player_id'] = player.id
    db.session.commit()

    return redirect(url_for('combat'))


@app.route('/combat')
@login_required
def combat():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    monster = session.get('combat_monster')
    if not monster:
        return redirect(url_for('dungeon'))

    combat_log = session.get('combat_log', [])

    known_spells = []
    for sid in player.get_known_spells():
        spell = SPELLS.get(sid)
        if spell:
            known_spells.append({'id': sid, **spell})

    return render_template('combat.html', monster=monster, combat_log=combat_log,
                           known_spells=known_spells)


@app.route('/combat/attack', methods=['POST'])
@login_required
def combat_attack():
    player = get_player()
    monster = session.get('combat_monster')
    if not player or not monster:
        return redirect(url_for('dungeon'))

    log = session.get('combat_log', [])
    messages, result = game_logic.combat_round(player, monster)
    log.extend(messages)

    if result == 'victory':
        reward_msgs = game_logic.process_victory(player, monster)
        log.extend(reward_msgs)
        session.pop('combat_monster', None)
        session['combat_log'] = log
        session['combat_result'] = 'victory'
        db.session.commit()
        return redirect(url_for('combat_result'))

    elif result == 'defeat':
        defeat_msgs = game_logic.process_defeat(player, monster)
        log.extend(defeat_msgs)
        session.pop('combat_monster', None)
        session['combat_log'] = log
        session['combat_result'] = 'defeat'
        db.session.commit()
        return redirect(url_for('combat_result'))

    session['combat_monster'] = monster
    session['combat_log'] = log
    db.session.commit()
    return redirect(url_for('combat'))


@app.route('/combat/spell', methods=['POST'])
@login_required
def combat_spell():
    player = get_player()
    monster = session.get('combat_monster')
    if not player or not monster:
        return redirect(url_for('dungeon'))

    try:
        spell_id = int(request.form.get('spell_id', 0))
    except (ValueError, TypeError):
        flash("Invalid spell.", 'error')
        return redirect(url_for('combat'))
    log = session.get('combat_log', [])

    success, message, damage = game_logic.cast_spell(player, spell_id, monster)
    log.append(message)

    if success and damage > 0:
        monster['hp'] -= damage
        log.append(f"The spell deals {damage} damage to the {monster['name']}!")

        if monster['hp'] <= 0:
            log.append(f"You have slain the {monster['name']} with magic!")
            reward_msgs = game_logic.process_victory(player, monster)
            log.extend(reward_msgs)
            session.pop('combat_monster', None)
            session['combat_log'] = log
            session['combat_result'] = 'victory'
            db.session.commit()
            return redirect(url_for('combat_result'))

    if success:
        # Monster counter-attacks
        monster_attack = game_logic.calculate_attack(
            monster['strength'], monster['weapon_power'], 0)
        player_def = game_logic.calculate_defense(player.defence, player.armor_power)
        monster_damage = max(1, monster_attack - player_def)
        player.hp -= monster_damage
        log.append(f"The {monster['name']} attacks you for {monster_damage} damage.")

        if player.hp <= 0:
            player.hp = 0
            defeat_msgs = game_logic.process_defeat(player, monster)
            log.extend(defeat_msgs)
            session.pop('combat_monster', None)
            session['combat_log'] = log
            session['combat_result'] = 'defeat'
            db.session.commit()
            return redirect(url_for('combat_result'))

    session['combat_monster'] = monster
    session['combat_log'] = log
    db.session.commit()
    return redirect(url_for('combat'))


@app.route('/combat/heal', methods=['POST'])
@login_required
def combat_heal():
    player = get_player()
    monster = session.get('combat_monster')
    if not player or not monster:
        return redirect(url_for('dungeon'))

    log = session.get('combat_log', [])
    success, msg = game_logic.use_healing_potion(player)
    log.append(msg)

    if success:
        # Monster still attacks
        monster_attack = game_logic.calculate_attack(
            monster['strength'], monster['weapon_power'], 0)
        player_def = game_logic.calculate_defense(player.defence, player.armor_power)
        monster_damage = max(1, monster_attack - player_def)
        player.hp -= monster_damage
        log.append(f"The {monster['name']} attacks you for {monster_damage} damage.")

        if player.hp <= 0:
            player.hp = 0
            defeat_msgs = game_logic.process_defeat(player, monster)
            log.extend(defeat_msgs)
            session.pop('combat_monster', None)
            session['combat_log'] = log
            session['combat_result'] = 'defeat'
            db.session.commit()
            return redirect(url_for('combat_result'))

    session['combat_log'] = log
    db.session.commit()
    return redirect(url_for('combat'))


@app.route('/combat/flee', methods=['POST'])
@login_required
def combat_flee():
    player = get_player()
    monster = session.get('combat_monster')
    if not player or not monster:
        return redirect(url_for('dungeon'))

    flee_chance = 40 + player.agility - monster.get('aggression', 1) * 10
    if random.randint(1, 100) <= flee_chance:
        session.pop('combat_monster', None)
        session.pop('combat_log', None)
        flash("You flee from combat!", 'warning')
        db.session.commit()
        return redirect(url_for('dungeon'))
    else:
        log = session.get('combat_log', [])
        log.append("You failed to escape!")

        # Monster gets a free hit
        monster_attack = game_logic.calculate_attack(
            monster['strength'], monster['weapon_power'], 0)
        player_def = game_logic.calculate_defense(player.defence, player.armor_power)
        monster_damage = max(1, monster_attack - player_def)
        player.hp -= monster_damage
        log.append(f"The {monster['name']} strikes you as you try to flee for {monster_damage} damage!")

        if player.hp <= 0:
            player.hp = 0
            defeat_msgs = game_logic.process_defeat(player, monster)
            log.extend(defeat_msgs)
            session.pop('combat_monster', None)
            session['combat_log'] = log
            session['combat_result'] = 'defeat'
            db.session.commit()
            return redirect(url_for('combat_result'))

        session['combat_log'] = log
        db.session.commit()
        return redirect(url_for('combat'))


@app.route('/combat/result')
@login_required
def combat_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    combat_log = session.get('combat_log', [])
    result = session.get('combat_result', 'unknown')
    session.pop('combat_log', None)
    session.pop('combat_result', None)

    return render_template('combat_result.html', combat_log=combat_log, result=result)


# ==================== FAIRY ENCOUNTERS (LORD-inspired) ====================

@app.route('/fairy')
@login_required
def fairy_encounter_page():
    """Display the result of a fairy encounter."""
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    result = session.pop('fairy_encounter', None)
    if not result:
        return redirect(url_for('dungeon'))

    return render_template('fairy_encounter.html', result=result)


# ==================== TOWN LOCATIONS ====================

@app.route('/inn')
@login_required
def inn():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if not is_shop_open('shop_inn'):
        flash("The Inn has been closed by royal decree!", 'error')
        return redirect(url_for('main_menu'))

    inn_name = GameConfig.get('inn_name', "The Dragon's Flagon")
    rest_cost = player.level * 5 + 10
    door_guards = DoorGuard.query.all()
    current_guard = db.session.get(DoorGuard, player.door_guard_id) if player.door_guard_id else None
    return render_template('inn.html', inn_name=inn_name, rest_cost=rest_cost,
                           door_guards=door_guards, current_guard=current_guard)


@app.route('/inn/rest', methods=['POST'])
@login_required
def inn_rest():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.heal_at_inn(player)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('inn'))


@app.route('/inn/hire_guard', methods=['POST'])
@login_required
def inn_hire_guard():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    try:
        guard_id = int(request.form.get('guard_id', 0))
        count = int(request.form.get('count', 1))
    except ValueError:
        flash("Invalid input.", 'error')
        return redirect(url_for('inn'))

    success, msg = game_logic.hire_door_guard(player, guard_id, count)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('inn'))


@app.route('/inn/dismiss_guards', methods=['POST'])
@login_required
def inn_dismiss_guards():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.dismiss_door_guards(player)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('inn'))


@app.route('/bank')
@login_required
def bank():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    # Collect accumulated bank wages on visit
    wages_collected = game_logic.collect_bank_wages(player)
    if wages_collected > 0:
        db.session.commit()
        flash(f"You collected {wages_collected} gold in bank guard salary!", 'success')

    bank_salary = (player.level * 1500) + (player.strength * 9) if player.is_bank_guard else 0
    return render_template('bank.html', bank_salary=bank_salary)


@app.route('/bank/deposit', methods=['POST'])
@login_required
def bank_deposit():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    try:
        amount = int(request.form.get('amount', 0))
    except ValueError:
        flash('Invalid amount.', 'error')
        return redirect(url_for('bank'))

    success, msg = game_logic.bank_deposit(player, amount)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('bank'))


@app.route('/bank/withdraw', methods=['POST'])
@login_required
def bank_withdraw():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    try:
        amount = int(request.form.get('amount', 0))
    except ValueError:
        flash('Invalid amount.', 'error')
        return redirect(url_for('bank'))

    success, msg = game_logic.bank_withdraw(player, amount)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('bank'))


@app.route('/bank/apply_guard', methods=['POST'])
@login_required
def bank_guard_apply():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.bank_guard_apply(player)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('bank'))


@app.route('/bank/resign_guard', methods=['POST'])
@login_required
def bank_guard_resign():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.bank_guard_resign(player)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('bank'))


# ==================== SHOPS ====================

@app.route('/shop/weapons')
@login_required
def weapon_shop():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if not is_shop_open('shop_weapons'):
        flash("The Weapon Shop has been closed by royal decree!", 'error')
        return redirect(url_for('main_menu'))

    items = Item.query.filter_by(in_shop=True, item_type='Weapon').order_by(Item.value).all()
    shop_name = GameConfig.get('weapon_shop_name', 'Weapon Shop')
    return render_template('shop.html', items=items, shop_name=shop_name,
                           shop_type='weapons', shop_image_key='weapon_shop')


@app.route('/shop/armor')
@login_required
def armor_shop():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if not is_shop_open('shop_armor'):
        flash("The Armor Shop has been closed by royal decree!", 'error')
        return redirect(url_for('main_menu'))

    armor_types = ['Body', 'Shield', 'Head', 'Arms', 'Hands', 'Legs', 'Feet',
                   'Waist', 'Neck', 'Face', 'Around Body', 'Fingers']
    items = Item.query.filter(
        Item.in_shop == True,
        Item.item_type.in_(armor_types)
    ).order_by(Item.item_type, Item.value).all()
    shop_name = GameConfig.get('armor_shop_name', 'Armor Shop')
    return render_template('shop.html', items=items, shop_name=shop_name,
                           shop_type='armor', shop_image_key='armor_shop')


@app.route('/shop/magic')
@login_required
def magic_shop():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if not is_shop_open('shop_magic'):
        flash("The Magic Shop has been closed by royal decree!", 'error')
        return redirect(url_for('main_menu'))

    # Show items that give mana/wisdom bonuses
    items = Item.query.filter(
        Item.in_shop == True,
        (Item.mana_bonus > 0) | (Item.wisdom_bonus > 0)
    ).order_by(Item.value).all()

    # Spells available to learn
    available_spells = {}
    if player.player_class in SPELLCASTER_CLASSES:
        for sid, spell in SPELLS.items():
            if (player.player_class in spell['classes'] and
                player.level >= spell['min_level'] and
                not player.knows_spell(sid)):
                available_spells[sid] = spell

    shop_name = GameConfig.get('magic_shop_name', 'The Arcane Emporium')
    return render_template('magic_shop.html', items=items, shop_name=shop_name,
                           available_spells=available_spells)


@app.route('/shop/buy/<int:item_id>', methods=['POST'])
@login_required
def buy_item(item_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.buy_item(player, item_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')

    # Redirect back to appropriate shop
    item = db.session.get(Item, item_id)
    if item:
        if item.shop_category == 'healing':
            return redirect(url_for('healing_shop'))
        elif item.shop_category == 'general':
            return redirect(url_for('general_store'))
        elif item.shop_category == 'shady':
            return redirect(url_for('shady_dealer'))
        elif item.shop_category == 'alchemist':
            return redirect(url_for('alchemist_shop'))
        elif item.item_type == 'Weapon':
            return redirect(url_for('weapon_shop'))
    return redirect(url_for('armor_shop'))


@app.route('/shop/learn_spell/<int:spell_id>', methods=['POST'])
@login_required
def learn_spell(spell_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    spell = SPELLS.get(spell_id)
    if not spell:
        flash('Unknown spell.', 'error')
        return redirect(url_for('magic_shop'))

    if player.player_class not in spell['classes']:
        flash('Your class cannot learn this spell.', 'error')
        return redirect(url_for('magic_shop'))

    if player.level < spell['min_level']:
        flash(f'You need to be level {spell["min_level"]} to learn this spell.', 'error')
        return redirect(url_for('magic_shop'))

    if player.knows_spell(spell_id):
        flash('You already know this spell.', 'info')
        return redirect(url_for('magic_shop'))

    cost = spell['mana_cost'] * 10
    if player.gold < cost:
        flash(f'Learning this spell costs {cost} gold.', 'error')
        return redirect(url_for('magic_shop'))

    player.gold -= cost
    player.learn_spell(spell_id)
    db.session.commit()
    flash(f'You have learned {spell["name"]}!', 'success')
    return redirect(url_for('magic_shop'))


# ==================== INVENTORY & EQUIPMENT ====================

@app.route('/inventory')
@login_required
def inventory():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    inv_items = InventoryItem.query.filter_by(player_id=player.id).all()
    equipped = {}
    for slot in EQUIPMENT_SLOTS:
        item_id = getattr(player, f'equipped_{slot}', None)
        if item_id:
            equipped[slot] = db.session.get(Item, item_id)
        else:
            equipped[slot] = None

    return render_template('inventory.html', inv_items=inv_items, equipped=equipped,
                           EQUIPMENT_SLOTS=EQUIPMENT_SLOTS,
                           EQUIPMENT_SLOT_LABELS=EQUIPMENT_SLOT_LABELS)


@app.route('/inventory/equip/<int:inv_item_id>', methods=['POST'])
@login_required
def equip_item(inv_item_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.equip_item(player, inv_item_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('inventory'))


@app.route('/inventory/unequip/<slot>', methods=['POST'])
@login_required
def unequip_item(slot):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if slot not in EQUIPMENT_SLOTS:
        flash('Invalid equipment slot.', 'error')
        return redirect(url_for('inventory'))

    success, msg = game_logic.unequip_item(player, slot)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('inventory'))


@app.route('/inventory/sell/<int:inv_item_id>', methods=['POST'])
@login_required
def sell_item(inv_item_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.sell_item(player, inv_item_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('inventory'))


# ==================== LEVEL MASTER (with Training Master Combat Gate) ====================

@app.route('/level_master')
@login_required
def level_master():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    can_level = player.can_level_up()
    xp_needed = player.xp_for_next_level()
    master = game_logic.get_training_master(player.level)
    master_combat = session.get('master_combat')

    return render_template('level_master.html', master=master,
                           can_level=can_level, xp_needed=xp_needed,
                           master_combat=master_combat)


@app.route('/level_master/challenge', methods=['POST'])
@login_required
def challenge_master():
    """Initiate combat with the training master to level up."""
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if not player.can_level_up():
        flash("You don't have enough experience to challenge a master.", 'warning')
        return redirect(url_for('level_master'))

    if player.hp <= 0:
        flash("You are too wounded to fight.", 'error')
        return redirect(url_for('level_master'))

    master = game_logic.get_training_master(player.level)
    master_state = game_logic.generate_master_stats(master, player)

    session['master_combat'] = master_state
    session['master_combat_log'] = [
        f"{master_state['name']} steps forward: \"{master_state['phrase']}\"",
        "The training fight begins!"
    ]
    db.session.commit()
    return redirect(url_for('master_fight'))


@app.route('/level_master/fight')
@login_required
def master_fight():
    """Display the master combat screen."""
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    master_state = session.get('master_combat')
    if not master_state:
        return redirect(url_for('level_master'))

    combat_log = session.get('master_combat_log', [])
    return render_template('master_fight.html', master=master_state,
                           combat_log=combat_log)


@app.route('/level_master/fight/action', methods=['POST'])
@login_required
def master_fight_action():
    """Process a combat action against the training master."""
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    master_state = session.get('master_combat')
    if not master_state:
        return redirect(url_for('level_master'))

    action = request.form.get('action', 'attack')
    if action not in ('attack', 'power_attack', 'defend'):
        action = 'attack'

    messages, master_defeated, player_defeated, master_state = \
        game_logic.master_combat_round(player, master_state, action)

    combat_log = session.get('master_combat_log', [])
    combat_log.extend(messages)

    if master_defeated:
        # Level up!
        success, level_msg = game_logic.level_up(player)
        if success:
            combat_log.append(level_msg)
            news = NewsEntry(
                player_id=player.id,
                category='social',
                message=f"{player.name} defeated {master_state['name']} and advanced to level {player.level}!"
            )
            db.session.add(news)
        session.pop('master_combat', None)
        session['master_combat_log'] = combat_log
        db.session.commit()
        flash(f"Victory! {level_msg}", 'success')
        return redirect(url_for('level_master'))

    if player_defeated:
        # Player lost - heal to 1 HP (training, not lethal)
        player.hp = max(1, player.max_hp // 10)
        session.pop('master_combat', None)
        session['master_combat_log'] = combat_log
        db.session.commit()
        flash(f"{master_state['name']} defeated you. Rest and try again!", 'warning')
        return redirect(url_for('level_master'))

    session['master_combat'] = master_state
    session['master_combat_log'] = combat_log
    db.session.commit()
    return redirect(url_for('master_fight'))


@app.route('/level_master/train', methods=['POST'])
@login_required
def train_level():
    """Legacy train route - now redirects to challenge."""
    return redirect(url_for('challenge_master'))


# ==================== HORSE STABLES (LORD-inspired) ====================

@app.route('/stables')
@login_required
def stables():
    """View the horse stables."""
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    available_horses = game_logic.get_available_horses(player)
    return render_template('stables.html', horses=available_horses)


@app.route('/stables/buy/<int:index>', methods=['POST'])
@login_required
def buy_horse(index):
    """Buy a horse from the stables."""
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.buy_horse(player, index)
    if success:
        news = NewsEntry(
            player_id=player.id,
            category='social',
            message=f"{player.name} purchased a {player.horse_name} from the stables!"
        )
        db.session.add(news)
    db.session.commit()
    flash(msg, 'success' if success else 'warning')
    return redirect(url_for('stables'))


@app.route('/stables/release', methods=['POST'])
@login_required
def release_horse():
    """Release the player's horse."""
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.release_horse(player)
    db.session.commit()
    flash(msg, 'success' if success else 'warning')
    return redirect(url_for('stables'))


# ==================== SOCIAL ====================

@app.route('/rankings')
@login_required
def rankings():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    players = game_logic.get_leaderboard()
    return render_template('rankings.html', players=players)


@app.route('/news')
@login_required
def news():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    page = request.args.get('page', 1, type=int)
    per_page = 20
    news_query = NewsEntry.query.order_by(NewsEntry.created_at.desc())
    total = news_query.count()
    entries = news_query.offset((page - 1) * per_page).limit(per_page).all()
    has_next = (page * per_page) < total
    has_prev = page > 1

    return render_template('news.html', entries=entries, page=page,
                           has_next=has_next, has_prev=has_prev)


@app.route('/mail')
@login_required
def mail_inbox():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    received = Mail.query.filter_by(receiver_id=player.id).order_by(
        Mail.created_at.desc()).limit(50).all()
    sent = Mail.query.filter_by(sender_id=player.id).order_by(
        Mail.created_at.desc()).limit(20).all()

    return render_template('mail.html', received=received, sent=sent)


@app.route('/mail/read/<int:mail_id>')
@login_required
def read_mail(mail_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    m = db.session.get(Mail, mail_id)
    if not m or m.receiver_id != player.id:
        flash('Mail not found.', 'error')
        return redirect(url_for('mail_inbox'))

    m.is_read = True
    db.session.commit()
    return render_template('read_mail.html', mail=m)


@app.route('/mail/send', methods=['POST'])
@login_required
def send_mail():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    receiver_name = request.form.get('receiver', '').strip()
    subject = request.form.get('subject', '').strip()
    message = request.form.get('message', '').strip()

    if not receiver_name or not message:
        flash('Recipient and message are required.', 'error')
        return redirect(url_for('mail_inbox'))

    success, msg = game_logic.send_mail(player, receiver_name, subject, message)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('mail_inbox'))


@app.route('/players')
@login_required
def player_list():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    players = Player.query.order_by(Player.level.desc()).all()
    return render_template('player_list.html', players=players)


# ==================== TEAMS ====================

@app.route('/teams')
@login_required
def teams():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    all_teams = game_logic.get_team_rankings()
    my_membership = TeamMember.query.filter_by(player_id=player.id).first()
    my_team = my_membership.team if my_membership else None

    return render_template('teams.html', teams=all_teams, my_team=my_team)


@app.route('/teams/create', methods=['POST'])
@login_required
def create_team():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    team_name = request.form.get('team_name', '').strip()
    success, msg = game_logic.create_team(player, team_name)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('teams'))


@app.route('/teams/join/<int:team_id>', methods=['POST'])
@login_required
def join_team(team_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.join_team(player, team_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('teams'))


@app.route('/teams/leave', methods=['POST'])
@login_required
def leave_team():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.leave_team(player)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('teams'))


# ==================== CASTLE / KING ====================

@app.route('/castle')
@login_required
def castle():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    king, king_record = game_logic.get_current_king()
    history = KingRecord.query.filter_by(is_current=False).order_by(
        KingRecord.dethroned_at.desc()).limit(10).all()
    prisoners = Player.query.filter_by(is_imprisoned=True).all() if (king and king.id == player.id) else []
    moat_creatures = MoatCreature.query.all()
    royal_guards = []
    hirable_players = []
    tax_relieved = []
    if king and king.id == player.id and king_record:
        royal_guards = RoyalGuard.query.filter_by(king_record_id=king_record.id).all()
        # Players available to hire as guards (not king, not already guards, not imprisoned)
        guard_ids = [g.player_id for g in royal_guards]
        hirable_players = Player.query.filter(
            Player.id != player.id,
            Player.is_imprisoned == False,
            ~Player.id.in_(guard_ids) if guard_ids else True
        ).order_by(Player.level.desc()).limit(20).all()
        tax_relieved = Player.query.filter_by(tax_relief=True).all()

    castle_name = GameConfig.get('castle_name', 'The Royal Castle')
    return render_template('castle.html', king=king, king_record=king_record,
                           history=history, prisoners=prisoners,
                           castle_name=castle_name, moat_creatures=moat_creatures,
                           royal_guards=royal_guards, hirable_players=hirable_players,
                           tax_relieved=tax_relieved)


@app.route('/castle/challenge', methods=['POST'])
@login_required
def challenge_king():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg, combat_log = game_logic.challenge_king(player)
    db.session.commit()

    if combat_log:
        session['throne_log'] = combat_log
        session['throne_result'] = 'victory' if success else 'defeat'
        return redirect(url_for('throne_result'))

    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/throne_result')
@login_required
def throne_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    combat_log = session.pop('throne_log', [])
    result = session.pop('throne_result', 'unknown')
    return render_template('throne_result.html', combat_log=combat_log, result=result)


@app.route('/castle/abdicate', methods=['POST'])
@login_required
def abdicate():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.abdicate(player)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/hire_moat_creatures', methods=['POST'])
@login_required
def hire_moat_creatures():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    king_record = KingRecord.query.filter_by(player_id=player.id, is_current=True).first()
    if not king_record:
        flash("No active reign found.", 'error')
        return redirect(url_for('castle'))

    try:
        creature_id = int(request.form.get('creature_id', 0))
        count = int(request.form.get('count', 1))
    except ValueError:
        flash("Invalid input.", 'error')
        return redirect(url_for('castle'))

    funding = request.form.get('funding', 'treasury')
    success, msg = game_logic.king_hire_moat_creatures(king_record, creature_id, count, funding)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/remove_moat_creatures', methods=['POST'])
@login_required
def remove_moat_creatures():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    king_record = KingRecord.query.filter_by(player_id=player.id, is_current=True).first()
    if not king_record:
        return redirect(url_for('castle'))

    try:
        count = int(request.form.get('count', 1))
    except ValueError:
        count = 1

    success, msg = game_logic.king_remove_moat_creatures(king_record, count)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/hire_guard', methods=['POST'])
@login_required
def hire_royal_guard():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    king_record = KingRecord.query.filter_by(player_id=player.id, is_current=True).first()
    if not king_record:
        return redirect(url_for('castle'))

    try:
        target_id = int(request.form.get('target_id', 0))
        salary = int(request.form.get('salary', 0))
    except ValueError:
        flash("Invalid input.", 'error')
        return redirect(url_for('castle'))

    success, msg = game_logic.king_hire_royal_guard(king_record, target_id, salary)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/sack_guard', methods=['POST'])
@login_required
def sack_royal_guard():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    king_record = KingRecord.query.filter_by(player_id=player.id, is_current=True).first()
    if not king_record:
        return redirect(url_for('castle'))

    try:
        guard_id = int(request.form.get('guard_id', 0))
    except ValueError:
        flash("Invalid input.", 'error')
        return redirect(url_for('castle'))

    success, msg = game_logic.king_sack_guard(king_record, guard_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/set_tax', methods=['POST'])
@login_required
def set_tax():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    king_record = KingRecord.query.filter_by(player_id=player.id, is_current=True).first()
    if not king_record:
        return redirect(url_for('castle'))

    try:
        rate = int(request.form.get('rate', 5))
        alignment = int(request.form.get('alignment', 0))
    except ValueError:
        flash("Invalid input.", 'error')
        return redirect(url_for('castle'))

    success, msg = game_logic.king_set_tax(king_record, rate, alignment)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/grant_tax_relief', methods=['POST'])
@login_required
def grant_tax_relief():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    target_name = request.form.get('target', '').strip()
    success, msg = game_logic.king_grant_tax_relief(player, target_name)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/revoke_tax_relief', methods=['POST'])
@login_required
def revoke_tax_relief():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    target_name = request.form.get('target', '').strip()
    success, msg = game_logic.king_revoke_tax_relief(player, target_name)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/withdraw', methods=['POST'])
@login_required
def castle_withdraw():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    king_record = KingRecord.query.filter_by(player_id=player.id, is_current=True).first()
    if not king_record:
        return redirect(url_for('castle'))

    try:
        amount = int(request.form.get('amount', 0))
    except ValueError:
        flash("Invalid amount.", 'error')
        return redirect(url_for('castle'))

    success, msg = game_logic.king_treasury_withdraw(king_record, amount)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/toggle_shop', methods=['POST'])
@login_required
def toggle_establishment():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    king_record = KingRecord.query.filter_by(player_id=player.id, is_current=True).first()
    if not king_record:
        return redirect(url_for('castle'))

    shop_key = request.form.get('shop_key', '')
    success, msg = game_logic.king_toggle_establishment(king_record, shop_key)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/proclamation', methods=['POST'])
@login_required
def royal_proclamation():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    message_text = request.form.get('message', '').strip()
    success, msg = game_logic.king_send_proclamation(player, message_text)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/imprison', methods=['POST'])
@login_required
def imprison_player():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    target_name = request.form.get('target', '').strip()
    success, msg = game_logic.king_imprison(player, target_name)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/release', methods=['POST'])
@login_required
def release_player():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    target_name = request.form.get('target', '').strip()
    success, msg = game_logic.king_release(player, target_name)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('castle'))


@app.route('/castle/deposit', methods=['POST'])
@login_required
def castle_deposit():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    king_record = KingRecord.query.filter_by(player_id=player.id, is_current=True).first()
    if not king_record:
        return redirect(url_for('castle'))

    try:
        amount = int(request.form.get('amount', 0))
    except ValueError:
        flash("Invalid amount.", 'error')
        return redirect(url_for('castle'))

    if amount <= 0 or amount > player.gold:
        flash("Invalid amount or insufficient gold.", 'error')
        return redirect(url_for('castle'))

    player.gold -= amount
    king_record.treasury += amount
    db.session.commit()
    flash(f"Deposited {amount} gold into royal treasury.", 'success')
    return redirect(url_for('castle'))


# ==================== PLAYER VS PLAYER ====================

@app.route('/pvp')
@login_required
def pvp():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if player.is_imprisoned:
        flash("You cannot fight while imprisoned.", 'error')
        return redirect(url_for('main_menu'))

    targets = Player.query.filter(
        Player.id != player.id,
        Player.is_imprisoned == False
    ).order_by(Player.level.desc()).all()

    return render_template('pvp.html', targets=targets)


@app.route('/pvp/fight/<int:target_id>', methods=['POST'])
@login_required
def pvp_fight(target_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    defender = db.session.get(Player, target_id)
    if not defender:
        flash("Player not found.", 'error')
        return redirect(url_for('pvp'))

    if player.hp <= 0:
        flash("You are too injured to fight.", 'error')
        return redirect(url_for('pvp'))

    if player.player_fights <= 0:
        flash("You have no player fights remaining today.", 'error')
        return redirect(url_for('pvp'))

    if player.is_imprisoned:
        flash("You cannot fight while imprisoned.", 'error')
        return redirect(url_for('pvp'))

    if defender.is_imprisoned:
        flash("That player is imprisoned.", 'error')
        return redirect(url_for('pvp'))

    winner, loser, combat_log = game_logic.pvp_combat(player, defender)
    db.session.commit()

    session['pvp_log'] = combat_log
    if winner is None:
        session['pvp_result'] = 'draw'
    elif winner.id == player.id:
        session['pvp_result'] = 'victory'
    else:
        session['pvp_result'] = 'defeat'

    return redirect(url_for('pvp_result'))


@app.route('/pvp/result')
@login_required
def pvp_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    combat_log = session.pop('pvp_log', [])
    result = session.pop('pvp_result', 'unknown')
    return render_template('pvp_result.html', combat_log=combat_log, result=result)


# ==================== TAVERN ====================

@app.route('/tavern')
@login_required
def tavern():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if not is_shop_open('shop_tavern'):
        flash("The Tavern has been closed by royal decree!", 'error')
        return redirect(url_for('main_menu'))

    if player.is_imprisoned:
        flash("You cannot visit the tavern while imprisoned.", 'error')
        return redirect(url_for('main_menu'))

    drink_cost = 10 + player.level * 2
    tavern_name = GameConfig.get('tavern_name', "Bob's Tavern")
    return render_template('tavern.html', drink_cost=drink_cost,
                           tavern_name=tavern_name)


@app.route('/tavern/brawl', methods=['POST'])
@login_required
def tavern_brawl():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg, log = game_logic.tavern_brawl(player)
    db.session.commit()

    if log:
        session['brawl_log'] = log
        return redirect(url_for('brawl_result'))

    flash(msg, 'success' if success else 'error')
    return redirect(url_for('tavern'))


@app.route('/tavern/brawl_result')
@login_required
def brawl_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    log = session.pop('brawl_log', [])
    return render_template('brawl_result.html', combat_log=log)


@app.route('/tavern/drink', methods=['POST'])
@login_required
def drinking_contest():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg, log = game_logic.drinking_contest(player)
    db.session.commit()

    if log:
        session['drink_log'] = log
        return redirect(url_for('drink_result'))

    flash(msg, 'success' if success else 'error')
    return redirect(url_for('tavern'))


@app.route('/tavern/drink_result')
@login_required
def drink_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    log = session.pop('drink_log', [])
    return render_template('brawl_result.html', combat_log=log)


# ==================== ORB'S BAR ====================

@app.route('/orbs-bar')
@login_required
def orbs_bar():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.is_imprisoned:
        flash("You cannot visit the bar while imprisoned.", 'error')
        return redirect(url_for('main_menu'))
    drinks = Drink.query.order_by(Drink.times_ordered.desc()).all()
    players = Player.query.filter(Player.id != player.id).order_by(Player.name).all()
    bartender = GameConfig.get('bartender_name', 'Sly')
    return render_template('orbs_bar.html', drinks=drinks, player=player,
                           bartender=bartender, players=players,
                           ingredients=DRINK_INGREDIENTS)


@app.route('/orbs-bar/create', methods=['POST'])
@login_required
def create_drink():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    name = request.form.get('name', '').strip()
    comment = request.form.get('comment', '').strip()
    secret = request.form.get('secret') == 'on'
    ingredients = {}
    for attr, _ in DRINK_INGREDIENTS:
        val = int(request.form.get(attr, 0) or 0)
        if val > 0:
            ingredients[attr] = val
    success, msg = game_logic.create_drink(player, name, comment, secret, ingredients)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('orbs_bar'))


@app.route('/orbs-bar/order/<int:drink_id>', methods=['POST'])
@login_required
def order_drink(drink_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    success, msg, log = game_logic.order_drink(player, drink_id)
    if success:
        # Apply stat effects from the drink
        drink = db.session.get(Drink, drink_id)
        if drink:
            effect_msg = game_logic.apply_drink_effects(player, drink)
            if effect_msg:
                log = log or []
                log.append(effect_msg)
            # Check for fatal drink combinations
            is_fatal, fatal_msg = game_logic.check_fatal_combo(player, drink_id)
            if is_fatal:
                log = log or []
                log.append(fatal_msg)
        db.session.commit()
        if log:
            session['drink_effect_log'] = log
            return redirect(url_for('drink_effect_result'))
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('orbs_bar'))


@app.route('/orbs-bar/drink_result')
@login_required
def drink_effect_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    log = session.pop('drink_effect_log', [])
    return render_template('brawl_result.html', combat_log=log)


@app.route('/orbs-bar/send', methods=['POST'])
@login_required
def send_drink():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    drink_id = safe_int(request.form.get('drink_id', 0))
    receiver_id = safe_int(request.form.get('receiver_id', 0))
    success, msg = game_logic.send_drink(player, receiver_id, drink_id)
    if success:
        game_logic.send_drink_mail(player, receiver_id, drink_id)
        db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('orbs_bar'))


# ==================== PICK-POCKETING ====================

@app.route('/pickpocket', methods=['POST'])
@login_required
def pickpocket():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    target_id = safe_int(request.form.get('target_id', 0))
    success, msg, log = game_logic.pickpocket(player, target_id)
    if success and log:
        session['pickpocket_log'] = log
        return redirect(url_for('pickpocket_result'))
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('shady_dealer'))


@app.route('/pickpocket/result')
@login_required
def pickpocket_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    log = session.pop('pickpocket_log', [])
    return render_template('brawl_result.html', combat_log=log)


# ==================== BANK ROBBERY ====================

@app.route('/bank/rob', methods=['POST'])
@login_required
def rob_bank():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    success, msg, log = game_logic.rob_bank(player)
    if success and log:
        session['robbery_log'] = log
        return redirect(url_for('robbery_result'))
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('bank'))


@app.route('/bank/rob/result')
@login_required
def robbery_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    log = session.pop('robbery_log', [])
    return render_template('brawl_result.html', combat_log=log)


# ==================== PRISON ESCAPE ====================

@app.route('/prison/escape', methods=['POST'])
@login_required
def prison_escape():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    success, msg, log = game_logic.escape_prison(player)
    if success and log:
        session['escape_log'] = log
        return redirect(url_for('escape_result'))
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('main_menu'))


@app.route('/prison/escape/result')
@login_required
def escape_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    log = session.pop('escape_log', [])
    return render_template('brawl_result.html', combat_log=log)


# ==================== BOUNTY BOARD ====================

@app.route('/bounty')
@login_required
def bounty_board():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    wanted = game_logic.get_wanted_list()
    my_bounties = Bounty.query.filter_by(poster_id=player.id, claimed=False).all()
    return render_template('bounty.html', wanted=wanted, my_bounties=my_bounties)


@app.route('/bounty/post', methods=['POST'])
@login_required
def post_bounty():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    target_name = request.form.get('target', '').strip()
    reason = request.form.get('reason', 'Wanted Dead or Alive').strip()
    try:
        amount = int(request.form.get('amount', 0))
    except ValueError:
        flash("Invalid amount.", 'error')
        return redirect(url_for('bounty_board'))

    success, msg = game_logic.post_bounty(player, target_name, amount, reason)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('bounty_board'))


# ==================== THE BEAUTY NEST ====================

@app.route('/beauty_nest')
@login_required
def beauty_nest():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if not is_shop_open('shop_beauty_nest'):
        flash("The Beauty Nest has been closed by royal decree!", 'error')
        return redirect(url_for('main_menu'))

    if GameConfig.get('beauty_nest_enabled', 'true').lower() != 'true':
        flash("This establishment is currently closed.", 'error')
        return redirect(url_for('main_menu'))

    if player.is_imprisoned:
        flash("You cannot visit while imprisoned.", 'error')
        return redirect(url_for('main_menu'))

    nest_name = GameConfig.get('beauty_nest_name', 'The Beauty Nest')
    owner_name = GameConfig.get('beauty_nest_owner', 'Clarissa')
    companions = game_logic.BEAUTY_NEST_COMPANIONS
    return render_template('beauty_nest.html', companions=companions,
                           nest_name=nest_name, owner_name=owner_name)


@app.route('/beauty_nest/visit/<int:index>', methods=['POST'])
@login_required
def beauty_nest_visit(index):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if GameConfig.get('beauty_nest_enabled', 'true').lower() != 'true':
        flash("This establishment is currently closed.", 'error')
        return redirect(url_for('main_menu'))

    if player.is_imprisoned:
        flash("You cannot visit while imprisoned.", 'error')
        return redirect(url_for('main_menu'))

    success, msg, log = game_logic.beauty_nest_visit(player, index)
    db.session.commit()

    if log:
        for entry in log:
            flash(entry, 'info')
    else:
        flash(msg, 'error' if not success else 'info')
    return redirect(url_for('beauty_nest'))


# ==================== LOVE CORNER / RELATIONSHIPS ====================

@app.route('/love_corner')
@login_required
def love_corner():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    relationships = game_logic.get_player_relationships(player)
    spouse = db.session.get(Player, player.spouse_id) if player.spouse_id else None

    # Pending proposals TO this player
    proposals = Relationship.query.filter_by(
        player2_id=player.id, rel_type='proposal'
    ).all()

    players_list = Player.query.filter(
        Player.id != player.id
    ).order_by(Player.name).all()

    married_couples = Relationship.query.filter_by(rel_type='married').all()
    love_corner_name = GameConfig.get('love_corner_name', 'The Love Corner')
    return render_template('love_corner.html', relationships=relationships,
                           spouse=spouse, proposals=proposals, players_list=players_list,
                           married_couples=married_couples,
                           love_corner_name=love_corner_name)


@app.route('/love_corner/propose', methods=['POST'])
@login_required
def propose():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    target_name = request.form.get('target', '').strip()
    success, msg = game_logic.propose_marriage(player, target_name)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('love_corner'))


@app.route('/love_corner/accept/<int:proposer_id>', methods=['POST'])
@login_required
def accept_proposal(proposer_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.accept_marriage(player, proposer_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('love_corner'))


@app.route('/love_corner/decline/<int:proposer_id>', methods=['POST'])
@login_required
def decline_proposal(proposer_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.decline_marriage(player, proposer_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('love_corner'))


@app.route('/love_corner/divorce', methods=['POST'])
@login_required
def divorce_spouse():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.divorce(player)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('love_corner'))


@app.route('/love_corner/add_relation', methods=['POST'])
@login_required
def add_relation():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    target_name = request.form.get('target', '').strip()
    rel_type = request.form.get('rel_type', '')
    success, msg = game_logic.add_relationship(player, target_name, rel_type)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('love_corner'))


@app.route('/love_corner/intimacy', methods=['POST'])
@login_required
def intimacy():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.attempt_intimacy(player)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('love_corner'))


@app.route('/love_corner/children')
@login_required
def children():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    kids = game_logic.get_player_children(player)
    spouse = db.session.get(Player, player.spouse_id) if player.spouse_id else None
    return render_template('children.html', children=kids, spouse=spouse)


# ==================== SOCIAL INTERACTIONS / APPROACH ====================

@app.route('/love_corner/approach')
@login_required
def approach():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    sex_filter = request.args.get('sex_filter', 'both')
    players_list = game_logic.get_approachable_players(player, sex_filter)
    return render_template('approach.html', players_list=players_list, sex_filter=sex_filter)


@app.route('/love_corner/approach/<int:target_id>')
@login_required
def approach_player(target_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    info = game_logic.approach_player_info(player, target_id)
    if not info:
        flash("Player not found.", 'error')
        return redirect(url_for('approach'))

    db.session.commit()
    return render_template('approach_player.html', info=info)


@app.route('/love_corner/interact', methods=['POST'])
@login_required
def social_interact():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    target_id = int(request.form.get('target_id', 0))
    action = request.form.get('action', '')

    success, msg, xp = game_logic.social_interact(player, target_id, action)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('approach_player', target_id=target_id))


@app.route('/love_corner/change_feeling', methods=['POST'])
@login_required
def change_feeling():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    target_id = int(request.form.get('target_id', 0))
    direction = request.form.get('direction', '')

    success, msg = game_logic.change_feeling(player, target_id, direction)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('approach_player', target_id=target_id))


# ==================== DUNGEON LEVEL CHANGE ====================

@app.route('/dungeon/change_level', methods=['POST'])
@login_required
def dungeon_change_level():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    try:
        new_level = int(request.form.get('new_level', 0))
    except ValueError:
        flash("Invalid level.", 'error')
        return redirect(url_for('dungeon'))

    success, msg = game_logic.change_dungeon_level(player, new_level)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('dungeon'))


# ==================== HOME (from original HOME.PAS) ====================

@app.route('/home')
@login_required
def home():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    info = game_logic.get_home_info(player)
    db.session.commit()
    return render_template('home.html', info=info)


@app.route('/home/sleep', methods=['POST'])
@login_required
def home_sleep():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.go_to_sleep(player)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('home'))


@app.route('/home/have_sex', methods=['POST'])
@login_required
def home_have_sex():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.have_sex_at_home(player)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('home'))


@app.route('/home/chest')
@login_required
def home_chest():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    chest_items = game_logic.get_chest_items(player)
    inv_items = InventoryItem.query.filter_by(player_id=player.id).all()
    # Resolve item details for inventory display
    inv_display = []
    for ii in inv_items:
        item = db.session.get(Item, ii.item_id)
        if item:
            # Check if equipped
            equipped = False
            for slot in EQUIPMENT_SLOTS:
                if getattr(player, f'equipped_{slot}', None) == item.id:
                    equipped = True
                    break
            inv_display.append({'inv_item': ii, 'item': item, 'equipped': equipped})

    return render_template('chest.html', chest_items=chest_items,
                           inv_display=inv_display,
                           max_chest=game_logic.MAX_CHEST_ITEMS)


@app.route('/home/chest/store/<int:inv_item_id>', methods=['POST'])
@login_required
def chest_store(inv_item_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.store_item_in_chest(player, inv_item_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('home_chest'))


@app.route('/home/chest/retrieve/<int:chest_item_id>', methods=['POST'])
@login_required
def chest_retrieve(chest_item_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.retrieve_item_from_chest(player, chest_item_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('home_chest'))


@app.route('/home/nursery')
@login_required
def nursery():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    children = game_logic.get_nursery_children(player)
    return render_template('nursery.html', children=children)


@app.route('/home/nursery/play/<int:child_id>', methods=['POST'])
@login_required
def nursery_play(child_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.nursery_play(player, child_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('nursery'))


@app.route('/home/custody')
@login_required
def custody():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    children = game_logic.get_player_children(player)
    accessible = [c for c in children if game_logic._has_access(player, c)]
    return render_template('custody.html', children=accessible)


@app.route('/home/custody/share/<int:child_id>', methods=['POST'])
@login_required
def custody_share(child_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.share_custody(player, child_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('custody'))


@app.route('/home/custody/abandon/<int:child_id>', methods=['POST'])
@login_required
def custody_abandon(child_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.abandon_child(player, child_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('custody'))


@app.route('/home/custody/orphanage/<int:child_id>', methods=['POST'])
@login_required
def custody_orphanage(child_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.send_to_orphanage(player, child_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('custody'))


@app.route('/home/ransom/<int:child_id>', methods=['POST'])
@login_required
def pay_ransom(child_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.pay_ransom(player, child_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('home'))


# ==================== TEAM MANAGEMENT ====================

@app.route('/teams/donate', methods=['POST'])
@login_required
def team_donate():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    my_membership = TeamMember.query.filter_by(player_id=player.id).first()
    if not my_membership:
        flash("You are not in a team.", 'error')
        return redirect(url_for('teams'))

    try:
        amount = int(request.form.get('amount', 0))
    except ValueError:
        flash("Invalid amount.", 'error')
        return redirect(url_for('teams'))

    success, msg = game_logic.team_donate(player, my_membership.team, amount)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('teams'))


@app.route('/teams/withdraw', methods=['POST'])
@login_required
def team_withdraw():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    my_membership = TeamMember.query.filter_by(player_id=player.id).first()
    if not my_membership:
        flash("You are not in a team.", 'error')
        return redirect(url_for('teams'))

    try:
        amount = int(request.form.get('amount', 0))
    except ValueError:
        flash("Invalid amount.", 'error')
        return redirect(url_for('teams'))

    success, msg = game_logic.team_withdraw(player, my_membership.team, amount)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('teams'))


@app.route('/teams/kick', methods=['POST'])
@login_required
def team_kick():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    my_membership = TeamMember.query.filter_by(player_id=player.id).first()
    if not my_membership:
        flash("You are not in a team.", 'error')
        return redirect(url_for('teams'))

    target_name = request.form.get('target', '').strip()
    success, msg = game_logic.kick_member(player, my_membership.team, target_name)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('teams'))


@app.route('/teams/transfer', methods=['POST'])
@login_required
def team_transfer():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    my_membership = TeamMember.query.filter_by(player_id=player.id).first()
    if not my_membership:
        flash("You are not in a team.", 'error')
        return redirect(url_for('teams'))

    target_name = request.form.get('target', '').strip()
    success, msg = game_logic.transfer_leadership(player, my_membership.team, target_name)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('teams'))


@app.route('/teams/claim_town', methods=['POST'])
@login_required
def claim_town():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    my_membership = TeamMember.query.filter_by(player_id=player.id).first()
    if not my_membership:
        flash("You must be in a team to claim the town.", 'error')
        return redirect(url_for('teams'))

    success, log, err = game_logic.claim_town(my_membership.team, player)
    db.session.commit()

    if log:
        session['gang_war_log'] = log
        return redirect(url_for('gang_war_result'))

    flash(err if err else "Town claimed!", 'error' if err else 'success')
    return redirect(url_for('teams'))


@app.route('/teams/gang_war_result')
@login_required
def gang_war_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    log = session.pop('gang_war_log', [])
    return render_template('gang_war_result.html', combat_log=log)


# ==================== ROYAL QUESTS ====================

@app.route('/castle/quests')
@login_required
def royal_quests():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    available = RoyalQuest.query.filter_by(
        is_completed=False, is_failed=False, is_public=True, occupier_id=None
    ).all()
    my_quests = RoyalQuest.query.filter_by(
        occupier_id=player.id, is_completed=False, is_failed=False
    ).all()
    completed = RoyalQuest.query.filter_by(
        occupier_id=player.id, is_completed=True
    ).order_by(RoyalQuest.created_at.desc()).limit(10).all()

    is_king = player.is_king
    king_record = KingRecord.query.filter_by(
        player_id=player.id, is_current=True
    ).first() if is_king else None

    return render_template('royal_quests.html', available=available,
                           my_quests=my_quests, completed=completed,
                           is_king=is_king, king_record=king_record)


@app.route('/castle/quests/create', methods=['POST'])
@login_required
def create_quest():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can create quests.", 'error')
        return redirect(url_for('royal_quests'))

    try:
        difficulty = int(request.form.get('difficulty', 5))
        reward_type = request.form.get('reward_type', 'experience')
        reward_size = int(request.form.get('reward_size', 2))
        penalty_type = request.form.get('penalty_type', '')
        penalty_size = int(request.form.get('penalty_size', 0))
        days = int(request.form.get('days', 3))
        min_level = int(request.form.get('min_level', 1))
        max_level = int(request.form.get('max_level', 100))
        comment = request.form.get('comment', '').strip()
        target_name = request.form.get('target_name', '').strip()
    except ValueError:
        flash("Invalid quest parameters.", 'error')
        return redirect(url_for('royal_quests'))

    success, quest, err = game_logic.create_royal_quest(
        player, difficulty, reward_type, reward_size,
        penalty_type, penalty_size, days, min_level, max_level,
        comment, target_name
    )
    db.session.commit()
    flash(err if err else "Quest created!", 'error' if err else 'success')
    return redirect(url_for('royal_quests'))


@app.route('/castle/quests/claim/<int:quest_id>', methods=['POST'])
@login_required
def claim_quest(quest_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.claim_quest(player, quest_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('royal_quests'))


# ==================== TEMPLE / GOD SYSTEM ====================

@app.route('/temple')
@login_required
def temple():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    gods = God.query.filter_by(is_active=True).order_by(God.experience.desc()).all()
    current_god = God.query.filter_by(name=player.god_name).first() if player.god_name else None

    temple_name = GameConfig.get('temple_name', 'Temple of the Gods')
    return render_template('temple.html', gods=gods, current_god=current_god,
                           temple_name=temple_name)


@app.route('/temple/worship', methods=['POST'])
@login_required
def worship():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    god_name = request.form.get('god_name', '').strip()
    success, msg = game_logic.worship_god(player, god_name)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('temple'))


@app.route('/temple/forsake', methods=['POST'])
@login_required
def forsake():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.forsake_god(player)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('temple'))


@app.route('/temple/pray', methods=['POST'])
@login_required
def pray():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.pray_to_god(player)
    db.session.commit()
    flash(msg, 'success' if success else 'info')
    return redirect(url_for('temple'))


@app.route('/temple/sacrifice', methods=['POST'])
@login_required
def sacrifice():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    try:
        amount = int(request.form.get('amount', 0))
    except ValueError:
        flash("Invalid amount.", 'error')
        return redirect(url_for('temple'))

    success, msg = game_logic.sacrifice_gold(player, amount)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('temple'))


@app.route('/temple/desecrate', methods=['POST'])
@login_required
def desecrate():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    god_name = request.form.get('god_name', '').strip()
    success, msg = game_logic.desecrate_altar(player, god_name)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('temple'))


# ==================== ADDITIONAL SHOPS ====================

@app.route('/shop/healing')
@login_required
def healing_shop():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if not is_shop_open('shop_healing'):
        flash("The Healing Center has been closed by royal decree!", 'error')
        return redirect(url_for('main_menu'))

    items = Item.query.filter_by(in_shop=True, shop_category='healing').order_by(Item.value).all()
    shop_name = GameConfig.get('healing_shop_name', 'The Healing Hut')
    return render_template('shop.html', items=items, shop_name=shop_name,
                           shop_type='healing', shop_image_key='healing_shop')


@app.route('/shop/general')
@login_required
def general_store():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if not is_shop_open('shop_general'):
        flash("The General Store has been closed by royal decree!", 'error')
        return redirect(url_for('main_menu'))

    items = Item.query.filter_by(in_shop=True, shop_category='general').order_by(Item.value).all()
    shop_name = GameConfig.get('general_store_name', 'General Store')
    return render_template('shop.html', items=items, shop_name=shop_name,
                           shop_type='general', shop_image_key='general_store')


@app.route('/shop/shady')
@login_required
def shady_dealer():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    items = Item.query.filter_by(in_shop=True, shop_category='shady').order_by(Item.value).all()
    dark_alley_name = GameConfig.get('dark_alley_name', 'The Dark Alley')
    targets = Player.query.filter(Player.id != player.id, Player.hp > 0).order_by(Player.name).all()
    return render_template('dark_alley.html', items=items, player=player,
                           dark_alley_name=dark_alley_name, targets=targets)


@app.route('/shop/alchemist')
@login_required
def alchemist_shop():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    if player.player_class != 'Alchemist':
        flash("Only Alchemists may enter this shop.", 'error')
        return redirect(url_for('main_menu'))

    items = Item.query.filter_by(in_shop=True, shop_category='alchemist').order_by(Item.value).all()
    return render_template('shop.html', items=items, shop_name="Alchemist's Heaven",
                           shop_type='alchemist')


# ==================== DRUG PALACE & STEROID SHOP ====================

@app.route('/shop/drugs')
@login_required
def drug_palace():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    return render_template('drug_palace.html', drugs=game_logic.DRUGS, player=player)


@app.route('/shop/drugs/buy/<int:index>', methods=['POST'])
@login_required
def buy_drug(index):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    success, msg, log = game_logic.buy_drug(player, index)
    if player.hp <= 0:
        # Overdose death - revive with penalties like combat defeat
        player.hp = max(1, player.max_hp // 4)
        player.experience = max(0, player.experience - player.experience // 10)
        player.gold = max(0, player.gold - player.gold // 5)
        log.append("You wake up in the gutter, stripped of some gold and dignity.")
    db.session.commit()
    if log:
        for entry in log:
            flash(entry, 'info')
    else:
        flash(msg, 'error' if not success else 'info')
    return redirect(url_for('drug_palace'))


@app.route('/shop/steroids')
@login_required
def steroid_shop():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    return render_template('steroid_shop.html', steroids=game_logic.STEROIDS, player=player)


@app.route('/shop/steroids/buy/<int:index>', methods=['POST'])
@login_required
def buy_steroid(index):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    success, msg, log = game_logic.buy_steroid(player, index)
    if player.hp <= 0:
        # Bad batch death - revive with penalties
        player.hp = max(1, player.max_hp // 4)
        player.experience = max(0, player.experience - player.experience // 10)
        player.gold = max(0, player.gold - player.gold // 5)
        log.append("You wake up on the floor of the shop, barely alive.")
    db.session.commit()
    if log:
        for entry in log:
            flash(entry, 'info')
    else:
        flash(msg, 'error' if not success else 'info')
    return redirect(url_for('steroid_shop'))


# ==================== PLAYER MARKET ====================

@app.route('/market')
@login_required
def player_market():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.is_imprisoned:
        flash("You cannot visit the market while imprisoned.", 'error')
        return redirect(url_for('main_menu'))

    listings = MarketListing.query.order_by(MarketListing.listed_at.desc()).all()
    my_listings = MarketListing.query.filter_by(seller_id=player.id).all()
    inventory = InventoryItem.query.filter_by(player_id=player.id).all()
    # Enrich inventory with item data
    inv_items = []
    for inv in inventory:
        item = db.session.get(Item, inv.item_id)
        if item:
            inv_items.append({'inv_id': inv.id, 'item': item})
    return render_template('player_market.html', listings=listings,
                           my_listings=my_listings, inv_items=inv_items,
                           max_listings=game_logic.MAX_LISTINGS_PER_PLAYER,
                           tax_percent=game_logic.MARKET_TAX_PERCENT)


@app.route('/market/list', methods=['POST'])
@login_required
def market_list_item():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    try:
        inv_id = int(request.form.get('inv_id', 0))
        price = int(request.form.get('price', 0))
    except (ValueError, TypeError):
        flash("Invalid input.", 'error')
        return redirect(url_for('player_market'))
    success, msg = game_logic.list_item_on_market(player, inv_id, price)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('player_market'))


@app.route('/market/buy/<int:listing_id>', methods=['POST'])
@login_required
def market_buy_item(listing_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    success, msg = game_logic.buy_market_item(player, listing_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('player_market'))


@app.route('/market/cancel/<int:listing_id>', methods=['POST'])
@login_required
def market_cancel_listing(listing_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    success, msg = game_logic.cancel_market_listing(player, listing_id)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('player_market'))


# ==================== BARD SONGS ====================

@app.route('/bard')
@login_required
def bard_stage():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.is_imprisoned:
        flash("You cannot perform while imprisoned.", 'error')
        return redirect(url_for('main_menu'))
    return render_template('bard_stage.html', songs=game_logic.BARD_SONGS,
                           is_bard=player.player_class == 'Bard')


@app.route('/bard/perform/<int:index>', methods=['POST'])
@login_required
def bard_perform(index):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    success, msg, log = game_logic.perform_bard_song(player, index)
    db.session.commit()
    if log:
        session['bard_log'] = log
        return redirect(url_for('bard_result'))
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('bard_stage'))


@app.route('/bard/result')
@login_required
def bard_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    log = session.pop('bard_log', [])
    return render_template('bard_result.html', log=log)


# ==================== WRESTLING MATCHES ====================

@app.route('/wrestling')
@login_required
def wrestling_arena():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.is_imprisoned:
        flash("You cannot wrestle while imprisoned.", 'error')
        return redirect(url_for('main_menu'))
    return render_template('wrestling.html',
                           opponents=game_logic.WRESTLING_OPPONENTS,
                           entry_base=game_logic.WRESTLING_ENTRY_FEE)


@app.route('/wrestling/fight/<int:index>', methods=['POST'])
@login_required
def wrestling_fight(index):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    success, msg, log = game_logic.wrestle(player, index)
    db.session.commit()
    if log:
        session['wrestling_log'] = log
        return redirect(url_for('wrestling_result'))
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('wrestling_arena'))


@app.route('/wrestling/result')
@login_required
def wrestling_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    log = session.pop('wrestling_log', [])
    return render_template('wrestling_result.html', log=log)


# ==================== BEAR TAMING (UMAN CAVE) ====================

@app.route('/cave')
@login_required
def uman_cave():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.is_imprisoned:
        flash("You cannot visit the cave while imprisoned.", 'error')
        return redirect(url_for('main_menu'))
    return render_template('uman_cave.html', bears=game_logic.BEAR_TYPES)


@app.route('/cave/tame/<int:index>', methods=['POST'])
@login_required
def tame_bear(index):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    success, msg, log = game_logic.attempt_bear_taming(player, index)
    db.session.commit()
    if log:
        session['cave_log'] = log
        return redirect(url_for('cave_result'))
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('uman_cave'))


@app.route('/cave/result')
@login_required
def cave_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    log = session.pop('cave_log', [])
    return render_template('cave_result.html', log=log)


@app.route('/cave/release', methods=['POST'])
@login_required
def release_bear():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    success, msg = game_logic.release_bear(player)
    db.session.commit()
    flash(msg, 'success' if success else 'error')
    return redirect(url_for('uman_cave'))


# ==================== DUNGEON EVENTS ====================

@app.route('/dungeon/event')
@login_required
def dungeon_event():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    event = session.get('dungeon_event')
    if not event:
        return redirect(url_for('dungeon'))

    return render_template('dungeon_event.html', event=event)


@app.route('/dungeon/event/resolve', methods=['POST'])
@login_required
def resolve_dungeon_event():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    event_id = request.form.get('event_id', '')
    choice = request.form.get('choice', '')
    current_step = request.form.get('current_step', '')

    result_text, next_step_data = game_logic.resolve_dungeon_event(
        player, event_id, choice, current_step=current_step or None)
    db.session.commit()

    if next_step_data:
        # Multi-step event continues - show result and next step
        session['dungeon_event'] = next_step_data
        flash(result_text, 'info')
        return redirect(url_for('dungeon_event'))

    # Event is complete
    session.pop('dungeon_event', None)
    flash(result_text, 'info')
    return redirect(url_for('dungeon'))


# ==================== API ENDPOINTS (for AJAX) ====================

@app.route('/api/player/stats')
@login_required
def api_player_stats():
    player = get_player()
    if not player:
        return jsonify({'error': 'No character'}), 404

    return jsonify({
        'name': player.name,
        'level': player.level,
        'hp': player.hp,
        'max_hp': player.max_hp,
        'mana': player.mana,
        'max_mana': player.max_mana,
        'gold': player.gold,
        'experience': player.experience,
        'fights_remaining': player.fights_remaining,
    })


# ==================== NPC STATUS ====================

@app.route('/npcs')
@login_required
def npc_list():
    """View all NPCs and their current status."""
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    npcs = Player.query.filter_by(is_npc=True).order_by(Player.level.desc()).all()
    return render_template('npc_list.html', npcs=npcs)


@app.route('/api/npcs')
@login_required
def api_npc_list():
    """JSON API for NPC status data."""
    npcs = Player.query.filter_by(is_npc=True).order_by(Player.level.desc()).all()
    return jsonify([{
        'id': npc.id,
        'name': npc.name,
        'level': npc.level,
        'race': npc.race,
        'player_class': npc.player_class,
        'alignment': npc.alignment_string(),
        'location': npc.npc_location,
        'team': npc.team_name or None,
        'married': npc.married,
        'is_king': npc.is_king,
        'is_imprisoned': npc.is_imprisoned,
    } for npc in npcs])


# ==================== ADMIN PANEL ====================

@app.route('/admin')
@admin_required
def admin_dashboard():
    """Admin dashboard - overview of game state."""
    stats = {
        'total_players': Player.query.filter_by(is_npc=False).count(),
        'total_npcs': Player.query.filter_by(is_npc=True).count(),
        'total_items': Item.query.count(),
        'total_monsters': Monster.query.count(),
        'total_teams': Team.query.count(),
        'total_users': User.query.count(),
        'total_mail': Mail.query.count(),
        'total_news': NewsEntry.query.count(),
        'total_bounties': Bounty.query.filter_by(claimed=False).count(),
        'total_gods': God.query.count(),
        'total_door_guards': DoorGuard.query.count(),
        'total_moat_creatures': MoatCreature.query.count(),
        'total_drinks': Drink.query.count(),
    }
    king = Player.query.filter_by(is_king=True).first()
    return render_template('admin/dashboard.html', stats=stats, king=king)


@app.route('/admin/config', methods=['GET', 'POST'])
@admin_required
def admin_config():
    """Edit game configuration values - mirrors original editor's config system."""
    config_groups = {
        'General': [
            ('bbs_name', 'Game Name', 'text'),
            ('sysop_name', 'Sysop Name', 'text'),
            ('town_name', 'Town Name', 'text'),
            ('dungeon_name', 'Dungeon Name', 'text'),
            ('challenges_place', 'Challenges Place', 'text'),
            ('start_gold', 'Starting Gold', 'number'),
            ('scrolling_text', 'Scrolling News Text (shown on all pages)', 'textarea'),
        ],
        'Combat & Limits': [
            ('max_fights_per_day', 'Dungeon Fights Per Day', 'number'),
            ('max_player_fights', 'Player Fights Per Day', 'number'),
            ('max_thefts_per_day', 'Theft Attempts Per Day', 'number'),
            ('max_brawls_per_day', 'Brawl Attempts Per Day', 'number'),
            ('team_fights_per_day', 'Team Fights Per Day', 'number'),
            ('max_healing_potions', 'Max Healing Potions', 'number'),
            ('dungeon_difficulty', 'Dungeon Difficulty (1-10)', 'number'),
            ('xp_loss_dungeon_pct', 'XP Loss % on Dungeon Death', 'number'),
            ('xp_loss_pvp_pct', 'XP Loss % on PvP Death', 'number'),
        ],
        'Throne & Governance': [
            ('level_to_usurp', 'Level Needed to Usurp Throne', 'number'),
            ('allow_offline_attacks', 'Allow Offline Player Attacks', 'toggle'),
            ('allow_team_attacks', 'Allow Attacking Teammates', 'toggle'),
            ('allow_resurrection', 'Allow Resurrection of Teammates', 'toggle'),
        ],
        'NPC Settings': [
            ('npc_enabled', 'NPCs Enabled', 'toggle'),
            ('npc_tick_minutes', 'NPC Action Interval (minutes)', 'number'),
            ('npc_max_count', 'Max NPCs', 'number'),
            ('allow_npc_teams', 'NPCs Can Form Teams', 'toggle'),
            ('allow_npc_equipment', 'NPCs Can Buy Equipment', 'toggle'),
            ('allow_npc_usurp', 'NPCs Can Usurp Throne', 'toggle'),
            ('allow_npc_marriage', 'NPCs Can Marry', 'toggle'),
            ('npc_allow_pvp', 'NPCs Can PvP', 'toggle'),
            ('npc_allow_bounty_hunting', 'NPCs Can Hunt Bounties', 'toggle'),
            ('npc_min_level_king', 'Min NPC Level for Throne', 'number'),
        ],
        'Economy': [
            ('bank_interest_rate', 'Bank Interest Rate (%)', 'number'),
            ('max_players', 'Max Players', 'number'),
            ('bank_robbery_attempts', 'Bank Robbery Attempts Per Day', 'number'),
        ],
        "Orb's Bar": [
            ('bartender_name', 'Bartender Name', 'text'),
            ('drinks_per_day', 'Drinks Per Day', 'number'),
            ('max_drinks', 'Max Custom Drinks', 'number'),
        ],
        'Prison': [
            ('prison_escape_attempts', 'Escape Attempts Per Day', 'number'),
        ],
        'Beauty Nest': [
            ('beauty_nest_name', 'Establishment Name', 'text'),
            ('beauty_nest_owner', 'Proprietress Name', 'text'),
            ('beauty_nest_visits_per_day', 'Visits Per Day', 'number'),
            ('beauty_nest_disease_chance', 'Disease Chance (1 in N)', 'number'),
            ('beauty_nest_enabled', 'Beauty Nest Enabled', 'toggle'),
        ],
        'NPC Names': [
            ('weaponshop_owner', 'Weapon Shop Owner', 'text'),
            ('armorshop_owner', 'Armor Shop Owner', 'text'),
            ('magicshop_owner', 'Magic Shop Owner', 'text'),
            ('combat_trainer', 'Combat Trainer', 'text'),
            ('bank_manager', 'Bank Manager', 'text'),
            ('inn_owner', 'Inn Owner', 'text'),
            ('bishop_name', 'Bishop', 'text'),
            ('gossip_name', 'Gossip/Midwife', 'text'),
            ('bartender_name', 'Bartender', 'text'),
            ('level_master_name', 'Level Master', 'text'),
        ],
        'Location Names': [
            ('inn_name', 'Inn Name', 'text'),
            ('weapon_shop_name', 'Weapon Shop Name', 'text'),
            ('armor_shop_name', 'Armor Shop Name', 'text'),
            ('magic_shop_name', 'Magic Shop Name', 'text'),
            ('healing_shop_name', 'Healing Shop Name', 'text'),
            ('general_store_name', 'General Store Name', 'text'),
            ('tavern_name', 'Tavern Name', 'text'),
            ('dark_alley_name', 'Dark Alley Name', 'text'),
            ('temple_name', 'Temple Name', 'text'),
            ('castle_name', 'Castle Name', 'text'),
            ('love_corner_name', 'Love Corner Name', 'text'),
        ],
        'Location Images': [
            ('image_main_menu', 'Town / Main Menu', 'text'),
            ('image_dungeon', 'Dungeon', 'text'),
            ('image_weapon_shop', 'Weapon Shop', 'text'),
            ('image_armor_shop', 'Armor Shop', 'text'),
            ('image_magic_shop', 'Magic Shop', 'text'),
            ('image_healing_shop', 'Healing Shop', 'text'),
            ('image_general_store', 'General Store', 'text'),
            ('image_inn', 'Inn', 'text'),
            ('image_tavern', 'Tavern', 'text'),
            ('image_bank', 'Bank', 'text'),
            ('image_castle', 'Castle', 'text'),
            ('image_temple', 'Temple', 'text'),
            ('image_dark_alley', 'Dark Alley', 'text'),
            ('image_beauty_nest', 'Beauty Nest', 'text'),
            ('image_love_corner', 'Love Corner', 'text'),
            ('image_home', 'Home', 'text'),
            ('image_dormitory', 'Dormitory (PvP)', 'text'),
            ('image_bounty_board', 'Bounty Board', 'text'),
            ('image_level_master', 'Level Master', 'text'),
            ('image_teams', 'Teams', 'text'),
        ],
    }

    if request.method == 'POST':
        changes = 0
        for group_name, fields in config_groups.items():
            for key, label, field_type in fields:
                new_value = request.form.get(key, '')
                if field_type == 'toggle':
                    new_value = 'true' if request.form.get(key) == 'on' else 'false'
                old_value = GameConfig.get(key, '')
                if new_value != old_value:
                    GameConfig.set(key, new_value)
                    changes += 1
        if changes:
            flash(f'Configuration updated ({changes} setting(s) changed).', 'success')
        else:
            flash('No changes detected.', 'info')
        return redirect(url_for('admin_config'))

    # Load current values
    config_values = {}
    for group_name, fields in config_groups.items():
        for key, label, field_type in fields:
            config_values[key] = GameConfig.get(key, '')

    return render_template('admin/config.html',
                           config_groups=config_groups,
                           config_values=config_values)


@app.route('/admin/items')
@admin_required
def admin_items():
    """List all items for editing."""
    items = Item.query.order_by(Item.item_type, Item.value).all()
    return render_template('admin/items.html', items=items, item_types=ITEM_TYPES)


@app.route('/admin/items/<int:item_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_item(item_id):
    """Edit a single item."""
    item = db.session.get(Item, item_id)
    if not item:
        flash('Item not found.', 'error')
        return redirect(url_for('admin_items'))

    if request.method == 'POST':
        item.name = request.form.get('name', item.name).strip()
        item.item_type = request.form.get('item_type', item.item_type)
        item.value = int(request.form.get('value', 0))
        item.attack_bonus = int(request.form.get('attack_bonus', 0))
        item.armor_bonus = int(request.form.get('armor_bonus', 0))
        item.hp_bonus = int(request.form.get('hp_bonus', 0))
        item.strength_bonus = int(request.form.get('strength_bonus', 0))
        item.defence_bonus = int(request.form.get('defence_bonus', 0))
        item.stamina_bonus = int(request.form.get('stamina_bonus', 0))
        item.agility_bonus = int(request.form.get('agility_bonus', 0))
        item.charisma_bonus = int(request.form.get('charisma_bonus', 0))
        item.dexterity_bonus = int(request.form.get('dexterity_bonus', 0))
        item.wisdom_bonus = int(request.form.get('wisdom_bonus', 0))
        item.mana_bonus = int(request.form.get('mana_bonus', 0))
        item.description = request.form.get('description', '')
        item.is_cursed = request.form.get('is_cursed') == 'on'
        item.is_unique = request.form.get('is_unique') == 'on'
        item.in_shop = request.form.get('in_shop') == 'on'
        item.in_dungeon = request.form.get('in_dungeon') == 'on'
        item.min_level = int(request.form.get('min_level', 1))
        item.max_level = int(request.form.get('max_level', 100))
        item.strength_required = int(request.form.get('strength_required', 0))
        item.good_only = request.form.get('good_only') == 'on'
        item.evil_only = request.form.get('evil_only') == 'on'
        item.class_restrictions = request.form.get('class_restrictions', '')
        item.shop_category = request.form.get('shop_category', '')
        db.session.commit()
        flash(f'Item "{item.name}" updated.', 'success')
        return redirect(url_for('admin_items'))

    return render_template('admin/edit_item.html', item=item,
                           item_types=ITEM_TYPES, classes=CLASSES)


@app.route('/admin/items/new', methods=['GET', 'POST'])
@admin_required
def admin_new_item():
    """Create a new item."""
    if request.method == 'POST':
        item = Item(
            name=request.form.get('name', 'New Item').strip(),
            item_type=request.form.get('item_type', 'Weapon'),
            value=int(request.form.get('value', 0)),
            attack_bonus=int(request.form.get('attack_bonus', 0)),
            armor_bonus=int(request.form.get('armor_bonus', 0)),
            hp_bonus=int(request.form.get('hp_bonus', 0)),
            strength_bonus=int(request.form.get('strength_bonus', 0)),
            defence_bonus=int(request.form.get('defence_bonus', 0)),
            stamina_bonus=int(request.form.get('stamina_bonus', 0)),
            agility_bonus=int(request.form.get('agility_bonus', 0)),
            charisma_bonus=int(request.form.get('charisma_bonus', 0)),
            dexterity_bonus=int(request.form.get('dexterity_bonus', 0)),
            wisdom_bonus=int(request.form.get('wisdom_bonus', 0)),
            mana_bonus=int(request.form.get('mana_bonus', 0)),
            description=request.form.get('description', ''),
            is_cursed=request.form.get('is_cursed') == 'on',
            is_unique=request.form.get('is_unique') == 'on',
            in_shop=request.form.get('in_shop') == 'on',
            in_dungeon=request.form.get('in_dungeon') == 'on',
            min_level=int(request.form.get('min_level', 1)),
            max_level=int(request.form.get('max_level', 100)),
            strength_required=int(request.form.get('strength_required', 0)),
            good_only=request.form.get('good_only') == 'on',
            evil_only=request.form.get('evil_only') == 'on',
            class_restrictions=request.form.get('class_restrictions', ''),
            shop_category=request.form.get('shop_category', ''),
        )
        db.session.add(item)
        db.session.commit()
        flash(f'Item "{item.name}" created.', 'success')
        return redirect(url_for('admin_items'))

    item = Item(name='', item_type='Weapon', min_level=1, max_level=100)
    return render_template('admin/edit_item.html', item=item, is_new=True,
                           item_types=ITEM_TYPES, classes=CLASSES)


@app.route('/admin/items/<int:item_id>/delete', methods=['POST'])
@admin_required
def admin_delete_item(item_id):
    """Delete an item."""
    item = db.session.get(Item, item_id)
    if item:
        db.session.delete(item)
        db.session.commit()
        flash(f'Item "{item.name}" deleted.', 'success')
    return redirect(url_for('admin_items'))


@app.route('/admin/monsters')
@admin_required
def admin_monsters():
    """List all monsters for editing."""
    monsters = Monster.query.order_by(Monster.min_dungeon_level, Monster.name).all()
    return render_template('admin/monsters.html', monsters=monsters)


@app.route('/admin/monsters/<int:monster_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_monster(monster_id):
    """Edit a single monster."""
    monster = db.session.get(Monster, monster_id)
    if not monster:
        flash('Monster not found.', 'error')
        return redirect(url_for('admin_monsters'))

    if request.method == 'POST':
        monster.name = request.form.get('name', monster.name).strip()
        monster.min_dungeon_level = int(request.form.get('min_dungeon_level', 1))
        monster.max_dungeon_level = int(request.form.get('max_dungeon_level', 10))
        monster.hp = int(request.form.get('hp', 20))
        monster.strength = int(request.form.get('strength', 10))
        monster.defence = int(request.form.get('defence', 5))
        monster.weapon_power = int(request.form.get('weapon_power', 0))
        monster.armor_power = int(request.form.get('armor_power', 0))
        monster.experience = int(request.form.get('experience', 10))
        monster.gold = int(request.form.get('gold', 5))
        monster.phrase = request.form.get('phrase', '')
        monster.weapon_name = request.form.get('weapon_name', 'claws')
        monster.armor_name = request.form.get('armor_name', '')
        monster.is_poisonous = request.form.get('is_poisonous') == 'on'
        monster.has_disease = request.form.get('has_disease') == 'on'
        monster.magic_resistance = int(request.form.get('magic_resistance', 0))
        monster.magic_level = int(request.form.get('magic_level', 0))
        monster.aggression = int(request.form.get('aggression', 1))
        monster.can_drop_weapon = request.form.get('can_drop_weapon') == 'on'
        monster.can_drop_armor = request.form.get('can_drop_armor') == 'on'
        db.session.commit()
        flash(f'Monster "{monster.name}" updated.', 'success')
        return redirect(url_for('admin_monsters'))

    return render_template('admin/edit_monster.html', monster=monster)


@app.route('/admin/monsters/new', methods=['GET', 'POST'])
@admin_required
def admin_new_monster():
    """Create a new monster."""
    if request.method == 'POST':
        monster = Monster(
            name=request.form.get('name', 'New Monster').strip(),
            min_dungeon_level=int(request.form.get('min_dungeon_level', 1)),
            max_dungeon_level=int(request.form.get('max_dungeon_level', 10)),
            hp=int(request.form.get('hp', 20)),
            strength=int(request.form.get('strength', 10)),
            defence=int(request.form.get('defence', 5)),
            weapon_power=int(request.form.get('weapon_power', 0)),
            armor_power=int(request.form.get('armor_power', 0)),
            experience=int(request.form.get('experience', 10)),
            gold=int(request.form.get('gold', 5)),
            phrase=request.form.get('phrase', ''),
            weapon_name=request.form.get('weapon_name', 'claws'),
            armor_name=request.form.get('armor_name', ''),
            is_poisonous=request.form.get('is_poisonous') == 'on',
            has_disease=request.form.get('has_disease') == 'on',
            magic_resistance=int(request.form.get('magic_resistance', 0)),
            magic_level=int(request.form.get('magic_level', 0)),
            aggression=int(request.form.get('aggression', 1)),
            can_drop_weapon=request.form.get('can_drop_weapon') == 'on',
            can_drop_armor=request.form.get('can_drop_armor') == 'on',
        )
        db.session.add(monster)
        db.session.commit()
        flash(f'Monster "{monster.name}" created.', 'success')
        return redirect(url_for('admin_monsters'))

    monster = Monster(name='', min_dungeon_level=1, max_dungeon_level=10,
                      hp=20, strength=10, defence=5, experience=10, gold=5,
                      weapon_name='claws', aggression=1)
    return render_template('admin/edit_monster.html', monster=monster, is_new=True)


@app.route('/admin/monsters/<int:monster_id>/delete', methods=['POST'])
@admin_required
def admin_delete_monster(monster_id):
    """Delete a monster."""
    monster = db.session.get(Monster, monster_id)
    if monster:
        db.session.delete(monster)
        db.session.commit()
        flash(f'Monster "{monster.name}" deleted.', 'success')
    return redirect(url_for('admin_monsters'))


@app.route('/admin/players')
@admin_required
def admin_players():
    """List all players (human and NPC) for editing."""
    show = request.args.get('show', 'humans')
    if show == 'npcs':
        players = Player.query.filter_by(is_npc=True).order_by(Player.level.desc()).all()
    else:
        players = Player.query.filter_by(is_npc=False).order_by(Player.level.desc()).all()
    return render_template('admin/players.html', players=players, show=show)


@app.route('/admin/players/<int:player_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_player(player_id):
    """Edit a player's stats and attributes."""
    player = db.session.get(Player, player_id)
    if not player:
        flash('Player not found.', 'error')
        return redirect(url_for('admin_players'))

    if request.method == 'POST':
        action = request.form.get('action', 'save')

        # Handle inventory actions
        if action == 'add_item':
            item_id = request.form.get('new_item_id')
            if item_id:
                inv_item = InventoryItem(player_id=player.id, item_id=int(item_id))
                db.session.add(inv_item)
                db.session.commit()
                flash('Item added to inventory.', 'success')
            return redirect(url_for('admin_edit_player', player_id=player_id))

        if action == 'remove_item':
            inv_id = request.form.get('inv_item_id')
            if inv_id:
                inv_item = db.session.get(InventoryItem, int(inv_id))
                if inv_item and inv_item.player_id == player.id:
                    db.session.delete(inv_item)
                    db.session.commit()
                    flash('Item removed from inventory.', 'success')
            return redirect(url_for('admin_edit_player', player_id=player_id))

        if action == 'equip_item':
            slot = request.form.get('equip_slot')
            item_id = request.form.get('equip_item_id')
            if slot in EQUIPMENT_SLOTS:
                setattr(player, f'equipped_{slot}', int(item_id) if item_id else None)
                player.recalculate_equipment_power()
                db.session.commit()
                flash(f'Equipment slot "{slot}" updated.', 'success')
            return redirect(url_for('admin_edit_player', player_id=player_id))

        # Standard field updates
        player.name = request.form.get('name', player.name).strip()
        player.race = request.form.get('race', player.race)
        player.player_class = request.form.get('player_class', player.player_class)
        player.sex = int(request.form.get('sex', player.sex))
        player.age = int(request.form.get('age', player.age))
        player.level = int(request.form.get('level', player.level))
        player.strength = int(request.form.get('strength', player.strength))
        player.defence = int(request.form.get('defence', player.defence))
        player.stamina = int(request.form.get('stamina', player.stamina))
        player.agility = int(request.form.get('agility', player.agility))
        player.charisma = int(request.form.get('charisma', player.charisma))
        player.dexterity = int(request.form.get('dexterity', player.dexterity))
        player.wisdom = int(request.form.get('wisdom', player.wisdom))
        player.hp = int(request.form.get('hp', player.hp))
        player.max_hp = int(request.form.get('max_hp', player.max_hp))
        player.mana = int(request.form.get('mana', player.mana))
        player.max_mana = int(request.form.get('max_mana', player.max_mana))
        player.experience = int(request.form.get('experience', player.experience))
        player.gold = int(request.form.get('gold', player.gold))
        player.bank_gold = int(request.form.get('bank_gold', player.bank_gold))
        player.chivalry = int(request.form.get('chivalry', player.chivalry))
        player.darkness = int(request.form.get('darkness', player.darkness))
        player.fights_remaining = int(request.form.get('fights_remaining', player.fights_remaining))
        player.player_fights = int(request.form.get('player_fights', player.player_fights))
        player.thefts_remaining = int(request.form.get('thefts_remaining', player.thefts_remaining))
        player.brawls_remaining = int(request.form.get('brawls_remaining', player.brawls_remaining))
        player.drinks_remaining = int(request.form.get('drinks_remaining', player.drinks_remaining))
        player.wrestling_matches = int(request.form.get('wrestling_matches', player.wrestling_matches))
        player.performances_remaining = int(request.form.get('performances_remaining', player.performances_remaining))
        player.team_fights = int(request.form.get('team_fights', player.team_fights))
        player.intimacy_acts = int(request.form.get('intimacy_acts', player.intimacy_acts))
        player.beauty_nest_visits = int(request.form.get('beauty_nest_visits', player.beauty_nest_visits))
        player.weapon_power = int(request.form.get('weapon_power', player.weapon_power))
        player.armor_power = int(request.form.get('armor_power', player.armor_power))
        player.monster_kills = int(request.form.get('monster_kills', player.monster_kills))
        player.monster_defeats = int(request.form.get('monster_defeats', player.monster_defeats))
        player.player_kills = int(request.form.get('player_kills', player.player_kills))
        player.player_defeats = int(request.form.get('player_defeats', player.player_defeats))
        player.healing_potions = int(request.form.get('healing_potions', player.healing_potions))
        player.dungeon_level = int(request.form.get('dungeon_level', player.dungeon_level))
        player.wrestling_wins = int(request.form.get('wrestling_wins', player.wrestling_wins))
        player.wrestling_losses = int(request.form.get('wrestling_losses', player.wrestling_losses))
        player.quests_completed = int(request.form.get('quests_completed', player.quests_completed))
        player.quests_failed = int(request.form.get('quests_failed', player.quests_failed))
        player.bank_wage = int(request.form.get('bank_wage', player.bank_wage))
        player.prison_days = int(request.form.get('prison_days', player.prison_days))
        player.escape_attempts = int(request.form.get('escape_attempts', player.escape_attempts))
        player.mental_health = int(request.form.get('mental_health', player.mental_health))
        player.addiction = int(request.form.get('addiction', player.addiction))
        player.bear_name = request.form.get('bear_name', player.bear_name).strip()
        player.bear_strength = int(request.form.get('bear_strength', player.bear_strength))
        player.children_count = int(request.form.get('children_count', player.children_count))
        player.pregnancy_days = int(request.form.get('pregnancy_days', player.pregnancy_days))
        player.door_guard_count = int(request.form.get('door_guard_count', player.door_guard_count))
        player.market_listings = int(request.form.get('market_listings', player.market_listings))
        player.is_poisoned = request.form.get('is_poisoned') == 'on'
        player.is_blind = request.form.get('is_blind') == 'on'
        player.has_plague = request.form.get('has_plague') == 'on'
        player.is_king = request.form.get('is_king') == 'on'
        player.is_imprisoned = request.form.get('is_imprisoned') == 'on'
        player.is_god = request.form.get('is_god') == 'on'
        player.tax_relief = request.form.get('tax_relief') == 'on'
        player.is_bank_guard = request.form.get('is_bank_guard') == 'on'
        player.has_tamed_bear = request.form.get('has_tamed_bear') == 'on'
        player.has_horse = request.form.get('has_horse') == 'on'
        player.horse_name = request.form.get('horse_name', player.horse_name).strip()
        player.horse_type = request.form.get('horse_type', player.horse_type).strip()
        player.horse_bonus_fights = int(request.form.get('horse_bonus_fights', player.horse_bonus_fights))
        player.fairy_dust = int(request.form.get('fairy_dust', player.fairy_dust))
        player.is_pregnant = request.form.get('is_pregnant') == 'on'
        player.married = request.form.get('married') == 'on'
        db.session.commit()
        flash(f'Player "{player.name}" updated.', 'success')
        return redirect(url_for('admin_players',
                                show='npcs' if player.is_npc else 'humans'))

    # Build equipped items dict
    equipped = {}
    for slot in EQUIPMENT_SLOTS:
        item_id = getattr(player, f'equipped_{slot}', None)
        equipped[slot] = db.session.get(Item, item_id) if item_id else None

    all_items = Item.query.order_by(Item.name).all()
    return render_template('admin/edit_player.html', player=player,
                           races=RACES, classes=CLASSES,
                           equipped=equipped, EQUIPMENT_SLOTS=EQUIPMENT_SLOTS,
                           EQUIPMENT_SLOT_LABELS=EQUIPMENT_SLOT_LABELS,
                           all_items=all_items)


@app.route('/admin/players/<int:player_id>/delete', methods=['POST'])
@admin_required
def admin_delete_player(player_id):
    """Delete a player."""
    player = db.session.get(Player, player_id)
    if not player:
        flash('Player not found.', 'error')
        return redirect(url_for('admin_players'))
    is_npc = player.is_npc
    name = player.name
    # Clean up king state if this player is the current monarch
    if player.is_king:
        king_records = KingRecord.query.filter_by(player_id=player_id, is_current=True).all()
        for kr in king_records:
            kr.is_current = False
            kr.dethroned_at = datetime.now(timezone.utc)
    # Delete related records
    KingRecord.query.filter_by(player_id=player_id).delete()
    InventoryItem.query.filter_by(player_id=player_id).delete()
    Mail.query.filter((Mail.sender_id == player_id) | (Mail.receiver_id == player_id)).delete(synchronize_session=False)
    NewsEntry.query.filter_by(player_id=player_id).delete()
    TeamMember.query.filter_by(player_id=player_id).delete()
    Bounty.query.filter((Bounty.target_id == player_id) | (Bounty.poster_id == player_id)).delete(synchronize_session=False)
    RoyalQuest.query.filter(
        (RoyalQuest.initiator_id == player_id) | (RoyalQuest.occupier_id == player_id)
    ).delete(synchronize_session=False)
    db.session.delete(player)
    db.session.commit()
    flash(f'Player "{name}" deleted.', 'success')
    return redirect(url_for('admin_players', show='npcs' if is_npc else 'humans'))


@app.route('/admin/users')
@admin_required
def admin_users():
    """Manage user accounts and admin privileges."""
    users = User.query.order_by(User.created_at).all()
    return render_template('admin/users.html', users=users)


@app.route('/admin/users/<int:user_id>/toggle-admin', methods=['POST'])
@admin_required
def admin_toggle_admin(user_id):
    """Grant or revoke admin privileges."""
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('admin_users'))
    if user.id == current_user.id:
        flash('You cannot change your own admin status.', 'error')
        return redirect(url_for('admin_users'))
    user.is_admin = not user.is_admin
    db.session.commit()
    status = 'granted' if user.is_admin else 'revoked'
    flash(f'Admin privileges {status} for "{user.username}".', 'success')
    return redirect(url_for('admin_users'))


@app.route('/admin/users/<int:user_id>/reset-password', methods=['POST'])
@admin_required
def admin_reset_password(user_id):
    """Reset a user's password."""
    user = db.session.get(User, user_id)
    if not user:
        flash('User not found.', 'error')
        return redirect(url_for('admin_users'))
    new_password = request.form.get('new_password', '').strip()
    if len(new_password) < 4:
        flash('Password must be at least 4 characters.', 'error')
        return redirect(url_for('admin_users'))
    user.set_password(new_password)
    db.session.commit()
    flash(f'Password reset for "{user.username}".', 'success')
    return redirect(url_for('admin_users'))


@app.route('/admin/gods')
@admin_required
def admin_gods():
    """List all gods for editing."""
    gods = God.query.order_by(God.level.desc()).all()
    return render_template('admin/gods.html', gods=gods)


@app.route('/admin/gods/<int:god_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_god(god_id):
    """Edit a god."""
    god = db.session.get(God, god_id)
    if not god:
        flash('God not found.', 'error')
        return redirect(url_for('admin_gods'))

    if request.method == 'POST':
        god.name = request.form.get('name', god.name).strip()
        god.sex = int(request.form.get('sex', god.sex))
        god.level = int(request.form.get('level', god.level))
        god.experience = int(request.form.get('experience', god.experience))
        god.deeds_left = int(request.form.get('deeds_left', god.deeds_left))
        god.alignment = request.form.get('alignment', god.alignment)
        god.domain = request.form.get('domain', god.domain)
        god.description = request.form.get('description', god.description)
        god.is_active = request.form.get('is_active') == 'on'
        db.session.commit()
        flash(f'God "{god.name}" updated.', 'success')
        return redirect(url_for('admin_gods'))

    return render_template('admin/edit_god.html', god=god)


@app.route('/admin/gods/new', methods=['GET', 'POST'])
@admin_required
def admin_new_god():
    """Create a new god."""
    if request.method == 'POST':
        god = God(
            name=request.form.get('name', 'New God').strip(),
            sex=int(request.form.get('sex', 1)),
            level=int(request.form.get('level', 1)),
            experience=int(request.form.get('experience', 0)),
            deeds_left=int(request.form.get('deeds_left', 5)),
            alignment=request.form.get('alignment', 'neutral'),
            domain=request.form.get('domain', ''),
            description=request.form.get('description', ''),
            is_active=request.form.get('is_active') == 'on',
        )
        db.session.add(god)
        db.session.commit()
        flash(f'God "{god.name}" created.', 'success')
        return redirect(url_for('admin_gods'))

    god = God(name='', level=1, deeds_left=5, alignment='neutral', is_active=True)
    return render_template('admin/edit_god.html', god=god, is_new=True)


@app.route('/admin/gods/<int:god_id>/delete', methods=['POST'])
@admin_required
def admin_delete_god(god_id):
    """Delete a god."""
    god = db.session.get(God, god_id)
    if god:
        db.session.delete(god)
        db.session.commit()
        flash(f'God "{god.name}" deleted.', 'success')
    return redirect(url_for('admin_gods'))


@app.route('/admin/news/clear', methods=['POST'])
@admin_required
def admin_clear_news():
    """Clear all news entries."""
    count = NewsEntry.query.count()
    NewsEntry.query.delete()
    db.session.commit()
    flash(f'Cleared {count} news entries.', 'success')
    return redirect(url_for('admin_dashboard'))


@app.route('/admin/maintenance', methods=['POST'])
@admin_required
def admin_run_maintenance():
    """Run daily maintenance for all players."""
    players = Player.query.filter_by(is_npc=False).all()
    count = 0
    for player in players:
        if game_logic.daily_maintenance(player):
            count += 1
    db.session.commit()
    flash(f'Daily maintenance run for {count} player(s).', 'success')
    return redirect(url_for('admin_dashboard'))


# ==================== ADMIN: DOOR GUARDS ====================

@app.route('/admin/door-guards')
@admin_required
def admin_door_guards():
    """List all door guard types for editing."""
    guards = DoorGuard.query.order_by(DoorGuard.cost).all()
    return render_template('admin/door_guards.html', guards=guards)


@app.route('/admin/door-guards/<int:guard_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_door_guard(guard_id):
    """Edit a door guard type."""
    guard = db.session.get(DoorGuard, guard_id)
    if not guard:
        flash('Door guard not found.', 'error')
        return redirect(url_for('admin_door_guards'))

    if request.method == 'POST':
        guard.name = request.form.get('name', guard.name).strip()
        guard.cost = int(request.form.get('cost', guard.cost))
        guard.hps = int(request.form.get('hps', guard.hps))
        guard.attack = int(request.form.get('attack', guard.attack))
        guard.armor = int(request.form.get('armor', guard.armor))
        guard.allow_multiple = request.form.get('allow_multiple') == 'on'
        guard.description = request.form.get('description', guard.description).strip()
        db.session.commit()
        flash(f'Door guard "{guard.name}" updated.', 'success')
        return redirect(url_for('admin_door_guards'))

    return render_template('admin/edit_door_guard.html', guard=guard)


@app.route('/admin/door-guards/new', methods=['GET', 'POST'])
@admin_required
def admin_new_door_guard():
    """Create a new door guard type."""
    if request.method == 'POST':
        guard = DoorGuard(
            name=request.form.get('name', 'New Guard').strip(),
            cost=int(request.form.get('cost', 100)),
            hps=int(request.form.get('hps', 50)),
            attack=int(request.form.get('attack', 10)),
            armor=int(request.form.get('armor', 0)),
            allow_multiple=request.form.get('allow_multiple') == 'on',
            description=request.form.get('description', '').strip(),
        )
        db.session.add(guard)
        db.session.commit()
        flash(f'Door guard "{guard.name}" created.', 'success')
        return redirect(url_for('admin_door_guards'))

    guard = DoorGuard(name='', cost=100, hps=50, attack=10, armor=0, allow_multiple=False, description='')
    return render_template('admin/edit_door_guard.html', guard=guard, is_new=True)


@app.route('/admin/door-guards/<int:guard_id>/delete', methods=['POST'])
@admin_required
def admin_delete_door_guard(guard_id):
    """Delete a door guard type."""
    guard = db.session.get(DoorGuard, guard_id)
    if guard:
        # Clear references from players using this guard type
        Player.query.filter_by(door_guard_id=guard_id).update(
            {'door_guard_id': None, 'door_guard_count': 0})
        db.session.delete(guard)
        db.session.commit()
        flash(f'Door guard "{guard.name}" deleted.', 'success')
    return redirect(url_for('admin_door_guards'))


# ==================== ADMIN: MOAT CREATURES ====================

@app.route('/admin/moat-creatures')
@admin_required
def admin_moat_creatures():
    """List all moat creature types for editing."""
    creatures = MoatCreature.query.order_by(MoatCreature.cost).all()
    return render_template('admin/moat_creatures.html', creatures=creatures)


@app.route('/admin/moat-creatures/<int:creature_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_moat_creature(creature_id):
    """Edit a moat creature type."""
    creature = db.session.get(MoatCreature, creature_id)
    if not creature:
        flash('Moat creature not found.', 'error')
        return redirect(url_for('admin_moat_creatures'))

    if request.method == 'POST':
        creature.name = request.form.get('name', creature.name).strip()
        creature.cost = int(request.form.get('cost', creature.cost))
        creature.hps = int(request.form.get('hps', creature.hps))
        creature.attack = int(request.form.get('attack', creature.attack))
        creature.armor = int(request.form.get('armor', creature.armor))
        creature.description = request.form.get('description', creature.description).strip()
        db.session.commit()
        flash(f'Moat creature "{creature.name}" updated.', 'success')
        return redirect(url_for('admin_moat_creatures'))

    return render_template('admin/edit_moat_creature.html', creature=creature)


@app.route('/admin/moat-creatures/new', methods=['GET', 'POST'])
@admin_required
def admin_new_moat_creature():
    """Create a new moat creature type."""
    if request.method == 'POST':
        creature = MoatCreature(
            name=request.form.get('name', 'New Creature').strip(),
            cost=int(request.form.get('cost', 1000)),
            hps=int(request.form.get('hps', 50)),
            attack=int(request.form.get('attack', 15)),
            armor=int(request.form.get('armor', 10)),
            description=request.form.get('description', '').strip(),
        )
        db.session.add(creature)
        db.session.commit()
        flash(f'Moat creature "{creature.name}" created.', 'success')
        return redirect(url_for('admin_moat_creatures'))

    creature = MoatCreature(name='', cost=1000, hps=50, attack=15, armor=10, description='')
    return render_template('admin/edit_moat_creature.html', creature=creature, is_new=True)


@app.route('/admin/moat-creatures/<int:creature_id>/delete', methods=['POST'])
@admin_required
def admin_delete_moat_creature(creature_id):
    """Delete a moat creature type."""
    creature = db.session.get(MoatCreature, creature_id)
    if creature:
        # Clear references from king records using this creature type
        KingRecord.query.filter_by(moat_creature_id=creature_id).update(
            {'moat_creature_id': None, 'moat_guards': 0})
        db.session.delete(creature)
        db.session.commit()
        flash(f'Moat creature "{creature.name}" deleted.', 'success')
    return redirect(url_for('admin_moat_creatures'))


# ==================== ADMIN: DRINKS ====================

@app.route('/admin/drinks')
@admin_required
def admin_drinks():
    """List all custom drinks for editing."""
    drinks = Drink.query.order_by(Drink.times_ordered.desc()).all()
    return render_template('admin/drinks.html', drinks=drinks)


@app.route('/admin/drinks/<int:drink_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_drink(drink_id):
    """Edit a drink."""
    drink = db.session.get(Drink, drink_id)
    if not drink:
        flash('Drink not found.', 'error')
        return redirect(url_for('admin_drinks'))

    if request.method == 'POST':
        drink.name = request.form.get('name', drink.name).strip()
        drink.creator_name = request.form.get('creator_name', drink.creator_name).strip()
        drink.comment = request.form.get('comment', drink.comment).strip()
        drink.secret = request.form.get('secret') == 'on'
        drink.times_ordered = int(request.form.get('times_ordered', drink.times_ordered))
        for attr, _ in DRINK_INGREDIENTS:
            setattr(drink, attr, int(request.form.get(attr, 0) or 0))
        db.session.commit()
        flash(f'Drink "{drink.name}" updated.', 'success')
        return redirect(url_for('admin_drinks'))

    iv = {attr: getattr(drink, attr, 0) for attr, _ in DRINK_INGREDIENTS}
    return render_template('admin/edit_drink.html', drink=drink,
                           ingredients=DRINK_INGREDIENTS, ingredient_values=iv)


@app.route('/admin/drinks/new', methods=['GET', 'POST'])
@admin_required
def admin_new_drink():
    """Create a new drink via admin."""
    if request.method == 'POST':
        drink = Drink(
            name=request.form.get('name', 'New Drink').strip(),
            creator_name=request.form.get('creator_name', 'Admin').strip(),
            comment=request.form.get('comment', '').strip(),
            secret=request.form.get('secret') == 'on',
        )
        for attr, _ in DRINK_INGREDIENTS:
            setattr(drink, attr, int(request.form.get(attr, 0) or 0))
        db.session.add(drink)
        db.session.commit()
        flash(f'Drink "{drink.name}" created.', 'success')
        return redirect(url_for('admin_drinks'))

    drink = Drink(name='', creator_name='Admin', comment='', secret=False)
    iv = {attr: 0 for attr, _ in DRINK_INGREDIENTS}
    return render_template('admin/edit_drink.html', drink=drink,
                           ingredients=DRINK_INGREDIENTS, ingredient_values=iv, is_new=True)


@app.route('/admin/drinks/<int:drink_id>/delete', methods=['POST'])
@admin_required
def admin_delete_drink(drink_id):
    """Delete a drink."""
    drink = db.session.get(Drink, drink_id)
    if drink:
        db.session.delete(drink)
        db.session.commit()
        flash(f'Drink "{drink.name}" deleted.', 'success')
    return redirect(url_for('admin_drinks'))


# ==================== ADMIN: LEVELS ====================

@app.route('/admin/levels', methods=['GET', 'POST'])
@admin_required
def admin_levels():
    """Edit level XP requirements."""
    from models import LEVEL_XP

    if request.method == 'POST':
        changes = 0
        for lvl in range(1, 101):
            form_val = request.form.get(f'level_{lvl}')
            if form_val is not None:
                new_xp = int(form_val)
                if LEVEL_XP.get(lvl) != new_xp:
                    LEVEL_XP[lvl] = new_xp
                    changes += 1
        if changes:
            # Persist to game config for survival across restarts
            import json
            GameConfig.set('level_xp_table', json.dumps(LEVEL_XP))
            flash(f'Level XP table updated ({changes} level(s) changed).', 'success')
        else:
            flash('No changes detected.', 'info')
        return redirect(url_for('admin_levels'))

    return render_template('admin/levels.html', levels=LEVEL_XP, level_count=100)


# ==================== ADMIN: TEAMS ====================

@app.route('/admin/teams')
@admin_required
def admin_teams():
    """List all teams for editing."""
    teams = Team.query.order_by(Team.name).all()
    return render_template('admin/teams.html', teams=teams)


@app.route('/admin/teams/<int:team_id>', methods=['GET', 'POST'])
@admin_required
def admin_edit_team(team_id):
    """Edit a team's details."""
    team = db.session.get(Team, team_id)
    if not team:
        flash('Team not found.', 'error')
        return redirect(url_for('admin_teams'))

    if request.method == 'POST':
        action = request.form.get('action', 'save')

        if action == 'add_member':
            player_name = request.form.get('player_name', '').strip()
            if player_name:
                p = Player.query.filter_by(name=player_name).first()
                if not p:
                    flash(f'Player "{player_name}" not found.', 'error')
                elif TeamMember.query.filter_by(player_id=p.id).first():
                    flash(f'{p.name} is already on a team.', 'error')
                else:
                    member = TeamMember(team_id=team.id, player_id=p.id)
                    db.session.add(member)
                    p.team_name = team.name
                    db.session.commit()
                    flash(f'{p.name} added to team.', 'success')
            return redirect(url_for('admin_edit_team', team_id=team_id))

        if action == 'remove_member':
            member_id = request.form.get('member_id')
            if member_id:
                member = db.session.get(TeamMember, int(member_id))
                if member and member.team_id == team.id:
                    if member.player:
                        member.player.team_name = ''
                    db.session.delete(member)
                    db.session.commit()
                    flash('Member removed.', 'success')
            return redirect(url_for('admin_edit_team', team_id=team_id))

        # Standard team field updates
        team.name = request.form.get('name', team.name).strip()
        leader_id = request.form.get('leader_id')
        if leader_id:
            new_leader_id = int(leader_id)
            if not TeamMember.query.filter_by(team_id=team.id, player_id=new_leader_id).first():
                flash('Leader must be an existing member of this team.', 'error')
                return redirect(url_for('admin_edit_team', team_id=team_id))
            team.leader_id = new_leader_id
        team.wins = int(request.form.get('wins', team.wins))
        team.losses = int(request.form.get('losses', team.losses))
        team.treasury = int(request.form.get('treasury', team.treasury))
        team.town_control = request.form.get('town_control') == 'on'
        team.town_control_days = int(request.form.get('town_control_days', team.town_control_days))
        # Update team_name on all members
        for member in team.members:
            if member.player:
                member.player.team_name = team.name
        db.session.commit()
        flash(f'Team "{team.name}" updated.', 'success')
        return redirect(url_for('admin_teams'))

    players = Player.query.order_by(Player.name).all()
    return render_template('admin/edit_team.html', team=team, players=players)


@app.route('/admin/teams/new', methods=['GET', 'POST'])
@admin_required
def admin_new_team():
    """Create a new team."""
    if request.method == 'POST':
        name = request.form.get('name', '').strip()
        leader_id = request.form.get('leader_id')
        if not name or not leader_id:
            flash('Team name and leader are required.', 'error')
            players = Player.query.order_by(Player.name).all()
            return render_template('admin/edit_team.html', team=None, players=players)

        leader = db.session.get(Player, int(leader_id))
        if not leader:
            flash('Leader not found.', 'error')
            players = Player.query.order_by(Player.name).all()
            return render_template('admin/edit_team.html', team=None, players=players)

        if Team.query.filter_by(name=name).first():
            flash('A team with that name already exists.', 'error')
            players = Player.query.order_by(Player.name).all()
            return render_template('admin/edit_team.html', team=None, players=players)

        if TeamMember.query.filter_by(player_id=leader.id).first():
            flash(f'{leader.name} is already on another team.', 'error')
            players = Player.query.order_by(Player.name).all()
            return render_template('admin/edit_team.html', team=None, players=players)

        team = Team(name=name, leader_id=int(leader_id))
        db.session.add(team)
        db.session.flush()
        # Add leader as member
        member = TeamMember(team_id=team.id, player_id=int(leader_id))
        db.session.add(member)
        leader.team_name = name
        db.session.commit()
        flash(f'Team "{name}" created.', 'success')
        return redirect(url_for('admin_teams'))

    players = Player.query.order_by(Player.name).all()
    return render_template('admin/edit_team.html', team=None, players=players)


@app.route('/admin/teams/<int:team_id>/delete', methods=['POST'])
@admin_required
def admin_delete_team(team_id):
    """Delete a team."""
    team = db.session.get(Team, team_id)
    if team:
        # Clear team_name on all members
        for member in team.members:
            if member.player:
                member.player.team_name = ''
        name = team.name
        db.session.delete(team)
        db.session.commit()
        flash(f'Team "{name}" deleted.', 'success')
    return redirect(url_for('admin_teams'))


# ==================== BEER STEALING ====================

@app.route('/beer_stealing', methods=['GET', 'POST'])
@login_required
def beer_stealing():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.is_imprisoned:
        flash("You cannot steal beer while imprisoned.", 'error')
        return redirect(url_for('main_menu'))
    if request.method == 'POST':
        success, msg, log = game_logic.beer_stealing(player)
        db.session.commit()
        if log:
            session['beer_stealing_log'] = log
        flash(msg, 'success' if success else 'error')
        return redirect(url_for('beer_stealing'))
    log = session.pop('beer_stealing_log', [])
    return render_template('beer_stealing.html', player=player, log=log)


# ==================== DORMITORY ====================

@app.route('/dormitory')
@login_required
def dormitory():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.is_imprisoned:
        flash("You cannot visit the dormitory while imprisoned.", 'error')
        return redirect(url_for('main_menu'))
    guests = Player.query.filter(
        Player.id != player.id, Player.hp > 0
    ).order_by(Player.level.desc()).all()
    return render_template('dormitory.html', player=player, guests=guests)


@app.route('/dormitory/fight', methods=['POST'])
@login_required
def dormitory_fight():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    num_opponents = safe_int(request.form.get('num_opponents', 1), 1)
    result = game_logic.dormitory_fistfight(player, num_opponents)
    db.session.commit()
    if result.get('log'):
        session['fistfight_log'] = result['log']
        return redirect(url_for('fistfight_result'))
    flash(result.get('message', ''), 'success' if result.get('success') else 'error')
    return redirect(url_for('dormitory'))


@app.route('/dormitory/fight/result')
@login_required
def fistfight_result():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    log = session.pop('fistfight_log', [])
    return render_template('fistfight_result.html', player=player, combat_log=log)


# ==================== GYM ====================

@app.route('/gym', methods=['GET', 'POST'])
@login_required
def gym():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.is_imprisoned:
        flash("You cannot visit the gym while imprisoned.", 'error')
        return redirect(url_for('main_menu'))
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'barrel_lift':
            success, msg = game_logic.gym_barrel_lift(player)
            db.session.commit()
            flash(msg, 'success' if success else 'error')
        elif action == 'massage':
            success, msg = game_logic.gym_massage(player)
            db.session.commit()
            flash(msg, 'success' if success else 'error')
        return redirect(url_for('gym'))
    records = BarrelLiftRecord.query.order_by(
        BarrelLiftRecord.weight.desc()).limit(10).all()
    return render_template('gym.html', player=player, records=records)


# ==================== GROGGO'S MAD MAGE ====================

@app.route('/groggo', methods=['GET', 'POST'])
@login_required
def groggo():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.is_imprisoned:
        flash("You cannot visit Groggo while imprisoned.", 'error')
        return redirect(url_for('main_menu'))
    if request.method == 'POST':
        action = request.form.get('action', '')
        target_id = safe_int(request.form.get('target_id', 0))
        if action == 'disease':
            success, msg = game_logic.groggo_disease(player, target_id)
        elif action == 'summon_demon':
            success, msg = game_logic.groggo_summon_demon(player, target_id)
        else:
            success, msg = False, "Unknown action."
        db.session.commit()
        flash(msg, 'success' if success else 'error')
        return redirect(url_for('groggo'))
    return render_template('groggo.html', player=player, diseases=DISEASES)


# ==================== GIGOLO HALL OF DREAMS ====================

@app.route('/gigolo', methods=['GET', 'POST'])
@login_required
def gigolo():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.is_imprisoned:
        flash("You cannot visit the Hall of Dreams while imprisoned.", 'error')
        return redirect(url_for('main_menu'))
    if request.method == 'POST':
        gigolo_id = safe_int(request.form.get('gigolo_id', 0))
        success, msg = game_logic.visit_gigolo(player, gigolo_id)
        db.session.commit()
        flash(msg, 'success' if success else 'error')
        return redirect(url_for('gigolo'))
    return render_template('gigolo.html', player=player, gigolos=GIGOLOS)


# ==================== GOOD DEEDS ====================

@app.route('/good_deeds', methods=['GET', 'POST'])
@login_required
def good_deeds():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'poor':
            amount = safe_int(request.form.get('amount', 0))
            success, msg = game_logic.good_deed_poor(player, amount)
        elif action == 'church':
            amount = safe_int(request.form.get('amount', 0))
            success, msg = game_logic.good_deed_church(player, amount)
        elif action == 'blessing':
            amount = safe_int(request.form.get('amount', 0))
            success, msg = game_logic.good_deed_blessing(player, amount)
        else:
            success, msg = False, "Unknown deed."
        db.session.commit()
        flash(msg, 'success' if success else 'error')
        return redirect(url_for('good_deeds'))
    return render_template('good_deeds.html', player=player)


# ==================== DARK DEEDS ====================

@app.route('/dark_deeds', methods=['GET', 'POST'])
@login_required
def dark_deeds():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.is_imprisoned:
        flash("You cannot perform dark deeds while imprisoned.", 'error')
        return redirect(url_for('main_menu'))
    players = Player.query.filter(Player.id != player.id).order_by(Player.name).all()
    children = Child.query.all()
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'kidnap':
            child_id = safe_int(request.form.get('child_id', 0))
            success, msg = game_logic.kidnap_child(player, child_id)
        elif action == 'poison':
            child_id = safe_int(request.form.get('child_id', 0))
            success, msg = game_logic.poison_child(player, child_id)
        elif action == 'murder':
            target_id = safe_int(request.form.get('target_id', 0))
            success, msg = game_logic.murder_player(player, target_id)
        elif action == 'loot':
            success, msg = game_logic.loot_chest(player)
        else:
            success, msg = False, "Unknown action."
        db.session.commit()
        flash(msg, 'success' if success else 'error')
        return redirect(url_for('dark_deeds'))
    return render_template('dark_deeds.html', player=player,
                           players=players, children=children)


# ==================== DEATH MAZE ====================

@app.route('/death_maze', methods=['GET', 'POST'])
@login_required
def death_maze():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.is_imprisoned:
        flash("You cannot enter the Death Maze while imprisoned.", 'error')
        return redirect(url_for('main_menu'))
    if request.method == 'POST':
        result = game_logic.haunting_check(player)
        db.session.commit()
        flash(result.get('message', ''), 'success' if result.get('success') else 'warning')
        return redirect(url_for('death_maze'))
    return render_template('death_maze.html', player=player)


# ==================== ICE CAVES ====================

@app.route('/ice_caves', methods=['GET', 'POST'])
@login_required
def ice_caves():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.is_imprisoned:
        flash("You cannot enter the Ice Caves while imprisoned.", 'error')
        return redirect(url_for('main_menu'))
    if request.method == 'POST':
        result = game_logic.haunting_check(player)
        db.session.commit()
        flash(result.get('message', ''), 'success' if result.get('success') else 'warning')
        return redirect(url_for('ice_caves'))
    return render_template('ice_caves.html', player=player)


# ==================== GODWORLD ====================

@app.route('/godworld')
@login_required
def godworld():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if not getattr(player, 'is_immortal', False):
        flash("Only immortal players may enter Godworld.", 'error')
        return redirect(url_for('main_menu'))
    gods = God.query.all()
    return render_template('godworld.html', player=player, gods=gods)


# ==================== INN CHAT ====================

@app.route('/inn/chat', methods=['GET', 'POST'])
@login_required
def inn_chat():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if request.method == 'POST':
        message = request.form.get('message', '').strip()
        if message:
            success, msg = game_logic.inn_chat_send(player, message)
            db.session.commit()
            if not success:
                flash(msg, 'error')
        return redirect(url_for('inn_chat'))
    messages = game_logic.inn_chat_get()
    return render_template('inn_chat.html', player=player, messages=messages)


# ==================== COMBAT TRAINING ====================

@app.route('/combat/train', methods=['GET', 'POST'])
@login_required
def combat_train():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if request.method == 'POST':
        move = request.form.get('move', '')
        success, msg = game_logic.train_combat_move(player, move)
        db.session.commit()
        flash(msg, 'success' if success else 'error')
        return redirect(url_for('combat_train'))
    return render_template('combat_training.html', player=player,
                           moves=CLOSE_COMBAT_MOVES, ranks=COMBAT_SKILL_RANKS)


# ==================== EQUIPMENT SWAP ====================

@app.route('/equipment/swap', methods=['GET', 'POST'])
@login_required
def equipment_swap():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if request.method == 'POST':
        action = request.form.get('action', '')
        if action == 'offer':
            item_id = safe_int(request.form.get('item_id', 0))
            target_id = safe_int(request.form.get('target_id', 0))
            wanted_id = safe_int(request.form.get('wanted_id', 0))
            success, msg = game_logic.equipment_swap_offer(
                player, target_id, item_id, wanted_id)
        elif action == 'respond':
            offer_id = safe_int(request.form.get('offer_id', 0))
            accept = request.form.get('accept') == 'yes'
            success, msg = game_logic.equipment_swap_respond(
                player, offer_id, accept)
        else:
            success, msg = False, "Unknown action."
        db.session.commit()
        flash(msg, 'success' if success else 'error')
        return redirect(url_for('equipment_swap'))
    offers = EquipmentSwapOffer.query.filter(
        (EquipmentSwapOffer.target_id == player.id) |
        (EquipmentSwapOffer.offerer_id == player.id)
    ).all()
    inventory = InventoryItem.query.filter_by(player_id=player.id).all()
    players = Player.query.filter(Player.id != player.id).order_by(Player.name).all()
    return render_template('equipment_swap.html', player=player,
                           offers=offers, inventory=inventory, players=players)


# ==================== PRISON TORTURE ====================

@app.route('/prison/torture')
@login_required
def prison_torture():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if not player.is_imprisoned:
        flash("You are not in prison.", 'error')
        return redirect(url_for('main_menu'))
    return render_template('prison_torture.html', player=player)


# ==================== ORPHANAGE ====================

@app.route('/orphanage', methods=['GET', 'POST'])
@login_required
def orphanage():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if request.method == 'POST':
        child_id = safe_int(request.form.get('child_id', 0))
        success, msg = game_logic.send_to_orphanage(player, child_id)
        db.session.commit()
        flash(msg, 'success' if success else 'error')
        return redirect(url_for('orphanage'))
    children = Child.query.filter_by(parent_id=None).all()
    player_children = Child.query.filter_by(parent_id=player.id).all()
    return render_template('orphanage.html', player=player,
                           children=children, player_children=player_children)


# ==================== SUPREME BEING ====================

@app.route('/supreme_being', methods=['GET', 'POST'])
@login_required
def supreme_being():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if request.method == 'POST':
        door = request.form.get('door', '')
        success, msg = game_logic.supreme_being_encounter(player, door)
        db.session.commit()
        flash(msg, 'success' if success else 'error')
        return redirect(url_for('supreme_being'))
    return render_template('supreme_being.html', player=player)


# ==================== SHOP HAGGLE ====================

@app.route('/shop/haggle/<int:item_id>', methods=['POST'])
@login_required
def shop_haggle(item_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    item = db.session.get(Item, item_id)
    if not item:
        flash("Item not found.", 'error')
        return redirect(url_for('weapon_shop'))
    new_price = game_logic.haggle_price(player, item.value)
    if new_price < item.value:
        discount = item.value - new_price
        flash(f"You haggled the price of {item.name} down by {discount}g! New price: {new_price}g.", 'success')
        session['haggle_prices'] = session.get('haggle_prices', {})
        session['haggle_prices'][str(item_id)] = new_price
        session.modified = True
    else:
        flash("The shopkeeper won't budge on the price.", 'error')
    db.session.commit()
    # Redirect back to the correct shop based on item type
    if item.item_type != 'Weapon':
        return redirect(url_for('armor_shop'))
    return redirect(url_for('weapon_shop'))


# ==================== KING SPELLS ====================

@app.route('/king/angel/<int:target_id>', methods=['POST'])
@login_required
def king_angel(target_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    result = game_logic.royal_angel_spell(player, target_id)
    db.session.commit()
    flash(result['message'], 'success' if result['success'] else 'error')
    return redirect(url_for('castle'))


@app.route('/king/avenger/<int:target_id>', methods=['POST'])
@login_required
def king_avenger(target_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    result = game_logic.royal_avenger_spell(player, target_id)
    db.session.commit()
    flash(result['message'], 'success' if result['success'] else 'error')
    return redirect(url_for('castle'))


# ==================== ALCHEMIST CRAFT ====================

@app.route('/alchemist/craft', methods=['GET', 'POST'])
@login_required
def alchemist_craft():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    if player.player_class != 'Alchemist':
        flash("Only Alchemists can craft poisons.", 'error')
        return redirect(url_for('main_menu'))
    if request.method == 'POST':
        poison_level = safe_int(request.form.get('poison_level', 0))
        success, msg = game_logic.craft_poison(player, poison_level)
        db.session.commit()
        flash(msg, 'success' if success else 'error')
        return redirect(url_for('alchemist_craft'))
    return render_template('alchemist_craft.html', player=player,
                           poison_levels=POISON_LEVELS)


# ==================== NPC RECRUITMENT ====================

@app.route('/npc/recruit/<int:npc_id>', methods=['POST'])
@login_required
def npc_recruit(npc_id):
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    result = game_logic.recruit_npc(player, npc_id)
    db.session.commit()
    flash(result['message'], 'success' if result['success'] else 'error')
    return redirect(url_for('npc_list'))


# ==================== INIT ====================

def load_custom_level_xp():
    """Load custom level XP table from config if it exists."""
    try:
        import json
        from models import LEVEL_XP
        custom = GameConfig.get('level_xp_table')
        if custom:
            data = json.loads(custom)
            for k, v in data.items():
                LEVEL_XP[int(k)] = int(v)
    except Exception:
        pass


def init_db():
    """Initialize the database and seed data."""
    with app.app_context():
        db.create_all()
        seed_all()
        load_custom_level_xp()


def start_npc_scheduler():
    """Start the background scheduler for NPC actions."""
    try:
        from apscheduler.schedulers.background import BackgroundScheduler
    except ImportError:
        logger.warning("APScheduler not installed - NPC actions will not run automatically. "
                       "Install with: pip install apscheduler")
        return None

    tick_minutes = 5
    try:
        with app.app_context():
            tick_minutes = int(GameConfig.get('npc_tick_minutes', '5'))
    except Exception:
        pass

    def npc_tick_job():
        with app.app_context():
            if GameConfig.get('npc_enabled', 'true').lower() == 'true':
                npc_engine.run_npc_tick()

    scheduler = BackgroundScheduler(daemon=True)
    scheduler.add_job(
        npc_tick_job,
        'interval',
        minutes=tick_minutes,
        id='npc_tick',
        name='NPC Action Tick',
        max_instances=1,
        coalesce=True,
    )
    scheduler.start()
    logger.info("NPC scheduler started (every %d minutes)", tick_minutes)
    return scheduler


if __name__ == '__main__':
    npc_scheduler = start_npc_scheduler()

    ssl_context = None
    if SSL_CERT and SSL_KEY:
        ssl_context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        ssl_context.load_cert_chain(SSL_CERT, SSL_KEY)
        logger.info("SSL enabled with cert=%s key=%s", SSL_CERT, SSL_KEY)
    elif SSL_ADHOC:
        ssl_context = 'adhoc'
        logger.info("SSL enabled with ad-hoc self-signed certificate")

    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, use_reloader=False,
            ssl_context=ssl_context)
