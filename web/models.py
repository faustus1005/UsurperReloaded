"""Database models for Usurper ReLoaded web version."""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# --- Enums as constants ---

RACES = [
    'Human', 'Hobbit', 'Elf', 'Half-Elf', 'Dwarf',
    'Troll', 'Orc', 'Gnome', 'Gnoll', 'Mutant'
]

CLASSES = [
    'Alchemist', 'Assassin', 'Barbarian', 'Bard', 'Cleric',
    'Jester', 'Magician', 'Paladin', 'Ranger', 'Sage', 'Warrior'
]

ITEM_TYPES = [
    'Head', 'Body', 'Arms', 'Hands', 'Fingers', 'Legs', 'Feet',
    'Waist', 'Neck', 'Face', 'Shield', 'Food', 'Drink', 'Weapon', 'Around Body'
]

EQUIPMENT_SLOTS = [
    'weapon', 'shield', 'head', 'body', 'arms', 'hands',
    'legs', 'feet', 'waist', 'neck', 'face', 'around_body'
]

# Race stat bonuses: [str, def, sta, agi, cha, dex, wis, hp_bonus, mana_bonus]
RACE_BONUSES = {
    'Human':    [0, 0, 0, 0, 0, 0, 0, 0, 0],
    'Hobbit':   [-2, 1, 1, 3, 1, 3, 0, -5, 0],
    'Elf':      [-1, 0, -1, 2, 2, 2, 2, -10, 10],
    'Half-Elf': [0, 0, 0, 1, 1, 1, 1, -5, 5],
    'Dwarf':    [2, 2, 2, -1, -2, 0, 0, 10, -5],
    'Troll':    [4, 3, 3, -3, -4, -2, -3, 20, -15],
    'Orc':      [3, 2, 1, -1, -3, -1, -2, 15, -10],
    'Gnome':    [-1, 0, 0, 1, 1, 2, 2, -5, 10],
    'Gnoll':    [2, 1, 1, 0, -3, 0, -1, 5, -5],
    'Mutant':   [1, 1, 1, 1, -2, 1, -1, 5, 0],
}

# Class stat bonuses: [str, def, sta, agi, cha, dex, wis, hp_bonus, mana_bonus]
CLASS_BONUSES = {
    'Alchemist': [-1, 0, 0, 0, 0, 2, 2, -5, 10],
    'Assassin':  [1, 0, 0, 2, -2, 2, 0, 0, 0],
    'Barbarian': [3, 2, 2, 0, -2, 0, -2, 15, -10],
    'Bard':      [0, 0, 0, 1, 3, 1, 0, 0, 5],
    'Cleric':    [-1, 1, 0, 0, 1, 0, 3, 0, 15],
    'Jester':    [0, 0, 1, 2, 1, 1, 0, 0, 0],
    'Magician':  [-2, -1, -1, 0, 0, 1, 4, -10, 25],
    'Paladin':   [2, 2, 1, 0, 1, 0, 1, 10, 5],
    'Ranger':    [1, 1, 1, 2, 0, 1, 0, 5, 0],
    'Sage':      [-2, -1, 0, 0, 1, 0, 4, -10, 20],
    'Warrior':   [3, 2, 2, 1, -1, 0, -2, 15, -10],
}

# Classes that can cast spells
SPELLCASTER_CLASSES = ['Alchemist', 'Cleric', 'Magician', 'Paladin', 'Sage']

# Experience required per level
LEVEL_XP = {
    1: 0, 2: 100, 3: 300, 4: 700, 5: 1500,
    6: 3000, 7: 6000, 8: 12000, 9: 24000, 10: 48000,
    11: 80000, 12: 130000, 13: 200000, 14: 300000, 15: 450000,
    16: 650000, 17: 900000, 18: 1200000, 19: 1600000, 20: 2100000,
    21: 2700000, 22: 3400000, 23: 4200000, 24: 5100000, 25: 6200000,
    26: 7500000, 27: 9000000, 28: 11000000, 29: 13500000, 30: 16500000,
}

