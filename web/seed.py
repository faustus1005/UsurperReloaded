"""Seed the database with monsters, items, default configuration, and NPCs."""

from models import db, Monster, Item, GameConfig, Player, God


def seed_config():
    """Set default game configuration."""
    defaults = {
        'town_name': 'Dolingen',
        'dungeon_name': 'The Dungeon Complex',
        'sysop_name': 'The Sysop',
        'bbs_name': 'Usurper ReLoaded',
        'max_fights_per_day': '20',
        'max_player_fights': '3',
        'max_thefts_per_day': '2',
        'max_brawls_per_day': '2',
        'bank_interest_rate': '1',
        'start_gold': '100',
        'inn_name': 'The Dragon\'s Flagon',
        'weapon_shop_name': 'Dolingen Weapon Shop',
        'armor_shop_name': 'Dolingen Armor Shop',
        'magic_shop_name': 'The Arcane Emporium',
        'healing_shop_name': 'The Healing Hut',
        'general_store_name': 'Dolingen General Store',
        'level_master_name': 'Gandalf the Trainer',
        'dungeon_difficulty': '4',
        'challenges_place': 'Anchor Road',
        'team_fights_per_day': '1',
        'max_healing_potions': '125',
        'max_players': '400',
        'xp_loss_dungeon_pct': '3',
        'xp_loss_pvp_pct': '0',
        'level_to_usurp': '25',
        'allow_offline_attacks': 'true',
        'allow_team_attacks': 'false',
        'allow_resurrection': 'true',
        'allow_npc_teams': 'true',
        'allow_npc_equipment': 'true',
        'allow_npc_usurp': 'true',
        'allow_npc_marriage': 'true',
        'auto_promote_first_admin': 'true',
        'weaponshop_owner': 'Tully',
        'armorshop_owner': 'Reese',
        'combat_trainer': 'Liu Zei',
        'magicshop_owner': 'Ravanella',
        'bank_manager': 'Lobba',
        'inn_owner': 'Garth',
        'bishop_name': 'Jakobinus',
        'gossip_name': 'Lydia',
        'bartender_name': 'Ted',
    }
    for key, value in defaults.items():
        existing = GameConfig.query.filter_by(key=key).first()
        if not existing:
            db.session.add(GameConfig(key=key, value=value))
    db.session.commit()


