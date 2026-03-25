"""Database models for Usurper ReLoaded web version."""

from datetime import datetime, timezone
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash

db = SQLAlchemy()

# --- Enums as constants ---

RACES = [
    'Human', 'Hobbit', 'Elf', 'Half-Elf', 'Dwarf',
    'Troll', 'Orc', 'Gnome', 'Gnoll', 'Mutant',
    'Tiefling', 'Dragonborn', 'Fae'
]

CLASSES = [
    'Alchemist', 'Assassin', 'Barbarian', 'Bard', 'Cleric',
    'Jester', 'Magician', 'Monk', 'Necromancer', 'Paladin',
    'Ranger', 'Sage', 'Warrior', 'Witch Hunter'
]

ITEM_TYPES = [
    'Head', 'Body', 'Arms', 'Hands', 'Fingers', 'Legs', 'Feet',
    'Waist', 'Neck', 'Face', 'Shield', 'Food', 'Drink', 'Weapon', 'Around Body'
]

EQUIPMENT_SLOTS = [
    'weapon', 'weapon2', 'shield', 'head', 'body', 'arms', 'hands',
    'legs', 'feet', 'waist', 'neck', 'neck2', 'face', 'around_body',
    'finger1', 'finger2'
]

# Display names for equipment slots
EQUIPMENT_SLOT_LABELS = {
    'weapon': 'Weapon (Right)', 'weapon2': 'Weapon (Left)', 'shield': 'Shield',
    'head': 'Head', 'body': 'Body', 'arms': 'Arms', 'hands': 'Hands',
    'legs': 'Legs', 'feet': 'Feet', 'waist': 'Waist',
    'neck': 'Neck 1', 'neck2': 'Neck 2', 'face': 'Face',
    'around_body': 'Around Body',
    'finger1': 'Ring 1', 'finger2': 'Ring 2',
}

# Close combat moves and skill ranking names
CLOSE_COMBAT_MOVES = [
    'Tackle', 'Drop-Kick', 'Uppercut', 'Bite', 'Leg-Sweep', 'JointBreak',
    'Knifehand', 'Nerve Punch', 'Chokehold', 'Headbash', 'Pull Hair',
    'Kick', 'Straight Punch', 'Ram'
]

COMBAT_SKILL_RANKS = [
    'Rotten', 'Awful', 'Lousy', 'Pathetic', 'Bad', 'Poor', 'Incompetent',
    'Below Average', 'Average', 'Above Average', 'Pretty Good', 'Competent',
    'Good', 'Very Good', 'Extraordinary', 'Excellent', 'Superb', '*COMPLETE*'
]

# Hit intensity levels for combat flavor text
HIT_INTENSITY = ['Light', 'Medium', 'Hard', 'Heavy', 'Extreme', 'ULTRA', 'MAX']

# Battle Master PvP rating titles
BATTLE_MASTER_RANKS = [
    (0, 'Wimp'), (1, 'Baby Soldier'), (8, 'Novice'), (16, 'Amateur'),
    (51, 'Adept'), (91, 'Warrior'), (111, 'Soldier'), (151, 'Veteran'),
    (251, 'Mercenary'), (351, 'Experienced Adventurer'), (471, 'Wardog'),
    (601, 'Battle Tank'), (900, 'Battle-god')
]

# Disease types with per-battle HP damage
DISEASES = {
    'plague': {'name': 'Plague', 'damage': 8},
    'smallpox': {'name': 'Smallpox', 'damage': 3},
    'measles': {'name': 'Measles', 'damage': 1},
    'leprosy': {'name': 'Leprosy', 'damage': 5},
}

# Gigolo companions (male counterpart to Beauty Nest)
GIGOLOS = [
    {'name': 'Signori', 'cost': 500, 'level': 1},
    {'name': 'Tod', 'cost': 2000, 'level': 5},
    {'name': 'Mbuto', 'cost': 5000, 'level': 10},
    {'name': 'Merson', 'cost': 10000, 'level': 15},
    {'name': 'Brian De Roy', 'cost': 20000, 'level': 20},
    {'name': 'Rasputin', 'cost': 30000, 'level': 25},
    {'name': 'Manhio', 'cost': 40000, 'level': 30},
    {'name': 'Jake', 'cost': 70000, 'level': 40},
    {'name': 'Banco', 'cost': 100000, 'level': 50},
]

# Alchemist poison strength levels
POISON_LEVELS = ['Light', 'Medium', 'Strong', 'Deadly']

# Fatal drink combinations (race/class + ingredient thresholds)
FATAL_DRINK_COMBOS = [
    {'race': 'Troll', 'ingredient': 'elf_water', 'threshold': 1, 'message': 'The Elf Water is lethal to Trolls!'},
    {'ingredient': 'tabasco', 'threshold': 80, 'message': 'The Tabasco burns through your insides!'},
    {'ingredient': 'chilipeppar', 'threshold': 80, 'message': 'The Chilipeppar is too intense!'},
    {'ingredient': 'bat_brain', 'threshold': 70, 'message': 'Too much Bat Brain has driven you mad!'},
    {'ingredient': 'horse_blood', 'threshold': 90, 'message': 'The Horse Blood has poisoned you!'},
    {'ingredient': 'bobs_bomber', 'threshold': 90, 'message': "Bob's Bomber has blown your mind... literally!"},
    {'ingredient': 'snake_spit', 'threshold': 80, 'message': 'The Snake Spit is pure venom!'},
]

# Drink ingredient stat effects (ingredient -> stat -> bonus_per_10_pct)
DRINK_STAT_EFFECTS = {
    'bat_brain': {'wisdom': 1, 'darkness': 2},
    'honeydew': {'charisma': 1, 'chivalry': 1},
    'orange_juice': {'stamina': 1},
    'tabasco': {'strength': 2},
    'ale': {'stamina': 1, 'charisma': -1},
    'hedgehog_saliva': {'dexterity': 1},
    'water': {},
    'horse_blood': {'strength': 1, 'darkness': 1},
    'bobs_bomber': {'strength': 1, 'stamina': -1},
    'troll_rum': {'strength': 2, 'wisdom': -1},
    'elf_water': {'wisdom': 1, 'agility': 1},
    'kicking_squaw': {'agility': 2},
    'milk': {'defence': 1},
    'wine_vinegar': {'dexterity': 1, 'charisma': -1},
    'snake_spit': {'agility': 1, 'darkness': 1},
    'duck_dropping': {'defence': 1, 'charisma': -2},
    'chilipeppar': {'strength': 1, 'stamina': 1},
}

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
    'Tiefling':  [1, 0, 0, 1, -1, 1, 1, 0, 10],
    'Dragonborn':[3, 2, 2, -2, 0, -1, 0, 15, -5],
    'Fae':       [-2, -1, -1, 3, 3, 2, 1, -15, 20],
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
    'Monk':         [1, 2, 2, 3, 0, 2, 1, 5, 5],
    'Necromancer':  [-1, -1, 0, 0, -2, 1, 4, -10, 20],
    'Witch Hunter': [2, 1, 1, 1, 0, 2, 1, 5, 0],
}

# Classes that can cast spells
SPELLCASTER_CLASSES = ['Alchemist', 'Cleric', 'Magician', 'Monk', 'Necromancer', 'Paladin', 'Sage', 'Witch Hunter']