# Spells available in the game
SPELLS = {
    1: {'name': 'Magic Missile', 'mana_cost': 5, 'type': 'attack', 'min_level': 1,
        'classes': ['Magician', 'Sage'], 'description': 'Fires a bolt of magical energy.'},
    2: {'name': 'Heal', 'mana_cost': 8, 'type': 'heal', 'min_level': 1,
        'classes': ['Cleric', 'Paladin', 'Sage'], 'description': 'Restores health.'},
    3: {'name': 'Fireball', 'mana_cost': 15, 'type': 'attack', 'min_level': 3,
        'classes': ['Magician'], 'description': 'Hurls an explosive ball of fire.'},
    4: {'name': 'Lightning Bolt', 'mana_cost': 12, 'type': 'attack', 'min_level': 2,
        'classes': ['Magician', 'Sage'], 'description': 'Strikes with electrical energy.'},
    5: {'name': 'Cure Disease', 'mana_cost': 10, 'type': 'cure', 'min_level': 2,
        'classes': ['Cleric', 'Paladin'], 'description': 'Cures diseases and afflictions.'},
    6: {'name': 'Shield', 'mana_cost': 8, 'type': 'buff', 'min_level': 2,
        'classes': ['Magician', 'Cleric', 'Sage'], 'description': 'Increases defense temporarily.'},
    7: {'name': 'Poison Cloud', 'mana_cost': 12, 'type': 'attack', 'min_level': 3,
        'classes': ['Alchemist'], 'description': 'Creates a cloud of noxious poison.'},
    8: {'name': 'Greater Heal', 'mana_cost': 20, 'type': 'heal', 'min_level': 5,
        'classes': ['Cleric', 'Sage'], 'description': 'Restores a large amount of health.'},
    9: {'name': 'Ice Storm', 'mana_cost': 18, 'type': 'attack', 'min_level': 5,
        'classes': ['Magician'], 'description': 'Summons a storm of ice shards.'},
    10: {'name': 'Holy Smite', 'mana_cost': 15, 'type': 'attack', 'min_level': 4,
         'classes': ['Paladin', 'Cleric'], 'description': 'Smites with divine power.'},
    11: {'name': 'Acid Splash', 'mana_cost': 10, 'type': 'attack', 'min_level': 2,
         'classes': ['Alchemist'], 'description': 'Throws corrosive acid.'},
    12: {'name': 'Resurrection', 'mana_cost': 50, 'type': 'heal', 'min_level': 10,
         'classes': ['Cleric', 'Sage'], 'description': 'Brings back from the brink of death.'},
}


