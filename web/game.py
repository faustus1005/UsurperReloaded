"""Core game logic for Usurper ReLoaded - combat, leveling, dungeon events."""

import random
from datetime import datetime, timezone
from models import (
    db, Player, Monster, Item, InventoryItem, NewsEntry, Mail,
    Team, TeamMember, KingRecord, Bounty, Relationship,
    Child, RoyalQuest, God, TeamRecord, HomeChestItem, GameConfig,
    MoatCreature, RoyalGuard, DoorGuard, Drink,
    RACE_BONUSES, CLASS_BONUSES, LEVEL_XP, SPELLS, SPELLCASTER_CLASSES, RACES,
    DRINK_INGREDIENTS
)


def create_character(player, name, race, player_class, sex):
    """Initialize a new character with race/class bonuses."""
    player.name = name
    player.race = race
    player.player_class = player_class
    player.sex = sex
    player.level = 1
    player.experience = 0
    player.gold = 100
    player.bank_gold = 0
    player.healing_potions = 2

    # Base stats
    base_str = 10
    base_def = 10
    base_sta = 10
    base_agi = 10
    base_cha = 10
    base_dex = 10
    base_wis = 10
    base_hp = 50
    base_mana = 0

    # Apply race bonuses
    rb = RACE_BONUSES.get(race, [0]*9)
    base_str += rb[0]
    base_def += rb[1]
    base_sta += rb[2]
    base_agi += rb[3]
    base_cha += rb[4]
    base_dex += rb[5]
    base_wis += rb[6]
    base_hp += rb[7]
    base_mana += rb[8]

    # Apply class bonuses
    cb = CLASS_BONUSES.get(player_class, [0]*9)
    base_str += cb[0]
    base_def += cb[1]
    base_sta += cb[2]
    base_agi += cb[3]
    base_cha += cb[4]
    base_dex += cb[5]
    base_wis += cb[6]
    base_hp += cb[7]
    base_mana += cb[8]

    player.strength = max(1, base_str)
    player.defence = max(1, base_def)
    player.stamina = max(1, base_sta)
    player.agility = max(1, base_agi)
    player.charisma = max(1, base_cha)
    player.dexterity = max(1, base_dex)
    player.wisdom = max(1, base_wis)
    player.hp = max(10, base_hp)
    player.max_hp = max(10, base_hp)

    # Mana for spellcasters
    if player_class in SPELLCASTER_CLASSES:
        player.mana = max(10, base_mana + 20)
        player.max_mana = player.mana
    else:
        player.mana = max(0, base_mana)
        player.max_mana = player.mana

    # Daily limits
    player.fights_remaining = 20
    player.player_fights = 3
    player.thefts_remaining = 2
    player.brawls_remaining = 2
    player.intimacy_acts = 5
    player.beauty_nest_visits = int(GameConfig.get('beauty_nest_visits_per_day', '3') or '3')
    player.dungeon_level = 1

    # Starting spells for spellcasters
    if player_class == 'Magician':
        player.spells_known = '1'  # Magic Missile
    elif player_class == 'Cleric':
        player.spells_known = '2'  # Heal
    elif player_class == 'Paladin':
        player.spells_known = '2'  # Heal
    elif player_class == 'Sage':
        player.spells_known = '1,2'  # Magic Missile + Heal
    elif player_class == 'Alchemist':
        player.spells_known = '11'  # Acid Splash
    elif player_class == 'Necromancer':
        player.spells_known = '49'  # Drain Life
    elif player_class == 'Monk':
        player.spells_known = '58'  # Inner Focus
    elif player_class == 'Witch Hunter':
        player.spells_known = '67'  # Silver Bolt


def level_up(player):
    """Level up a player, granting stat increases."""
    if not player.can_level_up():
        return False, "Not enough experience to level up."

    if player.level >= 100:
        return False, "You have reached the maximum level."

    player.level += 1

    # Stat increases based on class
    hp_gain = random.randint(3, 8)
    str_gain = random.randint(0, 2)
    def_gain = random.randint(0, 2)

    if player.player_class in ['Warrior', 'Barbarian']:
        hp_gain += random.randint(2, 5)
        str_gain += 1
    elif player.player_class in ['Paladin', 'Ranger']:
        hp_gain += random.randint(1, 3)
    elif player.player_class in ['Magician', 'Sage']:
        hp_gain += random.randint(0, 2)
    elif player.player_class == 'Assassin':
        str_gain += 1

    # Mana gain for casters
    mana_gain = 0
    if player.player_class in SPELLCASTER_CLASSES:
        mana_gain = random.randint(3, 8) + player.wisdom // 5
        if player.player_class in ['Magician', 'Sage']:
            mana_gain += random.randint(2, 5)

    player.max_hp += hp_gain
    player.hp = player.max_hp
    player.strength += str_gain
    player.defence += def_gain
    player.stamina += random.randint(0, 2)
    player.agility += random.randint(0, 1)
    player.dexterity += random.randint(0, 1)
    player.wisdom += random.randint(0, 1)
    player.max_mana += mana_gain
    player.mana = player.max_mana

    # Full heal on level up
    player.hp = player.max_hp
    player.mana = player.max_mana

    # Learn new spells at certain levels
    if player.player_class in SPELLCASTER_CLASSES:
        for spell_id, spell in SPELLS.items():
            if (spell['min_level'] <= player.level and
                player.player_class in spell['classes'] and
                not player.knows_spell(spell_id)):
                player.learn_spell(spell_id)
                break  # Learn one spell per level

    return True, f"Congratulations! You are now level {player.level}!"


def get_dungeon_monster(dungeon_level):
    """Select a random monster appropriate for the dungeon level."""
    monsters = Monster.query.filter(
        Monster.min_dungeon_level <= dungeon_level,
        Monster.max_dungeon_level >= dungeon_level
    ).all()

    if not monsters:
        # Fallback: get any monster
        monsters = Monster.query.all()

    if not monsters:
        return None

    monster = random.choice(monsters)

    # Scale monster stats based on dungeon level
    scale = 1.0 + (dungeon_level - monster.min_dungeon_level) * 0.15
    return {
        'id': monster.id,
        'name': monster.name,
        'hp': int(monster.hp * scale),
        'max_hp': int(monster.hp * scale),
        'strength': int(monster.strength * scale),
        'defence': int(monster.defence * scale),
        'weapon_power': int(monster.weapon_power * scale),
        'armor_power': int(monster.armor_power * scale),
        'experience': int(monster.experience * scale),
        'gold': int(monster.gold * scale * random.uniform(0.7, 1.3)),
        'phrase': monster.phrase,
        'weapon_name': monster.weapon_name,
        'is_poisonous': monster.is_poisonous,
        'has_disease': monster.has_disease,
        'magic_level': monster.magic_level,
        'aggression': monster.aggression,
        'drop_item_id': monster.drop_item_id,
    }