# Orb's Bar drink ingredients: (attribute_name, display_name)
DRINK_INGREDIENTS = [
    ('bat_brain', 'Bat Brain'),
    ('honeydew', 'Honeydew'),
    ('orange_juice', 'Orange Juice'),
    ('tabasco', 'Tabasco'),
    ('ale', 'Ale'),
    ('hedgehog_saliva', 'Hedgehog Saliva'),
    ('water', 'Water'),
    ('horse_blood', 'Horse Blood'),
    ('bobs_bomber', "Bob's Bomber"),
    ('troll_rum', 'Troll Rum'),
    ('elf_water', 'Elf Water'),
    ('kicking_squaw', 'Kicking Squaw'),
    ('milk', 'Milk'),
    ('wine_vinegar', 'Wine Vinegar'),
    ('snake_spit', 'Snake Spit'),
    ('duck_dropping', 'Duck Dropping'),
    ('chilipeppar', 'Chilipeppar'),
]

# Experience required per level (100 levels, exponential curve)
LEVEL_XP = {
    1: 0, 2: 100, 3: 300, 4: 700, 5: 1500,
    6: 3000, 7: 6000, 8: 12000, 9: 24000, 10: 48000,
    11: 80000, 12: 130000, 13: 200000, 14: 300000, 15: 450000,
    16: 650000, 17: 900000, 18: 1200000, 19: 1600000, 20: 2100000,
    21: 2700000, 22: 3400000, 23: 4200000, 24: 5100000, 25: 6200000,
    26: 7500000, 27: 9000000, 28: 11000000, 29: 13500000, 30: 16500000,
    31: 20000000, 32: 24000000, 33: 28500000, 34: 33500000, 35: 39000000,
    36: 45000000, 37: 52000000, 38: 60000000, 39: 69000000, 40: 79000000,
    41: 90000000, 42: 102000000, 43: 115000000, 44: 130000000, 45: 147000000,
    46: 166000000, 47: 187000000, 48: 210000000, 49: 236000000, 50: 265000000,
    51: 297000000, 52: 332000000, 53: 370000000, 54: 412000000, 55: 458000000,
    56: 509000000, 57: 565000000, 58: 627000000, 59: 695000000, 60: 770000000,
    61: 852000000, 62: 942000000, 63: 1040000000, 64: 1148000000, 65: 1266000000,
    66: 1396000000, 67: 1538000000, 68: 1694000000, 69: 1865000000, 70: 2053000000,
    71: 2260000000, 72: 2487000000, 73: 2737000000, 74: 3012000000, 75: 3314000000,
    76: 3647000000, 77: 4013000000, 78: 4416000000, 79: 4860000000, 80: 5348000000,
    81: 5885000000, 82: 6476000000, 83: 7127000000, 84: 7843000000, 85: 8632000000,
    86: 9500000000, 87: 10455000000, 88: 11506000000, 89: 12663000000, 90: 13937000000,
    91: 15339000000, 92: 16882000000, 93: 18581000000, 94: 20451000000, 95: 22510000000,
    96: 24777000000, 97: 27272000000, 98: 30019000000, 99: 33042000000, 100: 36370000000,
}

# Monster spells (used by monsters in combat)
# Training Masters - LORD-inspired level gate system
# Each master must be defeated in combat to advance past their level range
TRAINING_MASTERS = [
    {'name': 'Halder', 'max_level': 2, 'hp': 30, 'attack': 8, 'defense': 5,
     'phrase': 'You are not yet ready, whelp!'},
    {'name': 'Sandtiger', 'max_level': 5, 'hp': 80, 'attack': 18, 'defense': 12,
     'phrase': 'Let me see if you have what it takes.'},
    {'name': 'Aragorn', 'max_level': 10, 'hp': 200, 'attack': 40, 'defense': 25,
     'phrase': 'Prepare yourself, adventurer.'},
    {'name': 'Mistress Vena', 'max_level': 15, 'hp': 500, 'attack': 80, 'defense': 50,
     'phrase': 'Few survive my training...'},
    {'name': 'Asgoth', 'max_level': 25, 'hp': 1200, 'attack': 150, 'defense': 90,
     'phrase': 'You face the wrath of Asgoth!'},
    {'name': 'Grimjaw', 'max_level': 40, 'hp': 3000, 'attack': 300, 'defense': 180,
     'phrase': 'Only the strongest may pass!'},
    {'name': 'Darkstorm', 'max_level': 60, 'hp': 8000, 'attack': 600, 'defense': 400,
     'phrase': 'I have crushed a thousand warriors...'},
    {'name': 'Olivia', 'max_level': 80, 'hp': 20000, 'attack': 1200, 'defense': 800,
     'phrase': 'Do not be deceived by my grace.'},
    {'name': 'Turgon', 'max_level': 99, 'hp': 50000, 'attack': 2500, 'defense': 1500,
     'phrase': 'I am the final master. Prepare to die!'},
]

# Horse types available in the game (LORD-inspired mount system)
HORSE_TYPES = [
    {'name': 'Old Donkey', 'type': 'donkey', 'bonus_fights': 2, 'cost': 500,
     'description': 'Slow but reliable. Barely counts as a mount.'},
    {'name': 'Brown Mare', 'type': 'mare', 'bonus_fights': 3, 'cost': 2000,
     'description': 'A sturdy horse for everyday travel.'},
    {'name': 'White Stallion', 'type': 'stallion', 'bonus_fights': 4, 'cost': 8000,
     'description': 'A noble steed, swift and strong.'},
    {'name': 'Black Warhorse', 'type': 'warhorse', 'bonus_fights': 5, 'cost': 25000,
     'description': 'Bred for battle, feared by enemies.'},
    {'name': 'Shadow Nightmare', 'type': 'nightmare', 'bonus_fights': 7, 'cost': 100000,
     'description': 'A demonic steed wreathed in dark flames.'},
]

# Fairy encounter outcomes (LORD-inspired)
FAIRY_ENCOUNTERS = [
    {'type': 'heal', 'weight': 25, 'message': 'A tiny fairy appears in a flash of light and heals your wounds!'},
    {'type': 'gold', 'weight': 20, 'message': 'A mischievous fairy drops a shower of gold coins at your feet!'},
    {'type': 'xp', 'weight': 15, 'message': 'A radiant fairy blesses you with ancient wisdom!'},
    {'type': 'horse', 'weight': 5, 'message': 'A powerful fairy summons a magical steed for you!'},
    {'type': 'extra_fights', 'weight': 15, 'message': 'A playful fairy grants you renewed energy for more battles!'},
    {'type': 'stat_boost', 'weight': 10, 'message': 'A wise fairy touches your forehead and you feel power surge through you!'},
    {'type': 'dust', 'weight': 10, 'message': 'The fairy leaves behind a trail of sparkling fairy dust!'},
]

MONSTER_SPELLS = {
    1: {'name': 'Cause Damage', 'mana_cost': 10, 'multi_target': False,
        'description': 'The creature channels destructive energy!'},
    2: {'name': 'Snakes', 'mana_cost': 20, 'multi_target': False,
        'description': 'Silver Snakes appear in a puff of smoke!'},
    3: {'name': 'Cyclone', 'mana_cost': 25, 'multi_target': True,
        'description': 'They have summoned a CYCLONE!'},
    4: {'name': 'Summon Undead', 'mana_cost': 30, 'multi_target': False,
        'description': 'An undead creature rises from the ground!'},
    5: {'name': 'Vice of Death', 'mana_cost': 35, 'multi_target': False,
        'description': 'You have been seized by cramps!'},
    6: {'name': 'Drain Life', 'mana_cost': 40, 'multi_target': False,
        'description': 'A bright spark of red energy hits you!'},
}