def seed_monsters():
    """Create the monster bestiary."""
    if Monster.query.first():
        return

    monsters = [
        # Level 1-3: Beginner
        Monster(name='Giant Rat', min_dungeon_level=1, max_dungeon_level=3,
                hp=15, strength=5, defence=2, weapon_power=0, armor_power=0,
                experience=8, gold=3, phrase='Squeak! Squeak!', weapon_name='sharp teeth',
                aggression=1),
        Monster(name='Kobold', min_dungeon_level=1, max_dungeon_level=4,
                hp=20, strength=7, defence=3, weapon_power=2, armor_power=1,
                experience=12, gold=8, phrase='Die, human!', weapon_name='rusty dagger',
                aggression=1),
        Monster(name='Goblin', min_dungeon_level=1, max_dungeon_level=5,
                hp=25, strength=8, defence=4, weapon_power=3, armor_power=2,
                experience=15, gold=12, phrase='Gobbies gonna getcha!', weapon_name='short sword',
                aggression=2),
        Monster(name='Giant Spider', min_dungeon_level=1, max_dungeon_level=4,
                hp=18, strength=6, defence=3, weapon_power=1, armor_power=1,
                experience=10, gold=5, phrase='*hissss*', weapon_name='venomous fangs',
                is_poisonous=True, aggression=2),
        Monster(name='Skeleton', min_dungeon_level=2, max_dungeon_level=6,
                hp=30, strength=10, defence=5, weapon_power=4, armor_power=3,
                experience=20, gold=15, phrase='Clatter... clatter...', weapon_name='rusted sword',
                aggression=1),

        # Level 3-7: Intermediate
        Monster(name='Orc Warrior', min_dungeon_level=3, max_dungeon_level=8,
                hp=45, strength=15, defence=8, weapon_power=6, armor_power=4,
                experience=35, gold=25, phrase='WAAAGH!', weapon_name='battle axe',
                aggression=2),
        Monster(name='Zombie', min_dungeon_level=3, max_dungeon_level=7,
                hp=50, strength=12, defence=6, weapon_power=3, armor_power=2,
                experience=28, gold=10, phrase='Braaains...', weapon_name='rotting fists',
                has_disease=True, aggression=1),
        Monster(name='Dark Elf Scout', min_dungeon_level=4, max_dungeon_level=9,
                hp=40, strength=14, defence=10, weapon_power=8, armor_power=5,
                experience=40, gold=35, phrase='You trespass in our domain!', weapon_name='elven blade',
                magic_level=1, aggression=2),
        Monster(name='Troll Brute', min_dungeon_level=4, max_dungeon_level=9,
                hp=70, strength=20, defence=10, weapon_power=5, armor_power=3,
                experience=45, gold=30, phrase='SMASH PUNY HUMAN!', weapon_name='massive fists',
                aggression=3),
        Monster(name='Harpy', min_dungeon_level=3, max_dungeon_level=7,
                hp=35, strength=12, defence=7, weapon_power=5, armor_power=2,
                experience=30, gold=20, phrase='Screeeech!', weapon_name='razor talons',
                aggression=2),

        # Level 6-12: Advanced
        Monster(name='Ogre', min_dungeon_level=6, max_dungeon_level=12,
                hp=90, strength=25, defence=12, weapon_power=10, armor_power=6,
                experience=65, gold=50, phrase='Me crush you good!', weapon_name='huge club',
                aggression=2),
        Monster(name='Wraith', min_dungeon_level=6, max_dungeon_level=13,
                hp=60, strength=18, defence=15, weapon_power=8, armor_power=8,
                experience=70, gold=40, phrase='Your soul is mine...', weapon_name='spectral touch',
                magic_level=2, magic_resistance=10, aggression=2),
        Monster(name='Minotaur', min_dungeon_level=7, max_dungeon_level=14,
                hp=100, strength=30, defence=15, weapon_power=12, armor_power=8,
                experience=80, gold=60, phrase='You dare enter my labyrinth?!', weapon_name='great axe',
                aggression=3),
        Monster(name='Dark Knight', min_dungeon_level=8, max_dungeon_level=15,
                hp=110, strength=28, defence=20, weapon_power=15, armor_power=12,
                experience=90, gold=75, phrase='Prepare to meet your doom!', weapon_name='dark blade',
                aggression=2),
        Monster(name='Basilisk', min_dungeon_level=7, max_dungeon_level=13,
                hp=80, strength=22, defence=18, weapon_power=6, armor_power=15,
                experience=75, gold=45, phrase='*deadly gaze*', weapon_name='petrifying gaze',
                is_poisonous=True, aggression=2),

        # Level 10-20: Expert
        Monster(name='Vampire Lord', min_dungeon_level=10, max_dungeon_level=20,
                hp=150, strength=35, defence=25, weapon_power=18, armor_power=15,
                experience=120, gold=100, phrase='Ah, fresh blood...', weapon_name='draining bite',
                magic_level=3, magic_resistance=15, aggression=2),
        Monster(name='Frost Giant', min_dungeon_level=12, max_dungeon_level=22,
                hp=200, strength=45, defence=25, weapon_power=20, armor_power=12,
                experience=150, gold=120, phrase='FEEL THE COLD OF THE NORTH!', weapon_name='ice hammer',
                aggression=3),
        Monster(name='Lich', min_dungeon_level=13, max_dungeon_level=25,
                hp=130, strength=25, defence=30, weapon_power=10, armor_power=20,
                experience=180, gold=150, phrase='Death is but the beginning...', weapon_name='death touch',
                magic_level=5, magic_resistance=25, aggression=2),
        Monster(name='Iron Golem', min_dungeon_level=11, max_dungeon_level=20,
                hp=250, strength=40, defence=35, weapon_power=15, armor_power=25,
                experience=140, gold=80, phrase='*mechanical grinding*', weapon_name='iron fists',
                magic_resistance=30, aggression=1),
        Monster(name='Beholder', min_dungeon_level=14, max_dungeon_level=25,
                hp=120, strength=20, defence=20, weapon_power=15, armor_power=15,
                experience=160, gold=130, phrase='All shall gaze upon me!', weapon_name='eye rays',
                magic_level=4, magic_resistance=20, aggression=3),

        # Level 18-30: Legendary
        Monster(name='Ancient Dragon', min_dungeon_level=18, max_dungeon_level=30,
                hp=400, strength=60, defence=40, weapon_power=30, armor_power=25,
                experience=300, gold=250, phrase='FOOLISH MORTAL!', weapon_name='dragon fire',
                magic_level=5, magic_resistance=30, aggression=3),
        Monster(name='Demon Prince', min_dungeon_level=20, max_dungeon_level=30,
                hp=350, strength=55, defence=45, weapon_power=28, armor_power=30,
                experience=350, gold=300, phrase='Your soul belongs to the abyss!', weapon_name='hellfire blade',
                magic_level=5, magic_resistance=35, is_poisonous=True, aggression=3),
        Monster(name='Shadow Lord', min_dungeon_level=22, max_dungeon_level=30,
                hp=300, strength=50, defence=50, weapon_power=25, armor_power=35,
                experience=400, gold=350, phrase='Darkness eternal...', weapon_name='shadow essence',
                magic_level=5, magic_resistance=40, aggression=2),
        Monster(name='Titan', min_dungeon_level=25, max_dungeon_level=30,
                hp=500, strength=70, defence=40, weapon_power=35, armor_power=20,
                experience=500, gold=400, phrase='THE EARTH TREMBLES!', weapon_name='world-breaker',
                aggression=3),
    ]

    for m in monsters:
        db.session.add(m)
    db.session.commit()