def calculate_attack(attacker_strength, attacker_weapon_power, attacker_level):
    """Calculate attack damage."""
    base = attacker_strength + attacker_weapon_power
    level_bonus = attacker_level * 2
    variation = random.randint(-base // 4, base // 4) if base > 4 else random.randint(0, 2)
    return max(1, base + level_bonus + variation)


def calculate_defense(defender_defence, defender_armor_power):
    """Calculate defense reduction."""
    base = defender_defence + defender_armor_power
    variation = random.randint(0, base // 3) if base > 3 else 0
    return max(0, base + variation)


def combat_round(player, monster):
    """Execute one round of player vs monster combat. Returns combat log messages."""
    log = []

    # Player attacks
    player_attack = calculate_attack(player.strength, player.weapon_power, player.level)
    monster_def = calculate_defense(monster['defence'], monster['armor_power'])
    player_damage = max(1, player_attack - monster_def)

    # Critical hit chance based on dexterity
    if random.randint(1, 100) <= 5 + player.dexterity // 3:
        player_damage = int(player_damage * 1.5)
        log.append(f"**Critical hit!** You strike the {monster['name']} for {player_damage} damage!")
    else:
        log.append(f"You attack the {monster['name']} for {player_damage} damage.")

    monster['hp'] -= player_damage

    if monster['hp'] <= 0:
        log.append(f"You have slain the {monster['name']}!")
        return log, 'victory'

    # Monster attacks
    monster_attack = calculate_attack(monster['strength'], monster['weapon_power'], 0)
    player_def = calculate_defense(player.defence, player.armor_power)
    monster_damage = max(1, monster_attack - player_def)

    # Monster critical
    if random.randint(1, 100) <= 5:
        monster_damage = int(monster_damage * 1.5)
        log.append(f"**Critical hit!** The {monster['name']} strikes you for {monster_damage} damage!")
    else:
        log.append(f"The {monster['name']} attacks you for {monster_damage} damage.")

    player.hp -= monster_damage

    # Poison chance
    if monster['is_poisonous'] and random.randint(1, 100) <= 15:
        player.is_poisoned = True
        log.append(f"The {monster['name']} has poisoned you!")

    if player.hp <= 0:
        player.hp = 0
        log.append(f"You have been defeated by the {monster['name']}!")
        return log, 'defeat'

    return log, 'ongoing'


def process_victory(player, monster):
    """Process rewards after defeating a monster."""
    messages = []

    # Experience
    xp_gain = monster['experience']
    player.experience += xp_gain
    messages.append(f"You gained {xp_gain} experience points.")

    # Gold
    gold_gain = monster['gold']
    if gold_gain > 0:
        player.gold += gold_gain
        messages.append(f"You found {gold_gain} gold coins.")

    # Stats
    player.monster_kills += 1

    # Progress any active royal quests
    quest_monster_killed(player)

    # Item drop chance
    if monster['drop_item_id'] and random.randint(1, 100) <= 20:
        item = db.session.get(Item, monster['drop_item_id'])
        if item:
            inv_count = InventoryItem.query.filter_by(player_id=player.id).count()
            if inv_count < 15:
                inv_item = InventoryItem(player_id=player.id, item_id=item.id)
                db.session.add(inv_item)
                messages.append(f"The {monster['name']} dropped a {item.name}!")

    # Random dungeon item find
    if random.randint(1, 100) <= 10:
        dungeon_items = Item.query.filter_by(in_dungeon=True).filter(
            Item.min_level <= player.level,
            Item.max_level >= player.level
        ).all()
        if dungeon_items:
            found_item = random.choice(dungeon_items)
            inv_count = InventoryItem.query.filter_by(player_id=player.id).count()
            if inv_count < 15:
                inv_item = InventoryItem(player_id=player.id, item_id=found_item.id)
                db.session.add(inv_item)
                messages.append(f"You discovered a {found_item.name} hidden in the dungeon!")

    # Level up check
    if player.can_level_up():
        messages.append("You feel ready to visit the Level Master!")

    # Add news
    news = NewsEntry(
        player_id=player.id,
        category='combat',
        message=f"{player.name} defeated a {monster['name']} in the dungeons."
    )
    db.session.add(news)

    return messages


def process_defeat(player, monster):
    """Process consequences of being defeated."""
    messages = []

    # Lose some experience
    xp_loss = max(0, player.experience // 20)
    player.experience = max(0, player.experience - xp_loss)
    if xp_loss > 0:
        messages.append(f"You lost {xp_loss} experience points.")

    # Lose some gold
    gold_loss = max(0, player.gold // 10)
    player.gold = max(0, player.gold - gold_loss)
    if gold_loss > 0:
        messages.append(f"You lost {gold_loss} gold coins.")

    # Restore some HP
    player.hp = max(1, player.max_hp // 4)
    player.monster_defeats += 1

    messages.append("You wake up back in town, bruised but alive.")

    # Add news
    news = NewsEntry(
        player_id=player.id,
        category='combat',
        message=f"{player.name} was defeated by a {monster['name']} in the dungeons."
    )
    db.session.add(news)

    return messages


def use_healing_potion(player):
    """Use a healing potion."""
    if player.healing_potions <= 0:
        return False, "You don't have any healing potions!"

    player.healing_potions -= 1
    heal_amount = player.max_hp // 3 + random.randint(5, 15)
    player.hp = min(player.max_hp, player.hp + heal_amount)
    return True, f"You drink a healing potion and recover {heal_amount} HP."


def cast_spell(player, spell_id, monster=None):
    """Cast a spell during combat."""
    if not player.knows_spell(spell_id):
        return False, "You don't know that spell!", 0

    spell = SPELLS.get(spell_id)
    if not spell:
        return False, "Invalid spell!", 0

    if player.mana < spell['mana_cost']:
        return False, "Not enough mana!", 0

    player.mana -= spell['mana_cost']

    if spell['type'] == 'attack':
        damage = (player.wisdom * 2 + player.level * 3 +
                  random.randint(5, 15 + player.level))
        if monster and monster.get('magic_resistance', 0) > 0:
            damage = max(1, damage - monster['magic_resistance'])
        return True, f"You cast {spell['name']}!", damage

    elif spell['type'] == 'heal':
        heal_amount = (player.wisdom * 2 + player.level * 2 +
                       random.randint(10, 20 + player.level))
        player.hp = min(player.max_hp, player.hp + heal_amount)
        return True, f"You cast {spell['name']} and recover {heal_amount} HP!", 0

    elif spell['type'] == 'buff':
        buff_amount = player.wisdom + player.level
        # Temporary defense boost - stored in session during combat
        return True, f"You cast {spell['name']} and feel more protected! (+{buff_amount} defense)", 0

    elif spell['type'] == 'cure':
        player.is_poisoned = False
        player.is_blind = False
        player.has_plague = False
        return True, f"You cast {spell['name']} and feel cleansed!", 0

    return False, "Spell failed!", 0


def dungeon_event(player, dungeon_level):
    """Generate a random dungeon event (non-combat)."""
    events = [
        {
            'type': 'gold',
            'message': "You find a small pouch of gold coins hidden in a crevice.",
            'effect': lambda p, dl: setattr(p, 'gold', p.gold + random.randint(5, 20) * dl)
        },
        {
            'type': 'trap',
            'message': "You trigger a hidden trap!",
            'effect': lambda p, dl: setattr(p, 'hp', max(1, p.hp - random.randint(3, 10)))
        },
        {
            'type': 'fountain',
            'message': "You discover a healing fountain and drink deeply.",
            'effect': lambda p, dl: setattr(p, 'hp', min(p.max_hp, p.hp + random.randint(10, 25)))
        },
        {
            'type': 'nothing',
            'message': "The dungeon passage is eerily quiet. You continue onward.",
            'effect': lambda p, dl: None
        },
        {
            'type': 'shrine',
            'message': "You find a glowing shrine and feel spiritually refreshed.",
            'effect': lambda p, dl: setattr(p, 'mana', min(p.max_mana, p.mana + random.randint(5, 15)))
        },
        {
            'type': 'gold',
            'message': "You discover a skeleton clutching a coin purse.",
            'effect': lambda p, dl: setattr(p, 'gold', p.gold + random.randint(10, 30) * dl)
        },
        {
            'type': 'potion',
            'message': "You find a healing potion on the ground!",
            'effect': lambda p, dl: setattr(p, 'healing_potions', p.healing_potions + 1)
        },
    ]

    event = random.choice(events)
    event['effect'](player, dungeon_level)
    return event


def heal_at_inn(player):
    """Rest at the inn to recover HP/mana."""
    cost = player.level * 5 + 10
    if player.gold < cost:
        return False, f"You need {cost} gold to rest at the inn."

    player.gold -= cost
    heal = player.max_hp // 2
    mana_heal = player.max_mana // 2
    player.hp = min(player.max_hp, player.hp + heal)
    player.mana = min(player.max_mana, player.mana + mana_heal)
    return True, f"You rest at the inn and recover {heal} HP and {mana_heal} mana. (Cost: {cost} gold)"


def bank_deposit(player, amount):
    """Deposit gold in the bank."""
    if amount <= 0:
        return False, "Invalid amount."
    if amount > player.gold:
        return False, "You don't have that much gold."
    player.gold -= amount
    player.bank_gold += amount
    return True, f"Deposited {amount} gold. Bank balance: {player.bank_gold}"


def bank_withdraw(player, amount):
    """Withdraw gold from the bank."""
    if amount <= 0:
        return False, "Invalid amount."
    if amount > player.bank_gold:
        return False, "You don't have that much gold in the bank."
    player.bank_gold -= amount
    player.gold += amount
    return True, f"Withdrew {amount} gold. Gold in hand: {player.gold}"


def buy_item(player, item_id):
    """Buy an item from a shop."""
    item = db.session.get(Item, item_id)
    if not item:
        return False, "Item not found."
    if not item.in_shop:
        return False, "That item is not for sale."
    if player.gold < item.value:
        return False, f"You need {item.value} gold. You have {player.gold}."

    inv_count = InventoryItem.query.filter_by(player_id=player.id).count()
    if inv_count >= 15:
        return False, "Your inventory is full! (Max 15 items)"

    if not item.can_be_used_by(player):
        return False, "You cannot use this item."

    player.gold -= item.value
    inv_item = InventoryItem(player_id=player.id, item_id=item.id)
    db.session.add(inv_item)
    return True, f"You purchased {item.name} for {item.value} gold."


def sell_item(player, inventory_item_id):
    """Sell an item from inventory."""
    inv_item = db.session.get(InventoryItem, inventory_item_id)
    if not inv_item or inv_item.player_id != player.id:
        return False, "Item not found in your inventory."

    item = inv_item.item
    sell_price = item.value // 2

    player.gold += sell_price
    db.session.delete(inv_item)
    return True, f"You sold {item.name} for {sell_price} gold."


def equip_item(player, inventory_item_id):
    """Equip an item from inventory."""
    inv_item = db.session.get(InventoryItem, inventory_item_id)
    if not inv_item or inv_item.player_id != player.id:
        return False, "Item not found in your inventory."

    item = inv_item.item
    slot = item.get_slot()
    if not slot:
        return False, f"{item.name} cannot be equipped."

    if not item.can_be_used_by(player):
        return False, "You cannot use this item."

    # If something is already equipped in this slot, return it to inventory
    old_item_id = getattr(player, f'equipped_{slot}', None)
    if old_item_id:
        old_inv_item = InventoryItem(player_id=player.id, item_id=old_item_id)
        db.session.add(old_inv_item)

    # Equip and remove from inventory
    setattr(player, f'equipped_{slot}', item.id)
    db.session.delete(inv_item)
    player.recalculate_equipment_power()
    return True, f"You equipped {item.name}."


def unequip_item(player, slot):
    """Unequip an item from a slot."""
    item_id = getattr(player, f'equipped_{slot}', None)
    if not item_id:
        return False, "Nothing equipped in that slot."

    # Check inventory space before unequipping
    inv_count = InventoryItem.query.filter_by(player_id=player.id).count()
    if inv_count >= 15:
        return False, "Your inventory is full! Make room before unequipping."

    item = db.session.get(Item, item_id)
    setattr(player, f'equipped_{slot}', None)

    # Return item to inventory
    inv_item = InventoryItem(player_id=player.id, item_id=item_id)
    db.session.add(inv_item)

    player.recalculate_equipment_power()
    name = item.name if item else "item"
    return True, f"You unequipped {name}."


def daily_maintenance(player):
    """Reset daily limits - called when player logs in on a new day."""
    from datetime import datetime, timezone, timedelta
    now = datetime.now(timezone.utc)
    if player.last_maintenance:
        last = player.last_maintenance
        # SQLite may return naive datetimes; treat them as UTC
        if last.tzinfo is None:
            last = last.replace(tzinfo=timezone.utc)
        if (now - last) < timedelta(hours=20):
            return False

    player.fights_remaining = 20
    player.player_fights = 3
    player.thefts_remaining = 2
    player.brawls_remaining = 2
    player.team_fights = 1
    player.intimacy_acts = 5
    player.beauty_nest_visits = int(GameConfig.get('beauty_nest_visits_per_day', '3') or '3')
    player.drinks_remaining = int(GameConfig.get('drinks_per_day', '3') or '3')
    player.escape_attempts = 0
    player.hp = player.max_hp
    player.mana = player.max_mana
    player.last_maintenance = now

    # Bank interest
    if player.bank_gold > 0:
        interest = max(1, player.bank_gold // 100)
        player.bank_gold += interest

    # Run global maintenance tasks once (keyed off this player trigger)
    quest_maintenance()
    pregnancy_maintenance()

    return True


def get_leaderboard():
    """Get top players (including NPCs) by experience."""
    return Player.query.order_by(
        Player.level.desc(), Player.experience.desc()
    ).limit(20).all()


def send_mail(sender, receiver_name, subject, message):
    """Send mail to another player."""
    receiver = Player.query.filter(Player.name.ilike(receiver_name)).first()
    if not receiver:
        return False, f"Player '{receiver_name}' not found."

    mail = Mail(
        sender_id=sender.id,
        receiver_id=receiver.id,
        subject=subject,
        message=message
    )
    db.session.add(mail)
    return True, f"Mail sent to {receiver_name}."


# ==================== TEAMS ====================

MAX_TEAM_MEMBERS = 5


def create_team(player, team_name):
    """Create a new team with the player as leader."""
    if not team_name or len(team_name) < 2 or len(team_name) > 30:
        return False, "Team name must be 2-30 characters."

    existing = Team.query.filter_by(name=team_name).first()
    if existing:
        return False, "A team with that name already exists."

    membership = TeamMember.query.filter_by(player_id=player.id).first()
    if membership:
        return False, "You are already in a team. Leave it first."

    team = Team(name=team_name, leader_id=player.id)
    db.session.add(team)
    db.session.flush()

    member = TeamMember(team_id=team.id, player_id=player.id)
    db.session.add(member)
    player.team_name = team_name

    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"{player.name} has founded the team '{team_name}'!"
    )
    db.session.add(news)
    return True, f"You have founded the team '{team_name}'!"


def join_team(player, team_id):
    """Join an existing team."""
    membership = TeamMember.query.filter_by(player_id=player.id).first()
    if membership:
        return False, "You are already in a team. Leave it first."

    team = db.session.get(Team, team_id)
    if not team:
        return False, "Team not found."

    if team.member_count() >= MAX_TEAM_MEMBERS:
        return False, "That team is full."

    member = TeamMember(team_id=team.id, player_id=player.id)
    db.session.add(member)
    player.team_name = team.name

    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"{player.name} has joined the team '{team.name}'."
    )
    db.session.add(news)
    return True, f"You have joined '{team.name}'!"


def leave_team(player):
    """Leave your current team."""
    membership = TeamMember.query.filter_by(player_id=player.id).first()
    if not membership:
        return False, "You are not in a team."

    team = membership.team
    is_leader = (team.leader_id == player.id)

    db.session.delete(membership)
    player.team_name = ''

    # If leader leaves and team has other members, transfer leadership
    if is_leader:
        remaining = TeamMember.query.filter_by(team_id=team.id).first()
        if remaining:
            team.leader_id = remaining.player_id
            news = NewsEntry(
                player_id=remaining.player_id,
                category='social',
                message=f"{remaining.player.name} is now leader of '{team.name}'."
            )
            db.session.add(news)
        else:
            # No members left, disband
            db.session.delete(team)

    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"{player.name} has left the team '{team.name}'."
    )
    db.session.add(news)
    return True, f"You have left '{team.name}'."


def get_team_rankings():
    """Get teams ranked by power."""
    teams = Team.query.all()
    ranked = sorted(teams, key=lambda t: t.get_power(), reverse=True)
    return ranked


# ==================== KING / MONARCHY ====================

def get_current_king():
    """Get the current monarch, if any."""
    record = KingRecord.query.filter_by(is_current=True).first()
    if record:
        return record.player, record
    return None, None


def challenge_king(challenger):
    """Challenge the current king to combat for the throne."""
    king, king_record = get_current_king()

    if not king:
        # No king - claim the throne if strong enough (level 5+)
        if challenger.level < 5:
            return False, "You must be at least level 5 to claim the throne.", []
        success, msg = crown_new_king(challenger)
        return success, msg, []

    if king.id == challenger.id:
        return False, "You are already the ruler!", []

    if challenger.level < 5:
        return False, "You must be at least level 5 to challenge the throne.", []

    if challenger.hp < challenger.max_hp // 2:
        return False, "You are too wounded to challenge the throne. Heal first.", []

    # Fight through moat creatures first
    combat_log = []
    guards_remaining = king_record.moat_guards

    if guards_remaining > 0:
        # Determine moat creature stats
        moat_creature = king_record.moat_creature
        if moat_creature:
            creature_name = moat_creature.name
            guard_hp_base = moat_creature.hps
            guard_atk_base = moat_creature.attack
            guard_def_base = moat_creature.armor
        else:
            creature_name = "Moat Guard"
            guard_hp_base = 30 + king.level * 5
            guard_atk_base = 8 + king.level * 3
            guard_def_base = 5 + king.level * 2

        combat_log.append(f"You must swim across the moat! You encounter {guards_remaining} {creature_name}{'s' if guards_remaining > 1 else ''}!")
        for i in range(guards_remaining):
            combat_log.append(f"--- {creature_name} {i + 1} ---")
            ghp = guard_hp_base
            while ghp > 0 and challenger.hp > 0:
                # Challenger attacks creature
                atk = calculate_attack(challenger.strength, challenger.weapon_power, challenger.level)
                dmg = max(1, atk - guard_def_base)
                ghp -= dmg
                combat_log.append(f"You strike the {creature_name} for {dmg} damage.")

                if ghp <= 0:
                    combat_log.append(f"The {creature_name} is slain!")
                    # Creature dies - reduce moat count
                    king_record.moat_guards -= 1
                    break

                # Creature attacks challenger
                pdef = calculate_defense(challenger.defence, challenger.armor_power)
                gdmg = max(1, guard_atk_base - pdef)
                challenger.hp -= gdmg
                combat_log.append(f"The {creature_name} strikes you for {gdmg} damage.")

                if challenger.hp <= 0:
                    challenger.hp = max(1, challenger.max_hp // 4)
                    combat_log.append(f"The {creature_name}s have defeated you!")
                    news = NewsEntry(
                        player_id=challenger.id,
                        category='royal',
                        message=f"{challenger.name} was killed by {creature_name}s in the castle moat."
                    )
                    db.session.add(news)

                    # Mail the king about the failed attempt
                    mail = Mail(
                        sender_id=challenger.id,
                        receiver_id=king.id,
                        subject="The Moat",
                        message=f"{challenger.name} swam across the Moat but was killed by your {creature_name}s."
                    )
                    db.session.add(mail)
                    return False, f"You were killed by the {creature_name}s!", combat_log

        combat_log.append("You made it across the moat!")

    # Now fight the king
    combat_log.append(f"=== You face {king.name}, the {'King' if king.sex == 1 else 'Queen'}! ===")

    king_hp = king.max_hp
    rounds = 0
    max_rounds = 20

    while king_hp > 0 and challenger.hp > 0 and rounds < max_rounds:
        rounds += 1
        # Challenger attacks
        atk = calculate_attack(challenger.strength, challenger.weapon_power, challenger.level)
        kdef = calculate_defense(king.defence, king.armor_power)
        dmg = max(1, atk - kdef)
        king_hp -= dmg
        combat_log.append(f"You strike the {'King' if king.sex == 1 else 'Queen'} for {dmg} damage! (HP: {max(0, king_hp)})")

        if king_hp <= 0:
            break

        # King attacks
        katk = calculate_attack(king.strength, king.weapon_power, king.level)
        cdef = calculate_defense(challenger.defence, challenger.armor_power)
        kdmg = max(1, katk - cdef)
        challenger.hp -= kdmg
        combat_log.append(f"The {'King' if king.sex == 1 else 'Queen'} strikes you for {kdmg} damage! (HP: {max(0, challenger.hp)})")

    if king_hp <= 0:
        # Challenger wins!
        dethrone_king(king, king_record)
        success, msg = crown_new_king(challenger)
        combat_log.append(f"You have defeated {king.name} and claimed the throne!")
        return True, msg, combat_log
    elif challenger.hp <= 0:
        challenger.hp = max(1, challenger.max_hp // 4)
        combat_log.append("You have been defeated!")
        news = NewsEntry(
            player_id=challenger.id,
            category='royal',
            message=f"{challenger.name} challenged {king.name} for the throne and lost!"
        )
        db.session.add(news)
        return False, "You were defeated by the monarch!", combat_log
    else:
        # Draw (max rounds)
        combat_log.append("The battle ends in a stalemate!")
        return False, "The battle was inconclusive.", combat_log


def crown_new_king(player):
    """Crown a player as the new king/queen."""
    player.is_king = True

    record = KingRecord(
        player_id=player.id,
        moat_guards=0,
        tax_rate=5,
        treasury=0
    )
    db.session.add(record)

    title = 'King' if player.sex == 1 else 'Queen'
    news = NewsEntry(
        player_id=player.id,
        category='royal',
        message=f"All hail {player.name}, the new {title} of the realm!"
    )
    db.session.add(news)
    return True, f"You are now the {title} of the realm!"


def dethrone_king(king, king_record):
    """Remove a king from power."""
    king.is_king = False
    king_record.is_current = False
    king_record.dethroned_at = datetime.now(timezone.utc)

    # Sack all royal guards
    for guard in king_record.royal_guards:
        mail = Mail(
            sender_id=king.id,
            receiver_id=guard.player_id,
            subject="SACKED",
            message=f"The throne has been usurped. You have been dismissed from Royal Guard duty."
        )
        db.session.add(mail)
    RoyalGuard.query.filter_by(king_record_id=king_record.id).delete()


def abdicate(player):
    """Voluntarily give up the throne."""
    if not player.is_king:
        return False, "You are not the ruler."

    record = KingRecord.query.filter_by(player_id=player.id, is_current=True).first()
    if record:
        dethrone_king(player, record)

    title = 'King' if player.sex == 1 else 'Queen'
    news = NewsEntry(
        player_id=player.id,
        category='royal',
        message=f"{title} {player.name} has abdicated the throne!"
    )
    db.session.add(news)
    return True, "You have abdicated the throne."


def king_hire_moat_creatures(king_record, creature_id, count, funding='treasury'):
    """Buy moat creatures for castle defense.

    Args:
        king_record: The current KingRecord
        creature_id: ID of the MoatCreature type to buy
        count: How many to buy
        funding: 'treasury' or 'personal' (player's own gold)
    """
    creature = db.session.get(MoatCreature, creature_id)
    if not creature:
        return False, "Unknown creature type."

    max_moat = 100
    if king_record.moat_guards + count > max_moat:
        return False, f"Maximum {max_moat} creatures in the moat. You have {king_record.moat_guards}."

    # If changing creature type, must empty moat first
    if king_record.moat_creature_id and king_record.moat_creature_id != creature_id and king_record.moat_guards > 0:
        return False, f"The moat already has {king_record.moat_creature.name}s. Remove them first before adding a different creature."

    total_cost = count * creature.cost
    player = king_record.player

    if funding == 'personal':
        if player.gold < total_cost:
            return False, f"Not enough gold. Need {total_cost}, you have {player.gold}."
        player.gold -= total_cost
    else:
        if king_record.treasury < total_cost:
            return False, f"Not enough in treasury. Need {total_cost}, treasury has {king_record.treasury}."
        king_record.treasury -= total_cost

    king_record.moat_creature_id = creature_id
    king_record.moat_guards += count

    news = NewsEntry(
        player_id=player.id,
        category='royal',
        message=f"{'King' if player.sex == 1 else 'Queen'} {player.name} put {count} {creature.name}{'s' if count > 1 else ''} in the moat."
    )
    db.session.add(news)

    return True, f"Added {count} {creature.name}{'s' if count > 1 else ''} to the moat. Total: {king_record.moat_guards}"


def king_remove_moat_creatures(king_record, count):
    """Remove creatures from the moat."""
    if king_record.moat_guards <= 0:
        return False, "There are no creatures in the moat."
    if count > king_record.moat_guards:
        count = king_record.moat_guards

    king_record.moat_guards -= count
    creature_name = king_record.moat_creature.name if king_record.moat_creature else "creature"

    if king_record.moat_guards == 0:
        king_record.moat_creature_id = None

    return True, f"Removed {count} {creature_name}{'s' if count > 1 else ''} from the moat. Remaining: {king_record.moat_guards}"


def king_hire_royal_guard(king_record, target_id, salary):
    """Hire a player/NPC as a royal bodyguard."""
    max_guards = 5
    current_count = RoyalGuard.query.filter_by(king_record_id=king_record.id).count()
    if current_count >= max_guards:
        return False, f"You already have the maximum {max_guards} guards."

    target = db.session.get(Player, target_id)
    if not target:
        return False, "Player not found."

    if target.id == king_record.player_id:
        return False, "You cannot hire yourself as a guard."

    # Check if already a guard
    existing = RoyalGuard.query.filter_by(king_record_id=king_record.id, player_id=target_id).first()
    if existing:
        return False, f"{target.name} is already in the Royal Guard."

    if target.is_imprisoned:
        return False, f"{target.name} is imprisoned and cannot serve."

    # NPC auto-accepts; for human players this would normally be a mail request
    # but for web we simplify to direct hire
    if target.is_npc:
        # NPC salary is based on level
        salary = (target.level * 900) + random.randint(0, 450)

    guard = RoyalGuard(
        king_record_id=king_record.id,
        player_id=target_id,
        salary=salary
    )
    db.session.add(guard)

    news = NewsEntry(
        player_id=target_id,
        category='royal',
        message=f"{target.name} became a Royal Guard!"
    )
    db.session.add(news)

    if not target.is_npc:
        mail = Mail(
            sender_id=king_record.player_id,
            receiver_id=target_id,
            subject="Royal Employment",
            message=f"{'King' if king_record.player.sex == 1 else 'Queen'} {king_record.player.name} has appointed you as a Royal Guard with a salary of {salary} gold per day."
        )
        db.session.add(mail)

    return True, f"{target.name} has joined the Royal Guard with salary {salary}g/day."


def king_sack_guard(king_record, guard_id):
    """Fire a royal guard."""
    guard = RoyalGuard.query.filter_by(id=guard_id, king_record_id=king_record.id).first()
    if not guard:
        return False, "Guard not found."

    player = guard.player
    db.session.delete(guard)

    news = NewsEntry(
        player_id=player.id,
        category='royal',
        message=f"{player.name} was sacked from the Royal Guard!"
    )
    db.session.add(news)

    mail = Mail(
        sender_id=king_record.player_id,
        receiver_id=player.id,
        subject="SACKED",
        message=f"{'King' if king_record.player.sex == 1 else 'Queen'} {king_record.player.name} has dismissed you from the Royal Guard."
    )
    db.session.add(mail)

    return True, f"{player.name} has been sacked from the Royal Guard!"


def king_set_tax(king_record, rate, alignment=0):
    """Set the royal tax rate and alignment."""
    if rate < 0 or rate > 5:
        return False, "Tax rate must be between 0% and 5%."
    if alignment not in (0, 1, 2):
        return False, "Tax alignment must be 0 (all), 1 (good only), or 2 (evil only)."

    old_rate = king_record.tax_rate
    king_record.tax_rate = rate
    king_record.tax_alignment = alignment

    align_desc = {0: 'all subjects', 1: 'good-aligned only', 2: 'evil-aligned only'}

    player = king_record.player
    title = 'King' if player.sex == 1 else 'Queen'

    if rate != old_rate:
        action = 'raised' if rate > old_rate else 'lowered'
        news = NewsEntry(
            player_id=player.id,
            category='royal',
            message=f"{title} {player.name} {action} the Royal Tax to {rate}% ({align_desc[alignment]})."
        )
        db.session.add(news)

    return True, f"Tax set to {rate}% for {align_desc[alignment]}."


def king_grant_tax_relief(king, target_name):
    """Grant a player tax exemption."""
    target = Player.query.filter(Player.name.ilike(target_name)).first()
    if not target:
        return False, "Player not found."
    if target.tax_relief:
        return False, f"{target.name} already enjoys tax relief."
    target.tax_relief = True

    news = NewsEntry(
        player_id=target.id,
        category='royal',
        message=f"{target.name} has been relieved from Royal Taxes!"
    )
    db.session.add(news)

    mail = Mail(
        sender_id=king.id,
        receiver_id=target.id,
        subject="Free from Royal Tax!",
        message=f"{'King' if king.sex == 1 else 'Queen'} {king.name} has relieved you from Royal Taxes!"
    )
    db.session.add(mail)
    return True, f"{target.name} has been granted tax relief."


def king_revoke_tax_relief(king, target_name):
    """Revoke a player's tax exemption."""
    target = Player.query.filter(Player.name.ilike(target_name)).first()
    if not target:
        return False, "Player not found."
    if not target.tax_relief:
        return False, f"{target.name} does not have tax relief."
    target.tax_relief = False

    news = NewsEntry(
        player_id=target.id,
        category='royal',
        message=f"{target.name}'s tax privileges have been revoked!"
    )
    db.session.add(news)
    return True, f"{target.name}'s tax privileges have been revoked."


def king_treasury_withdraw(king_record, amount):
    """Withdraw gold from the royal treasury (considered an act of greed)."""
    if amount <= 0:
        return False, "Invalid amount."
    if king_record.treasury < amount:
        return False, f"Not enough gold in treasury. Have {king_record.treasury}."

    king_record.treasury -= amount
    king_record.player.gold += amount

    # 50% chance the press finds out
    if random.randint(0, 1) == 0:
        title = 'King' if king_record.player.sex == 1 else 'Queen'
        news = NewsEntry(
            player_id=king_record.player.id,
            category='royal',
            message=f"{title} {king_record.player.name} used the Royal Treasury for personal use!"
        )
        db.session.add(news)

    return True, f"Withdrew {amount} gold from the treasury."


def king_toggle_establishment(king_record, shop_key):
    """Open or close an establishment by royal decree."""
    valid_shops = {
        'shop_magic': 'Magic Shop',
        'shop_healing': 'Healing Center',
        'shop_general': 'General Store',
        'shop_inn': 'Inn',
        'shop_tavern': 'Tavern',
        'shop_beauty_nest': 'Beauty Nest',
    }
    # Weapon and armor shops cannot be closed (people must be able to arm themselves)
    if shop_key in ('shop_weapon', 'shop_armor'):
        return False, "People must be able to buy their weapons and armor!"

    if shop_key not in valid_shops:
        return False, "Unknown establishment."

    current = getattr(king_record, shop_key, True)
    new_val = not current
    setattr(king_record, shop_key, new_val)

    action = 'opened' if new_val else 'closed'
    shop_name = valid_shops[shop_key]
    player = king_record.player
    title = 'King' if player.sex == 1 else 'Queen'

    news = NewsEntry(
        player_id=player.id,
        category='royal',
        message=f"{title} {player.name} {action} the {shop_name}!"
    )
    db.session.add(news)

    return True, f"The {shop_name} has been {action}!"


def king_send_proclamation(king, message_text):
    """Send a royal proclamation to all subjects."""
    if not message_text or len(message_text.strip()) < 3:
        return False, "Proclamation must have content."

    title = 'King' if king.sex == 1 else 'Queen'
    subject = "Royal Proclamation"

    # Send mail to all non-deleted, non-king players
    players = Player.query.filter(Player.id != king.id, Player.name != '').all()
    count = 0
    for p in players:
        mail = Mail(
            sender_id=king.id,
            receiver_id=p.id,
            subject=subject,
            message=f"From {title} {king.name}:\n\n{message_text}"
        )
        db.session.add(mail)
        count += 1

    news = NewsEntry(
        player_id=king.id,
        category='royal',
        message=f"{title} {king.name} issued a Royal Proclamation to all subjects."
    )
    db.session.add(news)

    return True, f"Proclamation sent to {count} subjects."


def pay_royal_guard_salaries(king_record):
    """Pay daily salaries to royal guards from the treasury. Called during maintenance."""
    guards = RoyalGuard.query.filter_by(king_record_id=king_record.id).all()
    sacked = []
    for guard in guards:
        if king_record.treasury >= guard.salary:
            king_record.treasury -= guard.salary
        else:
            # Can't afford - sack the guard
            sacked.append(guard)

    for guard in sacked:
        mail = Mail(
            sender_id=king_record.player_id,
            receiver_id=guard.player_id,
            subject="SACKED - Unpaid",
            message="The Royal Treasury could not afford your salary. You have been dismissed from the Royal Guard."
        )
        db.session.add(mail)
        db.session.delete(guard)

    return sacked


# ==================== BANK GUARD SYSTEM ====================

def bank_guard_apply(player):
    """Apply for bank guard duty. Requires 0 darkness."""
    if player.is_bank_guard:
        return False, "You are already a bank guard."
    if player.darkness > 0:
        return False, "The bank manager eyes you suspiciously. 'We don't hire characters with a dark past. Come back when your record is clean.'"
    if player.hp <= 0:
        return False, "You must be alive to apply for guard duty."

    salary = (player.level * 1500) + (player.strength * 9)
    player.is_bank_guard = True

    news = NewsEntry(
        player_id=player.id,
        category='town',
        message=f"{player.name} has been hired as a bank guard!"
    )
    db.session.add(news)

    return True, f"Welcome to the bank guard force! Your daily salary will be {salary} gold, deposited to your account."


def bank_guard_resign(player):
    """Resign from bank guard duty."""
    if not player.is_bank_guard:
        return False, "You are not a bank guard."

    player.is_bank_guard = False

    news = NewsEntry(
        player_id=player.id,
        category='town',
        message=f"{player.name} has resigned from bank guard duty."
    )
    db.session.add(news)

    return True, "You are now free from your obligations at the bank. Good luck! (and don't try to rob us)."


def accumulate_bank_wages(player):
    """Accumulate daily bank guard salary. Called during maintenance."""
    if not player.is_bank_guard or player.hp <= 0:
        return 0
    wage = (player.level * 1500) + (player.strength * 9)
    player.bank_wage += wage
    return wage


def collect_bank_wages(player):
    """Collect accumulated bank wages. Called on login/session start."""
    if player.bank_wage <= 0:
        return 0
    amount = player.bank_wage
    player.gold += amount
    player.bank_wage = 0
    return amount


# ==================== DOOR GUARD SYSTEM ====================

def get_available_door_guards():
    """Get all available door guard types."""
    return DoorGuard.query.all()


def hire_door_guard(player, guard_id, count=1):
    """Hire door guards when sleeping at the inn."""
    guard = db.session.get(DoorGuard, guard_id)
    if not guard:
        return False, "Unknown guard type."

    if count < 1:
        return False, "Must hire at least 1 guard."

    if not guard.allow_multiple and count > 1:
        count = 1

    max_guards = 10
    if count > max_guards:
        count = max_guards

    total_cost = guard.cost * count
    if player.gold < total_cost:
        return False, f"Not enough gold. Need {total_cost}, you have {player.gold}."

    player.gold -= total_cost
    player.door_guard_id = guard_id
    player.door_guard_count = count

    return True, f"Hired {count} {guard.name}{'s' if count > 1 else ''} to guard your door."


def dismiss_door_guards(player):
    """Remove all door guards."""
    if player.door_guard_count <= 0:
        return False, "You have no door guards."
    player.door_guard_id = None
    player.door_guard_count = 0
    return True, "Door guards dismissed."


def fight_door_guards(attacker, defender):
    """Attacker must fight through defender's door guards before PvP.

    Returns (survived, combat_log, guards_killed).
    - survived: True if attacker defeated all guards
    - combat_log: list of combat messages
    - guards_killed: how many guards were slain
    """
    combat_log = []

    if defender.door_guard_count <= 0 or not defender.door_guard_id:
        return True, combat_log, 0

    guard = db.session.get(DoorGuard, defender.door_guard_id)
    if not guard:
        return True, combat_log, 0

    guard_count = defender.door_guard_count
    if guard_count == 1:
        combat_log.append(f"An angry {guard.name} guards the door!")
    else:
        combat_log.append(f"{guard_count} {guard.name}s guard the door!")

    guards_killed = 0

    for i in range(guard_count):
        combat_log.append(f"--- {guard.name} {i + 1} ---")
        ghp = guard.hps
        while ghp > 0 and attacker.hp > 0:
            # Attacker strikes guard
            atk = calculate_attack(attacker.strength, attacker.weapon_power, attacker.level)
            dmg = max(1, atk - guard.armor)
            ghp -= dmg
            combat_log.append(f"You strike the {guard.name} for {dmg} damage.")

            if ghp <= 0:
                combat_log.append(f"The {guard.name} is slain!")
                guards_killed += 1
                break

            # Guard strikes attacker
            pdef = calculate_defense(attacker.defence, attacker.armor_power)
            gdmg = max(1, guard.attack - pdef)
            attacker.hp -= gdmg
            combat_log.append(f"The {guard.name} strikes you for {gdmg} damage!")

            if attacker.hp <= 0:
                combat_log.append(f"You were killed by {defender.name}'s door guards!")
                break

    # Update defender's guard count
    defender.door_guard_count -= guards_killed
    if defender.door_guard_count <= 0:
        defender.door_guard_count = 0
        defender.door_guard_id = None

    survived = attacker.hp > 0
    return survived, combat_log, guards_killed


def king_imprison(king, target_name):
    """Imprison a player by royal decree."""
    target = Player.query.filter(Player.name.ilike(target_name)).first()
    if not target:
        return False, "Player not found."
    if target.id == king.id:
        return False, "You cannot imprison yourself."
    if target.is_king:
        return False, "You cannot imprison royalty."
    if target.is_imprisoned:
        return False, f"{target.name} is already imprisoned."

    target.is_imprisoned = True
    news = NewsEntry(
        player_id=target.id,
        category='royal',
        message=f"{target.name} has been imprisoned by royal decree!"
    )
    db.session.add(news)

    # Send mail notification
    mail = Mail(
        sender_id=king.id,
        receiver_id=target.id,
        subject="Royal Imprisonment",
        message=f"By decree of {'King' if king.sex == 1 else 'Queen'} {king.name}, you have been imprisoned!"
    )
    db.session.add(mail)
    return True, f"{target.name} has been imprisoned!"


def king_release(king, target_name):
    """Release a prisoner."""
    target = Player.query.filter(Player.name.ilike(target_name)).first()
    if not target:
        return False, "Player not found."
    if not target.is_imprisoned:
        return False, f"{target.name} is not imprisoned."

    target.is_imprisoned = False
    news = NewsEntry(
        player_id=target.id,
        category='royal',
        message=f"{target.name} has been released from prison by royal decree."
    )
    db.session.add(news)
    return True, f"{target.name} has been released."


# ==================== PLAYER VS PLAYER COMBAT ====================

def pvp_combat(attacker, defender):
    """Execute player vs player combat. Returns (winner, loser, combat_log)."""
    combat_log = []

    if attacker.player_fights <= 0:
        return None, None, ["You have no player fights remaining today."]

    if attacker.hp < attacker.max_hp // 3:
        return None, None, ["You are too wounded to fight another player."]

    attacker.player_fights -= 1

    combat_log.append(f"{attacker.name} challenges {defender.name} to combat!")
    if attacker.battlecry:
        combat_log.append(f'{attacker.name} shouts: "{attacker.battlecry}"')

    # Fight through door guards first (if defender has any)
    if defender.door_guard_count > 0 and defender.door_guard_id:
        survived, guard_log, guards_killed = fight_door_guards(attacker, defender)
        combat_log.extend(guard_log)
        if not survived:
            # Attacker died to door guards
            attacker.hp = max(1, attacker.max_hp // 4)
            news = NewsEntry(
                player_id=attacker.id,
                category='pvp',
                message=f"{attacker.name} was killed by {defender.name}'s door guards!"
            )
            db.session.add(news)
            # Mail the defender
            guard = db.session.get(DoorGuard, defender.door_guard_id) if defender.door_guard_id else None
            guard_name = guard.name if guard else "door guards"
            mail = Mail(
                sender_id=attacker.id,
                receiver_id=defender.id,
                subject="Intruder Stopped",
                message=f"{attacker.name} tried to attack you but was killed by your {guard_name}{'s' if guards_killed > 0 else ''}!"
            )
            db.session.add(mail)
            return defender, attacker, combat_log
        elif guards_killed > 0:
            combat_log.append(f"You defeated the door guards! Now to face {defender.name}...")
            # Mail defender about destroyed guards
            mail = Mail(
                sender_id=attacker.id,
                receiver_id=defender.id,
                subject="Door Guards Defeated",
                message=f"{attacker.name} killed {guards_killed} of your door guards and attacked you!"
            )
            db.session.add(mail)

    # Use copies of HP so we don't permanently kill the defender
    atk_hp = attacker.hp
    def_hp = defender.hp
    rounds = 0
    max_rounds = 15

    while atk_hp > 0 and def_hp > 0 and rounds < max_rounds:
        rounds += 1

        # Attacker strikes
        atk = calculate_attack(attacker.strength, attacker.weapon_power, attacker.level)
        ddef = calculate_defense(defender.defence, defender.armor_power)
        dmg = max(1, atk - ddef)

        if random.randint(1, 100) <= 5 + attacker.dexterity // 3:
            dmg = int(dmg * 1.5)
            combat_log.append(f"**Critical!** {attacker.name} strikes for {dmg} damage!")
        else:
            combat_log.append(f"{attacker.name} attacks for {dmg} damage.")
        def_hp -= dmg

        if def_hp <= 0:
            combat_log.append(f"{defender.name} has been defeated!")
            break

        # Defender strikes back
        datk = calculate_attack(defender.strength, defender.weapon_power, defender.level)
        adef = calculate_defense(attacker.defence, attacker.armor_power)
        ddmg = max(1, datk - adef)

        if random.randint(1, 100) <= 5 + defender.dexterity // 3:
            ddmg = int(ddmg * 1.5)
            combat_log.append(f"**Critical!** {defender.name} strikes for {ddmg} damage!")
        else:
            combat_log.append(f"{defender.name} attacks for {ddmg} damage.")
        atk_hp -= ddmg

        if atk_hp <= 0:
            combat_log.append(f"{attacker.name} has been defeated!")
            break

    if def_hp <= 0:
        # Attacker wins
        xp_gain = max(10, defender.level * 20)
        gold_stolen = min(defender.gold, defender.gold // 5 + random.randint(0, 50))
        attacker.experience += xp_gain
        attacker.gold += gold_stolen
        defender.gold -= gold_stolen
        attacker.player_kills += 1
        defender.player_defeats += 1
        attacker.hp = max(1, atk_hp)
        attacker.chivalry += 1 if defender.level >= attacker.level else 0
        attacker.darkness += 2 if defender.level < attacker.level - 3 else 0

        combat_log.append(f"You gained {xp_gain} XP and took {gold_stolen} gold!")

        # Check bounties
        bounties = Bounty.query.filter_by(target_id=defender.id, claimed=False).all()
        bounty_total = 0
        for b in bounties:
            b.claimed = True
            b.claimed_by_id = attacker.id
            bounty_total += b.amount
        if bounty_total > 0:
            attacker.gold += bounty_total
            combat_log.append(f"You collected {bounty_total} gold in bounties!")

        news = NewsEntry(
            player_id=attacker.id,
            category='combat',
            message=f"{attacker.name} defeated {defender.name} in combat!"
        )
        db.session.add(news)
        return attacker, defender, combat_log

    elif atk_hp <= 0:
        # Defender wins
        attacker.player_defeats += 1
        defender.player_kills += 1
        attacker.hp = max(1, attacker.max_hp // 4)

        news = NewsEntry(
            player_id=defender.id,
            category='combat',
            message=f"{defender.name} defeated {attacker.name} who challenged them!"
        )
        db.session.add(news)
        return defender, attacker, combat_log

    else:
        # Draw
        attacker.hp = max(1, atk_hp)
        combat_log.append("The battle ends in a draw!")
        return None, None, combat_log


# ==================== TAVERN / BAR ====================

def tavern_brawl(player):
    """Bar brawl at the tavern. Fight random NPCs for fun and XP."""
    if player.brawls_remaining <= 0:
        return False, "You've had enough brawling for today.", []

    if player.hp < player.max_hp // 4:
        return False, "You are too wounded to brawl.", []

    player.brawls_remaining -= 1
    log = []
    num_opponents = random.randint(1, 3)
    log.append(f"You pick a fight in the tavern! {num_opponents} patron(s) stand up to face you!")

    stamina = player.stamina + player.strength // 2
    wins = 0

    for i in range(num_opponents):
        opp_strength = random.randint(5, 10 + player.level * 2)
        opp_stamina = random.randint(10, 20 + player.level * 3)
        opp_name = random.choice([
            "a burly farmer", "a drunken sailor", "an off-duty guard",
            "a grizzled mercenary", "a rowdy miner", "a scarred veteran",
            "a boisterous blacksmith", "a wiry pickpocket"
        ])
        log.append(f"--- Round {i + 1}: You face {opp_name}! ---")

        while stamina > 0 and opp_stamina > 0:
            # Player punch
            punch = random.randint(1, player.strength // 2 + 5)
            opp_stamina -= punch
            log.append(f"You land a punch for {punch} damage!")

            if opp_stamina <= 0:
                log.append(f"You knocked out {opp_name}!")
                wins += 1
                break

            # Opponent punch
            opp_punch = random.randint(1, opp_strength // 2 + 3)
            stamina -= opp_punch
            log.append(f"{opp_name.capitalize()} hits you for {opp_punch}!")

            if stamina <= 0:
                log.append("You've been knocked out!")
                break

    # Results
    if wins > 0:
        xp = wins * random.randint(5, 15) * player.level
        gold = wins * random.randint(2, 10)
        player.experience += xp
        player.gold += gold
        log.append(f"Brawl over! Won {wins}/{num_opponents}. Gained {xp} XP and {gold} gold!")
        player.darkness += 1
    else:
        log.append("You lost the brawl!")
        dmg = random.randint(3, 10)
        player.hp = max(1, player.hp - dmg)
        log.append(f"You took {dmg} damage from the beating.")

    return True, f"Brawl results: {wins}/{num_opponents} wins", log


def drinking_contest(player):
    """Drinking competition at the tavern."""
    cost = 10 + player.level * 2
    if player.gold < cost:
        return False, f"Entry fee is {cost} gold. You can't afford it.", []

    player.gold -= cost
    log = []
    log.append(f"You enter the drinking contest! (Entry: {cost} gold)")

    player_tolerance = player.stamina + player.strength // 3
    opponent_name = random.choice([
        "Big Bertha", "One-Eyed Jack", "Iron Gut Pete",
        "Sloshy McGee", "The Dwarf Champion", "Barrel Bob"
    ])
    opp_tolerance = random.randint(10, 20 + player.level * 2)
    log.append(f"Your opponent is {opponent_name}!")

    rounds = 0
    player_drunk = 0
    opp_drunk = 0

    while True:
        rounds += 1
        # Both drink
        drink = random.randint(3, 8)
        player_drunk += drink
        opp_drunk += random.randint(3, 8)

        log.append(f"Round {rounds}: *gulp* *gulp* *gulp*")

        if player_drunk > player_tolerance:
            log.append("You fall off your stool! You lose!")
            player.hp = max(1, player.hp - random.randint(1, 5))
            return True, "You lost the drinking contest!", log

        if opp_drunk > opp_tolerance:
            prize = cost * 3
            player.gold += prize
            player.experience += random.randint(10, 30) * player.level
            log.append(f"{opponent_name} passes out! You win {prize} gold!")
            news = NewsEntry(
                player_id=player.id,
                category='social',
                message=f"{player.name} won a drinking contest against {opponent_name}!"
            )
            db.session.add(news)
            return True, f"You won the drinking contest! Prize: {prize} gold", log

        if rounds > 20:
            log.append("The contest is called a draw after 20 rounds!")
            player.gold += cost  # Refund
            return True, "The drinking contest ended in a draw.", log


# ==================== DRUG PALACE ====================

DRUGS = [
    {'name': 'Incense', 'cost': 900, 'xp_min': 100, 'xp_max': 199,
     'addiction_min': 2, 'addiction_max': 3,
     'desc': 'Quite harmless... or so they say.'},
    {'name': 'Psilocybin', 'cost': 3000, 'xp_min': 300, 'xp_max': 599,
     'addiction_min': 4, 'addiction_max': 5,
     'desc': 'Be happy, be happier!'},
    {'name': 'Oxytozin', 'cost': 13000, 'xp_min': 700, 'xp_max': 1399,
     'addiction_min': 8, 'addiction_max': 10,
     'desc': 'Ever wanted to fly?'},
    {'name': 'Psylxion', 'cost': 27000, 'xp_min': 1000, 'xp_max': 1999,
     'addiction_min': 10, 'addiction_max': 12,
     'desc': 'Orc stress reducer.'},
    {'name': 'Shang Ri La', 'cost': 50000, 'xp_min': 2000, 'xp_max': 3999,
     'addiction_min': 14, 'addiction_max': 17,
     'desc': 'Enter dreamland...'},
    {'name': 'Neopratin', 'cost': 70000, 'xp_min': 3000, 'xp_max': 5999,
     'addiction_min': 15, 'addiction_max': 20,
     'desc': 'Walk the rainbow.'},
    {'name': 'Galacticum', 'cost': 120000, 'xp_min': 4000, 'xp_max': 7999,
     'addiction_min': 18, 'addiction_max': 23,
     'desc': 'Float in space - dangerous!'},
    {'name': 'Inferno', 'cost': 175000, 'xp_min': 5000, 'xp_max': 9999,
     'addiction_min': 19, 'addiction_max': 26,
     'desc': 'Adrenalin skyrocket!'},
    {'name': 'Sanguin Hope', 'cost': 200000, 'xp_min': 6000, 'xp_max': 11999,
     'addiction_min': 20, 'addiction_max': 27,
     'desc': 'Unknown effects.'},
    {'name': 'Transactor', 'cost': 500000, 'xp_min': 9000, 'xp_max': 18999,
     'addiction_min': 20, 'addiction_max': 29,
     'desc': 'The heaviest stuff on the market.'},
]


def buy_drug(player, drug_index):
    """Buy and use a drug from the Drug Palace."""
    if drug_index < 0 or drug_index >= len(DRUGS):
        return False, "Invalid drug.", []

    drug = DRUGS[drug_index]
    log = []

    if player.gold < drug['cost']:
        return False, f"You need {drug['cost']} gold for {drug['name']}.", []

    player.gold -= drug['cost']
    log.append(f"You purchase a dose of {drug['name']} for {drug['cost']} gold.")
    log.append(f'"{drug["desc"]}"')

    # 10% chance of overdose death
    if random.randint(1, 10) == 1:
        player.hp = 0
        log.append("OVERDOSE! The drug was too much for your body!")
        log.append("You collapse to the ground. Everything goes dark...")
        news = NewsEntry(
            player_id=player.id,
            category='death',
            message=f"{player.name} died from a {drug['name']} overdose!"
        )
        db.session.add(news)
        return True, f"You overdosed on {drug['name']}!", log

    # XP gain
    xp_gain = random.randint(drug['xp_min'], drug['xp_max'])
    player.experience += xp_gain
    log.append(f"The experience expands your mind! (+{xp_gain} XP)")

    # Addiction increase (Gnomes get -2 reduction)
    addiction_gain = random.randint(drug['addiction_min'], drug['addiction_max'])
    if player.race == 'Gnome':
        addiction_gain = max(0, addiction_gain - 2)
    player.addiction = min(100, player.addiction + addiction_gain)
    log.append(f"You feel the pull of addiction... (+{addiction_gain}% addiction)")

    # Mental health decrease
    mental_loss = random.randint(1, 5)
    player.mental_health = max(0, player.mental_health - mental_loss)

    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"{player.name} was seen at the Drug Palace buying {drug['name']}."
    )
    db.session.add(news)

    return True, f"You used {drug['name']}.", log


# ==================== STEROID SHOP ====================

STEROIDS = [
    {'name': 'Teddy Bears', 'cost': 1500, 'str_min': 4, 'str_max': 7,
     'mental_min': 2, 'mental_max': 3,
     'desc': 'Long term effective.'},
    {'name': 'Ape Hormones', 'cost': 7000, 'str_min': 6, 'str_max': 11,
     'mental_min': 4, 'mental_max': 7,
     'desc': 'Cheap primitive strength.'},
    {'name': 'Centurion-X', 'cost': 20000, 'str_min': 8, 'str_max': 13,
     'mental_min': 6, 'mental_max': 11,
     'desc': 'Troll warrior favorite.'},
    {'name': 'Godzilla Red', 'cost': 50000, 'str_min': 10, 'str_max': 19,
     'mental_min': 8, 'mental_max': 15,
     'desc': 'Superb but nasty side effects.'},
    {'name': 'Slave 9000', 'cost': 70000, 'str_min': 12, 'str_max': 21,
     'mental_min': 10, 'mental_max': 19,
     'desc': 'Slave stamina booster.'},
    {'name': 'Pulsatormium', 'cost': 120000, 'str_min': 14, 'str_max': 25,
     'mental_min': 12, 'mental_max': 23,
     'desc': 'Druid-made. Premium quality.'},
    {'name': 'Implementor', 'cost': 175000, 'str_min': 14, 'str_max': 29,
     'mental_min': 14, 'mental_max': 29,
     'desc': 'Miracle maker, ages you.'},
    {'name': 'Dragon White', 'cost': 210000, 'str_min': 16, 'str_max': 35,
     'mental_min': 16, 'mental_max': 35,
     'desc': 'For experienced users only.'},
    {'name': 'Neon Kicker', 'cost': 350000, 'str_min': 18, 'str_max': 42,
     'mental_min': 26, 'mental_max': 50,
     'desc': 'Path to madness or salvation.'},
    {'name': 'D.E.M.O.N.', 'cost': 500000, 'str_min': 31, 'str_max': 90,
     'mental_min': 31, 'mental_max': 60,
     'desc': 'Unknown effects. Use at own risk.'},
]


def buy_steroid(player, steroid_index):
    """Buy and use a steroid from the Steroid Shop."""
    if steroid_index < 0 or steroid_index >= len(STEROIDS):
        return False, "Invalid steroid.", []

    steroid = STEROIDS[steroid_index]
    log = []

    if player.mental_health < 10:
        return False, "Your mental health is too low. You need at least 10 mental stability.", []

    if player.gold < steroid['cost']:
        return False, f"You need {steroid['cost']} gold for {steroid['name']}.", []

    player.gold -= steroid['cost']
    log.append(f"You purchase a dose of {steroid['name']} for {steroid['cost']} gold.")
    log.append(f'"{steroid["desc"]}"')

    # 10% chance of death from bad batch
    if random.randint(1, 10) == 1:
        player.hp = 0
        log.append("BAD BATCH! Your body rejects the steroid violently!")
        log.append("You collapse in agony. Everything fades...")
        news = NewsEntry(
            player_id=player.id,
            category='death',
            message=f"{player.name} died from a bad batch of {steroid['name']}!"
        )
        db.session.add(news)
        return True, f"Bad batch of {steroid['name']} killed you!", log

    # Strength gain
    str_gain = random.randint(steroid['str_min'], steroid['str_max'])
    player.strength += str_gain
    log.append(f"Your muscles bulge with power! (+{str_gain} Strength)")

    # Mental health decrease (Gnomes get -2 reduction)
    mental_loss = random.randint(steroid['mental_min'], steroid['mental_max'])
    if player.race == 'Gnome':
        mental_loss = max(0, mental_loss - 2)
    player.mental_health = max(0, player.mental_health - mental_loss)
    log.append(f"Your mind feels... fuzzy. (-{mental_loss} Mental Stability)")

    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"{player.name} was spotted leaving the Steroid Shop looking pumped."
    )
    db.session.add(news)

    return True, f"You used {steroid['name']}.", log


# ==================== BOUNTY SYSTEM ====================

def post_bounty(poster, target_name, amount, reason='Wanted Dead or Alive'):
    """Post a bounty on a player."""
    if amount < 50:
        return False, "Minimum bounty is 50 gold."
    if amount > poster.gold:
        return False, "You don't have enough gold."

    target = Player.query.filter(Player.name.ilike(target_name)).first()
    if not target:
        return False, "Player not found."
    if target.id == poster.id:
        return False, "You cannot place a bounty on yourself."

    poster.gold -= amount
    bounty = Bounty(
        target_id=target.id,
        poster_id=poster.id,
        amount=amount,
        reason=reason
    )
    db.session.add(bounty)

    news = NewsEntry(
        player_id=poster.id,
        category='social',
        message=f"A bounty of {amount} gold has been placed on {target.name}!"
    )
    db.session.add(news)
    return True, f"Bounty of {amount} gold posted on {target.name}."


def get_wanted_list():
    """Get the most wanted players by total bounty."""
    from sqlalchemy import func
    results = db.session.query(
        Bounty.target_id,
        func.sum(Bounty.amount).label('total')
    ).filter_by(claimed=False).group_by(Bounty.target_id).order_by(
        func.sum(Bounty.amount).desc()
    ).limit(20).all()

    wanted = []
    for target_id, total in results:
        player = db.session.get(Player, target_id)
        if player:
            wanted.append({'player': player, 'total_bounty': total})
    return wanted


# ==================== RELATIONSHIPS / MARRIAGE ====================

def propose_marriage(player, target_name):
    """Propose marriage to another player or NPC via mail."""
    target = Player.query.filter(Player.name.ilike(target_name)).first()
    if not target:
        return False, "Player not found."
    if target.id == player.id:
        return False, "You cannot marry yourself."
    if player.married:
        return False, "You are already married."
    if target.married:
        return False, f"{target.name} is already married."

    # Send proposal via mail
    mail = Mail(
        sender_id=player.id,
        receiver_id=target.id,
        subject="Marriage Proposal!",
        message=f"{player.name} has proposed marriage to you! Visit the Love Corner to accept or decline."
    )
    db.session.add(mail)

    # If target is an NPC, auto-accept the proposal (NPCs are sociable)
    if target.is_npc:
        rel = Relationship(
            player1_id=player.id,
            player2_id=target.id,
            rel_type='married'
        )
        db.session.add(rel)
        player.married = True
        player.spouse_id = target.id
        target.married = True
        target.spouse_id = player.id

        news = NewsEntry(
            player_id=player.id,
            category='social',
            message=f"{player.name} and {target.name} have been married!"
        )
        db.session.add(news)
        return True, f"You are now married to {target.name}!"

    # Create pending relationship for human players
    rel = Relationship(
        player1_id=player.id,
        player2_id=target.id,
        rel_type='proposal'
    )
    db.session.add(rel)
    return True, f"You have proposed marriage to {target.name}!"


def accept_marriage(player, proposer_id):
    """Accept a marriage proposal."""
    rel = Relationship.query.filter_by(
        player1_id=proposer_id, player2_id=player.id, rel_type='proposal'
    ).first()
    if not rel:
        return False, "No proposal found."

    proposer = db.session.get(Player, proposer_id)
    if not proposer:
        return False, "Player not found."
    if proposer.married or player.married:
        db.session.delete(rel)
        return False, "Marriage not possible - one party is already married."

    # Create marriage
    rel.rel_type = 'married'
    player.married = True
    player.spouse_id = proposer.id
    proposer.married = True
    proposer.spouse_id = player.id

    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"{proposer.name} and {player.name} have been married!"
    )
    db.session.add(news)
    return True, f"You are now married to {proposer.name}!"


def decline_marriage(player, proposer_id):
    """Decline a marriage proposal."""
    rel = Relationship.query.filter_by(
        player1_id=proposer_id, player2_id=player.id, rel_type='proposal'
    ).first()
    if not rel:
        return False, "No proposal found."
    proposer = db.session.get(Player, proposer_id)
    db.session.delete(rel)
    if proposer:
        mail = Mail(
            sender_id=player.id,
            receiver_id=proposer.id,
            subject="Proposal Declined",
            message=f"{player.name} has declined your marriage proposal."
        )
        db.session.add(mail)
    return True, "Proposal declined."


def divorce(player):
    """Divorce your spouse."""
    if not player.married or not player.spouse_id:
        return False, "You are not married."

    spouse = db.session.get(Player, player.spouse_id)
    if spouse:
        spouse.married = False
        spouse.spouse_id = None

        mail = Mail(
            sender_id=player.id,
            receiver_id=spouse.id,
            subject="Divorce",
            message=f"{player.name} has divorced you."
        )
        db.session.add(mail)

    player.married = False
    old_spouse_name = spouse.name if spouse else "unknown"
    player.spouse_id = None

    # Remove marriage relationship
    Relationship.query.filter(
        ((Relationship.player1_id == player.id) | (Relationship.player2_id == player.id)),
        Relationship.rel_type == 'married'
    ).delete(synchronize_session=False)

    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"{player.name} and {old_spouse_name} have divorced!"
    )
    db.session.add(news)
    return True, f"You have divorced {old_spouse_name}."


def add_relationship(player, target_name, rel_type):
    """Add a social relationship (ally, rival)."""
    if rel_type not in ('ally', 'rival'):
        return False, "Invalid relationship type."

    target = Player.query.filter(Player.name.ilike(target_name)).first()
    if not target:
        return False, "Player not found."
    if target.id == player.id:
        return False, "Cannot have a relationship with yourself."

    existing = Relationship.query.filter_by(
        player1_id=player.id, player2_id=target.id, rel_type=rel_type
    ).first()
    if existing:
        return False, f"{target.name} is already your {rel_type}."

    rel = Relationship(
        player1_id=player.id,
        player2_id=target.id,
        rel_type=rel_type
    )
    db.session.add(rel)
    return True, f"{target.name} is now your {rel_type}."


def get_player_relationships(player):
    """Get all relationships for a player."""
    rels = Relationship.query.filter(
        (Relationship.player1_id == player.id) | (Relationship.player2_id == player.id)
    ).all()

    result = []
    for r in rels:
        other = r.player2 if r.player1_id == player.id else r.player1
        result.append({
            'player': other,
            'type': r.rel_type,
            'id': r.id
        })
    return result


# =========================================================================
# SOCIAL INTERACTIONS / APPROACH SYSTEM (from original LOVERS.PAS)
# =========================================================================

# Feeling levels ordered from worst to best (matching original relation constants)
FEELING_LEVELS = [
    'hate', 'enemy', 'anger', 'suspicious', 'normal',
    'respect', 'trust', 'friendship', 'passion', 'love'
]


def _get_feeling_index(feeling):
    """Get numeric index of a feeling level."""
    try:
        return FEELING_LEVELS.index(feeling)
    except ValueError:
        return FEELING_LEVELS.index('normal')


def _improve_feeling(feeling):
    """Move feeling one step better."""
    idx = _get_feeling_index(feeling)
    if idx < len(FEELING_LEVELS) - 1:
        return FEELING_LEVELS[idx + 1]
    return feeling


def _worsen_feeling(feeling):
    """Move feeling one step worse."""
    idx = _get_feeling_index(feeling)
    if idx > 0:
        return FEELING_LEVELS[idx - 1]
    return feeling


def _is_negative_feeling(feeling):
    """Check if feeling is negative (hate, enemy, anger)."""
    return feeling in ('hate', 'enemy', 'anger')


def _feeling_display(feeling):
    """Human-readable feeling string."""
    return {
        'hate': 'Hatred',
        'enemy': 'Enemy',
        'anger': 'Anger',
        'suspicious': 'Suspicious',
        'normal': 'Neutral',
        'respect': 'Respect',
        'trust': 'Trust',
        'friendship': 'Friendship',
        'passion': 'Passion',
        'love': 'Love',
    }.get(feeling, 'Neutral')


def get_or_create_relation(player, target):
    """Get or create a relationship record between two players."""
    rel = Relationship.query.filter(
        ((Relationship.player1_id == player.id) & (Relationship.player2_id == target.id)) |
        ((Relationship.player1_id == target.id) & (Relationship.player2_id == player.id))
    ).filter(Relationship.rel_type.in_(['lover', 'ally', 'rival', 'married'])).first()

    if not rel:
        rel = Relationship(
            player1_id=player.id,
            player2_id=target.id,
            rel_type='lover',
            feeling_1to2='normal',
            feeling_2to1='normal',
        )
        db.session.add(rel)
        db.session.flush()
    return rel


def get_feeling_toward(rel, from_id):
    """Get the feeling that from_id has toward the other player in the relationship."""
    if rel.player1_id == from_id:
        return rel.feeling_1to2 or 'normal'
    return rel.feeling_2to1 or 'normal'


def set_feeling_toward(rel, from_id, feeling):
    """Set the feeling that from_id has toward the other player."""
    if rel.player1_id == from_id:
        rel.feeling_1to2 = feeling
    else:
        rel.feeling_2to1 = feeling


def get_approachable_players(player, sex_filter='both'):
    """Get list of players that can be approached for social interactions.

    Based on original LOVERS.PAS approach routine.
    sex_filter: 'male', 'female', or 'both'
    """
    query = Player.query.filter(
        Player.id != player.id,
        Player.hp > 0,
        Player.is_imprisoned == False,
    )

    if sex_filter == 'male':
        query = query.filter(Player.sex == 1)
    elif sex_filter == 'female':
        query = query.filter(Player.sex == 2)

    return query.order_by(Player.name).all()


def approach_player_info(player, target_id):
    """Get info about the relationship between player and target for the approach screen.

    Returns dict with target info, relationship status, feelings, etc.
    """
    target = db.session.get(Player, target_id)
    if not target:
        return None

    rel = get_or_create_relation(player, target)

    player_feeling = get_feeling_toward(rel, player.id)
    target_feeling = get_feeling_toward(rel, target.id)

    # Check if either is married to someone else
    player_married_to_other = player.married and player.spouse_id != target.id
    target_married_to_other = target.married and target.spouse_id != player.id
    married_to_each_other = player.married and player.spouse_id == target.id

    return {
        'target': target,
        'relationship': rel,
        'player_feeling': player_feeling,
        'target_feeling': target_feeling,
        'player_feeling_display': _feeling_display(player_feeling),
        'target_feeling_display': _feeling_display(target_feeling),
        'married_to_each_other': married_to_each_other,
        'player_married_to_other': player_married_to_other,
        'target_married_to_other': target_married_to_other,
        'intimacy_acts_left': player.intimacy_acts if player.intimacy_acts else 0,
    }


def social_interact(player, target_id, action):
    """Perform a social interaction with another player.

    Actions: hold_hands, dinner, kiss, go_to_bed
    Based on original LOVERS.PAS intimate actions.

    Returns (success, message, xp_gained).
    """
    target = db.session.get(Player, target_id)
    if not target:
        return False, "Player not found.", 0

    if player.id == target.id:
        return False, "You cannot interact with yourself.", 0

    # Re-check target availability (listing page filters these, but enforce here too)
    if target.hp <= 0:
        return False, f"{target.name} is too wounded for social activities.", 0
    if target.is_imprisoned:
        return False, f"{target.name} is currently imprisoned.", 0

    if action not in ('hold_hands', 'dinner', 'kiss', 'go_to_bed'):
        return False, "Invalid action.", 0

    # Check daily intimacy limit (original: player.IntimacyActs)
    if not player.intimacy_acts or player.intimacy_acts < 1:
        return False, "You have no intimate sessions left today.", 0

    rel = get_or_create_relation(player, target)
    target_feeling = get_feeling_toward(rel, target.id)
    married_to_each_other = player.married and player.spouse_id == target.id

    # Married couples do intimate things at home, not at Love Corner
    # (original: "Married couples entertain themselves at home!")
    if married_to_each_other and action in ('hold_hands', 'dinner', 'kiss'):
        return False, "You are married! Go home and spend time together instead.", 0

    # Check if target is married to someone else (faithfulness check)
    if target.married and target.spouse_id != player.id:
        spouse = db.session.get(Player, target.spouse_id)
        spouse_name = spouse.name if spouse else "someone"
        return False, f"{target.name} is married to {spouse_name} and is faithful!", 0

    # NPC response logic (from original: pl0^.ai='C')
    if target.is_npc:
        # 2/3 chance NPC refuses (original: random(3)<>0)
        if random.randint(1, 3) != 1:
            refuse_msgs = {
                'hold_hands': f"{target.name} refuses to meet you!",
                'dinner': f"{target.name} refuses to eat with you!",
                'kiss': f"{target.name} refuses to be kissed by you!",
                'go_to_bed': f"{target.name} refuses to be intimate with you!",
            }
            player.intimacy_acts -= 1
            return False, refuse_msgs[action], 0

        # NPCs with negative feelings refuse completely
        if _is_negative_feeling(target_feeling):
            hate_msgs = {
                'hold_hands': f"{target.name} doesn't like you very much! Forget about a date!",
                'dinner': f"{target.name} doesn't like you! Forget about dinner!",
                'kiss': f"{target.name} doesn't like you! Forget about kissing!",
                'go_to_bed': f"{target.name} hates you! Forget about it!",
            }
            player.intimacy_acts -= 1
            return False, hate_msgs[action], 0
    else:
        # Human player targets get a mail invitation instead of instant interaction
        action_names = {
            'hold_hands': 'hold hands',
            'dinner': 'dinner',
            'kiss': 'a kiss',
            'go_to_bed': 'an intimate encounter',
        }
        mail = Mail(
            sender_id=player.id,
            receiver_id=target.id,
            subject=f"Romantic Invitation",
            message=f"{player.name} has invited you for {action_names[action]} at the Love Corner!"
        )
        db.session.add(mail)
        player.intimacy_acts -= 1
        return True, f"Invitation sent to {target.name} for {action_names[action]}!", 0

    # ---- NPC accepted the interaction ----

    # 50% chance NPC improves their feeling toward player (original: random(2)=0)
    if random.randint(0, 1) == 0:
        new_feeling = _improve_feeling(target_feeling)
        set_feeling_toward(rel, target.id, new_feeling)

    # Calculate XP based on action type (from original multipliers)
    xp_multiplier = {
        'hold_hands': 155,  # original: player.level*155
        'dinner': 155,      # original: player.level*155
        'kiss': 234,        # original: player.level*234
        'go_to_bed': 244,   # original: player.level*244
    }[action]

    xp = (player.level * xp_multiplier + target.level * xp_multiplier) // 2
    xp = max(100, xp)

    # Apply XP
    player.experience += xp
    target.experience += xp

    # Reduce daily intimacy acts
    player.intimacy_acts -= 1

    # Generate success message and news
    if action == 'hold_hands':
        msg = f"You go out with {target.name} and have a great time! You both earn {xp:,} experience!"
        news_msg = f"{player.name} and {target.name} were seen together today. They were holding hands on a park bench."
        news_cat = 'Dating'
    elif action == 'dinner':
        msg = f"You have dinner with {target.name} and enjoy yourself! Everything was great, except the check. You both earn {xp:,} experience!"
        news_msg = f"{player.name} and {target.name} were seen having dinner this evening."
        news_cat = 'Dinner Date'
    elif action == 'kiss':
        msg = f"You kiss {target.name} passionately! Great Lips! You both earn {xp:,} experience!"
        news_msg = f"{player.name} kissed {target.name}!"
        news_cat = 'Love'
    else:  # go_to_bed
        msg = f"You embrace {target.name} passionately! Great Event! You earn {xp:,} experience!"
        news_msg = f"{player.name} slept with {target.name}!"
        news_cat = 'Romantic Event'

    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"{news_cat}: {news_msg}"
    )
    db.session.add(news)

    # Jealousy check - if player is married to someone else, spouse gets angry
    _check_jealousy(player, target)
    _check_jealousy(target, player)

    return True, msg, xp


def _check_jealousy(player, partner):
    """Check if player's spouse gets jealous about interaction with partner.

    Based on original Jealousy() procedure from RELATION.PAS.
    """
    if not player.married or not player.spouse_id:
        return
    if player.spouse_id == partner.id:
        return  # interacting with own spouse, no jealousy

    spouse = db.session.get(Player, player.spouse_id)
    if not spouse:
        return

    # Spouse finds out (50% chance)
    if random.randint(0, 1) == 0:
        return

    # Send angry mail from spouse
    mail = Mail(
        sender_id=spouse.id,
        receiver_id=player.id,
        subject="Jealousy!",
        message=f"{spouse.name} found out about your affair with {partner.name}! "
                f"Your spouse is furious!"
    )
    db.session.add(mail)

    # Worsen spouse's feeling toward player
    rel = get_or_create_relation(spouse, player)
    current = get_feeling_toward(rel, spouse.id)
    set_feeling_toward(rel, spouse.id, _worsen_feeling(current))

    news = NewsEntry(
        player_id=spouse.id,
        category='social',
        message=f"Jealousy! {spouse.name} is furious about {player.name}'s affair with {partner.name}!"
    )
    db.session.add(news)


def change_feeling(player, target_id, direction):
    """Player changes their attitude/feeling toward another player.

    direction: 'better' or 'worse'
    Based on original change_feelings_menu from LOVERS.PAS.
    """
    target = db.session.get(Player, target_id)
    if not target:
        return False, "Player not found."

    rel = get_or_create_relation(player, target)
    current = get_feeling_toward(rel, player.id)

    if direction == 'better':
        new_feeling = _improve_feeling(current)
    elif direction == 'worse':
        new_feeling = _worsen_feeling(current)
    else:
        return False, "Invalid direction."

    if new_feeling == current:
        limit = "love" if direction == 'better' else "hate"
        return False, f"Your feeling is already at {_feeling_display(current)} ({limit})."

    set_feeling_toward(rel, player.id, new_feeling)
    return True, f"Your feeling toward {target.name} changed from {_feeling_display(current)} to {_feeling_display(new_feeling)}."


# =========================================================================
# DUNGEON LEVEL CHANGE (from original DUNGEONC.PAS)
# =========================================================================

def change_dungeon_level(player, new_level):
    """Change the dungeon level the player is exploring.

    From original: players can access levels from their level to level+5.
    Total of 100 dungeon levels.
    Returns (success, message).
    """
    min_level = max(1, player.level - 5)
    max_level = min(100, player.level + 5)

    if new_level < min_level or new_level > max_level:
        return False, f"You can access dungeon levels {min_level} to {max_level}."

    old_level = player.dungeon_level or player.level

    player.dungeon_level = new_level

    if new_level == old_level:
        return True, f"You remain on dungeon level {new_level}."
    elif new_level > old_level:
        return True, f"You descend to dungeon level {new_level}."
    else:
        return True, f"You ascend to dungeon level {new_level}."


# =========================================================================
# TEAM / GANG TOWN CLAIMING SYSTEM
# =========================================================================

def gang_war(attacker_team, defender_team):
    """Simulate a gang war between two teams for town control.

    Based on the original GANGWARS.PAS - teams fight member vs member
    in rounds until one team is wiped out.
    Returns (winner_team, loser_team, battle_log).
    """
    att_members = [m.player for m in attacker_team.members
                   if m.player and m.player.hp > 0 and not m.player.is_imprisoned]
    def_members = [m.player for m in defender_team.members
                   if m.player and m.player.hp > 0 and not m.player.is_imprisoned]

    if not att_members:
        return None, None, ["Attacking team has no living, free members!"]
    if not def_members:
        return attacker_team, defender_team, ["Defending team has no members to fight! Easy takeover!"]

    random.shuffle(att_members)
    random.shuffle(def_members)

    log = []
    battle_round = 0

    while att_members and def_members and battle_round < 20:
        battle_round += 1
        log.append(f"--- Battle Round {battle_round} ---")

        matchups = list(zip(att_members[:], def_members[:]))
        for att, defn in matchups:
            if att.hp <= 0 or defn.hp <= 0:
                continue

            att_hp = att.hp
            def_hp = defn.hp
            rounds = 0
            while att_hp > 0 and def_hp > 0 and rounds < 15:
                rounds += 1
                atk = calculate_attack(att.strength, att.weapon_power, att.level)
                ddf = calculate_defense(defn.defence, defn.armor_power)
                dmg = max(1, atk - ddf + random.randint(-3, 5))
                def_hp -= dmg

                if def_hp <= 0:
                    break

                datk = calculate_attack(defn.strength, defn.weapon_power, defn.level)
                adf = calculate_defense(att.defence, att.armor_power)
                ddmg = max(1, datk - adf + random.randint(-3, 5))
                att_hp -= ddmg

            if def_hp <= 0:
                log.append(f"  {att.name} defeated {defn.name} in {rounds} rounds!")
                defn.hp = 0
                att.hp = max(1, att_hp)
                att.experience += max(10, defn.level * 250 + random.randint(0, 50))
                att.player_kills += 1
                defn.player_defeats += 1
            elif att_hp <= 0:
                log.append(f"  {defn.name} defeated {att.name} in {rounds} rounds!")
                att.hp = 0
                defn.hp = max(1, def_hp)
                defn.experience += max(10, att.level * 250 + random.randint(0, 50))
                defn.player_kills += 1
                att.player_defeats += 1
            else:
                log.append(f"  {att.name} vs {defn.name}: Draw after {rounds} rounds!")

        att_members = [m for m in att_members if m.hp > 0]
        def_members = [m for m in def_members if m.hp > 0]

    if not def_members:
        attacker_team.wins += 1
        defender_team.losses += 1
        log.append(f"{attacker_team.name} is victorious!")
        return attacker_team, defender_team, log
    elif not att_members:
        defender_team.wins += 1
        attacker_team.losses += 1
        log.append(f"{defender_team.name} repelled the attack!")
        return defender_team, attacker_team, log
    else:
        log.append("Both teams still standing - no clear winner!")
        return None, None, log


def claim_town(attacker_team, player):
    """Attempt to claim town control for a team.

    Based on original GANGWARS.PAS turf war system.
    """
    if player.team_fights < 1:
        return False, [], "No team fights remaining today."

    # Find current town controller
    controlling_team = Team.query.filter_by(town_control=True).first()

    if controlling_team and controlling_team.id == attacker_team.id:
        return False, [], "Your team already controls the town!"

    player.team_fights -= 1

    if not controlling_team:
        # No one controls the town - easy takeover
        attacker_team.town_control = True
        attacker_team.town_control_days = 0
        for member in attacker_team.members:
            if member.player:
                member.player.town_control = True
        log = ["No team controls the town!", f"{attacker_team.name} claims the town without bloodshed!"]

        news = NewsEntry(category='gang',
                         message=f"Gang Takeover! {attacker_team.name} took over the town without bloodshed.")
        db.session.add(news)

        # Mail all team members
        for member in attacker_team.members:
            if member.player and not member.player.is_npc and member.player.id != player.id:
                mail = Mail(sender_id=player.id, receiver_id=member.player.id,
                            subject="Town Control!",
                            message=f"{player.name} led your team to control the town!")
                db.session.add(mail)

        return True, log, ""

    # Check if defenders have living, free members
    def_alive = [m.player for m in controlling_team.members
                 if m.player and m.player.hp > 0 and not m.player.is_imprisoned]

    if not def_alive:
        # Defenders are all dead or in prison - easy takeover
        controlling_team.town_control = False
        for member in controlling_team.members:
            if member.player:
                member.player.town_control = False

        # Check for team record before transferring
        _check_team_record(controlling_team)

        attacker_team.town_control = True
        attacker_team.town_control_days = 0
        for member in attacker_team.members:
            if member.player:
                member.player.town_control = True

        log = [f"{controlling_team.name} members are all dead or in prison!",
               f"{attacker_team.name} takes over without bloodshed!"]

        news = NewsEntry(category='gang',
                         message=f"Gang Takeover! {attacker_team.name} took the town from {controlling_team.name} without a fight.")
        db.session.add(news)

        # Mail defenders
        for member in controlling_team.members:
            if member.player and not member.player.is_npc:
                mail = Mail(sender_id=player.id, receiver_id=member.player.id,
                            subject="Lost Town Control!",
                            message=f"{attacker_team.name} took over the town. Your team couldn't fight back!")
                db.session.add(mail)

        return True, log, ""

    # Full gang war!
    news = NewsEntry(category='gang',
                     message=f"Gang War! {attacker_team.name} challenged {controlling_team.name} for town control!")
    db.session.add(news)

    winner, loser, log = gang_war(attacker_team, controlling_team)

    if winner and winner.id == attacker_team.id:
        # Attacker wins - transfer town control
        _check_team_record(controlling_team)
        controlling_team.town_control = False
        for member in controlling_team.members:
            if member.player:
                member.player.town_control = False

        attacker_team.town_control = True
        attacker_team.town_control_days = 0
        for member in attacker_team.members:
            if member.player:
                member.player.town_control = True

        news = NewsEntry(category='gang',
                         message=f"{attacker_team.name} wiped out {controlling_team.name} and took over the town!")
        db.session.add(news)

        # Mail losers
        for member in controlling_team.members:
            if member.player and not member.player.is_npc:
                mail = Mail(sender_id=player.id, receiver_id=member.player.id,
                            subject="Lost Town Control!",
                            message=f"{attacker_team.name} defeated your team and took over the town!")
                db.session.add(mail)

        return True, log, ""
    else:
        news = NewsEntry(category='gang',
                         message=f"{attacker_team.name}'s attack on {controlling_team.name} was repelled!")
        db.session.add(news)
        return False, log, "Your attack was repelled!"


def _check_team_record(team):
    """Check if team's town control duration is a new record."""
    if team.town_control_days <= 0:
        return
    best = TeamRecord.query.order_by(TeamRecord.days_held.desc()).first()
    if not best or team.town_control_days > best.days_held:
        record = TeamRecord(team_name=team.name, days_held=team.town_control_days)
        db.session.add(record)
        news = NewsEntry(category='gang',
                         message=f"Record Broken! {team.name} held the town for {team.town_control_days} days!")
        db.session.add(news)


def team_donate(player, team, amount):
    """Donate gold to team treasury."""
    if amount <= 0 or player.gold < amount:
        return False, "Not enough gold."
    player.gold -= amount
    team.treasury += amount
    return True, f"Donated {amount} gold to {team.name}'s treasury."


def team_withdraw(player, team, amount):
    """Withdraw gold from team treasury (leader only)."""
    if team.leader_id != player.id:
        return False, "Only the team leader can withdraw."
    if amount <= 0 or team.treasury < amount:
        return False, "Not enough gold in treasury."
    team.treasury -= amount
    player.gold += amount
    return True, f"Withdrew {amount} gold from treasury."


def transfer_leadership(player, team, target_name):
    """Transfer team leadership to another member."""
    if team.leader_id != player.id:
        return False, "Only the leader can transfer leadership."
    target = Player.query.filter(Player.name.ilike(target_name)).first()
    if not target:
        return False, "Player not found."
    membership = TeamMember.query.filter_by(team_id=team.id, player_id=target.id).first()
    if not membership:
        return False, f"{target.name} is not in your team."
    team.leader_id = target.id
    news = NewsEntry(player_id=target.id, category='social',
                     message=f"{target.name} is now the leader of {team.name}!")
    db.session.add(news)
    return True, f"Leadership transferred to {target.name}."


def kick_member(player, team, target_name):
    """Kick a member from the team (leader only)."""
    if team.leader_id != player.id:
        return False, "Only the leader can kick members."
    target = Player.query.filter(Player.name.ilike(target_name)).first()
    if not target:
        return False, "Player not found."
    if target.id == player.id:
        return False, "Cannot kick yourself."
    membership = TeamMember.query.filter_by(team_id=team.id, player_id=target.id).first()
    if not membership:
        return False, f"{target.name} is not in your team."
    db.session.delete(membership)
    target.team_name = ''
    target.town_control = False
    if not target.is_npc:
        mail = Mail(sender_id=player.id, receiver_id=target.id,
                    subject="Kicked from Team",
                    message=f"You have been kicked from {team.name} by {player.name}.")
        db.session.add(mail)
    return True, f"{target.name} has been kicked from the team."


# =========================================================================
# ROYAL QUEST SYSTEM
# =========================================================================

QUEST_DIFFICULTY_MONSTERS = {
    1: 2, 2: 3, 3: 5, 4: 6, 5: 7, 6: 9, 7: 10, 8: 12, 9: 14, 10: 17
}

QUEST_REWARDS = {
    'experience': {1: 500, 2: 2000, 3: 8000},
    'gold': {1: 200, 2: 1000, 3: 5000},
    'potions': {1: 2, 2: 5, 3: 10},
    'chivalry': {1: 5, 2: 15, 3: 30},
    'darkness': {1: 5, 2: 15, 3: 30},
}


def create_royal_quest(king, difficulty, reward_type, reward_size,
                       penalty_type, penalty_size, days, min_level, max_level,
                       comment='', target_name=''):
    """King creates a new royal quest."""
    king_record = KingRecord.query.filter_by(player_id=king.id, is_current=True).first()
    if not king_record:
        return False, None, "You are not the current ruler."
    if king_record.quests_left < 1:
        return False, None, "No quests remaining today."

    monsters_needed = QUEST_DIFFICULTY_MONSTERS.get(difficulty, 7)

    quest = RoyalQuest(
        initiator_id=king.id,
        title=f"Royal Quest (Diff {difficulty})",
        comment=comment,
        difficulty=difficulty,
        monsters_required=monsters_needed * king.level,
        days_to_complete=days,
        min_level=min_level,
        max_level=max_level,
        reward_type=reward_type,
        reward_size=reward_size,
        penalty_type=penalty_type,
        penalty_size=penalty_size,
        is_public=not bool(target_name),
    )

    if target_name:
        target = Player.query.filter(Player.name.ilike(target_name)).first()
        if not target or target.id == king.id:
            return False, None, f"Player '{target_name}' not found or cannot assign quest to yourself."
        quest.occupier_id = target.id
        mail = Mail(sender_id=king.id, receiver_id=target.id,
                    subject="Royal Quest Assigned!",
                    message=f"The ruler has assigned you a quest! Difficulty: {difficulty}. "
                            f"You must defeat {quest.monsters_required} monsters in {days} days.")
        db.session.add(mail)

    db.session.add(quest)
    king_record.quests_left -= 1

    title = 'King' if king.sex == 1 else 'Queen'
    news = NewsEntry(player_id=king.id, category='royal',
                     message=f"{title} {king.name} initiated a Royal Quest! (Difficulty {difficulty})")
    db.session.add(news)

    return True, quest, ""


def claim_quest(player, quest_id):
    """Player claims an available quest."""
    quest = db.session.get(RoyalQuest, quest_id)
    if not quest:
        return False, "Quest not found."
    if quest.occupier_id:
        return False, "Quest is already claimed."
    if quest.is_completed or quest.is_failed:
        return False, "Quest is no longer available."
    if player.level < quest.min_level or player.level > quest.max_level:
        return False, f"Quest requires level {quest.min_level}-{quest.max_level}."

    quest.occupier_id = player.id
    news = NewsEntry(player_id=player.id, category='royal',
                     message=f"{player.name} has claimed a Royal Quest!")
    db.session.add(news)
    return True, f"Quest claimed! Defeat {quest.monsters_required} monsters in {quest.days_to_complete} days."


def quest_monster_killed(player):
    """Called when player kills a monster - progress active quests."""
    active_quests = RoyalQuest.query.filter_by(
        occupier_id=player.id, is_completed=False, is_failed=False
    ).all()
    for quest in active_quests:
        quest.monsters_killed += 1
        if quest.monsters_killed >= quest.monsters_required:
            complete_quest(player, quest)


def complete_quest(player, quest):
    """Complete a quest and grant rewards."""
    quest.is_completed = True
    player.quests_completed += 1

    reward_table = QUEST_REWARDS.get(quest.reward_type, {})
    reward_amount = reward_table.get(quest.reward_size, 0) * max(1, player.level)

    msg_parts = [f"Quest Complete! "]

    if quest.reward_type == 'experience':
        player.experience += reward_amount
        msg_parts.append(f"Gained {reward_amount} experience!")
    elif quest.reward_type == 'gold':
        player.gold += reward_amount
        msg_parts.append(f"Gained {reward_amount} gold!")
    elif quest.reward_type == 'potions':
        pot_amount = reward_table.get(quest.reward_size, 2)
        player.healing_potions += pot_amount
        msg_parts.append(f"Gained {pot_amount} potions!")
    elif quest.reward_type == 'chivalry':
        chiv_amount = reward_table.get(quest.reward_size, 5)
        player.chivalry += chiv_amount
        msg_parts.append(f"Gained {chiv_amount} chivalry!")
    elif quest.reward_type == 'darkness':
        dark_amount = reward_table.get(quest.reward_size, 5)
        player.darkness += dark_amount
        msg_parts.append(f"Gained {dark_amount} darkness!")

    news = NewsEntry(player_id=player.id, category='royal',
                     message=f"{player.name} completed a Royal Quest!")
    db.session.add(news)

    return ' '.join(msg_parts)


def fail_quest(player, quest):
    """Fail a quest and apply penalties."""
    quest.is_failed = True
    player.quests_failed += 1

    if quest.penalty_type and quest.penalty_size > 0:
        penalty_table = QUEST_REWARDS.get(quest.penalty_type, {})
        penalty_amount = penalty_table.get(quest.penalty_size, 0) * max(1, player.level // 2)

        if quest.penalty_type == 'experience':
            player.experience = max(0, player.experience - penalty_amount)
        elif quest.penalty_type == 'gold':
            player.gold = max(0, player.gold - penalty_amount)

    news = NewsEntry(player_id=player.id, category='royal',
                     message=f"{player.name} failed a Royal Quest!")
    db.session.add(news)


def quest_maintenance():
    """Daily maintenance for quests - increment days, fail expired ones."""
    active_quests = RoyalQuest.query.filter_by(is_completed=False, is_failed=False).filter(
        RoyalQuest.occupier_id.isnot(None)
    ).all()
    for quest in active_quests:
        quest.days_elapsed += 1
        if quest.days_elapsed >= quest.days_to_complete:
            occupier = db.session.get(Player, quest.occupier_id)
            if occupier:
                fail_quest(occupier, quest)


# =========================================================================
# CHILDREN / PREGNANCY / FAMILY SYSTEM
# =========================================================================

CHILD_NAMES_M = [
    "Aldric", "Bram", "Caelum", "Dain", "Eamon", "Falk", "Gareth",
    "Halvar", "Ingram", "Jorin", "Kael", "Lucian", "Marten", "Niles",
    "Osric", "Perin", "Quillan", "Rolf", "Soren", "Tobin",
]

CHILD_NAMES_F = [
    "Aelwen", "Briar", "Cora", "Desta", "Elsbeth", "Freya", "Greta",
    "Hilda", "Isolde", "Juna", "Kira", "Liora", "Maren", "Neve",
    "Olwen", "Petra", "Rosalind", "Sigrid", "Thora", "Una",
]


def attempt_intimacy(player):
    """Attempt intimacy with spouse, possibly resulting in pregnancy."""
    if not player.married or not player.spouse_id:
        return False, "You are not married."

    spouse = db.session.get(Player, player.spouse_id)
    if not spouse:
        return False, "Spouse not found."

    # Determine who can become pregnant (female partner)
    mother = player if player.sex == 2 else spouse
    father = spouse if player.sex == 2 else player

    if mother.sex != 2 or father.sex != 1:
        # Same sex couple - adoption chance instead
        return _try_adoption(player, spouse)

    if mother.is_pregnant:
        return True, "You spend time together. Your family is already growing!"

    # Romance event text
    events = [
        "You share a romantic evening by candlelight.",
        "You take a moonlit walk together through the gardens.",
        "You spend a passionate night together.",
        "You share sweet words and tender embraces.",
    ]
    msg = random.choice(events)

    # Pregnancy chance
    if random.randint(1, 4) == 1:  # 25% chance
        mother.is_pregnant = True
        mother.pregnancy_days = 0
        msg += " Wonderful news - you are expecting a child!"

        news = NewsEntry(category='social',
                         message=f"{player.name} and {spouse.name} are expecting a child!")
        db.session.add(news)

    return True, msg


def _try_adoption(player, spouse):
    """Same-sex couples can adopt orphans."""
    orphans = Child.query.filter_by(is_orphan=True).all()
    if orphans:
        child = random.choice(orphans)
        child.is_orphan = False
        child.mother_id = player.id if player.sex == 2 else spouse.id
        child.father_id = spouse.id if player.sex == 2 else player.id
        player.children_count += 1
        spouse.children_count += 1
        return True, f"You adopted {child.name} from the orphanage!"
    return True, "You spend a lovely evening together."


def pregnancy_maintenance():
    """Daily pregnancy advancement."""
    pregnant = Player.query.filter_by(is_pregnant=True).all()
    for mother in pregnant:
        mother.pregnancy_days += 1
        if mother.pregnancy_days >= 3:  # 3-day gestation
            _give_birth(mother)


def _give_birth(mother):
    """Mother gives birth to a child."""
    father = db.session.get(Player, mother.spouse_id) if mother.spouse_id else None

    sex = random.choice([1, 2])
    names = CHILD_NAMES_M if sex == 1 else CHILD_NAMES_F
    name = random.choice(names)

    # Inherit race from parents
    parent_races = [mother.race]
    if father:
        parent_races.append(father.race)
    child_race = random.choice(parent_races)

    descriptions = [
        "has bright eyes and a curious nature",
        "looks strong and healthy",
        "has a mischievous grin",
        "seems quiet and thoughtful",
        "cries loudly announcing their arrival",
    ]

    child = Child(
        name=name,
        mother_id=mother.id,
        father_id=father.id if father else mother.id,
        sex=sex,
        race=child_race,
        description=random.choice(descriptions),
    )
    db.session.add(child)

    mother.is_pregnant = False
    mother.pregnancy_days = 0
    mother.children_count += 1
    if father:
        father.children_count += 1

    sex_word = 'boy' if sex == 1 else 'girl'
    news = NewsEntry(category='social',
                     message=f"{mother.name} gave birth to a baby {sex_word} named {name}!")
    db.session.add(news)

    # Mail both parents
    if father and not father.is_npc and father.id != mother.id:
        mail = Mail(sender_id=mother.id, receiver_id=father.id,
                    subject=f"A {sex_word} is born!",
                    message=f"You are now the proud parent of {name}!")
        db.session.add(mail)


def get_player_children(player):
    """Get all children of a player."""
    return Child.query.filter(
        (Child.mother_id == player.id) | (Child.father_id == player.id)
    ).all()


# =========================================================================
# HOME SYSTEM (from original HOME.PAS)
# =========================================================================

MAX_CHEST_ITEMS = 10  # configurable: config.homeitems in original


def get_home_info(player):
    """Get all info needed for the home screen."""
    spouse = db.session.get(Player, player.spouse_id) if player.spouse_id else None
    children = get_player_children(player)
    home_children = [c for c in children if _has_access(player, c) and c.location == 'home']
    kidnapped_children = [c for c in children if c.kidnapped_by_id and _has_access(player, c)]
    chest_count = HomeChestItem.query.filter_by(player_id=player.id).count()

    # Marriage duration message
    marriage_msg = ''
    if spouse:
        rel = Relationship.query.filter(
            ((Relationship.player1_id == player.id) & (Relationship.player2_id == spouse.id)) |
            ((Relationship.player1_id == spouse.id) & (Relationship.player2_id == player.id))
        ).filter_by(rel_type='married').first()
        if rel:
            days = (datetime.now(timezone.utc) - rel.created_at).days
            marriage_msg = f"You have been married for {days} day{'s' if days != 1 else ''}."
            if days > 300:
                marriage_msg += " *You are a golden couple*"
            elif days > 100:
                marriage_msg += " Congratulations!"
            elif days > 50:
                marriage_msg += " Keep it up!"
            elif days > 10:
                marriage_msg += " Nice going."

    return {
        'spouse': spouse,
        'children': children,
        'home_children': home_children,
        'kidnapped_children': kidnapped_children,
        'chest_count': chest_count,
        'max_chest': MAX_CHEST_ITEMS,
        'marriage_msg': marriage_msg,
        'intimacy_acts': player.intimacy_acts if player.intimacy_acts else 0,
    }


def _has_access(player, child):
    """Check if player has custody access to this child."""
    if player.sex == 1 and child.father_id == player.id:
        return child.father_access if child.father_access is not None else True
    if player.sex == 2 and child.mother_id == player.id:
        return child.mother_access if child.mother_access is not None else True
    # Fallback: check if either parent
    if child.father_id == player.id or child.mother_id == player.id:
        return True
    return False


def go_to_sleep(player):
    """Player goes to sleep at home. Ends their session for the day.

    Based on original HOME.PAS 'G' option - Go to sleep.
    """
    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"Home sweet home: {player.name} fell asleep at home."
    )
    db.session.add(news)
    return True, "You drift off to sleep in the comfort of your own home... Sweet dreams."


def have_sex_at_home(player):
    """Have sex with spouse at home.

    Based on original HOME.PAS 'H' option and RELATION.PAS Sex_Act_Routine.
    """
    if not player.married or not player.spouse_id:
        return False, "You are not married. There's no one here to spend the night with."

    if not player.intimacy_acts or player.intimacy_acts < 1:
        return False, "You have no intimate sessions left today."

    spouse = db.session.get(Player, player.spouse_id)
    if not spouse:
        return False, "Your spouse has disappeared from the World of Usurper!"

    # NPC spouse: 50% chance of refusal (original: random(2) = 0)
    if spouse.is_npc and random.randint(0, 1) == 0:
        player.intimacy_acts -= 1
        return False, f"{spouse.name} doesn't feel like doing it right now."

    # Calculate experience (from original sex_experience function)
    xp = (player.level * 244 + spouse.level * 244) // 2
    xp = max(100, xp)

    player.experience += xp
    spouse.experience += xp
    player.intimacy_acts -= 1

    # Determine who can become pregnant
    mother = player if player.sex == 2 else spouse
    father = spouse if player.sex == 2 else player

    pregnancy_msg = ''
    if mother.sex == 2 and father.sex == 1 and not mother.is_pregnant:
        if random.randint(1, 4) == 1:  # 25% pregnancy chance
            mother.is_pregnant = True
            mother.pregnancy_days = 0
            pregnancy_msg = " Wonderful news - you are expecting a child!"
            news = NewsEntry(
                category='social',
                message=f"{player.name} and {spouse.name} are expecting a child!"
            )
            db.session.add(news)

    # Romantic descriptions
    scenes = [
        f"You and {spouse.name} share a passionate night together.",
        f"You embrace {spouse.name} tenderly. A wonderful evening!",
        f"You and {spouse.name} spend the night in each other's arms.",
        f"A romantic evening by candlelight with {spouse.name}.",
    ]
    msg = random.choice(scenes)
    msg += f" You both earned {xp:,} experience points!"
    msg += pregnancy_msg

    # News
    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"In Bed: {player.name} and {spouse.name} shared a bed."
    )
    db.session.add(news)

    # Mail spouse if human
    if not spouse.is_npc:
        mail = Mail(
            sender_id=player.id,
            receiver_id=spouse.id,
            subject="Spending the Night",
            message=f"{player.name} spent the night with you. "
                    f"You had a wonderful time! You earned {xp:,} experience points."
        )
        db.session.add(mail)

    return True, msg


# --- Home Chest (Item Storage) ---

def get_chest_items(player):
    """Get all items stored in player's home chest."""
    return HomeChestItem.query.filter_by(player_id=player.id).order_by(
        HomeChestItem.stored_at.desc()
    ).all()


def store_item_in_chest(player, inv_item_id):
    """Move an item from inventory to home chest.

    Based on original INVENT.PAS Chest_with_Items 'A' option.
    """
    chest_count = HomeChestItem.query.filter_by(player_id=player.id).count()
    if chest_count >= MAX_CHEST_ITEMS:
        return False, f"Your chest is full! (Max {MAX_CHEST_ITEMS} items)"

    inv_item = InventoryItem.query.filter_by(id=inv_item_id, player_id=player.id).first()
    if not inv_item:
        return False, "Item not found in your inventory."

    # Can't store equipped items
    item = db.session.get(Item, inv_item.item_id)
    if not item:
        return False, "Item data not found."

    # Check if item is currently equipped
    for slot in ['weapon', 'armor', 'shield', 'helmet', 'ring', 'amulet']:
        if getattr(player, f'equipped_{slot}', None) == item.id:
            return False, f"Unequip {item.name} before storing it."

    # Move to chest
    chest_item = HomeChestItem(player_id=player.id, item_id=item.id)
    db.session.add(chest_item)
    db.session.delete(inv_item)

    return True, f"You place the {item.name} carefully in your chest."


def retrieve_item_from_chest(player, chest_item_id):
    """Move an item from home chest back to inventory.

    Based on original INVENT.PAS Chest_with_Items 'G' option.
    """
    chest_item = HomeChestItem.query.filter_by(
        id=chest_item_id, player_id=player.id
    ).first()
    if not chest_item:
        return False, "Item not found in your chest."

    # Check inventory space (max 15 items, consistent with rest of game)
    inv_count = InventoryItem.query.filter_by(player_id=player.id).count()
    if inv_count >= 15:
        return False, "Your inventory is full! (Max 15 items)"

    item = db.session.get(Item, chest_item.item_id)
    if not item:
        db.session.delete(chest_item)
        return False, "Item data corrupted."

    # Move to inventory
    inv_item = InventoryItem(player_id=player.id, item_id=item.id)
    db.session.add(inv_item)
    db.session.delete(chest_item)

    return True, f"You take the {item.name} and put it in your inventory."


# --- Child Custody Management ---

def share_custody(player, child_id):
    """Share custody of a child with the other parent.

    Based on original HOME.PAS 'S' (Share custody) option.
    """
    child = db.session.get(Child, child_id)
    if not child:
        return False, "Child not found."

    if not _has_access(player, child):
        return False, "You don't have access to this child."

    if child.location != 'home':
        return False, f"{child.name} must be home before you can share custody."

    # Find the other parent
    if player.sex == 1:  # father
        other_parent_id = child.mother_id
        other_role = "mother"
    else:
        other_parent_id = child.father_id
        other_role = "father"

    other_parent = db.session.get(Player, other_parent_id) if other_parent_id else None
    if not other_parent:
        return False, f"{child.name}'s {other_role} has disappeared!"

    # Check if already shared
    if child.mother_access and child.father_access:
        return False, f"You already share custody of {child.name}!"

    # Check if parents are married (can't share if married - use nursery instead)
    # Actually in original, sharing is for divorced couples
    child.mother_access = True
    child.father_access = True

    # Notify other parent
    if not other_parent.is_npc:
        mail = Mail(
            sender_id=player.id,
            receiver_id=other_parent.id,
            subject="Custody Shared!",
            message=f"{player.name} shared custody of your "
                    f"{'son' if child.sex == 1 else 'daughter'} {child.name}! "
                    f"You can once again see your child."
        )
        db.session.add(mail)

    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"Child Happiness! {player.name} shared custody of {child.name}!"
    )
    db.session.add(news)

    return True, f"{child.name} has reunited with both parents! {child.name} is happy!"


def abandon_child(player, child_id):
    """Abandon custody of a child. Other parent gets full custody.

    Based on original HOME.PAS 'A' (Abandon child) option.
    """
    child = db.session.get(Child, child_id)
    if not child:
        return False, "Child not found."

    if not _has_access(player, child):
        return False, "You don't have access to this child."

    if child.location != 'home':
        return False, f"{child.name} must be home before you can abandon them."

    # Can't abandon if married to the other parent
    if player.sex == 1:
        other_parent_id = child.mother_id
    else:
        other_parent_id = child.father_id

    if player.married and player.spouse_id == other_parent_id:
        return False, "A child can't be rejected when the parents are married!"

    # Remove player's access
    if player.sex == 1:
        child.father_access = False
        child.mother_access = True
    else:
        child.mother_access = False
        child.father_access = True

    # Check if other parent exists
    other_parent = db.session.get(Player, other_parent_id) if other_parent_id else None
    if not other_parent:
        # No other parent - child goes to orphanage
        child.location = 'orphanage'
        child.is_orphan = True
        news = NewsEntry(
            player_id=player.id,
            category='social',
            message=f"Child Transport: {player.name} sent {child.name} to the Royal Orphanage!"
        )
        db.session.add(news)
        return True, f"{child.name} has been sent to the Royal Orphanage."

    # Notify other parent
    sex_word = 'son' if child.sex == 1 else 'daughter'
    if not other_parent.is_npc:
        mail = Mail(
            sender_id=player.id,
            receiver_id=other_parent.id,
            subject="Child Rejected!",
            message=f"{player.name} rejected your {sex_word} {child.name}! "
                    f"You are now on your own, with full responsibility."
        )
        db.session.add(mail)

    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"Child Rejected! {player.name} rejected {child.name}!"
    )
    db.session.add(news)

    return True, f"{child.name} was kicked out from the house! {child.name} is now living with the other parent."


def send_to_orphanage(player, child_id):
    """Send a child to the Royal Orphanage.

    Based on original HOME.PAS 'O' (Orphanage) option.
    """
    child = db.session.get(Child, child_id)
    if not child:
        return False, "Child not found."

    if not _has_access(player, child):
        return False, "You don't have access to this child."

    if child.location != 'home':
        return False, f"{child.name} must be home before you can transfer them."

    # Can't transfer if married to the other parent
    if player.sex == 1:
        other_parent_id = child.mother_id
    else:
        other_parent_id = child.father_id

    if player.married and player.spouse_id == other_parent_id:
        return False, "A child can't be transferred when the parents are married! Visit the nursery instead."

    child.location = 'orphanage'
    child.is_orphan = True

    # Remove player's access
    if player.sex == 1:
        child.father_access = False
    else:
        child.mother_access = False

    # Notify other parent
    other_parent = db.session.get(Player, other_parent_id) if other_parent_id else None
    if other_parent and not other_parent.is_npc:
        sex_word = 'son' if child.sex == 1 else 'daughter'
        mail = Mail(
            sender_id=player.id,
            receiver_id=other_parent.id,
            subject="Child Transferred!",
            message=f"{player.name} transferred your {sex_word} {child.name} to the Royal Orphanage!"
        )
        db.session.add(mail)

    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"Child Transport: {player.name} transferred {child.name} to the Royal Orphanage. The townspeople are upset!"
    )
    db.session.add(news)

    return True, f"{child.name} has been sent to the Royal Orphanage."


def pay_ransom(player, child_id):
    """Pay ransom to free a kidnapped child.

    Based on original HOME.PAS 'P' (Pay ransom) option.
    """
    child = db.session.get(Child, child_id)
    if not child:
        return False, "Child not found."

    # Verify the player is actually a parent of this child
    if not _has_access(player, child):
        return False, "This is not your child."

    if not child.kidnapped_by_id or child.location != 'kidnapped':
        return False, f"{child.name} is not kidnapped."

    ransom = child.ransom_amount or 0
    if ransom <= 0:
        return False, "No ransom has been demanded."

    if player.gold < ransom:
        return False, f"You don't have enough gold! Ransom: {ransom:,} gold."

    kidnapper = db.session.get(Player, child.kidnapped_by_id)

    # Pay ransom
    player.gold -= ransom
    if kidnapper:
        kidnapper.gold += ransom
        if not kidnapper.is_npc:
            mail = Mail(
                sender_id=player.id,
                receiver_id=kidnapper.id,
                subject="Ransom Paid",
                message=f"{player.name} paid the ransom for {child.name}! "
                        f"You received {ransom:,} gold. (good work evil one!)"
            )
            db.session.add(mail)

    # Free child
    child.kidnapped_by_id = None
    child.ransom_amount = 0
    child.location = 'home'

    news = NewsEntry(
        player_id=player.id,
        category='social',
        message=f"Released! {child.name} was released after {player.name} paid the {ransom:,} gold ransom!"
    )
    db.session.add(news)

    return True, f"{child.name} has been freed! You paid {ransom:,} gold."


def get_nursery_children(player):
    """Get children available for nursery activities."""
    children = Child.query.filter(
        ((Child.mother_id == player.id) | (Child.father_id == player.id)),
        Child.location == 'home',
        Child.health == 'normal',
    ).all()
    return [c for c in children if _has_access(player, c)]


def nursery_play(player, child_id):
    """Play with a child in the nursery, earning XP for both.

    Based on original HOME.PAS Nursery 'P' option - kid parties.
    """
    child = db.session.get(Child, child_id)
    if not child:
        return False, "Child not found."

    if child.location != 'home' or child.health != 'normal':
        return False, f"{child.name} is not available."

    if not _has_access(player, child):
        return False, "You don't have access to this child."

    # Play scenarios
    scenarios = [
        f"You play hide and seek with {child.name}! What fun!",
        f"You tell {child.name} a bedtime story. They listen with wide eyes.",
        f"You and {child.name} build a castle out of blocks together.",
        f"You teach {child.name} a few sword moves. They're a natural!",
        f"{child.name} shows you a drawing they made. It's beautiful!",
        f"You play catch with {child.name} in the yard.",
    ]

    xp = player.level * 50 + random.randint(50, 200)
    player.experience += xp

    msg = random.choice(scenarios)
    msg += f" You earned {xp:,} experience!"

    return True, msg


# =========================================================================
# DUNGEON EVENTS (original + new RPG events)
# =========================================================================

DUNGEON_EVENTS = [
    # --- Original Usurper events ---
    {
        'id': 'wounded_man',
        'name': 'Wounded Stranger',
        'description': 'You find a wounded man lying on the ground, groaning in pain.',
        'choices': {
            'help': {
                'label': 'Help him',
                'outcomes': [
                    {'weight': 3, 'text': 'The grateful stranger gives you a reward!',
                     'gold': (100, 500), 'chivalry': 5, 'xp': (50, 200)},
                    {'weight': 1, 'text': 'It was a trap! The man attacks you!',
                     'hp': (-30, -10), 'darkness': 2},
                ]
            },
            'rob': {
                'label': 'Rob him',
                'outcomes': [
                    {'weight': 2, 'text': 'You steal his gold. Easy pickings.',
                     'gold': (200, 2000), 'darkness': 5, 'xp': (50, 150)},
                ]
            },
            'ignore': {
                'label': 'Walk away',
                'outcomes': [
                    {'weight': 1, 'text': 'You leave the stranger to his fate.'},
                ]
            },
        },
    },
    {
        'id': 'merchant',
        'name': 'Dungeon Merchant',
        'description': 'A traveling merchant has set up a small stall in the dungeon.',
        'choices': {
            'buy_potion': {
                'label': 'Buy Healing Potion (50g)',
                'outcomes': [
                    {'weight': 1, 'text': 'You purchase a healing potion.',
                     'gold': -50, 'potions': 1, 'condition': 'gold >= 50'},
                    {'weight': 1, 'text': 'You cannot afford it.', 'condition': 'gold < 50'},
                ]
            },
            'browse': {
                'label': 'Browse wares',
                'outcomes': [
                    {'weight': 2, 'text': 'The merchant shows you fine wares but nothing catches your eye.'},
                    {'weight': 1, 'text': 'You spot a rare item! The merchant offers a good deal.',
                     'gold': -200, 'xp': (100, 300), 'condition': 'gold >= 200'},
                ]
            },
            'leave': {
                'label': 'Move on',
                'outcomes': [
                    {'weight': 1, 'text': 'You nod to the merchant and continue.'},
                ]
            },
        },
    },
    {
        'id': 'glue_potion',
        'name': 'Mysterious Potion',
        'description': 'You find a strange glue-like potion on the ground.',
        'choices': {
            'sniff': {
                'label': 'Sniff it',
                'outcomes': [
                    {'weight': 1, 'text': 'The fumes fill your mind with power! But you feel addicted...',
                     'xp_mult': 500, 'addiction': (5, 10)},
                ]
            },
            'leave': {
                'label': 'Leave it alone',
                'outcomes': [
                    {'weight': 1, 'text': 'A wise decision. Who knows what that was.'},
                ]
            },
        },
    },
    {
        'id': 'beggar',
        'name': 'Dungeon Beggar',
        'description': 'A ragged beggar sits against the wall, pleading for coins.',
        'choices': {
            'give': {
                'label': 'Give gold (25g)',
                'outcomes': [
                    {'weight': 2, 'text': 'The beggar blesses you warmly.',
                     'gold': -25, 'chivalry': 3, 'condition': 'gold >= 25'},
                    {'weight': 1, 'text': 'The beggar reveals a secret passage! You find treasure!',
                     'gold': (200, 800), 'xp': (100, 300), 'chivalry': 5, 'condition': 'gold >= 25'},
                ]
            },
            'attack': {
                'label': 'Attack him',
                'outcomes': [
                    {'weight': 1, 'text': 'The beggar was actually a powerful wizard in disguise!',
                     'hp': (-40, -20), 'darkness': 5},
                    {'weight': 1, 'text': 'You strike down the beggar. A few coins fall from his rags.',
                     'gold': (10, 50), 'darkness': 8},
                ]
            },
            'ignore': {
                'label': 'Walk past',
                'outcomes': [
                    {'weight': 1, 'text': 'You walk past the beggar without a second glance.'},
                ]
            },
        },
    },
    {
        'id': 'witch_doctor',
        'name': 'Witch Doctor',
        'description': 'A strange figure beckons you. "I am Mbluta, the witch doctor! I can cure what ails you!"',
        'choices': {
            'cure': {
                'label': 'Accept treatment (100g)',
                'outcomes': [
                    {'weight': 1, 'text': 'The witch doctor waves his hands and you feel renewed!',
                     'gold': -100, 'cure_all': True, 'hp_restore': 0.5, 'condition': 'gold >= 100'},
                    {'weight': 1, 'text': 'You cannot afford the treatment.', 'condition': 'gold < 100'},
                ]
            },
            'decline': {
                'label': 'Decline',
                'outcomes': [
                    {'weight': 1, 'text': '"Suit yourself," mutters Mbluta, fading into shadow.'},
                ]
            },
        },
    },
    # --- New RPG-themed events ---
    {
        'id': 'ancient_shrine',
        'name': 'Ancient Shrine',
        'description': 'You discover a crumbling shrine to a forgotten deity. Faint divine energy still lingers.',
        'choices': {
            'pray': {
                'label': 'Pray at the shrine',
                'outcomes': [
                    {'weight': 2, 'text': 'Divine energy fills you! Your wounds heal.',
                     'hp_restore': 0.75, 'mana_restore': 0.5, 'chivalry': 3},
                    {'weight': 1, 'text': 'The shrine crumbles and dark energy lashes out!',
                     'hp': (-25, -10), 'darkness': 3},
                    {'weight': 1, 'text': 'A vision shows you hidden treasures!',
                     'xp': (200, 500), 'gold': (100, 400)},
                ]
            },
            'desecrate': {
                'label': 'Desecrate it',
                'outcomes': [
                    {'weight': 1, 'text': 'You smash the shrine and dark power surges through you!',
                     'xp': (150, 400), 'darkness': 10},
                    {'weight': 1, 'text': 'The shrine explodes! You are caught in the blast.',
                     'hp': (-40, -15), 'darkness': 5},
                ]
            },
            'ignore': {
                'label': 'Pass by',
                'outcomes': [
                    {'weight': 1, 'text': 'You leave the shrine undisturbed.'},
                ]
            },
        },
    },
    {
        'id': 'trapped_chest',
        'name': 'Trapped Chest',
        'description': 'A ornate chest sits in the middle of the room. It looks suspiciously convenient.',
        'choices': {
            'open_careful': {
                'label': 'Open carefully',
                'outcomes': [
                    {'weight': 2, 'text': 'You disarm the trap and find treasure!',
                     'gold': (200, 1000), 'xp': (100, 300)},
                    {'weight': 1, 'text': 'Despite your caution, a needle pricks your finger!',
                     'poison': True, 'gold': (100, 500)},
                ]
            },
            'smash': {
                'label': 'Smash it open',
                'outcomes': [
                    {'weight': 1, 'text': 'The chest explodes! But some gold survives.',
                     'hp': (-20, -5), 'gold': (50, 300)},
                    {'weight': 1, 'text': 'The chest was a mimic! It bites you!',
                     'hp': (-35, -15)},
                ]
            },
            'leave': {
                'label': 'Leave it',
                'outcomes': [
                    {'weight': 1, 'text': 'Discretion is the better part of valor.'},
                ]
            },
        },
    },
    {
        'id': 'magic_fountain',
        'name': 'Magic Fountain',
        'description': 'A fountain of crystal-clear water glows with a soft blue light.',
        'choices': {
            'drink': {
                'label': 'Drink from it',
                'outcomes': [
                    {'weight': 3, 'text': 'The water refreshes and heals you!',
                     'hp_restore': 1.0, 'mana_restore': 1.0, 'cure_all': True},
                    {'weight': 1, 'text': 'The water was cursed! You feel weakened.',
                     'hp': (-20, -10), 'poison': True},
                ]
            },
            'fill_flask': {
                'label': 'Fill a flask',
                'outcomes': [
                    {'weight': 1, 'text': 'You bottle the magical water for later use.',
                     'potions': 2},
                ]
            },
            'leave': {
                'label': 'Move on',
                'outcomes': [
                    {'weight': 1, 'text': 'You leave the fountain behind.'},
                ]
            },
        },
    },
    {
        'id': 'ghostly_warrior',
        'name': 'Ghostly Warrior',
        'description': 'The spirit of a fallen warrior materializes before you, sword drawn.',
        'choices': {
            'fight': {
                'label': 'Stand your ground',
                'outcomes': [
                    {'weight': 2, 'text': 'You battle the spirit and banish it! You feel stronger.',
                     'xp': (200, 600), 'strength_temp': 2},
                    {'weight': 1, 'text': 'The ghost overwhelms you with spectral fury!',
                     'hp': (-40, -20)},
                ]
            },
            'talk': {
                'label': 'Speak to the spirit',
                'outcomes': [
                    {'weight': 2, 'text': 'The warrior shares ancient combat knowledge with you.',
                     'xp': (300, 800)},
                    {'weight': 1, 'text': '"Avenge me..." it whispers, then fades away.',
                     'chivalry': 5},
                ]
            },
            'flee': {
                'label': 'Run away',
                'outcomes': [
                    {'weight': 1, 'text': 'You flee from the apparition.'},
                ]
            },
        },
    },
    {
        'id': 'dragon_hoard',
        'name': 'Dragon\'s Cache',
        'description': 'You stumble upon a small pile of coins and gems. A sleeping drake guards them.',
        'choices': {
            'steal': {
                'label': 'Steal some treasure',
                'outcomes': [
                    {'weight': 2, 'text': 'You grab a handful of gold and slip away!',
                     'gold': (300, 1500), 'xp': (100, 300)},
                    {'weight': 1, 'text': 'The drake wakes up and breathes fire!',
                     'hp': (-50, -25)},
                ]
            },
            'slay': {
                'label': 'Attack the drake',
                'outcomes': [
                    {'weight': 1, 'text': 'You slay the beast and claim the entire hoard!',
                     'gold': (500, 3000), 'xp': (400, 1000)},
                    {'weight': 1, 'text': 'The drake is tougher than expected!',
                     'hp': (-60, -30), 'gold': (200, 800)},
                ]
            },
            'leave': {
                'label': 'Leave quietly',
                'outcomes': [
                    {'weight': 1, 'text': 'You wisely avoid the sleeping drake.'},
                ]
            },
        },
    },
    {
        'id': 'enchanted_armory',
        'name': 'Enchanted Armory',
        'description': 'You find an ancient armory with weapons floating in magical stasis.',
        'choices': {
            'take_weapon': {
                'label': 'Grab a weapon',
                'outcomes': [
                    {'weight': 2, 'text': 'You grab a fine weapon! It hums with power.',
                     'xp': (200, 500), 'weapon_bonus': (2, 5)},
                    {'weight': 1, 'text': 'The weapon is cursed! It burns your hands!',
                     'hp': (-20, -10)},
                ]
            },
            'study': {
                'label': 'Study the enchantments',
                'outcomes': [
                    {'weight': 1, 'text': 'You learn much about magical crafting.',
                     'xp': (300, 700), 'wisdom_temp': 2},
                ]
            },
            'leave': {
                'label': 'Leave it alone',
                'outcomes': [
                    {'weight': 1, 'text': 'Best not to meddle with ancient magic.'},
                ]
            },
        },
    },
    {
        'id': 'lost_adventurer',
        'name': 'Lost Adventurer',
        'description': 'A confused adventurer wanders the corridors, clearly lost.',
        'choices': {
            'help_guide': {
                'label': 'Guide them out',
                'outcomes': [
                    {'weight': 2, 'text': 'The adventurer thanks you and shares some loot!',
                     'gold': (100, 400), 'chivalry': 5, 'xp': (50, 200)},
                ]
            },
            'rob_them': {
                'label': 'Rob them',
                'outcomes': [
                    {'weight': 1, 'text': 'You take their belongings by force.',
                     'gold': (200, 800), 'darkness': 8, 'xp': (50, 100)},
                    {'weight': 1, 'text': 'They fight back! A tough struggle ensues.',
                     'hp': (-30, -15), 'gold': (100, 500), 'darkness': 5},
                ]
            },
            'ignore': {
                'label': 'Leave them',
                'outcomes': [
                    {'weight': 1, 'text': 'You leave them to find their own way.'},
                ]
            },
        },
    },
    {
        'id': 'collapsing_tunnel',
        'name': 'Collapsing Tunnel',
        'description': 'The ceiling starts to crumble! Rocks fall around you!',
        'choices': {
            'run_forward': {
                'label': 'Sprint forward',
                'outcomes': [
                    {'weight': 2, 'text': 'You dash through just in time! You find a new area.',
                     'xp': (100, 300)},
                    {'weight': 1, 'text': 'A rock hits you but you make it through!',
                     'hp': (-25, -10), 'xp': (50, 150)},
                ]
            },
            'take_cover': {
                'label': 'Take cover',
                'outcomes': [
                    {'weight': 2, 'text': 'You find shelter in an alcove and wait it out.'},
                    {'weight': 1, 'text': 'Debris buries you partially! You dig yourself out, bruised.',
                     'hp': (-20, -5)},
                ]
            },
        },
    },
    {
        'id': 'gambling_demons',
        'name': 'Gambling Demons',
        'description': 'A group of imp-like demons sit around a table playing dice. They invite you to join.',
        'choices': {
            'play': {
                'label': 'Play dice (100g wager)',
                'outcomes': [
                    {'weight': 1, 'text': 'You win! The demons pay up grudgingly.',
                     'gold': (100, 500), 'xp': (50, 200), 'condition': 'gold >= 100'},
                    {'weight': 1, 'text': 'You lose! The demons cackle with glee.',
                     'gold': -100, 'condition': 'gold >= 100'},
                    {'weight': 1, 'text': 'You cannot afford the wager.', 'condition': 'gold < 100'},
                ]
            },
            'attack': {
                'label': 'Attack them',
                'outcomes': [
                    {'weight': 1, 'text': 'You scatter the demons and grab the pot!',
                     'gold': (200, 800), 'xp': (100, 300), 'darkness': 3},
                    {'weight': 1, 'text': 'The demons fight back with hellfire!',
                     'hp': (-35, -15), 'darkness': 2},
                ]
            },
            'decline': {
                'label': 'Walk away',
                'outcomes': [
                    {'weight': 1, 'text': '"Your loss!" they shout as you leave.'},
                ]
            },
        },
    },
    # --- Original Usurper event: Harassed Woman ---
    {
        'id': 'harassed_woman',
        'name': 'Woman in Distress',
        'description': 'You hear screams ahead! A woman is being attacked by a group of orcs. They haven\'t noticed you yet.',
        'choices': {
            'rescue': {
                'label': 'Fight the orcs',
                'outcomes': [
                    {'weight': 2, 'text': 'You charge into the fray! The orcs scatter before your fury. The woman thanks you profusely and offers a reward.',
                     'hp': (-15, -5), 'gold': (200, 800), 'xp': (200, 500), 'chivalry': 10},
                    {'weight': 1, 'text': 'The orcs are tougher than they look! You take heavy blows but save the woman. She gives you her family heirloom.',
                     'hp': (-35, -15), 'gold': (400, 1200), 'xp': (300, 600), 'chivalry': 15},
                ]
            },
            'demand_payment': {
                'label': 'Offer help for a price',
                'outcomes': [
                    {'weight': 1, 'text': '"I\'ll pay anything!" she cries. You drive off the orcs and collect your fee.',
                     'gold': (300, 1000), 'xp': (100, 300), 'darkness': 3},
                ]
            },
            'walk_away': {
                'label': 'Walk away',
                'outcomes': [
                    {'weight': 1, 'text': 'You turn your back on her screams. The sounds soon fade.',
                     'darkness': 8},
                ]
            },
        },
    },
    # --- Original Usurper event: Find Item ---
    {
        'id': 'find_item',
        'name': 'Hidden Cache',
        'description': 'Behind a loose stone in the wall, you discover a hidden compartment! Inside you see a leather pouch and what appears to be a wrapped bundle.',
        'choices': {
            'take_pouch': {
                'label': 'Take the pouch',
                'outcomes': [
                    {'weight': 2, 'text': 'The pouch contains a stash of gold coins and a small gemstone!',
                     'gold': (200, 800), 'xp': (50, 150)},
                    {'weight': 1, 'text': 'The pouch is booby-trapped! A small needle pricks your finger.',
                     'gold': (100, 400), 'poison': True},
                ]
            },
            'take_bundle': {
                'label': 'Unwrap the bundle',
                'outcomes': [
                    {'weight': 2, 'text': 'Inside the bundle you find several healing potions, carefully preserved!',
                     'potions': 3, 'xp': (50, 100)},
                    {'weight': 1, 'text': 'The bundle contains a strange scroll. Reading it fills your mind with knowledge!',
                     'xp': (300, 700)},
                ]
            },
            'take_both': {
                'label': 'Grab everything',
                'outcomes': [
                    {'weight': 2, 'text': 'You stuff both the pouch and bundle into your pack. Greed pays off!',
                     'gold': (150, 500), 'potions': 1, 'xp': (100, 200)},
                    {'weight': 1, 'text': 'As you reach in, the compartment collapses! You grab what you can.',
                     'hp': (-10, -5), 'gold': (100, 300)},
                ]
            },
        },
    },
    # --- Dungeon Ambush event ---
    {
        'id': 'dungeon_ambush',
        'name': 'Dungeon Ambush',
        'description': 'You hear a twig snap behind you. Shadows move in the darkness. You are being followed.',
        'choices': {
            'confront': {
                'label': 'Turn and confront them',
                'outcomes': [
                    {'weight': 1, 'text': 'You spin around to face a gang of dungeon bandits!',
                     'hp': (-10, -5), 'xp': (50, 100)},
                ]
            },
            'hide': {
                'label': 'Duck into a side passage',
                'outcomes': [
                    {'weight': 2, 'text': 'You slip into a crevice and the footsteps pass by.',
                     'xp': (30, 80)},
                    {'weight': 1, 'text': 'The crevice leads to a hidden cache!',
                     'gold': (100, 400), 'xp': (50, 150)},
                ]
            },
            'run': {
                'label': 'Sprint ahead',
                'outcomes': [
                    {'weight': 2, 'text': 'You outrun whatever was following you.',
                     'xp': (20, 50)},
                    {'weight': 1, 'text': 'You trip on a loose stone and tumble!',
                     'hp': (-15, -5)},
                ]
            },
        },
    },
    # --- Cursed Tomb event ---
    {
        'id': 'cursed_tomb',
        'name': 'Cursed Tomb',
        'description': 'An ancient sarcophagus sits in an alcove, covered in warning runes that glow faintly red.',
        'choices': {
            'open': {
                'label': 'Open the sarcophagus',
                'outcomes': [
                    {'weight': 1, 'text': 'Inside lies a preserved warrior with a magnificent blade. You take it!',
                     'xp': (300, 700), 'gold': (200, 600)},
                    {'weight': 1, 'text': 'A mummy bursts forth and curses you!',
                     'hp': (-35, -15), 'poison': True, 'darkness': 3},
                ]
            },
            'read_runes': {
                'label': 'Study the runes',
                'outcomes': [
                    {'weight': 2, 'text': 'The runes contain ancient knowledge. You decipher their meaning.',
                     'xp': (200, 500)},
                    {'weight': 1, 'text': 'The runes are a ward. Reading them aloud triggers a blast!',
                     'hp': (-25, -10)},
                ]
            },
            'leave': {
                'label': 'Heed the warnings',
                'outcomes': [
                    {'weight': 1, 'text': 'You wisely leave the tomb undisturbed. Some things are best left alone.'},
                ]
            },
        },
    },
    # --- Wandering Bard event ---
    {
        'id': 'wandering_bard',
        'name': 'Wandering Bard',
        'description': 'A bard sits cross-legged on a stone, playing a haunting melody on a lute. He looks up as you approach.',
        'choices': {
            'listen': {
                'label': 'Listen to his song',
                'outcomes': [
                    {'weight': 2, 'text': 'The music soothes your soul and mends your wounds.',
                     'hp_restore': 0.5, 'mana_restore': 0.25, 'chivalry': 2},
                    {'weight': 1, 'text': 'The song tells of a hidden treasure nearby! He marks your map.',
                     'gold': (150, 500), 'xp': (100, 300)},
                ]
            },
            'request_tale': {
                'label': 'Ask for a tale',
                'outcomes': [
                    {'weight': 1, 'text': 'He tells you the tale of a legendary hero. You feel inspired!',
                     'xp': (200, 600), 'chivalry': 3},
                    {'weight': 1, 'text': 'He tells a dark tale of betrayal. The knowledge weighs on you.',
                     'xp': (250, 500), 'darkness': 2},
                ]
            },
            'rob_bard': {
                'label': 'Steal his lute',
                'outcomes': [
                    {'weight': 1, 'text': 'You snatch the lute. It is enchanted and worth a fortune!',
                     'gold': (300, 800), 'darkness': 8},
                    {'weight': 1, 'text': 'The bard curses you with a discordant note!',
                     'hp': (-20, -10), 'darkness': 5},
                ]
            },
        },
    },
]

# =========================================================================
# MULTI-STEP DUNGEON EVENTS (events with branching storylines)
# =========================================================================

MULTI_STEP_EVENTS = [
    # --- Event 1: Captive Princess Rescue ---
    {
        'id': 'captive_princess',
        'name': 'The Captive Princess',
        'steps': {
            'start': {
                'description': 'You hear muffled cries echoing from a barred chamber ahead. Peering through the rusted grate, you see a young noblewoman chained to the wall. Two brutish orc guards play cards at a table nearby.',
                'choices': {
                    'sneak': {
                        'label': 'Sneak past the guards',
                        'outcomes': [
                            {'weight': 2, 'text': 'You creep silently along the shadows and reach the cell door undetected.',
                             'xp': (50, 100), 'next_step': 'at_cell'},
                            {'weight': 1, 'text': 'A guard spots you! "Intruder!" he bellows.',
                             'hp': (-15, -5), 'next_step': 'guard_fight'},
                        ]
                    },
                    'fight_guards': {
                        'label': 'Attack the guards head-on',
                        'outcomes': [
                            {'weight': 1, 'text': 'You charge in with weapons drawn!',
                             'next_step': 'guard_fight'},
                        ]
                    },
                    'distraction': {
                        'label': 'Create a distraction',
                        'outcomes': [
                            {'weight': 2, 'text': 'You hurl a rock down the corridor. Both guards rush to investigate.',
                             'xp': (80, 150), 'next_step': 'at_cell'},
                            {'weight': 1, 'text': 'One guard investigates while the other stays. You must deal with him.',
                             'next_step': 'guard_fight'},
                        ]
                    },
                    'leave': {
                        'label': 'Walk away',
                        'outcomes': [
                            {'weight': 1, 'text': 'You turn your back on the cries. Not your problem.',
                             'darkness': 5},
                        ]
                    },
                },
            },
            'guard_fight': {
                'description': 'The orc guard swings a massive club at your head! You must fight or flee!',
                'choices': {
                    'fight': {
                        'label': 'Fight the guard',
                        'outcomes': [
                            {'weight': 2, 'text': 'You dodge the club and deliver a killing blow! The guard crumples.',
                             'xp': (200, 400), 'next_step': 'at_cell'},
                            {'weight': 1, 'text': 'The guard lands a heavy hit, but you overpower him in the end.',
                             'hp': (-30, -15), 'xp': (250, 500), 'next_step': 'at_cell'},
                        ]
                    },
                    'flee': {
                        'label': 'Flee for your life',
                        'outcomes': [
                            {'weight': 2, 'text': 'You escape the guard, abandoning the prisoner.',
                             'hp': (-10, -5)},
                            {'weight': 1, 'text': 'The guard catches you with a parting blow as you run!',
                             'hp': (-25, -10)},
                        ]
                    },
                },
            },
            'at_cell': {
                'description': 'You stand before the cell. The noblewoman looks at you with desperate hope. The lock is old but sturdy. You notice a ring of keys hanging on a wall hook nearby.',
                'choices': {
                    'use_keys': {
                        'label': 'Use the keys',
                        'outcomes': [
                            {'weight': 1, 'text': 'The third key works! The chains fall away and the princess is free.',
                             'next_step': 'princess_freed'},
                        ]
                    },
                    'break_lock': {
                        'label': 'Smash the lock with your weapon',
                        'outcomes': [
                            {'weight': 2, 'text': 'After several strikes, the lock shatters!',
                             'xp': (50, 100), 'next_step': 'princess_freed'},
                            {'weight': 1, 'text': 'The noise alerts more guards! You free her, but must hurry!',
                             'hp': (-10, -5), 'next_step': 'princess_freed'},
                        ]
                    },
                    'demand_ransom': {
                        'label': 'Demand payment for rescue',
                        'outcomes': [
                            {'weight': 1, 'text': '"I am Lady Elenora of House Ashford. Free me and you shall be rewarded handsomely."',
                             'darkness': 3, 'next_step': 'princess_freed'},
                        ]
                    },
                },
            },
            'princess_freed': {
                'description': 'Lady Elenora stands free, rubbing her wrists where the chains bit her skin. "You have saved me from a terrible fate," she says, tears in her eyes. "How can I repay you?"',
                'choices': {
                    'escort': {
                        'label': 'Escort her to safety',
                        'outcomes': [
                            {'weight': 2, 'text': 'You guide Lady Elenora safely to the surface. She sends for her family\'s guards. "You are a true hero," she says, pressing a heavy purse into your hands. Her family will remember your valor.',
                             'gold': (500, 2000), 'xp': (400, 800), 'chivalry': 15},
                            {'weight': 1, 'text': 'On the way out you encounter more enemies, but together you fight through! Lady Elenora rewards you generously.',
                             'hp': (-20, -10), 'gold': (800, 3000), 'xp': (500, 1000), 'chivalry': 20},
                        ]
                    },
                    'ask_reward': {
                        'label': 'Ask for a reward now',
                        'outcomes': [
                            {'weight': 1, 'text': 'She hands you a jeweled necklace from her throat. "This is worth more than gold. Take it with my gratitude."',
                             'gold': (300, 1500), 'xp': (200, 500), 'chivalry': 5},
                        ]
                    },
                    'rob_princess': {
                        'label': 'Take everything she has',
                        'outcomes': [
                            {'weight': 1, 'text': 'You strip her of all valuables. She weeps. "You are no better than they were..."',
                             'gold': (1000, 4000), 'darkness': 25, 'xp': (100, 200)},
                        ]
                    },
                },
            },
        },
    },

    # --- Event 2: The Necromancer's Laboratory ---
    {
        'id': 'necromancer_lab',
        'name': 'The Necromancer\'s Laboratory',
        'steps': {
            'start': {
                'description': 'A sickly green glow emanates from a chamber ahead. Inside, a robed necromancer hunches over a workbench covered in bones, vials of dark liquid, and a glowing grimoire. He has not noticed you yet.',
                'choices': {
                    'ambush': {
                        'label': 'Strike while he\'s distracted',
                        'outcomes': [
                            {'weight': 2, 'text': 'Your blade finds its mark! The necromancer staggers, dropping a vial of dark energy.',
                             'xp': (200, 400), 'next_step': 'necro_wounded'},
                            {'weight': 1, 'text': 'He senses your attack at the last moment and throws up a shield of bones!',
                             'next_step': 'necro_combat'},
                        ]
                    },
                    'parley': {
                        'label': 'Announce yourself',
                        'outcomes': [
                            {'weight': 2, 'text': 'The necromancer turns slowly. "Ah, a visitor. How... unexpected. Perhaps we can be of use to each other."',
                             'next_step': 'necro_deal'},
                            {'weight': 1, 'text': '"Fool!" he hisses, raising his hands. Skeletal arms burst from the floor!',
                             'next_step': 'necro_combat'},
                        ]
                    },
                    'steal_grimoire': {
                        'label': 'Try to grab the grimoire',
                        'outcomes': [
                            {'weight': 1, 'text': 'You lunge for the book! Your fingers close around it!',
                             'next_step': 'grimoire_grabbed'},
                            {'weight': 1, 'text': 'The grimoire is warded! Dark energy blasts you backward!',
                             'hp': (-30, -15), 'next_step': 'necro_combat'},
                        ]
                    },
                    'leave': {
                        'label': 'Back away quietly',
                        'outcomes': [
                            {'weight': 1, 'text': 'You wisely retreat from the chamber of horrors.'},
                        ]
                    },
                },
            },
            'necro_combat': {
                'description': 'The necromancer summons three skeletal warriors to fight for him! Their empty eye sockets glow with unholy fire. He begins chanting another spell.',
                'choices': {
                    'fight_skeletons': {
                        'label': 'Destroy the skeletons',
                        'outcomes': [
                            {'weight': 2, 'text': 'You shatter the undead one by one! The necromancer is now defenseless.',
                             'xp': (300, 600), 'next_step': 'necro_wounded'},
                            {'weight': 1, 'text': 'The skeletons are relentless. You destroy them but take heavy wounds.',
                             'hp': (-40, -20), 'xp': (400, 700), 'next_step': 'necro_wounded'},
                        ]
                    },
                    'charge_necro': {
                        'label': 'Ignore the skeletons, charge the necromancer',
                        'outcomes': [
                            {'weight': 1, 'text': 'You barrel past the undead and strike the necromancer! Without his magic, the skeletons collapse.',
                             'hp': (-20, -10), 'xp': (500, 800), 'next_step': 'necro_wounded'},
                            {'weight': 1, 'text': 'The skeletons tear at you as you charge. You reach the necromancer but are badly wounded.',
                             'hp': (-50, -25), 'xp': (400, 600), 'next_step': 'necro_wounded'},
                        ]
                    },
                    'flee': {
                        'label': 'Flee the chamber',
                        'outcomes': [
                            {'weight': 2, 'text': 'You escape the laboratory, skeletal hands clawing at your back.',
                             'hp': (-15, -5)},
                            {'weight': 1, 'text': 'A skeleton blocks the exit! You take a hit forcing your way through.',
                             'hp': (-30, -15)},
                        ]
                    },
                },
            },
            'necro_wounded': {
                'description': 'The necromancer lies bleeding on the floor, his power broken. "Mercy..." he gasps. His grimoire lies open on the table, dark knowledge within reach. Several potions line the shelves.',
                'choices': {
                    'spare': {
                        'label': 'Spare him and take the loot',
                        'outcomes': [
                            {'weight': 1, 'text': 'You gather potions and gold from the laboratory. The necromancer crawls away into the shadows.',
                             'gold': (400, 1200), 'potions': 3, 'xp': (200, 400), 'chivalry': 5},
                        ]
                    },
                    'finish_him': {
                        'label': 'End him permanently',
                        'outcomes': [
                            {'weight': 1, 'text': 'You deliver the killing blow. The laboratory\'s dark energy dissipates. Among his belongings you find a fortune.',
                             'gold': (600, 2000), 'xp': (500, 800), 'darkness': 5},
                        ]
                    },
                    'study_grimoire': {
                        'label': 'Study the grimoire',
                        'outcomes': [
                            {'weight': 2, 'text': 'Dark knowledge floods your mind! You learn terrible secrets of death magic.',
                             'xp': (800, 1500), 'mana_restore': 1.0, 'darkness': 10},
                            {'weight': 1, 'text': 'The grimoire\'s knowledge is too much for your mind! You reel in agony but retain some power.',
                             'hp': (-20, -10), 'xp': (500, 1000), 'darkness': 8},
                        ]
                    },
                },
            },
            'necro_deal': {
                'description': '"I seek a rare ingredient," the necromancer says, his eyes glinting. "Bring me the venom sac of one of the spiders that lurk nearby, and I shall reward you with potions and knowledge. Or... we could simply trade gold for my services."',
                'choices': {
                    'accept_quest': {
                        'label': 'Accept the task',
                        'outcomes': [
                            {'weight': 2, 'text': 'You find a giant spider nest nearby and retrieve a venom sac. The necromancer is pleased and brews you powerful potions.',
                             'hp': (-15, -5), 'potions': 4, 'xp': (300, 600)},
                            {'weight': 1, 'text': 'The spiders prove more dangerous than expected, but you succeed. The necromancer teaches you dark secrets.',
                             'hp': (-30, -15), 'xp': (500, 900), 'mana_restore': 0.5},
                        ]
                    },
                    'buy_potions': {
                        'label': 'Buy potions (200g)',
                        'outcomes': [
                            {'weight': 1, 'text': 'The necromancer sells you potions of unusual potency.',
                             'gold': -200, 'potions': 3, 'condition': 'gold >= 200'},
                            {'weight': 1, 'text': 'You cannot afford his prices.', 'condition': 'gold < 200'},
                        ]
                    },
                    'betray': {
                        'label': 'Attack him while his guard is down',
                        'outcomes': [
                            {'weight': 1, 'text': 'You strike! He was prepared for treachery and summons undead!',
                             'next_step': 'necro_combat'},
                            {'weight': 1, 'text': 'Your surprise attack succeeds! The necromancer falls.',
                             'gold': (300, 1000), 'xp': (300, 500), 'darkness': 12},
                        ]
                    },
                },
            },
            'grimoire_grabbed': {
                'description': 'You hold the grimoire! Dark energy crackles across its surface. The necromancer screams in fury. "GIVE THAT BACK!" He lunges at you, desperate and wild.',
                'choices': {
                    'keep_and_fight': {
                        'label': 'Keep the book and fight',
                        'outcomes': [
                            {'weight': 2, 'text': 'Without his grimoire, the necromancer is weak. You defeat him easily and claim both the book and his treasure.',
                             'gold': (500, 1500), 'xp': (600, 1200), 'darkness': 5},
                            {'weight': 1, 'text': 'He fights desperately and lands several hits, but you prevail.',
                             'hp': (-25, -10), 'gold': (400, 1200), 'xp': (500, 1000), 'darkness': 3},
                        ]
                    },
                    'return_book': {
                        'label': 'Return the book for a reward',
                        'outcomes': [
                            {'weight': 1, 'text': '"Perhaps you are not a fool after all," he says, calming down. He rewards your mercy with potions and gold.',
                             'gold': (200, 800), 'potions': 3, 'xp': (200, 500)},
                        ]
                    },
                    'destroy_book': {
                        'label': 'Destroy the grimoire',
                        'outcomes': [
                            {'weight': 1, 'text': 'You tear the pages and hurl them into the brazier! The necromancer screams as his power shatters. A burst of released energy fills you!',
                             'xp': (800, 1500), 'chivalry': 10, 'hp_restore': 0.5},
                        ]
                    },
                },
            },
        },
    },

    # --- Event 3: The Dwarven Forge ---
    {
        'id': 'dwarven_forge',
        'name': 'The Abandoned Dwarven Forge',
        'steps': {
            'start': {
                'description': 'You stumble upon an ancient dwarven forge, its fires long cold. Rusted tools and half-finished weapons litter the workbenches. A massive anvil sits at the center. On the far wall, a sealed vault door bears the clan crest of the Ironheart dwarves.',
                'choices': {
                    'examine_forge': {
                        'label': 'Examine the forge',
                        'outcomes': [
                            {'weight': 1, 'text': 'The forge is ancient but the bellows still work. With effort, you could relight it.',
                             'next_step': 'forge_lit'},
                        ]
                    },
                    'try_vault': {
                        'label': 'Try the vault door',
                        'outcomes': [
                            {'weight': 1, 'text': 'The vault door is locked with a complex dwarven mechanism. Three rune-carved dials must be aligned correctly.',
                             'next_step': 'vault_puzzle'},
                            {'weight': 1, 'text': 'As you touch the door, a dwarven guardian golem activates from the rubble!',
                             'next_step': 'golem_fight'},
                        ]
                    },
                    'search_workbenches': {
                        'label': 'Search the workbenches',
                        'outcomes': [
                            {'weight': 2, 'text': 'You find some salvageable materials and a few coins among the debris.',
                             'gold': (50, 200), 'xp': (50, 150)},
                            {'weight': 1, 'text': 'You find a half-finished masterwork blade! It is still sharp and well-balanced.',
                             'gold': (200, 600), 'xp': (100, 300)},
                        ]
                    },
                    'leave': {
                        'label': 'Move on',
                        'outcomes': [
                            {'weight': 1, 'text': 'You leave the forge to the dust and shadows.'},
                        ]
                    },
                },
            },
            'forge_lit': {
                'description': 'With great effort, you relight the ancient forge. Orange flames roar to life and the chamber fills with warmth. The dwarven runes on the walls begin to glow in response. You could try to smith something, or the heat might weaken the vault door.',
                'choices': {
                    'smith_weapon': {
                        'label': 'Try to forge a weapon',
                        'outcomes': [
                            {'weight': 2, 'text': 'You hammer out a crude but sturdy blade on the anvil. The dwarven forge enhances your work beyond expectation!',
                             'xp': (300, 600)},
                            {'weight': 1, 'text': 'Your blacksmithing is poor, but the experience is valuable. You create a serviceable dagger.',
                             'xp': (150, 300)},
                        ]
                    },
                    'heat_vault': {
                        'label': 'Use the heat on the vault hinges',
                        'outcomes': [
                            {'weight': 2, 'text': 'The intense heat weakens the ancient metal. The vault door swings open!',
                             'xp': (100, 200), 'next_step': 'vault_open'},
                            {'weight': 1, 'text': 'The heat activates a hidden defense mechanism! Gears grind and a golem assembles!',
                             'next_step': 'golem_fight'},
                        ]
                    },
                    'warm_up': {
                        'label': 'Rest by the fire',
                        'outcomes': [
                            {'weight': 1, 'text': 'The warmth of the ancient forge soothes your aching muscles and heals your wounds.',
                             'hp_restore': 0.75, 'mana_restore': 0.5},
                        ]
                    },
                },
            },
            'vault_puzzle': {
                'description': 'Three rune dials stare back at you: one carved with a hammer, one with a mountain, and one with a flame. Scratched into the wall nearby are the words: "Iron is born of mountain and flame, shaped by the hammer\'s name."',
                'choices': {
                    'mountain_flame_hammer': {
                        'label': 'Set: Mountain, Flame, Hammer',
                        'outcomes': [
                            {'weight': 1, 'text': 'The dials click into place! The vault door groans open, releasing ancient air!',
                             'xp': (200, 400), 'next_step': 'vault_open'},
                        ]
                    },
                    'hammer_mountain_flame': {
                        'label': 'Set: Hammer, Mountain, Flame',
                        'outcomes': [
                            {'weight': 1, 'text': 'Wrong combination! A burst of steam scalds your hands!',
                             'hp': (-15, -5), 'next_step': 'vault_puzzle'},
                        ]
                    },
                    'force_it': {
                        'label': 'Try to force the mechanism',
                        'outcomes': [
                            {'weight': 1, 'text': 'The mechanism jams and triggers the guardian!',
                             'next_step': 'golem_fight'},
                        ]
                    },
                },
            },
            'golem_fight': {
                'description': 'A massive stone golem assembles itself from the rubble, its eyes blazing with dwarven rune-magic! It swings a fist the size of a barrel at you!',
                'choices': {
                    'fight': {
                        'label': 'Battle the golem',
                        'outcomes': [
                            {'weight': 2, 'text': 'You find the glowing rune on its chest and strike it! The golem shatters into rubble, revealing the vault behind it.',
                             'xp': (400, 800), 'hp': (-20, -10), 'next_step': 'vault_open'},
                            {'weight': 1, 'text': 'The golem is incredibly tough! You barely destroy it after a brutal fight.',
                             'hp': (-50, -25), 'xp': (500, 1000), 'next_step': 'vault_open'},
                        ]
                    },
                    'dodge_and_flee': {
                        'label': 'Dodge and run',
                        'outcomes': [
                            {'weight': 2, 'text': 'You roll under its massive fist and sprint for the exit!',
                             'hp': (-10, -5)},
                            {'weight': 1, 'text': 'The golem clips you as you flee! You barely escape alive.',
                             'hp': (-35, -15)},
                        ]
                    },
                },
            },
            'vault_open': {
                'description': 'The dwarven vault lies open before you! Inside, shelves of gold bars gleam in the torchlight. A magnificent warhammer rests on a stone pedestal. Ancient dwarven armor hangs on a rack. You cannot carry everything.',
                'choices': {
                    'take_gold': {
                        'label': 'Fill your pockets with gold',
                        'outcomes': [
                            {'weight': 1, 'text': 'You stuff as much gold as you can carry! A king\'s ransom in dwarven gold bars!',
                             'gold': (1000, 5000), 'xp': (300, 500)},
                        ]
                    },
                    'take_warhammer': {
                        'label': 'Take the warhammer',
                        'outcomes': [
                            {'weight': 1, 'text': 'The warhammer hums with ancient power as you lift it. "Ironheart\'s Fury" is engraved on its head. You also grab some loose coins.',
                             'gold': (300, 800), 'xp': (500, 1000)},
                        ]
                    },
                    'take_armor': {
                        'label': 'Don the dwarven armor',
                        'outcomes': [
                            {'weight': 1, 'text': 'The masterwork armor fits surprisingly well. You feel nearly invincible! You grab a handful of gems on the way out.',
                             'gold': (400, 1000), 'xp': (400, 800)},
                        ]
                    },
                },
            },
        },
    },

    # --- Event 4: The Cursed Mirror ---
    {
        'id': 'cursed_mirror',
        'name': 'The Cursed Mirror',
        'steps': {
            'start': {
                'description': 'In a dusty chamber, a tall ornate mirror stands against the wall, its silver frame carved with tortured faces. As you approach, your reflection grins back at you -- but you are not smiling. Your reflection draws a weapon.',
                'choices': {
                    'shatter': {
                        'label': 'Smash the mirror',
                        'outcomes': [
                            {'weight': 2, 'text': 'Your weapon strikes the glass, but it does not break! The surface ripples like water.',
                             'next_step': 'mirror_active'},
                            {'weight': 1, 'text': 'The mirror cracks but does not shatter. Dark energy leaks from the fissures!',
                             'hp': (-15, -5), 'next_step': 'mirror_active'},
                        ]
                    },
                    'touch': {
                        'label': 'Touch the mirror surface',
                        'outcomes': [
                            {'weight': 1, 'text': 'Your hand passes through the glass! You feel a cold grip seize your wrist!',
                             'next_step': 'pulled_in'},
                        ]
                    },
                    'speak': {
                        'label': 'Speak to your reflection',
                        'outcomes': [
                            {'weight': 2, 'text': 'Your reflection speaks: "I am what you could become. Stronger. Darker. Step through and claim your power."',
                             'next_step': 'mirror_temptation'},
                            {'weight': 1, 'text': '"Help me!" your reflection suddenly changes to a trapped soul. "I\'ve been imprisoned here for centuries!"',
                             'next_step': 'trapped_soul'},
                        ]
                    },
                    'leave': {
                        'label': 'Back away slowly',
                        'outcomes': [
                            {'weight': 1, 'text': 'You retreat from the mirror. As you leave, you hear your reflection whisper: "Coward..."'},
                        ]
                    },
                },
            },
            'mirror_active': {
                'description': 'The mirror pulses with dark energy! Your shadow clone steps OUT of the mirror, a perfect dark copy of yourself. It raises its weapon menacingly. "Only one of us leaves this room," it hisses.',
                'choices': {
                    'fight_clone': {
                        'label': 'Fight your shadow self',
                        'outcomes': [
                            {'weight': 2, 'text': 'You battle your dark twin! It knows your every move, but you know its too! After a fierce duel, you prevail!',
                             'hp': (-30, -15), 'xp': (500, 1000), 'next_step': 'clone_defeated'},
                            {'weight': 1, 'text': 'Your shadow self is stronger than expected! The fight is brutal, but you ultimately triumph.',
                             'hp': (-50, -25), 'xp': (600, 1200), 'next_step': 'clone_defeated'},
                        ]
                    },
                    'outsmart': {
                        'label': 'Try to trick it back into the mirror',
                        'outcomes': [
                            {'weight': 2, 'text': 'You feint left and shove the clone back toward the mirror! It screams as the glass swallows it whole!',
                             'xp': (400, 800), 'next_step': 'clone_defeated'},
                            {'weight': 1, 'text': 'Your trick fails! The clone strikes you hard.',
                             'hp': (-25, -10), 'next_step': 'clone_defeated'},
                        ]
                    },
                },
            },
            'pulled_in': {
                'description': 'You are pulled through the mirror into a shadowy reflection of the dungeon! Everything is reversed and twisted. Your dark reflection stands before you, grinning. "Welcome to my world. Your strength is mine to take."',
                'choices': {
                    'fight_inside': {
                        'label': 'Fight to escape the mirror world',
                        'outcomes': [
                            {'weight': 2, 'text': 'You battle through the mirror realm! With a mighty effort, you shatter the barrier from within and tumble back into reality!',
                             'hp': (-35, -15), 'xp': (600, 1200), 'next_step': 'clone_defeated'},
                            {'weight': 1, 'text': 'The mirror world saps your strength, but you claw your way back to reality!',
                             'hp': (-50, -20), 'xp': (500, 1000), 'next_step': 'clone_defeated'},
                        ]
                    },
                    'absorb_shadow': {
                        'label': 'Embrace the darkness within',
                        'outcomes': [
                            {'weight': 1, 'text': 'You merge with your shadow self! Tremendous dark power floods through you as you step back through the mirror.',
                             'xp': (800, 1500), 'darkness': 15, 'mana_restore': 1.0},
                        ]
                    },
                },
            },
            'mirror_temptation': {
                'description': 'Your dark reflection gestures invitingly. Through the glass, you see a version of yourself crowned and powerful, surrounded by wealth and dark servants. "All you must do is step through," it whispers. "Leave your weakness behind."',
                'choices': {
                    'step_through': {
                        'label': 'Step through the mirror',
                        'outcomes': [
                            {'weight': 1, 'text': 'Dark energy engulfs you! Pain and power in equal measure! When it fades, you feel changed... stronger, but something good within you has died.',
                             'xp': (600, 1200), 'darkness': 20, 'mana_restore': 1.0},
                            {'weight': 1, 'text': 'It was a trick! You are trapped momentarily in the mirror world before breaking free!',
                             'hp': (-30, -15), 'xp': (300, 600), 'darkness': 5},
                        ]
                    },
                    'refuse': {
                        'label': 'Reject the temptation',
                        'outcomes': [
                            {'weight': 1, 'text': '"I am complete as I am." Your reflection screams in rage and the mirror cracks, releasing a burst of purifying light!',
                             'xp': (400, 800), 'chivalry': 10, 'hp_restore': 0.5},
                        ]
                    },
                    'shatter_now': {
                        'label': 'Destroy the mirror while it\'s distracted',
                        'outcomes': [
                            {'weight': 1, 'text': 'You smash the mirror! Shards fly everywhere and dark energy dissipates. Among the fragments, you find crystallized magic.',
                             'gold': (300, 1000), 'xp': (500, 800), 'chivalry': 5},
                        ]
                    },
                },
            },
            'trapped_soul': {
                'description': 'A spectral figure materializes in the mirror\'s surface -- not your reflection, but a ghostly woman in ancient garb. "I am Seraphina, court wizard of a kingdom long fallen. The mirror trapped me when I tried to destroy it. Please, help me break free!"',
                'choices': {
                    'help_free': {
                        'label': 'Help break the enchantment',
                        'outcomes': [
                            {'weight': 2, 'text': 'You channel your will into the mirror! Seraphina\'s spirit bursts free in a flash of golden light! "Thank you, brave one!" She bestows ancient magical knowledge upon you before ascending.',
                             'xp': (600, 1200), 'mana_restore': 1.0, 'chivalry': 12},
                            {'weight': 1, 'text': 'The enchantment fights back! Pain sears through your hands, but Seraphina breaks free! She heals your wounds with her last act of magic.',
                             'hp_restore': 1.0, 'xp': (400, 800), 'chivalry': 10},
                        ]
                    },
                    'demand_payment': {
                        'label': 'Demand her magical knowledge first',
                        'outcomes': [
                            {'weight': 1, 'text': 'Seraphina teaches you a spell before you free her. The combined effort shatters the mirror completely.',
                             'xp': (500, 1000), 'mana_restore': 0.75},
                        ]
                    },
                    'use_her_power': {
                        'label': 'Drain her spirit for power',
                        'outcomes': [
                            {'weight': 1, 'text': 'You absorb Seraphina\'s spirit! Her screams echo as dark power floods into you. The mirror shatters.',
                             'xp': (1000, 2000), 'darkness': 25, 'mana_restore': 1.0},
                        ]
                    },
                },
            },
            'clone_defeated': {
                'description': 'Your shadow clone dissolves into black mist. The mirror cracks from top to bottom, its dark enchantment broken. In the wreckage, something glimmers among the silver shards.',
                'choices': {
                    'search_shards': {
                        'label': 'Search through the shards',
                        'outcomes': [
                            {'weight': 2, 'text': 'You find a shard of enchanted mirror glass that pulses with captured energy. It\'s valuable to any wizard.',
                             'gold': (400, 1200), 'xp': (200, 400)},
                            {'weight': 1, 'text': 'Hidden behind the mirror was a secret compartment filled with treasure!',
                             'gold': (600, 2000), 'xp': (300, 500)},
                        ]
                    },
                    'absorb_energy': {
                        'label': 'Absorb the residual dark energy',
                        'outcomes': [
                            {'weight': 1, 'text': 'The mirror\'s dark energy flows into you! Your power grows, but at a cost.',
                             'xp': (500, 1000), 'mana_restore': 0.75, 'darkness': 8},
                        ]
                    },
                },
            },
        },
    },

    # --- Event 5: The Underground Arena ---
    {
        'id': 'underground_arena',
        'name': 'The Underground Arena',
        'steps': {
            'start': {
                'description': 'The sound of cheering grows louder as you follow a torchlit passage. You emerge onto a balcony overlooking an underground arena! Creatures of all kinds fill the stands. A scarred half-orc ringmaster spots you. "Fresh meat! Care to test your mettle? Gold and glory await the victor!"',
                'choices': {
                    'enter_arena': {
                        'label': 'Enter the arena',
                        'outcomes': [
                            {'weight': 1, 'text': 'The crowd roars as you step into the sand pit! The ringmaster grins. "Choose your challenge!"',
                             'next_step': 'choose_challenge'},
                        ]
                    },
                    'bet': {
                        'label': 'Place a bet on the fights (200g)',
                        'outcomes': [
                            {'weight': 1, 'text': 'You find a seat and place your wager. The fights are brutal and exciting!',
                             'next_step': 'betting', 'condition': 'gold >= 200'},
                            {'weight': 1, 'text': 'You don\'t have enough gold for the minimum wager.', 'condition': 'gold < 200'},
                        ]
                    },
                    'explore_tunnels': {
                        'label': 'Sneak into the back tunnels',
                        'outcomes': [
                            {'weight': 2, 'text': 'You slip into the fighters\' preparation area behind the arena.',
                             'next_step': 'backstage'},
                            {'weight': 1, 'text': 'A guard catches you! "Where do you think you\'re going?"',
                             'hp': (-10, -5)},
                        ]
                    },
                    'leave': {
                        'label': 'Leave the arena',
                        'outcomes': [
                            {'weight': 1, 'text': 'You turn away from the spectacle and continue your dungeon exploration.'},
                        ]
                    },
                },
            },
            'choose_challenge': {
                'description': 'The ringmaster presents three challengers: A hulking troll berserker covered in scars, a swift elven duelist twirling twin blades, and a robed figure crackling with magical energy. "Pick your poison!" the ringmaster cackles.',
                'choices': {
                    'fight_troll': {
                        'label': 'Fight the Troll Berserker',
                        'outcomes': [
                            {'weight': 2, 'text': 'The troll is powerful but slow! You dodge his wild swings and find openings!',
                             'hp': (-25, -10), 'next_step': 'arena_victory'},
                            {'weight': 1, 'text': 'The troll connects with a devastating blow! You barely survive but manage to bring him down!',
                             'hp': (-50, -30), 'next_step': 'arena_victory'},
                        ]
                    },
                    'fight_elf': {
                        'label': 'Fight the Elven Duelist',
                        'outcomes': [
                            {'weight': 2, 'text': 'The elf is fast, but you read her patterns and counter with precision!',
                             'hp': (-20, -10), 'next_step': 'arena_victory'},
                            {'weight': 1, 'text': 'Her twin blades are a blur! She scores several deep cuts before you disarm her.',
                             'hp': (-40, -20), 'next_step': 'arena_victory'},
                        ]
                    },
                    'fight_mage': {
                        'label': 'Fight the Battle Mage',
                        'outcomes': [
                            {'weight': 2, 'text': 'You close the distance before the mage can cast! A swift strike ends the match!',
                             'hp': (-15, -5), 'next_step': 'arena_victory'},
                            {'weight': 1, 'text': 'A fireball catches you square in the chest! You stagger but press through and overwhelm the mage!',
                             'hp': (-45, -25), 'next_step': 'arena_victory'},
                        ]
                    },
                },
            },
            'arena_victory': {
                'description': 'The crowd erupts! "VICTORY!" the ringmaster bellows. "We have a champion!" He approaches you with a sack of gold. "Impressive! The crowd wants more. Will you face the champion for double the prize? He\'s never been defeated..."',
                'choices': {
                    'face_champion': {
                        'label': 'Face the undefeated champion',
                        'outcomes': [
                            {'weight': 1, 'text': 'The champion is a massive minotaur gladiator! An epic battle ensues!',
                             'next_step': 'champion_fight'},
                        ]
                    },
                    'take_winnings': {
                        'label': 'Take your gold and leave',
                        'outcomes': [
                            {'weight': 1, 'text': 'Smart choice. You collect your winnings and leave the arena victorious!',
                             'gold': (500, 1500), 'xp': (400, 800)},
                        ]
                    },
                },
            },
            'champion_fight': {
                'description': 'The minotaur champion towers over you, muscles rippling beneath scarred hide. He carries a notched greatsword taller than most men. The arena falls silent. Then he charges!',
                'choices': {
                    'stand_ground': {
                        'label': 'Meet his charge head-on',
                        'outcomes': [
                            {'weight': 1, 'text': 'The collision is thunderous! You brace yourself and redirect his momentum, sending him crashing into the arena wall! Before he recovers, you strike the winning blow! The arena EXPLODES with cheering!',
                             'hp': (-40, -20), 'gold': (1000, 4000), 'xp': (800, 1500), 'chivalry': 8},
                            {'weight': 1, 'text': 'His charge hits you like a battering ram! You fly backward but roll to your feet. The battle rages on -- blow after blow -- until finally you find your opening and strike him down!',
                             'hp': (-60, -35), 'gold': (1500, 5000), 'xp': (1000, 2000), 'chivalry': 10},
                        ]
                    },
                    'dodge_and_counter': {
                        'label': 'Dodge sideways and counter',
                        'outcomes': [
                            {'weight': 2, 'text': 'You sidestep at the last moment! The minotaur crashes past you and you slash at his exposed flank! After a prolonged battle of attrition, you bring the champion down! The crowd goes wild!',
                             'hp': (-30, -15), 'gold': (1200, 4000), 'xp': (900, 1800), 'chivalry': 8},
                            {'weight': 1, 'text': 'Your dodge is too slow! His horn gores your side. But you fight on, driven by the roar of the crowd, and eventually triumph!',
                             'hp': (-55, -30), 'gold': (1000, 3500), 'xp': (800, 1600), 'chivalry': 8},
                        ]
                    },
                    'yield': {
                        'label': 'Yield before the fight begins',
                        'outcomes': [
                            {'weight': 1, 'text': 'The crowd boos, but you leave with your first-round winnings and your life.',
                             'gold': (300, 1000), 'xp': (200, 400)},
                        ]
                    },
                },
            },
            'betting': {
                'description': 'Two fighters enter the arena: a grizzled human pit fighter and a young but fierce goblin champion who has won three bouts in a row. The odds are 2:1 on the human, 3:1 on the goblin.',
                'choices': {
                    'bet_human': {
                        'label': 'Bet on the human (200g)',
                        'outcomes': [
                            {'weight': 3, 'text': 'The human wins after a tough fight! You collect your winnings!',
                             'gold': (200, 400), 'xp': (50, 100)},
                            {'weight': 2, 'text': 'The goblin pulls off an upset! Your gold is lost.',
                             'gold': -200},
                        ]
                    },
                    'bet_goblin': {
                        'label': 'Bet on the goblin (200g)',
                        'outcomes': [
                            {'weight': 2, 'text': 'The goblin wins! Your longshot bet pays off big!',
                             'gold': (400, 600), 'xp': (100, 200)},
                            {'weight': 3, 'text': 'The human overpowers the goblin. Your wager is forfeit.',
                             'gold': -200},
                        ]
                    },
                    'rig_fight': {
                        'label': 'Try to rig the fight',
                        'outcomes': [
                            {'weight': 1, 'text': 'You slip a paralysis potion into the human\'s water. The goblin wins easily and you collect a fortune from the bookmakers!',
                             'gold': (600, 1500), 'darkness': 10, 'xp': (100, 200)},
                            {'weight': 1, 'text': 'You\'re caught cheating! The arena guards rough you up and throw you out!',
                             'hp': (-30, -15), 'gold': -200, 'darkness': 5},
                        ]
                    },
                },
            },
            'backstage': {
                'description': 'Behind the arena, you find the fighters\' quarters. Cages hold monsters awaiting their turn. A locked chest sits in the corner, likely holding the arena\'s prize fund. A wounded fighter sits against the wall, blood seeping from a deep cut.',
                'choices': {
                    'loot_chest': {
                        'label': 'Break open the prize chest',
                        'outcomes': [
                            {'weight': 2, 'text': 'You crack open the chest and grab handfuls of gold before anyone notices!',
                             'gold': (500, 2000), 'darkness': 8, 'xp': (100, 200)},
                            {'weight': 1, 'text': 'An arena guard catches you red-handed! You fight your way out!',
                             'hp': (-25, -10), 'gold': (200, 800), 'darkness': 5},
                        ]
                    },
                    'help_fighter': {
                        'label': 'Help the wounded fighter',
                        'outcomes': [
                            {'weight': 1, 'text': '"Thank you, friend," the fighter gasps. "Take this -- I won it in the ring but I won\'t live to spend it." He presses a purse into your hands.',
                             'gold': (200, 600), 'chivalry': 8, 'xp': (100, 300)},
                        ]
                    },
                    'free_monsters': {
                        'label': 'Release the caged monsters',
                        'outcomes': [
                            {'weight': 1, 'text': 'Chaos erupts as monsters pour from their cages! In the confusion, you loot the arena and escape!',
                             'gold': (400, 1500), 'xp': (200, 500), 'darkness': 12},
                            {'weight': 1, 'text': 'You release the monsters but one turns on you before fleeing!',
                             'hp': (-30, -15), 'gold': (200, 800), 'xp': (150, 300)},
                        ]
                    },
                },
            },
        },
    },
]


def get_random_dungeon_event():
    """Select a random dungeon event (single-step or multi-step)."""
    # 30% chance of multi-step event, 70% single-step
    if MULTI_STEP_EVENTS and random.randint(1, 100) <= 30:
        event = random.choice(MULTI_STEP_EVENTS)
        step = event['steps']['start']
        return {
            'id': event['id'],
            'name': event['name'],
            'description': step['description'],
            'choices': step['choices'],
            'is_multi_step': True,
            'current_step': 'start',
        }
    event = random.choice(DUNGEON_EVENTS)
    return event


def _evaluate_condition(condition, player):
    """Evaluate a gold condition string against a player."""
    import re
    match = re.match(r'gold\s*(>=|<|<=|>|==)\s*(\d+)', condition)
    if not match:
        return True
    op, val = match.group(1), int(match.group(2))
    if op == '>=':
        return player.gold >= val
    elif op == '<':
        return player.gold < val
    elif op == '<=':
        return player.gold <= val
    elif op == '>':
        return player.gold > val
    elif op == '==':
        return player.gold == val
    return True


def _apply_outcome_effects(player, outcome):
    """Apply effects from an outcome dict to a player. Returns display text."""
    text = outcome['text']

    # Apply effects
    gold = outcome.get('gold', 0)
    if isinstance(gold, tuple):
        gold = random.randint(gold[0], gold[1])
    if gold:
        player.gold = max(0, player.gold + gold * max(1, player.level // 3))
        if gold > 0:
            text += f" (+{gold * max(1, player.level // 3)} gold)"
        else:
            text += f" ({gold} gold)"

    xp = outcome.get('xp', 0)
    if isinstance(xp, tuple):
        xp = random.randint(xp[0], xp[1])
    if xp:
        scaled_xp = xp * max(1, player.level)
        player.experience += scaled_xp
        text += f" (+{scaled_xp} XP)"

    xp_mult = outcome.get('xp_mult', 0)
    if xp_mult:
        scaled = xp_mult * player.level
        player.experience += scaled
        text += f" (+{scaled} XP)"

    hp = outcome.get('hp', 0)
    if isinstance(hp, tuple):
        hp = random.randint(hp[0], hp[1])
    if hp:
        player.hp = max(1, min(player.max_hp, player.hp + hp))
        if hp > 0:
            text += f" (+{hp} HP)"
        else:
            text += f" ({hp} HP)"

    if outcome.get('hp_restore'):
        restore = int(player.max_hp * outcome['hp_restore'])
        player.hp = min(player.max_hp, player.hp + restore)
        text += f" (+{restore} HP)"

    if outcome.get('mana_restore'):
        restore = int(player.max_mana * outcome['mana_restore'])
        player.mana = min(player.max_mana, player.mana + restore)

    potions = outcome.get('potions', 0)
    if potions:
        player.healing_potions += potions
        text += f" (+{potions} potions)"

    chiv = outcome.get('chivalry', 0)
    if chiv:
        player.chivalry += chiv

    dark = outcome.get('darkness', 0)
    if dark:
        player.darkness += dark

    if outcome.get('poison'):
        player.is_poisoned = True
        text += " (Poisoned!)"

    if outcome.get('cure_all'):
        player.is_poisoned = False
        player.is_blind = False
        player.has_plague = False
        text += " (Ailments cured!)"

    addiction = outcome.get('addiction', 0)
    if isinstance(addiction, tuple):
        addiction = random.randint(addiction[0], addiction[1])
    if addiction:
        player.addiction = min(100, player.addiction + addiction)
        text += f" (Addiction +{addiction}%)"

    return text


def resolve_dungeon_event(player, event_id, choice_key, current_step=None):
    """Resolve a dungeon event choice for a player.

    For multi-step events, current_step identifies which step we're on.
    Returns (text, next_step_data) where next_step_data is None for final
    outcomes or a dict with the next step info for multi-step events.
    """
    # Check if this is a multi-step event
    multi_event = next((e for e in MULTI_STEP_EVENTS if e['id'] == event_id), None)
    if multi_event and current_step:
        step = multi_event['steps'].get(current_step)
        if not step:
            return "Nothing happens.", None

        choice = step['choices'].get(choice_key)
        if not choice:
            return "Nothing happens.", None

        # Filter outcomes by condition
        valid_outcomes = [o for o in choice['outcomes']
                         if not o.get('condition') or _evaluate_condition(o['condition'], player)]
        if not valid_outcomes:
            return "Nothing happens.", None

        weights = [o.get('weight', 1) for o in valid_outcomes]
        outcome = random.choices(valid_outcomes, weights=weights, k=1)[0]

        text = _apply_outcome_effects(player, outcome)

        # Check if outcome leads to next step
        next_step_id = outcome.get('next_step')
        if next_step_id and next_step_id in multi_event['steps']:
            next_step = multi_event['steps'][next_step_id]
            next_step_data = {
                'id': event_id,
                'name': multi_event['name'],
                'description': next_step['description'],
                'choices': next_step['choices'],
                'is_multi_step': True,
                'current_step': next_step_id,
                'previous_result': text,
            }
            return text, next_step_data

        return text, None

    # Single-step event
    event = next((e for e in DUNGEON_EVENTS if e['id'] == event_id), None)
    if not event:
        return "Nothing happens.", None

    choice = event['choices'].get(choice_key)
    if not choice:
        return "Nothing happens.", None

    # Filter outcomes by condition
    valid_outcomes = [o for o in choice['outcomes']
                     if not o.get('condition') or _evaluate_condition(o['condition'], player)]
    if not valid_outcomes:
        return "Nothing happens.", None

    weights = [o.get('weight', 1) for o in valid_outcomes]
    outcome = random.choices(valid_outcomes, weights=weights, k=1)[0]

    text = _apply_outcome_effects(player, outcome)
    return text, None


# =========================================================================
# GOD / DEITY SYSTEM
# =========================================================================

SUPREME_CREATOR = 'Manwe'

GOD_DOMAINS = [
    'War', 'Love', 'Death', 'Nature', 'Knowledge',
    'Storms', 'Fire', 'Ice', 'Chaos', 'Order',
    'Shadows', 'Light', 'Beasts', 'Fortune', 'Harvest'
]

DEFAULT_GODS = [
    {'name': 'Tyr', 'domain': 'War', 'alignment': 'good', 'sex': 1,
     'description': 'The god of honorable combat and justice.'},
    {'name': 'Freya', 'domain': 'Love', 'alignment': 'good', 'sex': 2,
     'description': 'Goddess of love, beauty, and fertility.'},
    {'name': 'Hel', 'domain': 'Death', 'alignment': 'evil', 'sex': 2,
     'description': 'Dark goddess who rules the realm of the dead.'},
    {'name': 'Silvanus', 'domain': 'Nature', 'alignment': 'neutral', 'sex': 1,
     'description': 'Ancient god of forests and wild places.'},
    {'name': 'Oghma', 'domain': 'Knowledge', 'alignment': 'neutral', 'sex': 1,
     'description': 'God of knowledge, invention, and inspiration.'},
    {'name': 'Talos', 'domain': 'Storms', 'alignment': 'evil', 'sex': 1,
     'description': 'Destructive god of storms and devastation.'},
    {'name': 'Lathander', 'domain': 'Light', 'alignment': 'good', 'sex': 1,
     'description': 'God of dawn, renewal, and new beginnings.'},
    {'name': 'Shar', 'domain': 'Shadows', 'alignment': 'evil', 'sex': 2,
     'description': 'Goddess of darkness, secrets, and loss.'},
]


def seed_gods():
    """Create default gods if none exist."""
    if God.query.first():
        return
    for g in DEFAULT_GODS:
        god = God(
            name=g['name'], domain=g['domain'], alignment=g['alignment'],
            sex=g['sex'], description=g['description'], level=random.randint(5, 8),
            experience=random.randint(50000, 500000),
        )
        db.session.add(god)
    db.session.commit()


def worship_god(player, god_name):
    """Player begins worshipping a god."""
    god = God.query.filter_by(name=god_name, is_active=True).first()
    if not god:
        return False, "That deity does not exist."

    if player.god_name == god_name:
        return False, f"You already worship {god_name}."

    old_god = player.god_name
    player.god_name = god_name

    news = NewsEntry(player_id=player.id, category='divine',
                     message=f"{player.name} began worshipping {god_name}!")
    db.session.add(news)

    if old_god:
        return True, f"You have forsaken {old_god} and now worship {god_name}."
    return True, f"You kneel before the altar of {god_name} and pledge your devotion."


def forsake_god(player):
    """Player stops worshipping their god."""
    if not player.god_name:
        return False, "You don't worship any deity."
    old = player.god_name
    player.god_name = ''
    return True, f"You have forsaken {old}. You are now without divine guidance."


def pray_to_god(player):
    """Player prays to their god for a blessing."""
    if not player.god_name:
        return False, "You don't worship any deity."

    god = God.query.filter_by(name=player.god_name, is_active=True).first()
    if not god:
        player.god_name = ''
        return False, "Your deity no longer exists."

    # Chance of blessing based on god's level and alignment match
    blessing_chance = 30 + god.level * 5
    alignment_match = False
    if god.alignment == 'good' and player.chivalry > player.darkness:
        alignment_match = True
        blessing_chance += 15
    elif god.alignment == 'evil' and player.darkness > player.chivalry:
        alignment_match = True
        blessing_chance += 15
    elif god.alignment == 'neutral':
        blessing_chance += 10

    if random.randint(1, 100) > blessing_chance:
        responses = [
            f"{god.name} does not respond to your prayers.",
            f"Your prayers echo into silence.",
            f"{god.name} is busy with other matters.",
        ]
        return True, random.choice(responses)

    # Grant blessing based on domain
    domain_blessings = {
        'War': ('strength', 'Your muscles surge with divine power!'),
        'Love': ('charisma', 'You feel more charming and attractive!'),
        'Death': ('darkness', 'Dark power flows through you!'),
        'Nature': ('stamina', 'Nature\'s vitality fills you!'),
        'Knowledge': ('wisdom', 'Divine insight fills your mind!'),
        'Storms': ('agility', 'Lightning reflexes course through you!'),
        'Fire': ('strength', 'Fiery strength burns in your veins!'),
        'Ice': ('defence', 'An icy shield forms around you!'),
        'Chaos': ('dexterity', 'Chaotic energy sharpens your reflexes!'),
        'Order': ('defence', 'Order and discipline strengthen your defenses!'),
        'Shadows': ('agility', 'Shadows wrap around you, quickening your step!'),
        'Light': ('hp_heal', 'Holy light bathes you in warmth!'),
        'Beasts': ('stamina', 'Bestial endurance fills you!'),
        'Fortune': ('gold', 'Gold coins materialize from thin air!'),
        'Harvest': ('hp_heal', 'The bounty of the harvest restores you!'),
    }

    stat, text = domain_blessings.get(god.domain, ('hp_heal', 'Divine energy heals you!'))

    god.experience += random.randint(10, 50)

    if stat == 'hp_heal':
        heal = max(10, player.max_hp // 3)
        player.hp = min(player.max_hp, player.hp + heal)
        return True, f"{god.name} hears your prayer! {text} (+{heal} HP)"
    elif stat == 'gold':
        amount = random.randint(50, 300) * player.level
        player.gold += amount
        return True, f"{god.name} hears your prayer! {text} (+{amount} gold)"
    elif stat == 'darkness':
        player.darkness += random.randint(3, 8)
        player.experience += random.randint(100, 500) * player.level
        return True, f"{god.name} hears your prayer! {text}"
    else:
        bonus = random.randint(1, 3)
        old_val = getattr(player, stat, 10)
        setattr(player, stat, old_val + bonus)
        return True, f"{god.name} hears your prayer! {text} (+{bonus} {stat})"


def sacrifice_gold(player, amount):
    """Sacrifice gold to a god at the temple."""
    if not player.god_name:
        return False, "You don't worship any deity."
    if amount <= 0 or player.gold < amount:
        return False, "Not enough gold."

    god = God.query.filter_by(name=player.god_name, is_active=True).first()
    if not god:
        return False, "Your deity no longer exists."

    player.gold -= amount

    # Determine power gained based on sacrifice amount
    if amount <= 20:
        power = 1
    elif amount <= 2000:
        power = 2
    elif amount <= 45000:
        power = 3
    elif amount <= 150000:
        power = 4
    else:
        power = 5

    god.experience += power * 100

    xp_gain = amount // 2
    player.experience += xp_gain

    if player.chivalry >= player.darkness:
        player.chivalry += power
    else:
        player.darkness += power

    return True, f"You sacrifice {amount} gold to {god.name}. Divine favor increases! (+{xp_gain} XP)"


def desecrate_altar(player, god_name):
    """Desecrate another god's altar."""
    if god_name == player.god_name:
        return False, "You cannot desecrate your own god's altar!"

    god = God.query.filter_by(name=god_name, is_active=True).first()
    if not god:
        return False, "That deity does not exist."

    # Risk/reward
    if random.randint(1, 3) == 1:
        # Punished by the god
        dmg = random.randint(10, 40)
        player.hp = max(1, player.hp - dmg)
        return True, f"{god.name} strikes you down for your insolence! (-{dmg} HP)"

    player.darkness += random.randint(5, 15)
    xp = random.randint(50, 200) * player.level
    player.experience += xp
    god.experience = max(0, god.experience - random.randint(50, 200))

    news = NewsEntry(player_id=player.id, category='divine',
                     message=f"{player.name} desecrated the altar of {god.name}!")
    db.session.add(news)

    return True, f"You desecrate {god.name}'s altar! Dark power fills you. (+{xp} XP)"


def god_maintenance():
    """Daily god maintenance - refresh deeds, give believer XP."""
    gods = God.query.filter_by(is_active=True).all()
    for god in gods:
        god.deeds_left = 5
        believers = god.believer_count()
        god.experience += believers * 10

        new_level = god.check_level_up()
        if new_level > god.level:
            god.level = new_level
            news = NewsEntry(category='divine',
                             message=f"{god.name} has ascended to {god.title()}!")
            db.session.add(news)


# ==================== THE BEAUTY NEST ====================

BEAUTY_NEST_COMPANIONS = [
    {
        'name': 'Grukka',
        'race': 'Troll',
        'description': 'A hulking troll woman with surprisingly gentle eyes and tusks adorned with silver rings.',
        'cost': 500,
        'xp_base': 25,
        'darkness': 15,
        'flavor': 'Grukka leads you to a reinforced room upstairs. Despite her fearsome appearance, '
                  'she proves surprisingly tender. You leave feeling oddly refreshed.',
    },
    {
        'name': 'Skara',
        'race': 'Orc',
        'description': 'A muscular orc maiden with ritual scarification and a warrior\'s bearing.',
        'cost': 2000,
        'xp_base': 50,
        'darkness': 25,
        'flavor': 'Skara sizes you up approvingly before taking your hand. Her room smells of '
                  'incense and battle trophies. An unforgettable evening follows.',
    },
    {
        'name': 'Whisper',
        'race': 'Gnoll',
        'description': 'A lithe gnoll woman with spotted fur and a mischievous grin full of sharp teeth.',
        'cost': 5000,
        'xp_base': 100,
        'darkness': 50,
        'flavor': 'Whisper purrs and leads you through a beaded curtain into her den. Her '
                  'gnoll-like enthusiasm leaves you exhausted but smiling.',
    },
    {
        'name': 'Bronwyn',
        'race': 'Dwarf',
        'description': 'A stout dwarven woman with braided copper hair and a hearty laugh.',
        'cost': 10000,
        'xp_base': 150,
        'darkness': 75,
        'flavor': 'Bronwyn cracks open a barrel of dwarven stout and insists you drink first. '
                  'What follows is an evening of surprising passion and excellent ale.',
    },
    {
        'name': 'Silvanya',
        'race': 'Elf',
        'description': 'A beautiful elven woman with silver hair and ancient, knowing eyes.',
        'cost': 20000,
        'xp_base': 175,
        'darkness': 100,
        'flavor': 'Silvanya whispers enchantments that make the candlelight dance. Her elven '
                  'magic turns the evening into something otherworldly. You feel renewed.',
    },
    {
        'name': 'Zara',
        'race': 'Tiefling',
        'description': 'A striking tiefling with crimson skin, small horns, and a devilish smile.',
        'cost': 30000,
        'xp_base': 200,
        'darkness': 150,
        'flavor': 'Zara traces a clawed finger along your jaw. Her infernal heritage lends an '
                  'intoxicating warmth to the encounter. You leave slightly singed but satisfied.',
    },
    {
        'name': 'Ashkara',
        'race': 'Dragonborn',
        'description': 'A towering dragonborn woman with iridescent bronze scales and smoldering amber eyes.',
        'cost': 40000,
        'xp_base': 250,
        'darkness': 200,
        'flavor': 'Ashkara breathes a small puff of warm smoke and grins. Her scaled embrace '
                  'is surprisingly warm. You leave with the faint scent of brimstone.',
    },
    {
        'name': 'Lirael',
        'race': 'Fae',
        'description': 'A luminous fae creature with gossamer wings and eyes that shift color like opals.',
        'cost': 70000,
        'xp_base': 350,
        'darkness': 300,
        'flavor': 'Lirael floats ahead of you, trailing motes of light. The night passes like '
                  'a fever dream of moonlight and whispered fae promises.',
    },
    {
        'name': 'Empress Velvet',
        'race': 'Human',
        'description': 'The crown jewel of the Beauty Nest. A woman of legendary beauty and devastating charm.',
        'cost': 100000,
        'xp_base': 450,
        'darkness': 500,
        'flavor': 'Empress Velvet regards you with a regal gaze. She is worth every coin. '
                  'You awake the next morning convinced you dreamt the entire encounter.',
    },
]


def beauty_nest_visit(player, companion_index):
    """Visit a companion at The Beauty Nest. Returns (success, message, log)."""
    if companion_index < 0 or companion_index >= len(BEAUTY_NEST_COMPANIONS):
        return False, "Invalid choice.", []

    if not player.beauty_nest_visits or player.beauty_nest_visits < 1:
        return False, "You are too tired for any more visits today. Return tomorrow.", []

    companion = BEAUTY_NEST_COMPANIONS[companion_index]
    log = []

    owner_name = GameConfig.get('beauty_nest_owner', 'Clarissa')
    nest_name = GameConfig.get('beauty_nest_name', 'The Beauty Nest')
    disease_chance = int(GameConfig.get('beauty_nest_disease_chance', '3') or '3')

    if player.gold < companion['cost']:
        return False, (f"{owner_name} laughs. 'You can't afford {companion['name']}! "
                       f"Come back with {companion['cost']:,} gold.'"), []

    # Pay the gold
    player.gold -= companion['cost']
    player.beauty_nest_visits -= 1

    # XP reward scales with level
    xp = (random.randint(companion['xp_base'], companion['xp_base'] * 2)) * player.level
    player.experience += xp

    # Darkness points
    dark = random.randint(companion['darkness'] // 2, companion['darkness'])
    player.darkness += dark

    log.append(f"**Visit to {nest_name}**")
    log.append(companion['flavor'])
    log.append(f"You gained {xp:,} experience points!")
    log.append(f"You gained {dark} darkness points.")

    # Configurable disease chance (default 1 in 3)
    if random.randint(1, max(1, disease_chance)) == 1:
        player.has_plague = True
        dmg = random.randint(5, 20)
        player.hp = max(1, player.hp - dmg)
        log.append("As you leave, you feel a burning pain! The encounter has left you diseased!")
        log.append(f"You lost {dmg} HP and contracted the plague!")

        news = NewsEntry(player_id=player.id, category='social',
                         message=f"{player.name} visited {companion['name']} at {nest_name} "
                                 f"and caught a disease!")
        db.session.add(news)
    else:
        # News about the visit
        quips = [
            f"{player.name} had a night filled with pleasures.",
            f"{player.name} proved to be a real charmer.",
            f"{player.name} spent lavishly at {nest_name}.",
            f"{player.name} enjoyed the company of {companion['name']}.",
        ]
        news = NewsEntry(player_id=player.id, category='social',
                         message=f"{player.name} spent the night with {companion['name']} "
                                 f"at {nest_name}. {random.choice(quips)}")
        db.session.add(news)

    # If married, notify spouse
    if player.married and player.spouse_id:
        spouse = db.session.get(Player, player.spouse_id)
        if spouse:
            mail = Mail(
                sender_id=player.id,
                receiver_id=spouse.id,
                subject="Unfaithful!",
                message=f"{player.name} has been unfaithful! They visited {companion['name']} "
                        f"at {nest_name}!"
            )
            db.session.add(mail)
            log.append("Your spouse has been notified of your infidelity...")

    return True, f"You visited {nest_name}.", log


# ==================== ORB'S BAR ====================

def create_drink(player, name, comment, secret, ingredients):
    """Create a custom drink at Orb's Bar.
    ingredients: dict of attr_name -> amount (0-100), must sum to 100.
    """
    cost = 2800
    if player.gold < cost:
        return False, f"You need {cost} gold to create a drink."

    total = sum(ingredients.values())
    if total != 100:
        return False, f"Ingredients must total 100% (currently {total}%)."

    if not name or len(name) > 30:
        return False, "Drink name must be 1-30 characters."

    # Check max drinks limit
    max_drinks = int(GameConfig.get('max_drinks', '50') or '50')
    if Drink.query.count() >= max_drinks:
        return False, "The drink menu is full! No room for new recipes."

    player.gold -= cost
    drink = Drink(
        name=name.strip(),
        creator_id=player.id,
        creator_name=player.name,
        comment=comment.strip()[:70] if comment else '',
        secret=secret,
    )
    for attr, _ in DRINK_INGREDIENTS:
        setattr(drink, attr, ingredients.get(attr, 0))

    db.session.add(drink)
    add_news(f"{player.name} created a new cocktail at Orb's Bar: '{name}'!")
    db.session.commit()
    return True, f"Your drink '{name}' has been added to the menu!"


def order_drink(player, drink_id):
    """Order and consume a drink from Orb's Bar. Returns (success, msg, log)."""
    if player.drinks_remaining <= 0:
        return False, "You've had enough drinks for today.", []

    drink = db.session.get(Drink, drink_id)
    if not drink:
        return False, "That drink doesn't exist.", []

    log = []
    log.append(f"The bartender mixes you a '{drink.name}'...")

    # Check for lethal combinations (matching original)
    lethal = False
    death_msg = ""

    if player.player_class == 'Assassin' and drink.troll_rum > 0:
        lethal = True
        death_msg = "The Troll Rum reacts fatally with your assassin's constitution!"
    elif player.player_class in ('Cleric', 'Jester') and drink.elf_water > 0:
        lethal = True
        death_msg = "The Elf Water is pure poison to your kind!"
    elif drink.tabasco > 80:
        lethal = True
        death_msg = "Too much Tabasco! Your insides are on fire!"
    elif drink.chilipeppar > 80:
        lethal = True
        death_msg = "The Chilipeppar burns through your stomach!"
    elif drink.bat_brain > 70:
        lethal = True
        death_msg = "The concentrated Bat Brain drives you mad!"
    elif drink.horse_blood > 90:
        lethal = True
        death_msg = "You choke on the thick Horse Blood!"
    elif drink.bobs_bomber > 90:
        lethal = True
        death_msg = "Bob's Bomber is too concentrated! It explodes in your stomach!"
    elif drink.snake_spit > 80:
        lethal = True
        death_msg = "The Snake Spit is lethal at this concentration!"

    player.drinks_remaining -= 1
    drink.times_ordered += 1
    drink.last_customer = player.name

    if lethal:
        log.append(f"*** {death_msg} ***")
        log.append(f"{player.name} has died from drinking '{drink.name}'!")
        player.hp = 0
        add_news(f"{player.name} died after drinking '{drink.name}' at Orb's Bar!")
        db.session.commit()
        return True, death_msg, log

    # Calculate stat bonuses based on ingredient amounts
    log.append("You feel the drink's effects coursing through you...")
    bonuses = {}

    for attr, name in DRINK_INGREDIENTS:
        amount = getattr(drink, attr)
        if amount == 0:
            continue
        if amount <= 10:
            bonuses['stamina'] = bonuses.get('stamina', 0) + random.randint(0, 1)
            bonuses['charisma'] = bonuses.get('charisma', 0) + random.randint(0, 1)
        elif amount <= 25:
            bonuses['agility'] = bonuses.get('agility', 0) + random.randint(0, 1)
            bonuses['dexterity'] = bonuses.get('dexterity', 0) + random.randint(0, 1)
            bonuses['wisdom'] = bonuses.get('wisdom', 0) + random.randint(0, 1)
        elif amount <= 50:
            bonuses['stamina'] = bonuses.get('stamina', 0) + random.randint(0, 2)
            bonuses['darkness'] = bonuses.get('darkness', 0) + random.randint(0, 50)
        elif amount <= 75:
            bonuses['strength'] = bonuses.get('strength', 0) + random.randint(0, 1)
            bonuses['defence'] = bonuses.get('defence', 0) + random.randint(0, 1)
            bonuses['wisdom'] = bonuses.get('wisdom', 0) + random.randint(0, 1)
        elif amount <= 90:
            bonuses['agility'] = bonuses.get('agility', 0) + random.randint(0, 2)
            bonuses['charisma'] = bonuses.get('charisma', 0) + random.randint(0, 1)
            bonuses['chivalry'] = bonuses.get('chivalry', 0) + random.randint(0, 30)
        else:  # 91-100
            bonuses['stamina'] = bonuses.get('stamina', 0) + random.randint(0, 3)
            bonuses['charisma'] = bonuses.get('charisma', 0) + random.randint(0, 2)
            bonuses['wisdom'] = bonuses.get('wisdom', 0) + random.randint(0, 2)

    # Apply bonuses
    stat_attrs = ['strength', 'defence', 'stamina', 'agility', 'charisma', 'dexterity', 'wisdom']
    for stat in stat_attrs:
        val = bonuses.get(stat, 0)
        if val > 0:
            setattr(player, stat, getattr(player, stat) + val)
            log.append(f"  +{val} {stat.capitalize()}")
    if bonuses.get('darkness', 0) > 0:
        player.darkness += bonuses['darkness']
        log.append(f"  +{bonuses['darkness']} Darkness")
    if bonuses.get('chivalry', 0) > 0:
        player.chivalry += bonuses['chivalry']
        log.append(f"  +{bonuses['chivalry']} Chivalry")

    # 10% chance of combat training bonus
    if random.random() < 0.10:
        xp_bonus = player.level * 700
        player.experience += xp_bonus
        log.append(f"The drink inspires you! +{xp_bonus} XP from combat insight!")

    log.append(f"AWESOME! You enjoyed '{drink.name}'!")
    add_news(f"{player.name} enjoyed '{drink.name}' at Orb's Bar.")
    db.session.commit()
    return True, f"You enjoyed '{drink.name}'!", log


def send_drink(sender, receiver_id, drink_id):
    """Send a free drink to another player via mail."""
    drink = db.session.get(Drink, drink_id)
    receiver = db.session.get(Player, receiver_id)
    if not drink or not receiver:
        return False, "Invalid drink or player."
    cost = 50 + drink.times_ordered  # small cost to send
    if sender.gold < cost:
        return False, f"You need {cost} gold to send a drink."
    sender.gold -= cost
    mail = Mail(
        sender_id=sender.id,
        receiver_id=receiver.id,
        subject=f"A drink from {sender.name}!",
        message=f"{sender.name} has sent you a '{drink.name}' from Orb's Bar!"
    )
    db.session.add(mail)
    db.session.commit()
    return True, f"You sent '{drink.name}' to {receiver.name}!"


# ==================== PICK-POCKETING ====================

def pickpocket(player, target_id):
    """Attempt to pick-pocket another player. Returns (success, msg, log)."""
    if player.thefts_remaining <= 0:
        return False, "You've used all your theft attempts for today.", []

    target = db.session.get(Player, target_id)
    if not target:
        return False, "Target not found.", []
    if target.id == player.id:
        return False, "You can't steal from yourself.", []

    player.thefts_remaining -= 1
    log = []
    log.append(f"You creep up behind {target.name}...")

    # Success based on dexterity and agility vs target's
    skill = player.dexterity + player.agility + random.randint(0, 20)
    defence = target.dexterity + target.agility + random.randint(0, 30)

    if skill > defence:
        # Successful theft
        max_steal = max(1, target.gold // 4)
        stolen = random.randint(1, max(1, max_steal))
        if stolen > target.gold:
            stolen = target.gold
        if stolen <= 0:
            log.append(f"{target.name} has no gold to steal!")
            return True, f"{target.name} is broke!", log

        player.gold += stolen
        target.gold -= stolen
        player.darkness += random.randint(5, 20)
        log.append(f"SUCCESS! You stole {stolen} gold from {target.name}!")

        # Notify victim
        mail = Mail(
            sender_id=player.id,
            receiver_id=target.id,
            subject="You've been robbed!",
            message=f"Someone stole {stolen} gold from you while you weren't looking!"
        )
        db.session.add(mail)
        add_news(f"A thief struck in the dark alley! {target.name} lost gold!")
        db.session.commit()
        return True, f"You stole {stolen} gold!", log
    else:
        # Failed - caught!
        log.append(f"CAUGHT! {target.name}'s guards spot you!")
        fine = random.randint(10, 50) * player.level
        if fine > player.gold:
            fine = player.gold
        player.gold -= fine
        player.darkness += random.randint(1, 5)
        log.append(f"You were fined {fine} gold!")
        add_news(f"{player.name} was caught trying to pickpocket {target.name}!")
        db.session.commit()
        return True, "You were caught!", log


# ==================== BANK ROBBERY ====================

def rob_bank(player):
    """Attempt to rob the bank. Returns (success, msg, log)."""
    log = []
    log.append("You sneak into the bank vault...")

    # Calculate robbery difficulty
    success_chance = (player.dexterity + player.agility + player.level * 2) / 300
    success_chance = min(0.35, max(0.05, success_chance))  # 5-35% chance

    player.darkness += random.randint(10, 50)

    if random.random() < success_chance:
        # Successful robbery
        loot = random.randint(500, 2000) * player.level
        player.gold += loot
        log.append(f"SUCCESS! You grabbed {loot} gold from the vault!")

        # Bank guards may pursue
        guards = Player.query.filter_by(is_bank_guard=True).all()
        if guards:
            guard = random.choice(guards)
            log.append(f"Bank guard {guard.name} gives chase!")
            # Simple escape check
            escape = player.agility + random.randint(0, 50)
            catch = guard.agility + guard.strength + random.randint(0, 30)
            if escape > catch:
                log.append("You outrun the guard and escape!")
            else:
                lost = loot // 2
                player.gold -= lost
                log.append(f"The guard catches you and recovers {lost} gold!")
                loot -= lost

        add_news(f"The bank was robbed! {loot} gold was stolen!")
        db.session.commit()
        return True, f"You robbed {loot} gold from the bank!", log
    else:
        # Failed robbery
        log.append("CAUGHT! The bank guards seize you!")
        fine = random.randint(100, 500) * player.level
        if fine > player.gold:
            fine = player.gold
        player.gold -= fine
        player.is_imprisoned = True
        player.prison_days = random.randint(1, 3)
        log.append(f"You were fined {fine} gold and thrown in prison for {player.prison_days} day(s)!")
        add_news(f"{player.name} was caught trying to rob the bank and was imprisoned!")
        db.session.commit()
        return True, "You were caught and imprisoned!", log


# ==================== PRISON ESCAPE ====================

def escape_prison(player):
    """Attempt to escape from prison. Returns (success, msg, log)."""
    if not player.is_imprisoned:
        return False, "You are not imprisoned.", []

    max_attempts = int(GameConfig.get('prison_escape_attempts', '2') or '2')
    if player.escape_attempts >= max_attempts:
        return False, f"You've used all {max_attempts} escape attempts today.", []

    player.escape_attempts += 1
    log = []
    log.append("You try to pick the lock on your cell...")

    # Escape chance based on dexterity and agility
    chance = (player.dexterity + player.agility) / 200
    chance = min(0.40, max(0.05, chance))  # 5-40% chance

    if random.random() < chance:
        player.is_imprisoned = False
        player.prison_days = 0
        log.append("SUCCESS! You pick the lock and slip out into the night!")
        add_news(f"{player.name} escaped from prison!")
        db.session.commit()
        return True, "You escaped!", log
    else:
        # Failed - extra day added
        player.prison_days += 1
        log.append(f"FAILED! The guards add another day to your sentence. ({player.prison_days} days left)")
        db.session.commit()
        return True, "Escape failed!", log