class User(UserMixin, db.Model):
    """Authentication account - separate from game character."""
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(30), unique=True, nullable=False, index=True)
    password_hash = db.Column(db.String(256), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_login = db.Column(db.DateTime)

    player = db.relationship('Player', backref='user', uselist=False, lazy=True)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


class Player(db.Model):
    """Game character - the main player record, modeled after UserRec."""
    __tablename__ = 'players'

    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'), unique=True, nullable=True)

    # Identity
    name = db.Column(db.String(30), unique=True, nullable=False)  # game alias (name2)
    race = db.Column(db.String(10), nullable=False)
    player_class = db.Column(db.String(12), nullable=False)
    sex = db.Column(db.Integer, default=1)  # 1=male, 2=female
    age = db.Column(db.Integer, default=18)
    level = db.Column(db.Integer, default=1)
    is_npc = db.Column(db.Boolean, default=False)

    # NPC-specific fields
    npc_location = db.Column(db.String(20), default='dormitory')  # dormitory, inn, prison, beggar_wall, castle
    npc_days_in_prison = db.Column(db.Integer, default=0)
    npc_buy_strategy = db.Column(db.Integer, default=3)  # 1-5, how aggressively NPC shops
    npc_last_action = db.Column(db.DateTime, nullable=True)  # when NPC last took an action

    # Core stats
    strength = db.Column(db.Integer, default=10)
    defence = db.Column(db.Integer, default=10)
    stamina = db.Column(db.Integer, default=10)
    agility = db.Column(db.Integer, default=10)
    charisma = db.Column(db.Integer, default=10)
    dexterity = db.Column(db.Integer, default=10)
    wisdom = db.Column(db.Integer, default=10)

    # Vitals
    hp = db.Column(db.Integer, default=50)
    max_hp = db.Column(db.Integer, default=50)
    mana = db.Column(db.Integer, default=0)
    max_mana = db.Column(db.Integer, default=0)

    # Progression
    experience = db.Column(db.Integer, default=0)
    gold = db.Column(db.Integer, default=100)
    bank_gold = db.Column(db.Integer, default=0)

    # Alignment
    chivalry = db.Column(db.Integer, default=0)
    darkness = db.Column(db.Integer, default=0)

    # Daily limits
    fights_remaining = db.Column(db.Integer, default=20)
    player_fights = db.Column(db.Integer, default=3)
    thefts_remaining = db.Column(db.Integer, default=2)
    brawls_remaining = db.Column(db.Integer, default=2)

    # Combat stats
    weapon_power = db.Column(db.Integer, default=0)
    armor_power = db.Column(db.Integer, default=0)
    monster_kills = db.Column(db.Integer, default=0)
    monster_defeats = db.Column(db.Integer, default=0)
    player_kills = db.Column(db.Integer, default=0)
    player_defeats = db.Column(db.Integer, default=0)

    # Status effects
    is_poisoned = db.Column(db.Boolean, default=False)
    is_blind = db.Column(db.Boolean, default=False)
    has_plague = db.Column(db.Boolean, default=False)

    # Health
    healing_potions = db.Column(db.Integer, default=2)
    mental_health = db.Column(db.Integer, default=100)
    addiction = db.Column(db.Integer, default=0)

    # Social
    team_name = db.Column(db.String(25), default='')
    is_king = db.Column(db.Boolean, default=False)
    married = db.Column(db.Boolean, default=False)
    spouse_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    is_imprisoned = db.Column(db.Boolean, default=False)
    town_control = db.Column(db.Boolean, default=False)  # turf flag
    team_fights = db.Column(db.Integer, default=1)  # gang war attempts per day
    quests_completed = db.Column(db.Integer, default=0)
    quests_failed = db.Column(db.Integer, default=0)

    # God/religion
    god_name = db.Column(db.String(30), default='')  # name of deity worshipped
    is_god = db.Column(db.Boolean, default=False)  # has ascended to godhood

    # Family
    is_pregnant = db.Column(db.Boolean, default=False)
    pregnancy_days = db.Column(db.Integer, default=0)
    children_count = db.Column(db.Integer, default=0)

    spouse = db.relationship('Player', foreign_keys=[spouse_id], remote_side='Player.id')

    # Equipment slots (store item IDs, 0 = empty)
    equipped_weapon = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_shield = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_head = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_body = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_arms = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_hands = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_legs = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_feet = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_waist = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_neck = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_face = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_around_body = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)

    # Phrases
    phrase_attacked = db.Column(db.String(70), default='')
    phrase_victory = db.Column(db.String(70), default='')
    phrase_defeat = db.Column(db.String(70), default='')
    battlecry = db.Column(db.String(70), default='')

    # Spells known (comma-separated spell IDs)
    spells_known = db.Column(db.String(100), default='')

    # Timestamps
    last_played = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    last_maintenance = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    # Relationships
    inventory_items = db.relationship('InventoryItem', backref='player', lazy=True,
                                       cascade='all, delete-orphan')
    sent_mail = db.relationship('Mail', foreign_keys='Mail.sender_id', backref='sender', lazy=True)
    received_mail = db.relationship('Mail', foreign_keys='Mail.receiver_id', backref='receiver', lazy=True)
    news_entries = db.relationship('NewsEntry', backref='player', lazy=True)

    def get_total_attack(self):
        """Calculate total attack power including equipment."""
        base = self.strength + self.weapon_power
        return max(1, base)

    def get_total_defense(self):
        """Calculate total defense including equipment."""
        base = self.defence + self.armor_power
        return max(1, base)

    def alignment_string(self):
        if self.chivalry > self.darkness:
            if self.chivalry > 100:
                return 'Virtuous'
            elif self.chivalry > 50:
                return 'Noble'
            return 'Good'
        elif self.darkness > self.chivalry:
            if self.darkness > 100:
                return 'Diabolical'
            elif self.darkness > 50:
                return 'Wicked'
            return 'Evil'
        return 'Neutral'

    def can_level_up(self):
        next_level = self.level + 1
        if next_level > 30:
            return False
        return self.experience >= LEVEL_XP.get(next_level, float('inf'))

    def xp_for_next_level(self):
        next_level = self.level + 1
        return LEVEL_XP.get(next_level, 0)

    def get_known_spells(self):
        if not self.spells_known:
            return []
        return [int(x) for x in self.spells_known.split(',') if x]

    def knows_spell(self, spell_id):
        return spell_id in self.get_known_spells()

    def learn_spell(self, spell_id):
        known = self.get_known_spells()
        if spell_id not in known:
            known.append(spell_id)
            self.spells_known = ','.join(str(x) for x in known)

    def recalculate_equipment_power(self):
        """Recalculate weapon and armor power from equipped items."""
        weapon_pow = 0
        armor_pow = 0
        for slot in EQUIPMENT_SLOTS:
            item_id = getattr(self, f'equipped_{slot}', None)
            if item_id:
                item = db.session.get(Item, item_id)
                if item:
                    if item.item_type == 'Weapon':
                        weapon_pow += item.attack_bonus
                    armor_pow += item.armor_bonus
                    # Don't add stat bonuses here - they're item properties
        self.weapon_power = weapon_pow
        self.armor_power = armor_pow