def seed_items():
    """Create the item catalog."""
    if Item.query.first():
        return

    items = [
        # === WEAPONS ===
        # Shop weapons (available for purchase)
        Item(name='Rusty Dagger', item_type='Weapon', value=20, attack_bonus=3,
             description='A worn dagger, barely sharp.', in_shop=True, min_level=1, max_level=5),
        Item(name='Short Sword', item_type='Weapon', value=50, attack_bonus=6,
             description='A simple short sword.', in_shop=True, min_level=1, max_level=8),
        Item(name='Broad Sword', item_type='Weapon', value=120, attack_bonus=10,
             description='A sturdy broad sword.', in_shop=True, min_level=2, max_level=12),
        Item(name='Battle Axe', item_type='Weapon', value=200, attack_bonus=14,
             description='A fearsome battle axe.', in_shop=True, min_level=4, max_level=15),
        Item(name='War Hammer', item_type='Weapon', value=300, attack_bonus=18,
             description='A heavy war hammer.', in_shop=True, min_level=6, max_level=18),
        Item(name='Longsword', item_type='Weapon', value=450, attack_bonus=22,
             description='An elegant longsword.', in_shop=True, min_level=8, max_level=20),
        Item(name='Claymore', item_type='Weapon', value=700, attack_bonus=28,
             description='A massive two-handed sword.', in_shop=True, min_level=10, max_level=25),
        Item(name='Enchanted Blade', item_type='Weapon', value=1200, attack_bonus=35,
             description='A blade that glows with arcane energy.', in_shop=True, min_level=14, max_level=30),
        # Dungeon-only weapons
        Item(name='Flaming Sword', item_type='Weapon', value=800, attack_bonus=25,
             strength_bonus=3, description='A sword wreathed in magical flames.',
             in_dungeon=True, min_level=8, max_level=20),
        Item(name='Frost Brand', item_type='Weapon', value=1500, attack_bonus=32,
             agility_bonus=2, description='An icy blade that chills to the bone.',
             in_dungeon=True, min_level=12, max_level=25),
        Item(name='Vorpal Blade', item_type='Weapon', value=3000, attack_bonus=45,
             strength_bonus=5, dexterity_bonus=3, description='A legendary blade of incredible sharpness.',
             in_dungeon=True, min_level=20, max_level=30, is_unique=True),
        Item(name='Staff of Power', item_type='Weapon', value=1000, attack_bonus=15,
             wisdom_bonus=8, mana_bonus=20, description='A staff crackling with magical energy.',
             in_shop=True, min_level=8, max_level=30, class_restrictions='Magician,Sage,Cleric'),

        # === ARMOR (Body) ===
        Item(name='Leather Armor', item_type='Body', value=30, armor_bonus=3,
             description='Basic leather protection.', in_shop=True, min_level=1, max_level=8),
        Item(name='Studded Leather', item_type='Body', value=80, armor_bonus=6,
             description='Leather reinforced with metal studs.', in_shop=True, min_level=2, max_level=12),
        Item(name='Chain Mail', item_type='Body', value=180, armor_bonus=10,
             description='Interlocking metal rings.', in_shop=True, min_level=4, max_level=15),
        Item(name='Scale Mail', item_type='Body', value=300, armor_bonus=14,
             description='Overlapping metal scales.', in_shop=True, min_level=6, max_level=18),
        Item(name='Plate Armor', item_type='Body', value=500, armor_bonus=20,
             description='Heavy plate armor.', in_shop=True, min_level=8, max_level=22,
             strength_required=15),
        Item(name='Mithril Chain', item_type='Body', value=1000, armor_bonus=25,
             agility_bonus=2, description='Lightweight and incredibly strong.',
             in_shop=True, min_level=12, max_level=30),
        Item(name='Dragon Scale Armor', item_type='Body', value=3000, armor_bonus=35,
             strength_bonus=3, defence_bonus=5,
             description='Forged from the scales of an ancient dragon.',
             in_dungeon=True, min_level=18, max_level=30, is_unique=True),

        # === SHIELDS ===
        Item(name='Wooden Shield', item_type='Shield', value=15, armor_bonus=2,
             description='A simple wooden shield.', in_shop=True, min_level=1, max_level=6),
        Item(name='Iron Shield', item_type='Shield', value=60, armor_bonus=5,
             description='A solid iron shield.', in_shop=True, min_level=3, max_level=12),
        Item(name='Tower Shield', item_type='Shield', value=150, armor_bonus=10,
             description='A massive tower shield.', in_shop=True, min_level=6, max_level=18,
             strength_required=12),
        Item(name='Enchanted Buckler', item_type='Shield', value=400, armor_bonus=8,
             agility_bonus=3, description='A small shield that seems to move on its own.',
             in_dungeon=True, min_level=8, max_level=20),

        # === HEAD ===
        Item(name='Leather Cap', item_type='Head', value=10, armor_bonus=1,
             description='A simple leather cap.', in_shop=True, min_level=1, max_level=6),
        Item(name='Iron Helm', item_type='Head', value=45, armor_bonus=3,
             description='A sturdy iron helmet.', in_shop=True, min_level=3, max_level=12),
        Item(name='Plumed Helm', item_type='Head', value=120, armor_bonus=5,
             charisma_bonus=2, description='A decorative yet functional helmet.',
             in_shop=True, min_level=6, max_level=18),
        Item(name='Crown of Wisdom', item_type='Head', value=800, armor_bonus=4,
             wisdom_bonus=5, mana_bonus=10, description='A circlet that enhances mental power.',
             in_dungeon=True, min_level=10, max_level=25),

        # === HANDS/ARMS/LEGS/FEET ===
        Item(name='Leather Gloves', item_type='Hands', value=8, armor_bonus=1,
             description='Simple leather gloves.', in_shop=True, min_level=1, max_level=8),
        Item(name='Gauntlets of Strength', item_type='Hands', value=300, armor_bonus=3,
             strength_bonus=4, description='Heavy gauntlets that enhance grip.',
             in_dungeon=True, min_level=8, max_level=20),
        Item(name='Leather Boots', item_type='Feet', value=12, armor_bonus=1,
             description='Sturdy leather boots.', in_shop=True, min_level=1, max_level=8),
        Item(name='Boots of Speed', item_type='Feet', value=500, armor_bonus=2,
             agility_bonus=5, description='Enchanted boots that quicken your step.',
             in_dungeon=True, min_level=10, max_level=25),
        Item(name='Arm Guards', item_type='Arms', value=25, armor_bonus=2,
             description='Simple arm guards.', in_shop=True, min_level=2, max_level=10),
        Item(name='Greaves', item_type='Legs', value=30, armor_bonus=2,
             description='Metal leg guards.', in_shop=True, min_level=2, max_level=10),

        # === ACCESSORIES ===
        Item(name='Amulet of Protection', item_type='Neck', value=200, armor_bonus=3,
             defence_bonus=2, description='A protective charm.', in_shop=True, min_level=4, max_level=15),
        Item(name='Cloak of Shadows', item_type='Around Body', value=350, armor_bonus=4,
             agility_bonus=3, description='A dark cloak that helps you blend into shadows.',
             in_shop=True, min_level=5, max_level=18),
        Item(name='Belt of Fortitude', item_type='Waist', value=150, stamina_bonus=4,
             hp_bonus=10, description='A thick belt that bolsters endurance.',
             in_dungeon=True, min_level=5, max_level=15),
        Item(name='War Paint', item_type='Face', value=25, charisma_bonus=-1,
             strength_bonus=2, description='Fearsome war paint.',
             in_shop=True, min_level=1, max_level=10),
        Item(name='Ring of Power', item_type='Fingers', value=2000, strength_bonus=5,
             wisdom_bonus=5, mana_bonus=15, description='A ring of immense power.',
             in_dungeon=True, min_level=15, max_level=30, is_unique=True),

        # === CONSUMABLES (found in dungeon) ===
        Item(name='Health Potion', item_type='Food', value=25, hp_bonus=30,
             description='A vial of red liquid that restores health.',
             in_shop=True, in_dungeon=True, min_level=1, max_level=30),
        Item(name='Mana Potion', item_type='Drink', value=30, mana_bonus=20,
             description='A vial of blue liquid that restores mana.',
             in_shop=True, in_dungeon=True, min_level=1, max_level=30),
    ]

    for item in items:
        db.session.add(item)
    db.session.commit()


