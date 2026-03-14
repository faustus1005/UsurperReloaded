"""Usurper ReLoaded - Web Edition

A fantasy RPG game, converted from BBS door game to web application.
Original by Jakob Dangarden, web conversion for modern access.
"""

import os
import ssl
import random
import logging
from functools import wraps
from datetime import datetime, timezone

from flask import (Flask, render_template, redirect, url_for, flash, request,
                   session, jsonify, abort)
from flask_login import (LoginManager, login_user, logout_user, login_required,
                          current_user)
from werkzeug.security import generate_password_hash

from models import (
    db, User, Player, Item, InventoryItem, Monster, Mail, NewsEntry,
    GameConfig, Team, TeamMember, KingRecord, Bounty, Relationship,
    Child, RoyalQuest, God, TeamRecord,
    RACES, CLASSES, RACE_BONUSES, CLASS_BONUSES,
    SPELLCASTER_CLASSES, SPELLS, LEVEL_XP, EQUIPMENT_SLOTS, ITEM_TYPES
)
import game as game_logic
from seed import seed_all
import npc_engine

logger = logging.getLogger(__name__)

app = Flask(__name__)
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', os.urandom(32).hex())
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///' + os.path.join(
    os.path.dirname(os.path.abspath(__file__)), 'usurper.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# SSL configuration via environment variables
SSL_CERT = os.environ.get('SSL_CERT')
SSL_KEY = os.environ.get('SSL_KEY')
SSL_ADHOC = os.environ.get('SSL_ADHOC', '').lower() in ('1', 'true', 'yes')

if SSL_CERT or SSL_ADHOC:
    app.config['SESSION_COOKIE_SECURE'] = True
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

db.init_app(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'
login_manager.login_message_category = 'info'


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


def get_player():
    """Get the current user's player character."""
    if not current_user.is_authenticated:
        return None
    return Player.query.filter_by(user_id=current_user.id).first()


def admin_required(f):
    """Decorator that requires the current user to be an admin."""
    @wraps(f)
    @login_required
    def decorated_function(*args, **kwargs):
        if not current_user.is_admin:
            abort(403)
        return f(*args, **kwargs)
    return decorated_function


# --- Context processor for templates ---
@app.context_processor
def inject_game_data():
    player = get_player() if current_user.is_authenticated else None
    town_name = GameConfig.get('town_name', 'Dolingen')
    return {
        'player': player,
        'town_name': town_name,
        'is_admin': current_user.is_admin if current_user.is_authenticated else False,
        'RACES': RACES,
        'CLASSES': CLASSES,
        'SPELLS': SPELLS,
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

            # Run daily maintenance
            player = get_player()
            if player:
                if game_logic.daily_maintenance(player):
                    db.session.commit()
                    flash('A new day dawns. Your daily actions have been refreshed!', 'info')

            return redirect(url_for('index'))
        flash('Invalid username or password.', 'error')

    return render_template('login.html')


@app.route('/logout')
@login_required
def logout():
    logout_user()
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
                           LEVEL_XP=LEVEL_XP)


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
    return render_template('dungeon.html', dungeon_name=dungeon_name)


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

    dungeon_level = min(player.level, 100)

    # 30% chance of non-combat event
    if random.randint(1, 100) <= 30:
        # 50% chance of new interactive event vs old simple event
        if random.randint(1, 2) == 1:
            event = game_logic.get_random_dungeon_event()
            session['dungeon_event'] = event
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


# ==================== TOWN LOCATIONS ====================

@app.route('/inn')
@login_required
def inn():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    inn_name = GameConfig.get('inn_name', "The Dragon's Flagon")
    rest_cost = player.level * 5 + 10
    return render_template('inn.html', inn_name=inn_name, rest_cost=rest_cost)


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


@app.route('/bank')
@login_required
def bank():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))
    return render_template('bank.html')


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


# ==================== SHOPS ====================

@app.route('/shop/weapons')
@login_required
def weapon_shop():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    items = Item.query.filter_by(in_shop=True, item_type='Weapon').order_by(Item.value).all()
    shop_name = GameConfig.get('weapon_shop_name', 'Weapon Shop')
    return render_template('shop.html', items=items, shop_name=shop_name, shop_type='weapons')


@app.route('/shop/armor')
@login_required
def armor_shop():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    armor_types = ['Body', 'Shield', 'Head', 'Arms', 'Hands', 'Legs', 'Feet',
                   'Waist', 'Neck', 'Face', 'Around Body']
    items = Item.query.filter(
        Item.in_shop == True,
        Item.item_type.in_(armor_types)
    ).order_by(Item.item_type, Item.value).all()
    shop_name = GameConfig.get('armor_shop_name', 'Armor Shop')
    return render_template('shop.html', items=items, shop_name=shop_name, shop_type='armor')