# Spells available in the game
# Fields: name, mana_cost, type, min_level, classes, description,
#         incantation (arcane word), duration ('turn'/'fight'), multi_target, freeze_turns
SPELLS = {
    1: {'name': 'Magic Missile', 'mana_cost': 5, 'type': 'attack', 'min_level': 1,
        'classes': ['Magician', 'Sage'], 'description': 'Fires a bolt of magical energy.',
        'incantation': 'Zazzaknah', 'duration': 'turn'},
    2: {'name': 'Heal', 'mana_cost': 8, 'type': 'heal', 'min_level': 1,
        'classes': ['Cleric', 'Paladin', 'Sage'], 'description': 'Restores health.',
        'incantation': 'Abrazak', 'duration': 'turn'},
    3: {'name': 'Fireball', 'mana_cost': 15, 'type': 'attack', 'min_level': 3,
        'classes': ['Magician'], 'description': 'Hurls an explosive ball of fire.',
        'incantation': 'Zimmokoth', 'duration': 'turn'},
    4: {'name': 'Lightning Bolt', 'mana_cost': 12, 'type': 'attack', 'min_level': 2,
        'classes': ['Magician', 'Sage'], 'description': 'Strikes with electrical energy.',
        'incantation': 'Egribegah', 'duration': 'turn', 'multi_target': True},
    5: {'name': 'Cure Disease', 'mana_cost': 10, 'type': 'cure', 'min_level': 2,
        'classes': ['Cleric', 'Paladin'], 'description': 'Cures diseases and afflictions.',
        'incantation': 'Razzxixx', 'duration': 'turn'},
    6: {'name': 'Shield', 'mana_cost': 8, 'type': 'buff', 'min_level': 2,
        'classes': ['Magician', 'Cleric', 'Sage'], 'description': 'Increases defense temporarily.',
        'incantation': 'Mokkoshu', 'duration': 'fight'},
    7: {'name': 'Poison Cloud', 'mana_cost': 12, 'type': 'attack', 'min_level': 3,
        'classes': ['Alchemist'], 'description': 'Creates a cloud of noxious poison.',
        'incantation': 'Gonngexha', 'duration': 'fight'},
    8: {'name': 'Greater Heal', 'mana_cost': 20, 'type': 'heal', 'min_level': 5,
        'classes': ['Cleric', 'Sage'], 'description': 'Restores a large amount of health.',
        'incantation': 'Garghamangan', 'duration': 'turn'},
    9: {'name': 'Ice Storm', 'mana_cost': 18, 'type': 'attack', 'min_level': 5,
        'classes': ['Magician'], 'description': 'Summons a storm of ice shards.',
        'incantation': 'Artizafisch', 'duration': 'turn'},
    10: {'name': 'Holy Smite', 'mana_cost': 15, 'type': 'attack', 'min_level': 4,
         'classes': ['Paladin', 'Cleric'], 'description': 'Smites with divine power.',
         'incantation': 'Kazarbah', 'duration': 'turn', 'multi_target': True},
    11: {'name': 'Acid Splash', 'mana_cost': 10, 'type': 'attack', 'min_level': 2,
         'classes': ['Alchemist'], 'description': 'Throws corrosive acid.',
         'incantation': 'Sheshnaxe', 'duration': 'turn'},
    12: {'name': 'Resurrection', 'mana_cost': 50, 'type': 'heal', 'min_level': 10,
         'classes': ['Cleric', 'Sage'], 'description': 'Brings back from the brink of death.',
         'incantation': 'Sondocesah', 'duration': 'turn'},
    # Mid-level spells (levels 8-20)
    13: {'name': 'Chain Lightning', 'mana_cost': 25, 'type': 'attack', 'min_level': 8,
         'classes': ['Magician', 'Sage'], 'description': 'Lightning arcs between multiple foes.',
         'incantation': 'Tenibma', 'duration': 'turn', 'multi_target': True},
    14: {'name': 'Flame Wall', 'mana_cost': 22, 'type': 'attack', 'min_level': 10,
         'classes': ['Magician'], 'description': 'Conjures a wall of searing flames.',
         'incantation': 'Viloshmazza', 'duration': 'turn'},
    15: {'name': 'Divine Shield', 'mana_cost': 20, 'type': 'buff', 'min_level': 8,
         'classes': ['Cleric', 'Paladin'], 'description': 'Surrounds you with divine protection.',
         'incantation': 'Xamientivah', 'duration': 'fight'},
    16: {'name': 'Toxic Plague', 'mana_cost': 18, 'type': 'attack', 'min_level': 7,
         'classes': ['Alchemist'], 'description': 'Unleashes a virulent disease upon your foe.',
         'incantation': 'Meshushattagut', 'duration': 'turn'},
    17: {'name': 'Blizzard', 'mana_cost': 30, 'type': 'attack', 'min_level': 12,
         'classes': ['Magician', 'Sage'], 'description': 'Summons a devastating blizzard.',
         'incantation': 'Ynoskattarb', 'duration': 'turn'},
    18: {'name': 'Smite Evil', 'mana_cost': 25, 'type': 'attack', 'min_level': 12,
         'classes': ['Paladin', 'Cleric'], 'description': 'Channels righteous fury against evil.',
         'incantation': 'Bokajinnah', 'duration': 'turn'},
    19: {'name': 'Mass Heal', 'mana_cost': 35, 'type': 'heal', 'min_level': 15,
         'classes': ['Cleric', 'Sage'], 'description': 'Heals all wounds with a burst of light.',
         'incantation': 'Swiillixtavh', 'duration': 'turn'},
    20: {'name': 'Meteor Storm', 'mana_cost': 40, 'type': 'attack', 'min_level': 18,
         'classes': ['Magician'], 'description': 'Calls down a rain of meteors.',
         'incantation': 'Aivannaxievh', 'duration': 'turn'},
    # --- Freeze/Stun spells (from original) ---
    21: {'name': 'Sleep', 'mana_cost': 30, 'type': 'freeze', 'min_level': 10,
         'classes': ['Magician'], 'description': 'Puts the enemy into a deep sleep.',
         'incantation': 'Sabdrak', 'duration': 'fight', 'freeze_turns': 2},
    22: {'name': 'Baptize Monster', 'mana_cost': 30, 'type': 'freeze', 'min_level': 10,
         'classes': ['Cleric'], 'description': 'The enemy freezes under holy influence.',
         'incantation': 'Ushmanikixz', 'duration': 'fight', 'freeze_turns': 2},
    23: {'name': 'Web', 'mana_cost': 40, 'type': 'freeze', 'min_level': 15,
         'classes': ['Magician'], 'description': 'Immobilizes the enemy in sticky webs.',
         'incantation': 'Sekaramata', 'duration': 'turn', 'freeze_turns': 1},
    24: {'name': 'Fear', 'mana_cost': 70, 'type': 'freeze', 'min_level': 30,
         'classes': ['Magician'], 'description': 'The enemy is fear stricken and cannot move.',
         'incantation': 'Urpashke', 'duration': 'fight', 'freeze_turns': 3},
    25: {'name': 'Freeze', 'mana_cost': 30, 'type': 'freeze', 'min_level': 10,
         'classes': ['Sage'], 'description': 'The enemy becomes an ice block!',
         'incantation': 'Artizafisch', 'duration': 'turn', 'freeze_turns': 1},
    # --- Sage utility spells (from original) ---
    26: {'name': 'Duplicate', 'mana_cost': 40, 'type': 'buff', 'min_level': 15,
         'classes': ['Sage'], 'description': 'Creates a hologram duplicate that attacks alongside you.',
         'incantation': 'Ishusabbhes', 'duration': 'fight', 'hp_cost': 25},
    27: {'name': 'Giant', 'mana_cost': 80, 'type': 'buff', 'min_level': 40,
         'classes': ['Sage'], 'description': 'Metamorphosis into a giant! +25 damage for whole fight.',
         'incantation': 'Setuminahx', 'duration': 'fight'},
    28: {'name': 'Steal', 'mana_cost': 90, 'type': 'attack', 'min_level': 50,
         'classes': ['Sage'], 'description': 'Steals a random amount of enemy gold.',
         'incantation': 'Algesmoxhu', 'duration': 'turn'},
    # --- Cleric special spells (from original) ---
    29: {'name': 'Summon Angel', 'mana_cost': 80, 'type': 'buff', 'min_level': 40,
         'classes': ['Cleric'], 'description': 'Summons an angel that deals 100 damage per round.',
         'incantation': 'Bokajinnah', 'duration': 'fight'},
    30: {'name': 'Divination', 'mana_cost': 110, 'type': 'buff', 'min_level': 70,
         'classes': ['Cleric'], 'description': 'Massive protection boost and increases goodness.',
         'incantation': 'Swiillixtavh', 'duration': 'fight'},
    # --- High-level spells ---
    31: {'name': 'Disintegrate', 'mana_cost': 50, 'type': 'attack', 'min_level': 20,
         'classes': ['Magician', 'Sage'], 'description': 'Reduces matter to dust.',
         'incantation': 'Xoxxammeuh', 'duration': 'turn'},
    32: {'name': 'Wrath of God', 'mana_cost': 45, 'type': 'attack', 'min_level': 22,
         'classes': ['Cleric', 'Paladin'], 'description': 'Calls down divine wrath upon the wicked.',
         'incantation': 'Gnisuremvenodh', 'duration': 'turn'},
    33: {'name': 'Death Cloud', 'mana_cost': 35, 'type': 'attack', 'min_level': 20,
         'classes': ['Alchemist'], 'description': 'A cloud of pure necrotic toxin.',
         'incantation': 'Reprusu', 'duration': 'turn'},
    34: {'name': 'Arcane Shield', 'mana_cost': 30, 'type': 'buff', 'min_level': 18,
         'classes': ['Magician', 'Sage', 'Cleric'], 'description': 'An impenetrable barrier of arcane energy.',
         'incantation': 'Noitarudamin', 'duration': 'fight'},
    35: {'name': 'Power Word Kill', 'mana_cost': 60, 'type': 'attack', 'min_level': 25,
         'classes': ['Magician'], 'description': 'A single word that can slay the weak.',
         'incantation': 'Gnisuremvenodh', 'duration': 'turn'},
    36: {'name': 'Divine Resurrection', 'mana_cost': 80, 'type': 'heal', 'min_level': 25,
         'classes': ['Cleric', 'Sage'], 'description': 'Fully restores life and vigor.',
         'incantation': 'Umbarakahstahx', 'duration': 'turn'},
    37: {'name': 'Philosopher\'s Fire', 'mana_cost': 45, 'type': 'attack', 'min_level': 25,
         'classes': ['Alchemist'], 'description': 'Alchemical fire that burns the soul.',
         'incantation': 'Attigribinnizsch', 'duration': 'turn'},
    38: {'name': 'Time Stop', 'mana_cost': 70, 'type': 'freeze', 'min_level': 30,
         'classes': ['Magician', 'Sage'], 'description': 'Briefly halts the flow of time.',
         'incantation': 'Mattravidduzzievh', 'duration': 'turn', 'freeze_turns': 2},
    39: {'name': 'Judgement', 'mana_cost': 65, 'type': 'attack', 'min_level': 30,
         'classes': ['Paladin', 'Cleric'], 'description': 'Passes divine judgement upon your foe.',
         'incantation': 'Edujnomed', 'duration': 'turn'},
    40: {'name': 'Hellfire', 'mana_cost': 75, 'type': 'attack', 'min_level': 35,
         'classes': ['Magician'], 'description': 'Summons flames from the abyss itself.',
         'incantation': 'Zimmokoth', 'duration': 'turn'},
    # Epic spells (levels 40-60)
    41: {'name': 'Armageddon', 'mana_cost': 100, 'type': 'attack', 'min_level': 40,
         'classes': ['Magician', 'Sage'], 'description': 'Unleashes catastrophic destruction.',
         'incantation': 'Aivannaxievh', 'duration': 'turn', 'multi_target': True},
    42: {'name': 'Miracle', 'mana_cost': 100, 'type': 'heal', 'min_level': 40,
         'classes': ['Cleric', 'Sage'], 'description': 'A true miracle of healing.',
         'incantation': 'Sondocesah', 'duration': 'turn'},
    43: {'name': 'Elixir of Annihilation', 'mana_cost': 80, 'type': 'attack', 'min_level': 40,
         'classes': ['Alchemist'], 'description': 'The ultimate alchemical weapon.',
         'incantation': 'Sheshnaxe', 'duration': 'turn'},
    44: {'name': 'Celestial Wrath', 'mana_cost': 90, 'type': 'attack', 'min_level': 45,
         'classes': ['Paladin', 'Cleric'], 'description': 'Channels the fury of the heavens.',
         'incantation': 'Kazarbah', 'duration': 'turn', 'multi_target': True},
    45: {'name': 'Void Bolt', 'mana_cost': 85, 'type': 'attack', 'min_level': 50,
         'classes': ['Magician', 'Sage'], 'description': 'A bolt of pure nothingness.',
         'incantation': 'Noitarudamin', 'duration': 'turn'},
    46: {'name': 'Avatar', 'mana_cost': 120, 'type': 'buff', 'min_level': 50,
         'classes': ['Cleric', 'Paladin'], 'description': 'Temporarily becomes an avatar of divine power.',
         'incantation': 'Umbarakahstahx', 'duration': 'fight'},
    47: {'name': 'Transmutation', 'mana_cost': 90, 'type': 'attack', 'min_level': 50,
         'classes': ['Alchemist'], 'description': 'Transmutes your enemy\'s flesh to lead.',
         'incantation': 'Algesmoxhu', 'duration': 'turn'},
    # Legendary spells (levels 60-80)
    48: {'name': 'Apocalypse', 'mana_cost': 150, 'type': 'attack', 'min_level': 60,
         'classes': ['Magician'], 'description': 'The ultimate destructive force.',
         'incantation': 'Mattravidduzzievh', 'duration': 'turn', 'multi_target': True},
    49: {'name': 'Divine Intervention', 'mana_cost': 150, 'type': 'heal', 'min_level': 60,
         'classes': ['Cleric', 'Sage'], 'description': 'Direct intervention from the gods.',
         'incantation': 'Swiillixtavh', 'duration': 'turn'},
    50: {'name': 'Holy Avenger', 'mana_cost': 130, 'type': 'attack', 'min_level': 65,
         'classes': ['Paladin'], 'description': 'Becomes the instrument of divine vengeance.',
         'incantation': 'Bokajinnah', 'duration': 'turn'},
    51: {'name': 'Wish', 'mana_cost': 200, 'type': 'buff', 'min_level': 70,
         'classes': ['Magician', 'Sage'], 'description': 'Bends reality to your will.',
         'incantation': 'Viloshmazza', 'duration': 'fight'},
    52: {'name': 'Omega Toxin', 'mana_cost': 140, 'type': 'attack', 'min_level': 70,
         'classes': ['Alchemist'], 'description': 'A poison that unravels life itself.',
         'incantation': 'Gonngexha', 'duration': 'turn'},
    # Mythic spells (levels 80-100)
    53: {'name': 'Cataclysm', 'mana_cost': 250, 'type': 'attack', 'min_level': 80,
         'classes': ['Magician', 'Sage'], 'description': 'Reshapes the world with raw power.',
         'incantation': 'Gnisuremvenodh', 'duration': 'turn', 'multi_target': True},
    54: {'name': 'Genesis', 'mana_cost': 250, 'type': 'heal', 'min_level': 80,
         'classes': ['Cleric', 'Sage'], 'description': 'Creates life from nothing.',
         'incantation': 'Abrazak', 'duration': 'turn'},
    55: {'name': 'God Slayer', 'mana_cost': 300, 'type': 'attack', 'min_level': 90,
         'classes': ['Magician'], 'description': 'A spell capable of slaying gods.',
         'incantation': 'Edujnomed', 'duration': 'turn'},
    56: {'name': 'Eternal Light', 'mana_cost': 300, 'type': 'attack', 'min_level': 90,
         'classes': ['Paladin', 'Cleric'], 'description': 'Banishes all darkness forever.',
         'incantation': 'Xamientivah', 'duration': 'turn'},
    57: {'name': 'Panacea', 'mana_cost': 200, 'type': 'heal', 'min_level': 85,
         'classes': ['Alchemist', 'Sage'], 'description': 'The universal cure for all ailments.',
         'incantation': 'Razzxixx', 'duration': 'turn'},
    58: {'name': 'Ragnarok', 'mana_cost': 500, 'type': 'attack', 'min_level': 100,
         'classes': ['Magician', 'Sage'], 'description': 'The end of all things.',
         'incantation': 'Mattravidduzzievh', 'duration': 'turn', 'multi_target': True},
    # Sage Death Kiss (from original)
    59: {'name': 'Death Kiss', 'mana_cost': 120, 'type': 'attack', 'min_level': 80,
         'classes': ['Sage'], 'description': 'An undead spirit delivers a fatal kiss.',
         'incantation': 'Edujnomed', 'duration': 'turn'},
    # Sage Escape (freeze variant)
    60: {'name': 'Escape', 'mana_cost': 70, 'type': 'freeze', 'min_level': 30,
         'classes': ['Sage'], 'description': 'Enemy is frozen in place while you reposition.',
         'incantation': 'Reprusu', 'duration': 'fight', 'freeze_turns': 3},
    # Sage Energy Drain (from original)
    61: {'name': 'Energy Drain', 'mana_cost': 100, 'type': 'attack', 'min_level': 60,
         'classes': ['Sage'], 'description': 'Drains the life energy from your foe.',
         'incantation': 'Noitarudamin', 'duration': 'turn'},
    # Sage Summon Demon (from original)
    62: {'name': 'Summon Demon', 'mana_cost': 110, 'type': 'buff', 'min_level': 70,
         'classes': ['Sage', 'Magician'], 'description': 'A servant demon that fights alongside you.',
         'incantation': 'Attigribinnizsch', 'duration': 'fight'},
    # Cleric Invisibility (from original)
    63: {'name': 'Invisibility', 'mana_cost': 70, 'type': 'buff', 'min_level': 30,
         'classes': ['Cleric'], 'description': 'Become invisible, gaining massive protection.',
         'incantation': 'Xamientivah', 'duration': 'fight'},
    # Cleric Disease (from original)
    64: {'name': 'Disease', 'mana_cost': 50, 'type': 'attack', 'min_level': 20,
         'classes': ['Cleric'], 'description': 'Inflicts a random disease upon the enemy.',
         'incantation': 'Meshushattagut', 'duration': 'turn'},
    # Cleric Gods Finger (from original)
    65: {'name': 'Gods Finger', 'mana_cost': 120, 'type': 'attack', 'min_level': 80,
         'classes': ['Cleric'], 'description': 'An energy blast from the divine finger of God.',
         'incantation': 'Umbarakahstahx', 'duration': 'turn'},
    # Magician Prismatic Cage (from original)
    66: {'name': 'Prismatic Cage', 'mana_cost': 90, 'type': 'buff', 'min_level': 50,
         'classes': ['Magician'], 'description': 'A shimmering cage of light protects you.',
         'incantation': 'Ynoskattarb', 'duration': 'fight'},
    # Magician Pillar of Fire (from original)
    67: {'name': 'Pillar of Fire', 'mana_cost': 100, 'type': 'attack', 'min_level': 60,
         'classes': ['Magician'], 'description': 'A massive pillar of flame erupts beneath the enemy.',
         'incantation': 'Aivannaxievh', 'duration': 'turn'},
    # Sage Fog of War (from original)
    68: {'name': 'Fog of War', 'mana_cost': 10, 'type': 'buff', 'min_level': 1,
         'classes': ['Sage'], 'description': 'Only you are visible in the fog.',
         'incantation': 'Umannaghra', 'duration': 'fight'},
    # Sage Roast (from original)
    69: {'name': 'Roast', 'mana_cost': 50, 'type': 'attack', 'min_level': 20,
         'classes': ['Sage'], 'description': 'Fire damage that pierces armor.',
         'incantation': 'Sheshnaxe', 'duration': 'turn'},
    # Sage Hit Self (from original - mind control)
    70: {'name': 'Hit Self', 'mana_cost': 60, 'type': 'attack', 'min_level': 25,
         'classes': ['Sage'], 'description': 'Mind control causes the enemy to strike itself.',
         'incantation': 'Xoxxammeuh', 'duration': 'turn'},
    # Cleric Call Lightning (from original)
    71: {'name': 'Call Lightning', 'mana_cost': 90, 'type': 'attack', 'min_level': 50,
         'classes': ['Cleric'], 'description': 'Lightning called from the heavens.',
         'incantation': 'Tenibma', 'duration': 'turn'},
    # Cleric Armor (from original - protection buff)
    72: {'name': 'Armor', 'mana_cost': 20, 'type': 'buff', 'min_level': 5,
         'classes': ['Cleric'], 'description': 'Invisible armor grants +5 protection.',
         'incantation': 'Razzxixx', 'duration': 'fight'},
    # Magician Power Hat (from original)
    73: {'name': 'Power Hat', 'mana_cost': 50, 'type': 'heal', 'min_level': 20,
         'classes': ['Magician'], 'description': 'Restores HP and grants protection.',
         'incantation': 'Viloshmazza', 'duration': 'fight'},
    # --- Necromancer spells ---
    74: {'name': 'Drain Life', 'mana_cost': 8, 'type': 'attack', 'min_level': 1,
         'classes': ['Necromancer'], 'description': 'Siphons the life force from your enemy.',
         'incantation': 'Zazzaknah', 'duration': 'turn'},
    75: {'name': 'Raise Dead', 'mana_cost': 15, 'type': 'buff', 'min_level': 3,
         'classes': ['Necromancer'], 'description': 'Raises a corpse to fight alongside you.',
         'incantation': 'Ishusabbhes', 'duration': 'fight'},
    76: {'name': 'Bone Spear', 'mana_cost': 12, 'type': 'attack', 'min_level': 4,
         'classes': ['Necromancer'], 'description': 'Hurls a shard of sharpened bone.',
         'incantation': 'Gonngexha', 'duration': 'turn'},
    77: {'name': 'Corpse Explosion', 'mana_cost': 22, 'type': 'attack', 'min_level': 8,
         'classes': ['Necromancer'], 'description': 'Detonates the fallen dead with terrible force.',
         'incantation': 'Sheshnaxe', 'duration': 'turn'},
    78: {'name': 'Soul Rend', 'mana_cost': 35, 'type': 'attack', 'min_level': 15,
         'classes': ['Necromancer'], 'description': 'Tears at the very soul of your foe.',
         'incantation': 'Xoxxammeuh', 'duration': 'turn'},
    79: {'name': 'Army of the Dead', 'mana_cost': 60, 'type': 'buff', 'min_level': 25,
         'classes': ['Necromancer'], 'description': 'Summons a legion of undead warriors.',
         'incantation': 'Attigribinnizsch', 'duration': 'fight'},
    80: {'name': 'Plague of Undeath', 'mana_cost': 90, 'type': 'attack', 'min_level': 40,
         'classes': ['Necromancer'], 'description': 'Spreads a necrotic plague that devours the living.',
         'incantation': 'Meshushattagut', 'duration': 'turn'},
    81: {'name': 'Death Pact', 'mana_cost': 150, 'type': 'attack', 'min_level': 60,
         'classes': ['Necromancer'], 'description': 'Forges a dark bargain with death itself.',
         'incantation': 'Edujnomed', 'duration': 'turn'},
    82: {'name': 'Lichdom', 'mana_cost': 300, 'type': 'buff', 'min_level': 85,
         'classes': ['Necromancer'], 'description': 'Transforms you into an undying lich.',
         'incantation': 'Mattravidduzzievh', 'duration': 'fight'},
    # --- Monk spells ---
    83: {'name': 'Inner Focus', 'mana_cost': 6, 'type': 'buff', 'min_level': 1,
         'classes': ['Monk'], 'description': 'Centers your chi to sharpen reflexes.',
         'incantation': 'Umannaghra', 'duration': 'fight'},
    84: {'name': 'Palm Strike', 'mana_cost': 10, 'type': 'attack', 'min_level': 2,
         'classes': ['Monk'], 'description': 'Channels ki into a devastating open-palm blow.',
         'incantation': 'Zazzaknah', 'duration': 'turn'},
    85: {'name': 'Iron Skin', 'mana_cost': 14, 'type': 'buff', 'min_level': 5,
         'classes': ['Monk'], 'description': 'Hardens your body against physical harm.',
         'incantation': 'Mokkoshu', 'duration': 'fight'},
    86: {'name': 'Flurry of Blows', 'mana_cost': 20, 'type': 'attack', 'min_level': 8,
         'classes': ['Monk'], 'description': 'A rapid barrage of fists and kicks.',
         'incantation': 'Sabdrak', 'duration': 'turn'},
    87: {'name': 'Quivering Palm', 'mana_cost': 35, 'type': 'attack', 'min_level': 15,
         'classes': ['Monk'], 'description': 'Sets up lethal vibrations within the target.',
         'incantation': 'Sekaramata', 'duration': 'turn'},
    88: {'name': 'Diamond Soul', 'mana_cost': 50, 'type': 'buff', 'min_level': 25,
         'classes': ['Monk'], 'description': 'Your spirit becomes as unyielding as diamond.',
         'incantation': 'Artizafisch', 'duration': 'fight'},
    89: {'name': 'Astral Projection', 'mana_cost': 80, 'type': 'buff', 'min_level': 40,
         'classes': ['Monk'], 'description': 'Projects your consciousness beyond the mortal plane.',
         'incantation': 'Ishusabbhes', 'duration': 'fight'},
    90: {'name': 'Void Fist', 'mana_cost': 120, 'type': 'attack', 'min_level': 60,
         'classes': ['Monk'], 'description': 'A punch that disrupts the fabric of reality.',
         'incantation': 'Noitarudamin', 'duration': 'turn'},
    91: {'name': 'Transcendence', 'mana_cost': 250, 'type': 'buff', 'min_level': 85,
         'classes': ['Monk'], 'description': 'Ascend beyond mortal limitations entirely.',
         'incantation': 'Mattravidduzzievh', 'duration': 'fight'},
    # --- Witch Hunter spells (innate abilities, not true magic) ---
    92: {'name': 'Silver Bolt', 'mana_cost': 5, 'type': 'attack', 'min_level': 1,
         'classes': ['Witch Hunter'], 'description': 'Fires a bolt infused with pure silver.',
         'incantation': 'Zazzaknah', 'duration': 'turn'},
    93: {'name': 'Purging Flame', 'mana_cost': 12, 'type': 'attack', 'min_level': 3,
         'classes': ['Witch Hunter'], 'description': 'Sacred fire that burns the unholy.',
         'incantation': 'Zimmokoth', 'duration': 'turn'},
    94: {'name': 'Hex Ward', 'mana_cost': 10, 'type': 'buff', 'min_level': 5,
         'classes': ['Witch Hunter'], 'description': 'Wards against curses and dark magic.',
         'incantation': 'Mokkoshu', 'duration': 'fight'},
    95: {'name': 'Sigil of Binding', 'mana_cost': 18, 'type': 'buff', 'min_level': 10,
         'classes': ['Witch Hunter'], 'description': 'Inscribes a sigil that weakens magical foes.',
         'incantation': 'Sekaramata', 'duration': 'fight'},
    96: {'name': 'Inquisitor\'s Brand', 'mana_cost': 30, 'type': 'attack', 'min_level': 18,
         'classes': ['Witch Hunter'], 'description': 'Brands the enemy with a mark of judgement.',
         'incantation': 'Kazarbah', 'duration': 'turn'},
    97: {'name': 'Banishment', 'mana_cost': 50, 'type': 'attack', 'min_level': 30,
         'classes': ['Witch Hunter'], 'description': 'Attempts to banish a creature to another plane.',
         'incantation': 'Reprusu', 'duration': 'turn'},
    98: {'name': 'Witch Pyre', 'mana_cost': 90, 'type': 'attack', 'min_level': 50,
         'classes': ['Witch Hunter'], 'description': 'Engulfs the target in purifying flame.',
         'incantation': 'Aivannaxievh', 'duration': 'turn'},
    99: {'name': 'Final Judgement', 'mana_cost': 200, 'type': 'attack', 'min_level': 80,
         'classes': ['Witch Hunter'], 'description': 'Condemns the wicked with absolute authority.',
         'incantation': 'Umbarakahstahx', 'duration': 'turn'},
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
    race = db.Column(db.String(15), nullable=False)
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
    intimacy_acts = db.Column(db.Integer, default=5)  # daily intimate interactions
    beauty_nest_visits = db.Column(db.Integer, default=3)  # daily visits to The Beauty Nest

    # Selene (LORD-inspired Violet character)
    selene_charm = db.Column(db.Integer, default=0)  # relationship level with Selene (0-100)
    selene_flirted_today = db.Column(db.Boolean, default=False)  # once-per-day flirt limit
    selene_married = db.Column(db.Boolean, default=False)  # married to Selene

    # Dungeon
    dungeon_level = db.Column(db.Integer, default=1)  # current dungeon level

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
    has_smallpox = db.Column(db.Boolean, default=False)
    has_measles = db.Column(db.Boolean, default=False)
    has_leprosy = db.Column(db.Boolean, default=False)
    is_haunted = db.Column(db.Integer, default=0)  # haunt counter (demon haunting from Groggo's)

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
    tax_relief = db.Column(db.Boolean, default=False)  # exempt from royal tax
    town_control = db.Column(db.Boolean, default=False)  # turf flag
    team_fights = db.Column(db.Integer, default=1)  # gang war attempts per day
    quests_completed = db.Column(db.Integer, default=0)
    quests_failed = db.Column(db.Integer, default=0)

    # Bank guard
    is_bank_guard = db.Column(db.Boolean, default=False)  # employed as bank guard
    bank_wage = db.Column(db.Integer, default=0)  # accumulated salary from bank

    # Orb's Bar
    drinks_remaining = db.Column(db.Integer, default=3)  # drinks per day at Orb's

    # Door guards (protect player when offline at inn)
    door_guard_id = db.Column(db.Integer, db.ForeignKey('door_guards.id'), nullable=True)
    door_guard_count = db.Column(db.Integer, default=0)  # number of door guards hired

    # Prison escape
    prison_days = db.Column(db.Integer, default=0)  # days left in prison
    escape_attempts = db.Column(db.Integer, default=0)  # escape attempts used today

    # Player Market
    market_listings = db.Column(db.Integer, default=0)  # active listing count

    # Wrestling
    wrestling_wins = db.Column(db.Integer, default=0)
    wrestling_losses = db.Column(db.Integer, default=0)
    wrestling_matches = db.Column(db.Integer, default=2)  # daily limit

    # Bear Taming (Uman Cave)
    has_tamed_bear = db.Column(db.Boolean, default=False)
    bear_name = db.Column(db.String(30), default='')
    bear_strength = db.Column(db.Integer, default=0)  # bonus attack from bear

    # Bard performances
    performances_remaining = db.Column(db.Integer, default=3)  # daily bard performance limit

    # Horse/Mount system (LORD-inspired)
    has_horse = db.Column(db.Boolean, default=False)
    horse_name = db.Column(db.String(30), default='')
    horse_type = db.Column(db.String(30), default='')  # e.g. 'White Stallion', 'Black Mare'
    horse_bonus_fights = db.Column(db.Integer, default=0)  # extra daily dungeon fights from mount

    # Fairy encounter tracking
    fairy_dust = db.Column(db.Integer, default=0)  # accumulated fairy dust (currency/blessing)

    # Dark/Good deed quotas
    dark_deeds_remaining = db.Column(db.Integer, default=3)  # daily dark deed limit
    good_deeds_remaining = db.Column(db.Integer, default=3)  # daily good deed limit

    # Gym / training
    gym_sessions = db.Column(db.Integer, default=4)  # daily gym sessions
    massage_visits = db.Column(db.Integer, default=3)  # daily massage visits
    barrel_lift_record = db.Column(db.Integer, default=0)  # best barrel lift count
    prayers_remaining = db.Column(db.Integer, default=3)  # daily prayer limit

    # Close combat skills (JSON string: {"Tackle": 5, "Kick": 3, ...})
    close_combat_skills = db.Column(db.Text, default='{}')

    # Alchemist poison (current poison level: 0=none, 1=Light, 2=Medium, 3=Strong, 4=Deadly)
    poison_level = db.Column(db.Integer, default=0)

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
    equipped_weapon2 = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)  # left hand
    equipped_shield = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_head = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_body = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_arms = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_hands = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_legs = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_feet = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_waist = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_neck = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_neck2 = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)  # second necklace
    equipped_face = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_around_body = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_finger1 = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    equipped_finger2 = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)

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
        """Calculate total attack power including equipment and bear companion."""
        base = self.strength + self.weapon_power + self.bear_strength
        return max(1, base)

    def get_total_defense(self):
        """Calculate total defense including equipment."""
        base = self.defence + self.armor_power
        return max(1, base)

    def alignment_string(self):
        if self.chivalry > self.darkness:
            c = self.chivalry
            if c >= 100000:
                return "God's Device"
            elif c >= 55001:
                return 'Angel Heart'
            elif c >= 27001:
                return 'Extremely Virtuous'
            elif c >= 15001:
                return 'Extremely Kind'
            elif c >= 9001:
                return 'Good-doer'
            elif c >= 5001:
                return 'Good'
            elif c >= 1001:
                return 'Kind'
            elif c >= 101:
                return 'Warm-hearted'
            return 'Happy'
        elif self.darkness > self.chivalry:
            d = self.darkness
            if d >= 100000:
                return "Devil's Right Hand"
            elif d >= 55001:
                return "Satan's Child"
            elif d >= 27001:
                return 'Extremely Evil'
            elif d >= 15001:
                return 'Black Soul'
            elif d >= 9001:
                return 'Evil'
            elif d >= 5001:
                return 'Sadist'
            elif d >= 1001:
                return 'Brutal'
            elif d >= 101:
                return 'Vicious'
            return 'Mean'
        return 'Neutral'

    def battle_master_rank(self):
        """PvP reputation rank based on total kills + defeats."""
        total = self.player_kills + self.player_defeats
        rank = 'Wimp'
        for threshold, title in BATTLE_MASTER_RANKS:
            if total >= threshold:
                rank = title
        return rank

    def get_combat_skills(self):
        """Return close combat skill dict."""
        import json
        try:
            return json.loads(self.close_combat_skills or '{}')
        except (json.JSONDecodeError, TypeError):
            return {}

    def set_combat_skill(self, move, level):
        """Set a close combat move skill level."""
        import json
        skills = self.get_combat_skills()
        skills[move] = min(level, 17)
        self.close_combat_skills = json.dumps(skills)

    def get_disease_damage(self):
        """Calculate per-battle disease damage from all active diseases."""
        dmg = 0
        if self.has_plague:
            dmg += DISEASES['plague']['damage']
        if self.has_smallpox:
            dmg += DISEASES['smallpox']['damage']
        if self.has_measles:
            dmg += DISEASES['measles']['damage']
        if self.has_leprosy:
            dmg += DISEASES['leprosy']['damage']
        return dmg

    def active_diseases(self):
        """Return list of active disease names."""
        diseases = []
        if self.has_plague:
            diseases.append('Plague')
        if self.has_smallpox:
            diseases.append('Smallpox')
        if self.has_measles:
            diseases.append('Measles')
        if self.has_leprosy:
            diseases.append('Leprosy')
        return diseases

    def can_level_up(self):
        next_level = self.level + 1
        if next_level > 100:
            return False
        return self.experience >= LEVEL_XP.get(next_level, float('inf'))

    def xp_for_next_level(self):
        next_level = self.level + 1
        return LEVEL_XP.get(next_level, float('inf'))

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
        """Recalculate weapon and armor power from equipped items (includes dual-wield)."""
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
    max_level = db.Column(db.Integer, default=100)
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
        """Map item_type to equipment slot name.

        For 'Fingers' items, returns 'finger1' as the default slot.
        The equip logic handles placing rings in finger2 when finger1
        is occupied. Same for Neck -> neck/neck2 and Weapon -> weapon/weapon2.
        """
        slot_map = {
            'Weapon': 'weapon', 'Shield': 'shield', 'Head': 'head',
            'Body': 'body', 'Arms': 'arms', 'Hands': 'hands',
            'Legs': 'legs', 'Feet': 'feet', 'Waist': 'waist',
            'Neck': 'neck', 'Face': 'face', 'Around Body': 'around_body',
            'Fingers': 'finger1',
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
    mana = db.Column(db.Integer, default=0)
    max_mana = db.Column(db.Integer, default=0)
    spells_known = db.Column(db.String(30), default='')  # comma-separated monster spell IDs
    aggression = db.Column(db.Integer, default=1)  # 0-3
    dungeon_area = db.Column(db.String(20), default='dungeon')  # dungeon, death_maze, ice_caves

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


class Drink(db.Model):
    """Custom drinks created at Orb's Bar."""
    __tablename__ = 'drinks'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    creator_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    creator_name = db.Column(db.String(50), default='')
    comment = db.Column(db.String(70), default='')
    times_ordered = db.Column(db.Integer, default=0)
    last_customer = db.Column(db.String(50), default='')
    secret = db.Column(db.Boolean, default=False)  # recipe hidden?
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    # Ingredient amounts (0-100 each, total must equal 100)
    bat_brain = db.Column(db.Integer, default=0)
    honeydew = db.Column(db.Integer, default=0)
    orange_juice = db.Column(db.Integer, default=0)
    tabasco = db.Column(db.Integer, default=0)
    ale = db.Column(db.Integer, default=0)
    hedgehog_saliva = db.Column(db.Integer, default=0)
    water = db.Column(db.Integer, default=0)
    horse_blood = db.Column(db.Integer, default=0)
    bobs_bomber = db.Column(db.Integer, default=0)
    troll_rum = db.Column(db.Integer, default=0)
    elf_water = db.Column(db.Integer, default=0)
    kicking_squaw = db.Column(db.Integer, default=0)
    milk = db.Column(db.Integer, default=0)
    wine_vinegar = db.Column(db.Integer, default=0)
    snake_spit = db.Column(db.Integer, default=0)
    duck_dropping = db.Column(db.Integer, default=0)
    chilipeppar = db.Column(db.Integer, default=0)

    creator = db.relationship('Player', backref='created_drinks', foreign_keys=[creator_id])

    def get_ingredients(self):
        """Return dict of ingredient_name: amount for non-zero ingredients."""
        return {name: getattr(self, attr) for attr, name in DRINK_INGREDIENTS
                if getattr(self, attr) > 0}

    def total_amount(self):
        return sum(getattr(self, attr) for attr, _ in DRINK_INGREDIENTS)


class DoorGuard(db.Model):
    """Types of guards available to protect player rooms at the inn."""
    __tablename__ = 'door_guards'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    cost = db.Column(db.Integer, nullable=False)  # cost per guard
    hps = db.Column(db.Integer, nullable=False)  # hitpoints
    attack = db.Column(db.Integer, nullable=False)  # base attack
    armor = db.Column(db.Integer, default=0)  # base armor/defense
    allow_multiple = db.Column(db.Boolean, default=False)  # can hire more than one?
    description = db.Column(db.String(200), default='')


class MoatCreature(db.Model):
    """Types of creatures available for moat defense."""
    __tablename__ = 'moat_creatures'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    cost = db.Column(db.Integer, nullable=False)  # cost per creature
    hps = db.Column(db.Integer, nullable=False)  # hitpoints
    attack = db.Column(db.Integer, nullable=False)  # base attack
    armor = db.Column(db.Integer, default=0)  # base armor/defense
    description = db.Column(db.String(200), default='')


class RoyalGuard(db.Model):
    """Player/NPC bodyguards hired by the king."""
    __tablename__ = 'royal_guards'

    id = db.Column(db.Integer, primary_key=True)
    king_record_id = db.Column(db.Integer, db.ForeignKey('king_records.id'), nullable=False)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    salary = db.Column(db.Integer, default=0)  # daily pay from treasury
    hired_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    king_record = db.relationship('KingRecord', backref='royal_guards')
    player = db.relationship('Player', backref='guard_duty')


class KingRecord(db.Model):
    """Tracks the current and historical monarchs."""
    __tablename__ = 'king_records'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    crowned_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    dethroned_at = db.Column(db.DateTime, nullable=True)
    is_current = db.Column(db.Boolean, default=True)
    moat_guards = db.Column(db.Integer, default=0)  # number of creatures in moat
    moat_creature_id = db.Column(db.Integer, db.ForeignKey('moat_creatures.id'), nullable=True)
    tax_rate = db.Column(db.Integer, default=5)  # percentage 0-5
    tax_alignment = db.Column(db.Integer, default=0)  # 0=all, 1=good only, 2=evil only
    treasury = db.Column(db.Integer, default=0)
    quests_left = db.Column(db.Integer, default=3)  # quests king can issue per day
    town_control_days = db.Column(db.Integer, default=0)  # days team has held town
    marry_actions = db.Column(db.Integer, default=5)  # matrimonial actions per day
    # Establishment open/close controls (king can shut down shops)
    shop_weapon = db.Column(db.Boolean, default=True)
    shop_armor = db.Column(db.Boolean, default=True)
    shop_magic = db.Column(db.Boolean, default=True)
    shop_healing = db.Column(db.Boolean, default=True)
    shop_general = db.Column(db.Boolean, default=True)
    shop_inn = db.Column(db.Boolean, default=True)
    shop_tavern = db.Column(db.Boolean, default=True)
    shop_beauty_nest = db.Column(db.Boolean, default=True)

    moat_creature = db.relationship('MoatCreature')
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
    rel_type = db.Column(db.String(20), nullable=False)  # 'married', 'ally', 'rival', 'lover', 'proposal'
    # Feeling levels: hate, enemy, anger, suspicious, normal, respect, trust, friendship, passion, love
    feeling_1to2 = db.Column(db.String(15), default='normal')  # player1's feeling toward player2
    feeling_2to1 = db.Column(db.String(15), default='normal')  # player2's feeling toward player1
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
    race = db.Column(db.String(15), default='Human')
    description = db.Column(db.String(100), default='')
    born_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))
    is_orphan = db.Column(db.Boolean, default=False)
    kidnapped_by_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=True)
    # Child location: 'home', 'orphanage', 'kidnapped'
    location = db.Column(db.String(15), default='home')
    # Custody tracking (which parent has access)
    mother_access = db.Column(db.Boolean, default=True)
    father_access = db.Column(db.Boolean, default=True)
    ransom_amount = db.Column(db.Integer, default=0)
    # Child health: 'normal', 'sick', 'dead'
    health = db.Column(db.String(10), default='normal')

    mother = db.relationship('Player', foreign_keys=[mother_id], backref='children_as_mother')
    father = db.relationship('Player', foreign_keys=[father_id], backref='children_as_father')
    kidnapped_by = db.relationship('Player', foreign_keys=[kidnapped_by_id])