class Item(db.Model):
    """Item/equipment definition, modeled after ORec."""
    __tablename__ = 'items'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(70), nullable=False)
    item_type = db.Column(db.String(15), nullable=False)  # from ITEM_TYPES
    value = db.Column(db.Integer, default=0)  # gold value

    # Stat bonuses when equipped
    attack_bonus = db.Column(db.Integer, default=0)
    armor_bonus = db.Column(db.Integer, default=0)
    hp_bonus = db.Column(db.Integer, default=0)
    strength_bonus = db.Column(db.Integer, default=0)
    defence_bonus = db.Column(db.Integer, default=0)
    stamina_bonus = db.Column(db.Integer, default=0)
    agility_bonus = db.Column(db.Integer, default=0)
    charisma_bonus = db.Column(db.Integer, default=0)
    dexterity_bonus = db.Column(db.Integer, default=0)
    wisdom_bonus = db.Column(db.Integer, default=0)
    mana_bonus = db.Column(db.Integer, default=0)

    # Properties
    description = db.Column(db.String(200), default='')
    is_cursed = db.Column(db.Boolean, default=False)
    is_unique = db.Column(db.Boolean, default=False)
    min_level = db.Column(db.Integer, default=1)
    max_level = db.Column(db.Integer, default=30)
    in_shop = db.Column(db.Boolean, default=False)
    in_dungeon = db.Column(db.Boolean, default=False)
    strength_required = db.Column(db.Integer, default=0)
    good_only = db.Column(db.Boolean, default=False)
    evil_only = db.Column(db.Boolean, default=False)
    shop_category = db.Column(db.String(20), default='')  # weapon, armor, magic, alchemist, general, shady

    # Class restrictions (comma-separated class names, empty = all classes)
    class_restrictions = db.Column(db.String(200), default='')

    def can_be_used_by(self, player):
        if self.strength_required > 0 and player.strength < self.strength_required:
            return False
        if self.good_only and player.darkness > player.chivalry:
            return False
        if self.evil_only and player.chivalry > player.darkness:
            return False
        if self.class_restrictions:
            allowed = [c.strip() for c in self.class_restrictions.split(',')]
            if player.player_class not in allowed:
                return False
        return True

    def get_slot(self):
        """Map item_type to equipment slot name."""
        slot_map = {
            'Weapon': 'weapon', 'Shield': 'shield', 'Head': 'head',
            'Body': 'body', 'Arms': 'arms', 'Hands': 'hands',
            'Legs': 'legs', 'Feet': 'feet', 'Waist': 'waist',
            'Neck': 'neck', 'Face': 'face', 'Around Body': 'around_body',
        }
        return slot_map.get(self.item_type)


class InventoryItem(db.Model):
    """Player inventory - items being carried."""
    __tablename__ = 'inventory'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)

    item = db.relationship('Item', lazy=True)