@app.route('/shop/magic')
@login_required
def magic_shop():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

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
                           EQUIPMENT_SLOTS=EQUIPMENT_SLOTS)


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


# ==================== LEVEL MASTER ====================

@app.route('/level_master')
@login_required
def level_master():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    master_name = GameConfig.get('level_master_name', 'Gandalf the Trainer')
    can_level = player.can_level_up()
    xp_needed = player.xp_for_next_level()
    return render_template('level_master.html', master_name=master_name,
                           can_level=can_level, xp_needed=xp_needed)


@app.route('/level_master/train', methods=['POST'])
@login_required
def train_level():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    success, msg = game_logic.level_up(player)
    if success:
        news = NewsEntry(
            player_id=player.id,
            category='social',
            message=f"{player.name} has advanced to level {player.level}!"
        )
        db.session.add(news)
    db.session.commit()
    flash(msg, 'success' if success else 'warning')
    return redirect(url_for('level_master'))


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

    return render_template('castle.html', king=king, king_record=king_record,
                           history=history, prisoners=prisoners)


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


@app.route('/castle/hire_guards', methods=['POST'])
@login_required
def hire_guards():
    player = get_player()
    if not player or not player.is_king:
        flash("Only the ruler can do this.", 'error')
        return redirect(url_for('castle'))

    king_record = KingRecord.query.filter_by(player_id=player.id, is_current=True).first()
    if not king_record:
        flash("No active reign found.", 'error')
        return redirect(url_for('castle'))

    try:
        count = int(request.form.get('count', 1))
    except ValueError:
        count = 1

    success, msg = game_logic.king_hire_guards(king_record, count)
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

    if player.is_imprisoned:
        flash("You cannot visit the tavern while imprisoned.", 'error')
        return redirect(url_for('main_menu'))

    drink_cost = 10 + player.level * 2
    return render_template('tavern.html', drink_cost=drink_cost)


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

    return render_template('love_corner.html', relationships=relationships,
                           spouse=spouse, proposals=proposals, players_list=players_list)


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

    return render_template('temple.html', gods=gods, current_god=current_god)


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

    items = Item.query.filter_by(in_shop=True, shop_category='healing').order_by(Item.value).all()
    return render_template('shop.html', items=items, shop_name='The Healing Hut',
                           shop_type='healing')


@app.route('/shop/general')
@login_required
def general_store():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    items = Item.query.filter_by(in_shop=True, shop_category='general').order_by(Item.value).all()
    return render_template('shop.html', items=items, shop_name='General Store',
                           shop_type='general')


@app.route('/shop/shady')
@login_required
def shady_dealer():
    player = get_player()
    if not player:
        return redirect(url_for('create_character'))

    items = Item.query.filter_by(in_shop=True, shop_category='shady').order_by(Item.value).all()
    return render_template('shop.html', items=items, shop_name='The Dark Alley',
                           shop_type='shady')


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

    result_text = game_logic.resolve_dungeon_event(player, event_id, choice)
    session.pop('dungeon_event', None)
    db.session.commit()

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
        player.weapon_power = int(request.form.get('weapon_power', player.weapon_power))
        player.armor_power = int(request.form.get('armor_power', player.armor_power))
        player.monster_kills = int(request.form.get('monster_kills', player.monster_kills))
        player.player_kills = int(request.form.get('player_kills', player.player_kills))
        player.healing_potions = int(request.form.get('healing_potions', player.healing_potions))
        player.is_poisoned = request.form.get('is_poisoned') == 'on'
        player.is_blind = request.form.get('is_blind') == 'on'
        player.has_plague = request.form.get('has_plague') == 'on'
        player.is_king = request.form.get('is_king') == 'on'
        player.is_imprisoned = request.form.get('is_imprisoned') == 'on'
        player.is_god = request.form.get('is_god') == 'on'
        db.session.commit()
        flash(f'Player "{player.name}" updated.', 'success')
        return redirect(url_for('admin_players',
                                show='npcs' if player.is_npc else 'humans'))

    return render_template('admin/edit_player.html', player=player,
                           races=RACES, classes=CLASSES)


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
    Mail.query.filter((Mail.sender_id == player_id) | (Mail.receiver_id == player_id)).delete()
    NewsEntry.query.filter_by(player_id=player_id).delete()
    TeamMember.query.filter_by(player_id=player_id).delete()
    Bounty.query.filter((Bounty.target_id == player_id) | (Bounty.poster_id == player_id)).delete()
    RoyalQuest.query.filter(
        (RoyalQuest.initiator_id == player_id) | (RoyalQuest.occupier_id == player_id)
    ).delete()
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


# ==================== INIT ====================

def init_db():
    """Initialize the database and seed data."""
    with app.app_context():
        db.create_all()
        seed_all()


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
    init_db()
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
    app.run(debug=True, host='0.0.0.0', port=port, use_reloader=False,
            ssl_context=ssl_context)