class HomeChestItem(db.Model):
    """Items stored in a player's home chest."""
    __tablename__ = 'home_chest_items'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    stored_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    player = db.relationship('Player', backref='chest_items')
    item = db.relationship('Item')


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
    max_level = db.Column(db.Integer, default=100)
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
            if self.experience >= threshold:
                new_level = i + 1
        return new_level


class TeamRecord(db.Model):
    """Track records for team town control duration."""
    __tablename__ = 'team_records'

    id = db.Column(db.Integer, primary_key=True)
    team_name = db.Column(db.String(30), nullable=False)
    days_held = db.Column(db.Integer, default=0)
    recorded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))


class MarketListing(db.Model):
    """Player-to-player item marketplace listing."""
    __tablename__ = 'market_listings'

    id = db.Column(db.Integer, primary_key=True)
    seller_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    seller_name = db.Column(db.String(30), nullable=False)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    item_name = db.Column(db.String(70), nullable=False)
    price = db.Column(db.Integer, nullable=False)
    listed_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    seller = db.relationship('Player', foreign_keys=[seller_id])
    item = db.relationship('Item', foreign_keys=[item_id])


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


class InnChat(db.Model):
    """Chat messages at the inn."""
    __tablename__ = 'inn_chat'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    player_name = db.Column(db.String(30), nullable=False)
    message = db.Column(db.String(200), nullable=False)
    is_anonymous = db.Column(db.Boolean, default=False)
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    player = db.relationship('Player', backref='inn_chats')


class BarrelLiftRecord(db.Model):
    """Records for the gym barrel lifting competition."""
    __tablename__ = 'barrel_lift_records'

    id = db.Column(db.Integer, primary_key=True)
    player_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    player_name = db.Column(db.String(30), nullable=False)
    barrels = db.Column(db.Integer, nullable=False)
    recorded_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    player = db.relationship('Player', backref='barrel_records')


class EquipmentSwapOffer(db.Model):
    """Equipment swap offers between players."""
    __tablename__ = 'equipment_swaps'

    id = db.Column(db.Integer, primary_key=True)
    offerer_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('players.id'), nullable=False)
    offered_item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=False)
    wanted_item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)
    status = db.Column(db.String(10), default='pending')  # pending, accepted, declined
    created_at = db.Column(db.DateTime, default=lambda: datetime.now(timezone.utc))

    offerer = db.relationship('Player', foreign_keys=[offerer_id], backref='swap_offers_sent')
    target = db.relationship('Player', foreign_keys=[target_id], backref='swap_offers_received')
    offered_item = db.relationship('Item', foreign_keys=[offered_item_id])
    wanted_item = db.relationship('Item', foreign_keys=[wanted_item_id])
