"""Core game logic for Usurper ReLoaded - combat, leveling, dungeon events."""

import random
from datetime import datetime, timezone
from models import (
    db, Player, Monster, Item, InventoryItem, NewsEntry, Mail,
    Team, TeamMember, KingRecord, Bounty, Relationship,
    Child, RoyalQuest, God, TeamRecord,
    RACE_BONUSES, CLASS_BONUSES, LEVEL_XP, SPELLS, SPELLCASTER_CLASSES, RACES
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
        return crown_new_king(challenger)

    if king.id == challenger.id:
        return False, "You are already the ruler!", []

    if challenger.level < 5:
        return False, "You must be at least level 5 to challenge the throne.", []

    if challenger.hp < challenger.max_hp // 2:
        return False, "You are too wounded to challenge the throne. Heal first.", []

    # Fight through moat guards first
    combat_log = []
    guards_remaining = king_record.moat_guards

    if guards_remaining > 0:
        combat_log.append(f"You must fight through {guards_remaining} moat guards!")
        guard_hp = 30 + king.level * 5
        for i in range(guards_remaining):
            combat_log.append(f"--- Moat Guard {i + 1} ---")
            ghp = guard_hp
            while ghp > 0 and challenger.hp > 0:
                # Challenger attacks guard
                atk = calculate_attack(challenger.strength, challenger.weapon_power, challenger.level)
                guard_def = 5 + king.level * 2
                dmg = max(1, atk - guard_def)
                ghp -= dmg
                combat_log.append(f"You strike the guard for {dmg} damage.")

                if ghp <= 0:
                    combat_log.append("The guard falls!")
                    break

                # Guard attacks challenger
                guard_atk = 8 + king.level * 3
                pdef = calculate_defense(challenger.defence, challenger.armor_power)
                gdmg = max(1, guard_atk - pdef)
                challenger.hp -= gdmg
                combat_log.append(f"The guard strikes you for {gdmg} damage.")

                if challenger.hp <= 0:
                    challenger.hp = max(1, challenger.max_hp // 4)
                    combat_log.append("The moat guards have defeated you!")
                    news = NewsEntry(
                        player_id=challenger.id,
                        category='royal',
                        message=f"{challenger.name} failed to get past the castle moat guards."
                    )
                    db.session.add(news)
                    return False, "You were defeated by the moat guards!", combat_log

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
        moat_guards=5,
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
    from datetime import datetime, timezone
    king_record.dethroned_at = datetime.now(timezone.utc)


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


def king_hire_guards(king_record, count):
    """Hire moat guards (costs gold from treasury)."""
    cost_per_guard = 100
    total_cost = count * cost_per_guard
    if king_record.treasury < total_cost:
        return False, f"Not enough gold in treasury. Need {total_cost}, have {king_record.treasury}."
    if king_record.moat_guards + count > 100:
        return False, "Maximum 100 moat guards."
    king_record.treasury -= total_cost
    king_record.moat_guards += count
    return True, f"Hired {count} moat guards. Total: {king_record.moat_guards}"


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
]


def get_random_dungeon_event():
    """Select a random dungeon event."""
    return random.choice(DUNGEON_EVENTS)


def resolve_dungeon_event(player, event_id, choice_key):
    """Resolve a dungeon event choice for a player."""
    event = next((e for e in DUNGEON_EVENTS if e['id'] == event_id), None)
    if not event:
        return "Nothing happens."

    choice = event['choices'].get(choice_key)
    if not choice:
        return "Nothing happens."

    # Filter outcomes by condition
    valid_outcomes = []
    for outcome in choice['outcomes']:
        condition = outcome.get('condition', '')
        if condition:
            if condition == 'gold >= 50' and player.gold < 50:
                continue
            elif condition == 'gold < 50' and player.gold >= 50:
                continue
            elif condition == 'gold >= 100' and player.gold < 100:
                continue
            elif condition == 'gold < 100' and player.gold >= 100:
                continue
            elif condition == 'gold >= 200' and player.gold < 200:
                continue
            elif condition == 'gold < 200' and player.gold >= 200:
                continue
        valid_outcomes.append(outcome)

    if not valid_outcomes:
        return "Nothing happens."

    # Weighted random selection
    weights = [o.get('weight', 1) for o in valid_outcomes]
    outcome = random.choices(valid_outcomes, weights=weights, k=1)[0]

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