class Monster(db.Model):
    """Monster definition for dungeon encounters."""
    __tablename__ = 'monsters'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    min_dungeon_level = db.Column(db.Integer, default=1)
    max_dungeon_level = db.Column(db.Integer, default=10)

    # Stats
    hp = db.Column(db.Integer, default=20)
    strength = db.Column(db.Integer, default=10)
    defence = db.Column(db.Integer, default=5)
    weapon_power = db.Column(db.Integer, default=0)
    armor_power = db.Column(db.Integer, default=0)

    # Rewards
    experience = db.Column(db.Integer, default=10)
    gold = db.Column(db.Integer, default=5)

    # Combat properties
    phrase = db.Column(db.String(70), default='')
    weapon_name = db.Column(db.String(40), default='claws')
    armor_name = db.Column(db.String(40), default='')
    is_poisonous = db.Column(db.Boolean, default=False)
    has_disease = db.Column(db.Boolean, default=False)
    magic_resistance = db.Column(db.Integer, default=0)
    magic_level = db.Column(db.Integer, default=0)
    aggression = db.Column(db.Integer, default=1)  # 0-3

    # Can drop items?
    can_drop_weapon = db.Column(db.Boolean, default=False)
    can_drop_armor = db.Column(db.Boolean, default=False)
    drop_item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)

    drop_item = db.relationship('Item', lazy=True)