def seed_npcs():
    """Create a starting population of NPC characters at various levels."""
    # Only seed if no NPCs exist yet
    if Player.query.filter_by(is_npc=True).first():
        return

    from npc_engine import create_npc, equip_npc_for_level

    # Create NPCs across a range of levels for a living world
    npc_levels = [
        1, 1, 2, 2, 3, 3, 4, 5, 5,    # 9 low-level NPCs
        6, 7, 8, 9, 10,                  # 5 mid-level NPCs
        12, 15, 18, 20,                   # 4 high-level NPCs
        22, 25,                           # 2 very high-level NPCs
    ]

    for level in npc_levels:
        npc = create_npc(level=level)
        equip_npc_for_level(npc)

    db.session.commit()


def seed_npc_config():
    """Set NPC-related game configuration defaults."""
    npc_defaults = {
        'npc_enabled': 'true',
        'npc_tick_minutes': '5',
        'npc_allow_usurping': 'true',
        'npc_allow_marriage': 'true',
        'npc_allow_teams': 'true',
        'npc_allow_bounty_hunting': 'true',
        'npc_allow_pvp': 'true',
        'npc_min_level_king': '5',
        'npc_max_count': '20',
    }
    for key, value in npc_defaults.items():
        existing = GameConfig.query.filter_by(key=key).first()
        if not existing:
            db.session.add(GameConfig(key=key, value=value))
    db.session.commit()