class Mail(db.Model):
    """Inter-player messaging system."""
    __tablename__ = 'mail'

    id = db.Column(db.Integer, primary_key=True)
    sender_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    receiver_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    subject = db.Column(db.String(70), default='')
    message = db.Column(db.Text, default='')
    is_read = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class NewsEntry(db.Model):
    """Daily news/events log."""
    __tablename__ = 'news'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    category = db.Column(db.String(20), default='general')  # combat, social, royal, etc.
    message = db.Column(db.Text, nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class Team(db.Model):
    """Teams/gangs that players can create and join."""
    __tablename__ = 'teams'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    leader_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    wins = db.Column(db.Integer, default=0)
    losses = db.Column(db.Integer, default=0)
    town_control = db.Column(db.Boolean, default=False)
    treasury = db.Column(db.Integer, default=0)
    town_control_days = db.Column(db.Integer, default=0)  # how many days held town

    leader = db.relationship('Player', foreign_keys=[leader_id], backref='led_team')
    members = db.relationship('TeamMember', backref='team', lazy=True, cascade='all, delete-orphan')

    def get_power(self):
        """Total team power based on members."""
        total = 0
        for member in self.members:
            if member.player:
                total += member.player.max_hp + member.player.level * 10
        return total

    def member_count(self):
        return len(self.members)


class TeamMember(db.Model):
    """Team membership records."""
    __tablename__ = 'team_members'

    id = db.Column(db.Integer, primary_key=True)
    team_id = db.Column(db.Integer, db.ForeignKey('teams.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False, unique=True)
    joined_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    player = db.relationship('Player', backref='team_membership')


class KingRecord(db.Model):
    """Tracks the current and historical monarchs."""
    __tablename__ = 'king_records'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    crowned_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    dethroned_at = db.Column(db.DateTime, nullable=True)
    is_current = db.Column(db.Boolean, default=True)
    moat_guards = db.Column(db.Integer, default=5)
    tax_rate = db.Column(db.Integer, default=5)  # percentage
    treasury = db.Column(db.Integer, default=0)
    quests_left = db.Column(db.Integer, default=3)  # quests king can issue per day
    town_control_days = db.Column(db.Integer, default=0)  # days team has held town

    player = db.relationship('Player', backref='king_records')


class Bounty(db.Model):
    """Bounties placed on players."""
    __tablename__ = 'bounties'

    id = db.Column(db.Integer, primary_key=True)
    target_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    poster_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    amount = db.Column(db.Integer, nullable=False)
    reason = db.Column(db.String(100), default='Wanted Dead or Alive')
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    claimed = db.Column(db.Boolean, default=False)
    claimed_by_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)

    target = db.relationship('Player', foreign_keys=[target_id], backref='bounties_on')
    poster = db.relationship('Player', foreign_keys=[poster_id], backref='bounties_posted')
    claimed_by = db.relationship('Player', foreign_keys=[claimed_by_id])


class Relationship(db.Model):
    """Social relationships between players."""
    __tablename__ = 'relationships'

    id = db.Column(db.Integer, primary_key=True)
    player1_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    player2_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    rel_type = db.Column(db.String(20), nullable=False)  # 'married', 'ally', 'rival', 'lover'
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    player1 = db.relationship('Player', foreign_keys=[player1_id], backref='relationships_as_p1')
    player2 = db.relationship('Player', foreign_keys=[player2_id], backref='relationships_as_p2')

    __table_args__ = (
        db.UniqueConstraint('player1_id', 'player2_id', 'rel_type', name='unique_relationship'),
    )


class Child(db.Model):
    """Children born to married couples."""
    __tablename__ = 'children'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    mother_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    father_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    sex = db.Column(db.Integer, default=1)  # 1=male, 2=female
    age = db.Column(db.Integer, default=0)
    race = db.Column(db.String(10), default='Human')
    description = db.Column(db.String(100), default='')
    born_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_orphan = db.Column(db.Boolean, default=False)
    kidnapped_by_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)

    mother = db.relationship('Player', foreign_keys=[mother_id], backref='children_as_mother')
    father = db.relationship('Player', foreign_keys=[father_id], backref='children_as_father')
    kidnapped_by = db.relationship('Player', foreign_keys=[kidnapped_by_id])


class RoyalQuest(db.Model):
    """Royal quests issued by the King/Queen."""
    __tablename__ = 'royal_quests'

    id = db.Column(db.Integer, primary_key=True)
    initiator_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    occupier_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    title = db.Column(db.String(60), default='Royal Quest')
    comment = db.Column(db.String(200), default='')
    difficulty = db.Column(db.Integer, default=5)  # 1-10
    monsters_required = db.Column(db.Integer, default=5)  # number of monsters to kill
    monsters_killed = db.Column(db.Integer, default=0)
    days_to_complete = db.Column(db.Integer, default=3)
    days_elapsed = db.Column(db.Integer, default=0)
    min_level = db.Column(db.Integer, default=1)
    max_level = db.Column(db.Integer, default=30)
    reward_type = db.Column(db.String(15), default='experience')  # experience, gold, potions, chivalry, darkness
    reward_size = db.Column(db.Integer, default=2)  # 1=low, 2=medium, 3=high
    penalty_type = db.Column(db.String(15), default='')  # same options or empty
    penalty_size = db.Column(db.Integer, default=0)
    is_completed = db.Column(db.Boolean, default=False)
    is_failed = db.Column(db.Boolean, default=False)
    is_public = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    initiator = db.relationship('Player', foreign_keys=[initiator_id], backref='quests_initiated')
    occupier = db.relationship('Player', foreign_keys=[occupier_id], backref='quests_accepted')


class God(db.Model):
    """Divine beings - players who have ascended or NPC deities."""
    __tablename__ = 'gods'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True, nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)  # null for primordial gods
    sex = db.Column(db.Integer, default=1)
    level = db.Column(db.Integer, default=1)  # 1-9
    experience = db.Column(db.Integer, default=0)  # havre/divine power
    deeds_left = db.Column(db.Integer, default=5)
    alignment = db.Column(db.String(10), default='neutral')  # good, evil, neutral
    domain = db.Column(db.String(30), default='')  # War, Love, Death, Nature, etc.
    description = db.Column(db.String(200), default='')
    is_active = db.Column(db.Boolean, default=True)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    player = db.relationship('Player', backref='god_record')

    def title(self):
        titles = {
            1: 'Lesser Spirit', 2: 'Minor Spirit', 3: 'Spirit',
            4: 'Major Spirit', 5: 'Minor Deity', 6: 'Deity',
            7: 'Major Deity', 8: 'DemiGod', 9: 'God'
        }
        return titles.get(self.level, 'Lesser Spirit')

    def believer_count(self):
        return Player.query.filter_by(god_name=self.name).count()

    def check_level_up(self):
        thresholds = [0, 5000, 15000, 50000, 70000, 90000, 110000, 550000, 1000500]
        new_level = 1
        for i, threshold in enumerate(thresholds):
            if self.experience > threshold:
                new_level = i + 1
        return new_level


class TeamRecord(db.Model):
    """Track records for team town control duration."""
    __tablename__ = 'team_records'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(30), nullable=False)
    days_held = db.Column(db.Integer, default=0)
    recorded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class GameConfig(db.Model):
    """Game configuration settings."""
    __tablename__ = 'config'

    id = db.Column(db.Integer, primary_key=True)
    key = db.Column(db.String(50), unique=True, nullable=False)
    value = db.Column(db.String(200), default='')

    @staticmethod
    def get(key, default=''):
        config = GameConfig.query.filter_by(key=key).first()
        return config.value if config else default

    @staticmethod
    def set(key, value):
        config = GameConfig.query.filter_by(key=key).first()
        if config:
            config.value = str(value)
        else:
            config = GameConfig(key=key, value=str(value))
            db.session.add(config)
        db.session.commit()