def seed_additional_items():
    """Seed additional shop items from original game (alchemist, healing, general store)."""
    # Check if we've already seeded these
    if Item.query.filter_by(shop_category='alchemist').first():
        return

    extra_items = [
        # === ALCHEMIST SHOP (Poisons - Alchemist class only) ===
        Item(name='Snake Bite Poison', item_type='Weapon', value=1500, attack_bonus=4,
             description='A basic poison. Coats your weapon with venom.', in_shop=True,
             shop_category='alchemist', min_level=1, max_level=30,
             class_restrictions='Alchemist'),
        Item(name='Diamond Sting', item_type='Weapon', value=10000, attack_bonus=12,
             description='An advanced poison that burns on contact.', in_shop=True,
             shop_category='alchemist', min_level=5, max_level=30,
             class_restrictions='Alchemist'),
        Item(name='Joy of Death', item_type='Weapon', value=50000, attack_bonus=20,
             description='A deadly poison feared across the realm.', in_shop=True,
             shop_category='alchemist', min_level=10, max_level=30,
             class_restrictions='Alchemist'),
        Item(name='Devils Cure', item_type='Weapon', value=100000, attack_bonus=30,
             description='The most lethal poison known to alchemists.', in_shop=True,
             shop_category='alchemist', min_level=18, max_level=30,
             class_restrictions='Alchemist'),

        # === HEALING HUT (Consumables) ===
        Item(name='Cure Disease Tonic', item_type='Food', value=50,
             description='Cures disease and plague.', in_shop=True,
             shop_category='healing', min_level=1, max_level=30),
        Item(name='Antidote', item_type='Food', value=30,
             description='Cures poison.', in_shop=True,
             shop_category='healing', min_level=1, max_level=30),
        Item(name='Eye Drops', item_type='Food', value=40,
             description='Cures blindness.', in_shop=True,
             shop_category='healing', min_level=1, max_level=30),
        Item(name='Greater Healing Potion', item_type='Food', value=100, hp_bonus=80,
             description='A potent healing elixir.', in_shop=True,
             shop_category='healing', min_level=5, max_level=30),
        Item(name='Full Restoration Elixir', item_type='Food', value=300, hp_bonus=200,
             description='Fully restores health.', in_shop=True,
             shop_category='healing', min_level=10, max_level=30),

        # === GENERAL STORE (Misc equipment) ===
        Item(name='Torch', item_type='Hands', value=5, armor_bonus=0,
             description='Lights your way in the dungeon.', in_shop=True,
             shop_category='general', min_level=1, max_level=30),
        Item(name='Rope', item_type='Waist', value=10, armor_bonus=0, agility_bonus=1,
             description='Useful for climbing and escaping.', in_shop=True,
             shop_category='general', min_level=1, max_level=30),
        Item(name='Traveler\'s Pack', item_type='Around Body', value=35, armor_bonus=1,
             stamina_bonus=2, description='A sturdy pack for long journeys.', in_shop=True,
             shop_category='general', min_level=1, max_level=15),
        Item(name='Silver Mirror', item_type='Face', value=80, charisma_bonus=3,
             description='A polished mirror that reveals truth.', in_shop=True,
             shop_category='general', min_level=3, max_level=20),
        Item(name='Lucky Charm', item_type='Neck', value=200, charisma_bonus=2,
             dexterity_bonus=2, description='A rabbit\'s foot on a chain.', in_shop=True,
             shop_category='general', min_level=1, max_level=30),

        # === SHADY DEALER (Dark Alley items) ===
        Item(name='Thieves\' Dagger', item_type='Weapon', value=350, attack_bonus=12,
             dexterity_bonus=3, description='A dagger favored by cutpurses.', in_shop=True,
             shop_category='shady', min_level=3, max_level=15, evil_only=True),
        Item(name='Shadow Cloak', item_type='Around Body', value=600, armor_bonus=5,
             agility_bonus=4, description='A cloak woven from shadow threads.', in_shop=True,
             shop_category='shady', min_level=5, max_level=25, evil_only=True),
        Item(name='Cursed Ring', item_type='Fingers', value=50, strength_bonus=8,
             wisdom_bonus=-3, description='Grants power at a terrible cost.', in_shop=True,
             shop_category='shady', min_level=1, max_level=30, is_cursed=True),
        Item(name='Mask of Deception', item_type='Face', value=400, charisma_bonus=5,
             description='Hides your true identity.', in_shop=True,
             shop_category='shady', min_level=5, max_level=25),
        Item(name='Assassin\'s Blade', item_type='Weapon', value=1500, attack_bonus=28,
             dexterity_bonus=4, description='A blade made for killing.', in_shop=True,
             shop_category='shady', min_level=10, max_level=30,
             class_restrictions='Assassin'),
    ]

    for item in extra_items:
        db.session.add(item)
    db.session.commit()


def seed_gods():
    """Create default gods if none exist."""
    if God.query.first():
        return

    import random
    default_gods = [
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
    for g in default_gods:
        god = God(
            name=g['name'], domain=g['domain'], alignment=g['alignment'],
            sex=g['sex'], description=g['description'],
            level=random.randint(5, 8),
            experience=random.randint(50000, 500000),
        )
        db.session.add(god)
    db.session.commit()


def seed_all():
    """Run all seed functions."""
    seed_config()
    seed_monsters()
    seed_items()
    seed_additional_items()
    seed_gods()
    seed_npc_config()
    seed_npcs()
