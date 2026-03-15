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
        # Beauty Nest
        'beauty_nest_name': 'The Beauty Nest',
        'beauty_nest_owner': 'Clarissa',
        'beauty_nest_visits_per_day': '3',
        'beauty_nest_disease_chance': '3',
        'beauty_nest_enabled': 'true',
        # Additional location names
        'tavern_name': 'Bob\'s Tavern',
        'dark_alley_name': 'The Dark Alley',
        'temple_name': 'Temple of the Gods',
        'castle_name': 'The Royal Castle',
        'love_corner_name': 'The Love Corner',
        # Scrolling text
        'scrolling_text': '',
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
        # Original Usurper monsters (alchemy quest creatures & missing types)
        Monster(name='Great Boa', min_dungeon_level=4, max_dungeon_level=10,
                hp=60, strength=18, defence=8, weapon_power=6, armor_power=3,
                experience=40, gold=25, phrase='*coils tighten*', weapon_name='crushing coils',
                is_poisonous=True, aggression=2),
        Monster(name='Great Boar', min_dungeon_level=3, max_dungeon_level=8,
                hp=55, strength=16, defence=10, weapon_power=7, armor_power=5,
                experience=35, gold=20, phrase='SNORT! CHARGE!', weapon_name='razor tusks',
                aggression=3),
        Monster(name='Huge Tiger', min_dungeon_level=4, max_dungeon_level=9,
                hp=50, strength=20, defence=9, weapon_power=8, armor_power=3,
                experience=42, gold=30, phrase='*ROARRR*', weapon_name='savage claws',
                aggression=3),
        Monster(name='Iceman', min_dungeon_level=5, max_dungeon_level=12,
                hp=65, strength=15, defence=12, weapon_power=5, armor_power=8,
                experience=50, gold=35, phrase='The cold... embraces you...', weapon_name='frozen touch',
                magic_level=2, aggression=2),
        Monster(name='Dungeon Bandit', min_dungeon_level=2, max_dungeon_level=6,
                hp=30, strength=10, defence=5, weapon_power=4, armor_power=3,
                experience=18, gold=25, phrase='Your gold or your life!', weapon_name='short blade',
                aggression=2),
        Monster(name='Cave Troll', min_dungeon_level=5, max_dungeon_level=10,
                hp=80, strength=22, defence=8, weapon_power=7, armor_power=4,
                experience=48, gold=35, phrase='TROOOLLL SMASH!', weapon_name='stone club',
                aggression=3),
        Monster(name='Giant Scorpion', min_dungeon_level=3, max_dungeon_level=8,
                hp=35, strength=14, defence=12, weapon_power=6, armor_power=6,
                experience=32, gold=18, phrase='*click click*', weapon_name='venomous stinger',
                is_poisonous=True, aggression=2),
        Monster(name='Ghoul', min_dungeon_level=4, max_dungeon_level=9,
                hp=42, strength=13, defence=6, weapon_power=4, armor_power=2,
                experience=28, gold=15, phrase='Hungry... so hungry...', weapon_name='paralyzing claws',
                has_disease=True, aggression=2),

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

        # Level 18-35: Legendary
        Monster(name='Ancient Dragon', min_dungeon_level=18, max_dungeon_level=35,
                hp=400, strength=60, defence=40, weapon_power=30, armor_power=25,
                experience=300, gold=250, phrase='FOOLISH MORTAL!', weapon_name='dragon fire',
                magic_level=5, magic_resistance=30, aggression=3),
        Monster(name='Demon Prince', min_dungeon_level=20, max_dungeon_level=35,
                hp=350, strength=55, defence=45, weapon_power=28, armor_power=30,
                experience=350, gold=300, phrase='Your soul belongs to the abyss!', weapon_name='hellfire blade',
                magic_level=5, magic_resistance=35, is_poisonous=True, aggression=3),
        Monster(name='Shadow Lord', min_dungeon_level=22, max_dungeon_level=35,
                hp=300, strength=50, defence=50, weapon_power=25, armor_power=35,
                experience=400, gold=350, phrase='Darkness eternal...', weapon_name='shadow essence',
                magic_level=5, magic_resistance=40, aggression=2),
        Monster(name='Titan', min_dungeon_level=25, max_dungeon_level=40,
                hp=500, strength=70, defence=40, weapon_power=35, armor_power=20,
                experience=500, gold=400, phrase='THE EARTH TREMBLES!', weapon_name='world-breaker',
                aggression=3),

        # Level 28-45: Epic
        Monster(name='Bone Dragon', min_dungeon_level=28, max_dungeon_level=42,
                hp=550, strength=75, defence=50, weapon_power=38, armor_power=30,
                experience=600, gold=500, phrase='Rise from the grave!', weapon_name='necrotic breath',
                magic_level=5, magic_resistance=35, aggression=3),
        Monster(name='Pit Fiend', min_dungeon_level=30, max_dungeon_level=45,
                hp=500, strength=70, defence=55, weapon_power=35, armor_power=35,
                experience=650, gold=550, phrase='Hell awaits you!', weapon_name='infernal trident',
                magic_level=5, magic_resistance=40, is_poisonous=True, aggression=3),
        Monster(name='Elder Lich', min_dungeon_level=28, max_dungeon_level=45,
                hp=400, strength=55, defence=60, weapon_power=30, armor_power=40,
                experience=700, gold=600, phrase='Undeath is merely the beginning...', weapon_name='soul drain',
                magic_level=6, magic_resistance=50, aggression=2),
        Monster(name='Storm Giant King', min_dungeon_level=30, max_dungeon_level=45,
                hp=700, strength=90, defence=50, weapon_power=45, armor_power=25,
                experience=750, gold=650, phrase='LIGHTNING SHALL BE YOUR END!', weapon_name='storm hammer',
                magic_level=4, magic_resistance=30, aggression=3),
        Monster(name='Medusa Queen', min_dungeon_level=28, max_dungeon_level=40,
                hp=350, strength=50, defence=45, weapon_power=25, armor_power=30,
                experience=550, gold=500, phrase='Look into my eyes...', weapon_name='petrifying gaze',
                magic_level=5, magic_resistance=35, is_poisonous=True, aggression=2),
        Monster(name='Death Knight Commander', min_dungeon_level=32, max_dungeon_level=48,
                hp=600, strength=80, defence=60, weapon_power=42, armor_power=38,
                experience=800, gold=700, phrase='In death, I serve!', weapon_name='runic greatsword',
                magic_level=4, magic_resistance=30, aggression=3),

        # Level 38-58: Mythic
        Monster(name='Balrog', min_dungeon_level=38, max_dungeon_level=55,
                hp=800, strength=100, defence=65, weapon_power=50, armor_power=40,
                experience=1000, gold=900, phrase='YOU SHALL NOT PASS!', weapon_name='whip of flame',
                magic_level=6, magic_resistance=45, aggression=3),
        Monster(name='Kraken', min_dungeon_level=35, max_dungeon_level=52,
                hp=900, strength=95, defence=55, weapon_power=48, armor_power=35,
                experience=950, gold=800, phrase='The deep claims all!', weapon_name='crushing tentacles',
                magic_level=3, magic_resistance=25, aggression=3),
        Monster(name='Arch-Demon', min_dungeon_level=40, max_dungeon_level=58,
                hp=750, strength=90, defence=70, weapon_power=45, armor_power=45,
                experience=1100, gold=1000, phrase='Your realm shall burn!', weapon_name='chaos blade',
                magic_level=7, magic_resistance=50, is_poisonous=True, aggression=3),
        Monster(name='Phoenix Lord', min_dungeon_level=38, max_dungeon_level=55,
                hp=600, strength=85, defence=60, weapon_power=55, armor_power=30,
                experience=1050, gold=950, phrase='From ashes, I rise eternal!', weapon_name='solar flare',
                magic_level=6, magic_resistance=40, aggression=2),
        Monster(name='Void Worm', min_dungeon_level=42, max_dungeon_level=58,
                hp=1000, strength=80, defence=50, weapon_power=40, armor_power=50,
                experience=1200, gold=1100, phrase='*reality warps*', weapon_name='void maw',
                magic_level=5, magic_resistance=60, aggression=2),
        Monster(name='Lich Emperor', min_dungeon_level=45, max_dungeon_level=60,
                hp=700, strength=70, defence=80, weapon_power=35, armor_power=55,
                experience=1300, gold=1200, phrase='I have conquered death itself!', weapon_name='staff of oblivion',
                magic_level=8, magic_resistance=60, aggression=2),

        # Level 50-72: Abyssal
        Monster(name='Elder Wyrm', min_dungeon_level=50, max_dungeon_level=68,
                hp=1200, strength=120, defence=80, weapon_power=60, armor_power=50,
                experience=1600, gold=1500, phrase='I am older than your world!', weapon_name='prismatic breath',
                magic_level=7, magic_resistance=50, aggression=3),
        Monster(name='Abyssal Lord', min_dungeon_level=52, max_dungeon_level=70,
                hp=1000, strength=110, defence=90, weapon_power=55, armor_power=60,
                experience=1800, gold=1700, phrase='The abyss hungers!', weapon_name='doom blade',
                magic_level=8, magic_resistance=55, is_poisonous=True, aggression=3),
        Monster(name='Celestial Guardian', min_dungeon_level=50, max_dungeon_level=68,
                hp=1100, strength=100, defence=100, weapon_power=50, armor_power=65,
                experience=1700, gold=1600, phrase='You are not worthy!', weapon_name='holy lance',
                magic_level=7, magic_resistance=60, aggression=2),
        Monster(name='Mind Flayer Overlord', min_dungeon_level=48, max_dungeon_level=65,
                hp=800, strength=80, defence=75, weapon_power=45, armor_power=50,
                experience=1500, gold=1400, phrase='Your thoughts are mine!', weapon_name='psychic blast',
                magic_level=9, magic_resistance=65, aggression=2),
        Monster(name='Tarrasque', min_dungeon_level=55, max_dungeon_level=72,
                hp=2000, strength=150, defence=70, weapon_power=70, armor_power=40,
                experience=2000, gold=1800, phrase='*earth-shaking roar*', weapon_name='devastating bite',
                magic_level=3, magic_resistance=40, aggression=3),

        # Level 60-85: Primordial
        Monster(name='Primordial Chaos Beast', min_dungeon_level=60, max_dungeon_level=78,
                hp=1500, strength=130, defence=90, weapon_power=65, armor_power=55,
                experience=2500, gold=2200, phrase='ORDER IS AN ILLUSION!', weapon_name='entropy claw',
                magic_level=8, magic_resistance=55, aggression=3),
        Monster(name='Astral Devourer', min_dungeon_level=62, max_dungeon_level=80,
                hp=1300, strength=120, defence=100, weapon_power=60, armor_power=65,
                experience=2700, gold=2400, phrase='The stars weep at my approach!', weapon_name='dimension rend',
                magic_level=8, magic_resistance=60, aggression=3),
        Monster(name='Empyrean Titan', min_dungeon_level=65, max_dungeon_level=82,
                hp=2500, strength=170, defence=85, weapon_power=80, armor_power=45,
                experience=3000, gold=2700, phrase='KNEEL BEFORE THE HEAVENS!', weapon_name='divine fist',
                magic_level=6, magic_resistance=50, aggression=3),
        Monster(name='Demilich', min_dungeon_level=60, max_dungeon_level=80,
                hp=900, strength=90, defence=120, weapon_power=50, armor_power=80,
                experience=2800, gold=2500, phrase='I transcended mere undeath eons ago...', weapon_name='howl of the banshee',
                magic_level=10, magic_resistance=75, aggression=2),
        Monster(name='World Serpent', min_dungeon_level=68, max_dungeon_level=85,
                hp=3000, strength=180, defence=80, weapon_power=85, armor_power=50,
                experience=3500, gold=3000, phrase='I encircle the world!', weapon_name='cataclysmic coils',
                magic_level=7, magic_resistance=55, is_poisonous=True, aggression=3),

        # Level 75-95: Godlike
        Monster(name='Avatar of Destruction', min_dungeon_level=75, max_dungeon_level=92,
                hp=2500, strength=200, defence=120, weapon_power=100, armor_power=70,
                experience=5000, gold=4500, phrase='ALL SHALL BE UNMADE!', weapon_name='annihilation beam',
                magic_level=9, magic_resistance=65, aggression=3),
        Monster(name='Void Dragon', min_dungeon_level=78, max_dungeon_level=95,
                hp=3000, strength=190, defence=130, weapon_power=95, armor_power=80,
                experience=5500, gold=5000, phrase='I am the emptiness between stars!', weapon_name='void breath',
                magic_level=9, magic_resistance=70, aggression=3),
        Monster(name='Eldritch Horror', min_dungeon_level=75, max_dungeon_level=92,
                hp=2000, strength=160, defence=140, weapon_power=80, armor_power=90,
                experience=5200, gold=4800, phrase='*sanity-shattering whispers*', weapon_name='maddening gaze',
                magic_level=10, magic_resistance=80, aggression=2),
        Monster(name='Fallen Seraph', min_dungeon_level=80, max_dungeon_level=95,
                hp=2200, strength=180, defence=150, weapon_power=90, armor_power=85,
                experience=6000, gold=5500, phrase='Even angels fall!', weapon_name='corrupted holy blade',
                magic_level=10, magic_resistance=70, aggression=3),

        # Level 85-100: Cosmic
        Monster(name='Cosmic Leviathan', min_dungeon_level=85, max_dungeon_level=100,
                hp=4000, strength=230, defence=140, weapon_power=110, armor_power=80,
                experience=8000, gold=7000, phrase='WORLDS CRUMBLE IN MY WAKE!', weapon_name='cosmic maw',
                magic_level=9, magic_resistance=70, aggression=3),
        Monster(name='Time Weaver', min_dungeon_level=85, max_dungeon_level=100,
                hp=2500, strength=170, defence=170, weapon_power=85, armor_power=100,
                experience=8500, gold=7500, phrase='Past, present, future - all are mine!', weapon_name='temporal rift',
                magic_level=10, magic_resistance=85, aggression=2),
        Monster(name='God-King of the Abyss', min_dungeon_level=90, max_dungeon_level=100,
                hp=5000, strength=250, defence=160, weapon_power=120, armor_power=90,
                experience=10000, gold=9000, phrase='I AM THE DARKNESS ETERNAL!', weapon_name='blade of damnation',
                magic_level=10, magic_resistance=80, is_poisonous=True, aggression=3),
        Monster(name='The Usurper', min_dungeon_level=95, max_dungeon_level=100,
                hp=6000, strength=280, defence=180, weapon_power=140, armor_power=100,
                experience=15000, gold=12000, phrase='I CLAIMED THIS REALM BEFORE TIME BEGAN!', weapon_name='world-ender',
                magic_level=10, magic_resistance=90, aggression=3),
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
             description='A blade that glows with arcane energy.', in_shop=True, min_level=14, max_level=40),
        # Dungeon-only weapons
        Item(name='Flaming Sword', item_type='Weapon', value=800, attack_bonus=25,
             strength_bonus=3, description='A sword wreathed in magical flames.',
             in_dungeon=True, min_level=8, max_level=20),
        Item(name='Frost Brand', item_type='Weapon', value=1500, attack_bonus=32,
             agility_bonus=2, description='An icy blade that chills to the bone.',
             in_dungeon=True, min_level=12, max_level=25),
        Item(name='Vorpal Blade', item_type='Weapon', value=3000, attack_bonus=45,
             strength_bonus=5, dexterity_bonus=3, description='A legendary blade of incredible sharpness.',
             in_dungeon=True, min_level=20, max_level=50, is_unique=True),
        Item(name='Staff of Power', item_type='Weapon', value=1000, attack_bonus=15,
             wisdom_bonus=8, mana_bonus=20, description='A staff crackling with magical energy.',
             in_shop=True, min_level=8, max_level=40, class_restrictions='Magician,Sage,Cleric'),

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
             in_shop=True, min_level=12, max_level=45),
        Item(name='Dragon Scale Armor', item_type='Body', value=3000, armor_bonus=35,
             strength_bonus=3, defence_bonus=5,
             description='Forged from the scales of an ancient dragon.',
             in_dungeon=True, min_level=18, max_level=55, is_unique=True),

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
             in_dungeon=True, min_level=15, max_level=50, is_unique=True),

        # === CONSUMABLES (found in dungeon) ===
        Item(name='Health Potion', item_type='Food', value=25, hp_bonus=30,
             description='A vial of red liquid that restores health.',
             in_shop=True, in_dungeon=True, min_level=1, max_level=100),
        Item(name='Mana Potion', item_type='Drink', value=30, mana_bonus=20,
             description='A vial of blue liquid that restores mana.',
             in_shop=True, in_dungeon=True, min_level=1, max_level=100),

        # === HIGH-LEVEL WEAPONS (Levels 25-100) ===
        Item(name='Adamantine Greatsword', item_type='Weapon', value=2000, attack_bonus=40,
             strength_bonus=3, description='An indestructible greatsword of adamantine.',
             in_shop=True, min_level=18, max_level=50),
        Item(name='Runic War Axe', item_type='Weapon', value=3500, attack_bonus=48,
             strength_bonus=5, description='An axe inscribed with ancient runes of power.',
             in_shop=True, min_level=25, max_level=60),
        Item(name='Dragonslayer', item_type='Weapon', value=6000, attack_bonus=58,
             strength_bonus=8, dexterity_bonus=3, description='A legendary blade forged to slay dragons.',
             in_shop=True, min_level=35, max_level=70),
        Item(name='Astral Blade', item_type='Weapon', value=12000, attack_bonus=72,
             strength_bonus=10, agility_bonus=5, description='A blade that cuts through dimensions.',
             in_shop=True, min_level=50, max_level=85),
        Item(name='Godsbane', item_type='Weapon', value=25000, attack_bonus=90,
             strength_bonus=15, dexterity_bonus=8, description='The weapon that slew a god.',
             in_shop=True, min_level=65, max_level=100),
        Item(name='World-Ender', item_type='Weapon', value=50000, attack_bonus=110,
             strength_bonus=20, dexterity_bonus=10, description='A weapon of absolute destruction.',
             in_shop=True, min_level=80, max_level=100),
        # High-level dungeon weapons
        Item(name='Soulsword', item_type='Weapon', value=8000, attack_bonus=65,
             strength_bonus=8, wisdom_bonus=5, description='A blade forged from captured souls.',
             in_dungeon=True, min_level=35, max_level=65, is_unique=True),
        Item(name='Blade of Eternity', item_type='Weapon', value=20000, attack_bonus=85,
             strength_bonus=12, agility_bonus=8, description='A blade that has existed since the dawn of time.',
             in_dungeon=True, min_level=55, max_level=85, is_unique=True),
        Item(name='The Cosmic Reaper', item_type='Weapon', value=60000, attack_bonus=130,
             strength_bonus=25, dexterity_bonus=15, description='Harvests the essence of reality itself.',
             in_dungeon=True, min_level=80, max_level=100, is_unique=True),
        # High-level caster weapons
        Item(name='Archmage Staff', item_type='Weapon', value=5000, attack_bonus=25,
             wisdom_bonus=15, mana_bonus=40, description='A staff wielded by archmages of old.',
             in_shop=True, min_level=25, max_level=60, class_restrictions='Magician,Sage,Cleric'),
        Item(name='Staff of the Void', item_type='Weapon', value=15000, attack_bonus=40,
             wisdom_bonus=25, mana_bonus=80, description='A staff that channels the power of the void.',
             in_shop=True, min_level=50, max_level=85, class_restrictions='Magician,Sage,Cleric'),
        Item(name='Staff of Creation', item_type='Weapon', value=40000, attack_bonus=60,
             wisdom_bonus=40, mana_bonus=150, description='The staff used to shape the world.',
             in_shop=True, min_level=75, max_level=100, class_restrictions='Magician,Sage,Cleric'),

        # === HIGH-LEVEL ARMOR (Levels 25-100) ===
        Item(name='Adamantine Plate', item_type='Body', value=2500, armor_bonus=30,
             strength_bonus=2, description='Nigh-indestructible plate armor.',
             in_shop=True, min_level=20, max_level=55, strength_required=20),
        Item(name='Runic Battle Armor', item_type='Body', value=5000, armor_bonus=40,
             defence_bonus=5, strength_bonus=3, description='Armor inscribed with protective runes.',
             in_shop=True, min_level=30, max_level=65),
        Item(name='Celestial Plate', item_type='Body', value=10000, armor_bonus=55,
             defence_bonus=8, stamina_bonus=5, description='Armor blessed by the gods themselves.',
             in_shop=True, min_level=45, max_level=80),
        Item(name='Void Armor', item_type='Body', value=25000, armor_bonus=75,
             defence_bonus=12, agility_bonus=5, description='Armor woven from the fabric of the void.',
             in_shop=True, min_level=65, max_level=100),
        Item(name='Armor of the Cosmos', item_type='Body', value=50000, armor_bonus=100,
             defence_bonus=20, strength_bonus=10, stamina_bonus=10,
             description='Armor forged from the essence of creation.',
             in_shop=True, min_level=85, max_level=100),
        # Dungeon armor
        Item(name='Demon Lord Plate', item_type='Body', value=15000, armor_bonus=60,
             strength_bonus=8, defence_bonus=10,
             description='Armor stripped from a slain demon lord.',
             in_dungeon=True, min_level=40, max_level=70, is_unique=True),
        Item(name='Titan\'s Aegis', item_type='Body', value=35000, armor_bonus=85,
             strength_bonus=15, defence_bonus=15, stamina_bonus=10,
             description='The armor of a fallen titan.',
             in_dungeon=True, min_level=70, max_level=100, is_unique=True),

        # === HIGH-LEVEL SHIELDS (Levels 25-100) ===
        Item(name='Adamantine Shield', item_type='Shield', value=1500, armor_bonus=15,
             defence_bonus=3, description='An unbreakable shield.',
             in_shop=True, min_level=20, max_level=55, strength_required=15),
        Item(name='Aegis of Light', item_type='Shield', value=5000, armor_bonus=25,
             defence_bonus=5, wisdom_bonus=3, description='A shield radiating divine light.',
             in_shop=True, min_level=35, max_level=70),
        Item(name='Cosmic Bulwark', item_type='Shield', value=15000, armor_bonus=40,
             defence_bonus=10, stamina_bonus=5, description='A shield forged from stardust.',
             in_shop=True, min_level=60, max_level=100),
        Item(name='Shield of the Usurper', item_type='Shield', value=40000, armor_bonus=55,
             defence_bonus=15, strength_bonus=8, description='The shield of the realm\'s greatest conqueror.',
             in_dungeon=True, min_level=80, max_level=100, is_unique=True),

        # === HIGH-LEVEL HELMS (Levels 25-100) ===
        Item(name='Helm of the Conqueror', item_type='Head', value=3000, armor_bonus=10,
             strength_bonus=5, charisma_bonus=3, description='A helm that inspires fear and awe.',
             in_shop=True, min_level=25, max_level=60),
        Item(name='Crown of Stars', item_type='Head', value=10000, armor_bonus=15,
             wisdom_bonus=10, mana_bonus=30, description='A crown set with imprisoned starlight.',
             in_dungeon=True, min_level=45, max_level=80),
        Item(name='Helm of the Void', item_type='Head', value=20000, armor_bonus=22,
             wisdom_bonus=12, defence_bonus=8, description='A helm that sees into the void.',
             in_shop=True, min_level=65, max_level=100),

        # === HIGH-LEVEL ACCESSORIES (Levels 25-100) ===
        Item(name='Gauntlets of Titan Grip', item_type='Hands', value=5000, armor_bonus=8,
             strength_bonus=10, description='Gauntlets that grant the grip of a titan.',
             in_dungeon=True, min_level=35, max_level=70),
        Item(name='Boots of the Wind', item_type='Feet', value=4000, armor_bonus=5,
             agility_bonus=10, dexterity_bonus=5, description='Boots lighter than air itself.',
             in_dungeon=True, min_level=30, max_level=65),
        Item(name='Amulet of the Archmage', item_type='Neck', value=8000, armor_bonus=5,
             wisdom_bonus=12, mana_bonus=40, description='An amulet of supreme magical power.',
             in_shop=True, min_level=40, max_level=80),
        Item(name='Belt of Giant Strength', item_type='Waist', value=6000, armor_bonus=3,
             strength_bonus=12, stamina_bonus=8, hp_bonus=50,
             description='A belt imbued with the strength of giants.',
             in_dungeon=True, min_level=35, max_level=70),
        Item(name='Cloak of the Cosmos', item_type='Around Body', value=15000, armor_bonus=12,
             agility_bonus=8, defence_bonus=8, description='A cloak woven from the fabric of space.',
             in_dungeon=True, min_level=55, max_level=90),
        Item(name='Ring of Omnipotence', item_type='Fingers', value=30000, strength_bonus=15,
             wisdom_bonus=15, mana_bonus=50, hp_bonus=100,
             description='A ring of absolute power.',
             in_dungeon=True, min_level=70, max_level=100, is_unique=True),
        Item(name='Voidwalker Boots', item_type='Feet', value=12000, armor_bonus=10,
             agility_bonus=15, dexterity_bonus=10, description='Boots that walk between dimensions.',
             in_shop=True, min_level=60, max_level=100),
        Item(name='Cosmic Gauntlets', item_type='Hands', value=18000, armor_bonus=15,
             strength_bonus=15, dexterity_bonus=8, description='Gauntlets forged from cosmic energy.',
             in_shop=True, min_level=65, max_level=100),
        Item(name='Greaves of the Titan', item_type='Legs', value=8000, armor_bonus=12,
             stamina_bonus=8, strength_bonus=5, description='Leg armor from a fallen titan.',
             in_shop=True, min_level=40, max_level=80),
        Item(name='Arm Guards of Eternity', item_type='Arms', value=6000, armor_bonus=8,
             defence_bonus=5, stamina_bonus=5, description='Arm guards that never tarnish.',
             in_shop=True, min_level=35, max_level=75),

        # === NECROMANCER CLASS ITEMS ===
        Item(name='Bone Staff', item_type='Weapon', value=150, attack_bonus=10,
             wisdom_bonus=4, mana_bonus=10, description='A staff carved from humanoid bones.',
             in_shop=True, min_level=3, max_level=15, class_restrictions='Necromancer'),
        Item(name='Soulreaper Scythe', item_type='Weapon', value=1500, attack_bonus=30,
             wisdom_bonus=8, mana_bonus=20, description='A scythe that harvests souls.',
             in_shop=True, min_level=15, max_level=45, class_restrictions='Necromancer'),
        Item(name='Phylactery', item_type='Neck', value=2500, armor_bonus=4,
             wisdom_bonus=10, mana_bonus=30, hp_bonus=20,
             description='A vessel containing a fragment of your soul.',
             in_dungeon=True, min_level=25, max_level=60, class_restrictions='Necromancer'),
        Item(name='Robes of the Lich', item_type='Body', value=5000, armor_bonus=15,
             wisdom_bonus=12, mana_bonus=40, description='Tattered robes radiating necrotic energy.',
             in_dungeon=True, min_level=40, max_level=80, class_restrictions='Necromancer'),
        Item(name='Death\'s Embrace', item_type='Weapon', value=20000, attack_bonus=55,
             wisdom_bonus=15, mana_bonus=50, description='A weapon forged in the plane of death itself.',
             in_dungeon=True, min_level=60, max_level=100, class_restrictions='Necromancer', is_unique=True),

        # === MONK CLASS ITEMS ===
        Item(name='Wrapped Fists', item_type='Hands', value=80, attack_bonus=5,
             agility_bonus=3, dexterity_bonus=2, description='Cloth wrappings that focus your strikes.',
             in_shop=True, min_level=1, max_level=10, class_restrictions='Monk'),
        Item(name='Ki Focus Staff', item_type='Weapon', value=200, attack_bonus=12,
             agility_bonus=4, wisdom_bonus=3, description='A balanced staff for channeling ki.',
             in_shop=True, min_level=5, max_level=20, class_restrictions='Monk'),
        Item(name='Gi of the Grandmaster', item_type='Body', value=2000, armor_bonus=12,
             agility_bonus=8, dexterity_bonus=6, description='The uniform of a legendary martial artist.',
             in_shop=True, min_level=15, max_level=45, class_restrictions='Monk'),
        Item(name='Dragon Fist Wraps', item_type='Hands', value=4000, attack_bonus=20,
             agility_bonus=10, dexterity_bonus=8, strength_bonus=5,
             description='Ancient wraps that channel draconic fury.',
             in_dungeon=True, min_level=30, max_level=65, class_restrictions='Monk'),
        Item(name='Enlightened One\'s Mantle', item_type='Around Body', value=15000, armor_bonus=10,
             agility_bonus=15, wisdom_bonus=12, mana_bonus=30,
             description='A mantle worn by those who have achieved inner peace.',
             in_dungeon=True, min_level=55, max_level=100, class_restrictions='Monk', is_unique=True),

        # === WITCH HUNTER CLASS ITEMS ===
        Item(name='Silver-Edged Sword', item_type='Weapon', value=250, attack_bonus=14,
             description='A sword with a silver-coated edge for slaying the unholy.',
             in_shop=True, min_level=3, max_level=15, class_restrictions='Witch Hunter'),
        Item(name='Crossbow of Purity', item_type='Weapon', value=800, attack_bonus=22,
             dexterity_bonus=4, description='A crossbow loaded with sanctified bolts.',
             in_shop=True, min_level=8, max_level=25, class_restrictions='Witch Hunter'),
        Item(name='Inquisitor\'s Longcoat', item_type='Body', value=1500, armor_bonus=14,
             defence_bonus=5, charisma_bonus=3,
             description='The distinctive coat of a sanctioned witch hunter.',
             in_shop=True, min_level=12, max_level=40, class_restrictions='Witch Hunter'),
        Item(name='Sigil-Branded Gauntlets', item_type='Hands', value=3000, armor_bonus=8,
             strength_bonus=5, wisdom_bonus=5,
             description='Gauntlets inscribed with wards against dark magic.',
             in_dungeon=True, min_level=20, max_level=55, class_restrictions='Witch Hunter'),
        Item(name='Malleus Maleficarum', item_type='Weapon', value=18000, attack_bonus=50,
             wisdom_bonus=10, strength_bonus=10,
             description='The legendary Hammer of Witches, bane of all that is unholy.',
             in_dungeon=True, min_level=55, max_level=100, class_restrictions='Witch Hunter', is_unique=True),

        # === TIEFLING RACE ITEMS ===
        Item(name='Hellfire Circlet', item_type='Head', value=1200, armor_bonus=5,
             wisdom_bonus=6, mana_bonus=15, description='A circlet forged in infernal flames.',
             in_shop=True, min_level=10, max_level=35),
        Item(name='Tiefling Tail Ring', item_type='Fingers', value=500, agility_bonus=4,
             charisma_bonus=3, description='A ring designed to adorn a tiefling\'s tail.',
             in_shop=True, min_level=5, max_level=25),

        # === DRAGONBORN RACE ITEMS ===
        Item(name='Dragonscale Helm', item_type='Head', value=2000, armor_bonus=10,
             strength_bonus=5, defence_bonus=3,
             description='A helm fashioned from the scales of your ancestors.',
             in_shop=True, min_level=12, max_level=40),
        Item(name='Breath Focus Amulet', item_type='Neck', value=1500, attack_bonus=8,
             stamina_bonus=5, description='Focuses and enhances your draconic breath.',
             in_shop=True, min_level=8, max_level=30),

        # === FAE RACE ITEMS ===
        Item(name='Glamour Veil', item_type='Face', value=800, armor_bonus=3,
             charisma_bonus=8, description='A shimmering veil of fae illusion magic.',
             in_shop=True, min_level=5, max_level=25),
        Item(name='Moonpetal Cloak', item_type='Around Body', value=2500, armor_bonus=6,
             agility_bonus=6, mana_bonus=20, description='A cloak woven from petals that bloom under moonlight.',
             in_dungeon=True, min_level=15, max_level=45),
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
        12, 15, 18, 20,                   # 4 mid-high NPCs
        25, 30, 35, 40,                   # 4 high-level NPCs
        50, 60, 70, 80,                   # 4 very high-level NPCs
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
        # Based on original Usurper poison list from ALCHEMI.PAS
        Item(name='Snake Bite Poison', item_type='Weapon', value=1500, attack_bonus=4,
             description='A basic poison. Coats your weapon with venom.', in_shop=True,
             shop_category='alchemist', min_level=1, max_level=100,
             class_restrictions='Alchemist'),
        Item(name='Xaminah Stir', item_type='Weapon', value=11000, attack_bonus=10,
             description='A stinging poison that numbs the flesh.', in_shop=True,
             shop_category='alchemist', min_level=3, max_level=100,
             class_restrictions='Alchemist'),
        Item(name='Zargothicia', item_type='Weapon', value=25000, attack_bonus=14,
             description='A corrosive venom that eats through armor.', in_shop=True,
             shop_category='alchemist', min_level=5, max_level=100,
             class_restrictions='Alchemist'),
        Item(name='Diamond Sting', item_type='Weapon', value=100000, attack_bonus=17,
             description='An advanced poison that burns on contact.', in_shop=True,
             shop_category='alchemist', min_level=8, max_level=100,
             class_restrictions='Alchemist'),
        Item(name='Mynthia', item_type='Weapon', value=300000, attack_bonus=21,
             description='A rare poison distilled from moonflowers.', in_shop=True,
             shop_category='alchemist', min_level=12, max_level=100,
             class_restrictions='Alchemist'),
        Item(name='Exxodus', item_type='Weapon', value=550000, attack_bonus=30,
             description='A legendary toxin that attacks the nervous system.', in_shop=True,
             shop_category='alchemist', min_level=18, max_level=100,
             class_restrictions='Alchemist'),
        Item(name='Wolf Spit', item_type='Weapon', value=850000, attack_bonus=38,
             description='Extracted from dire wolves. Causes paralysis.', in_shop=True,
             shop_category='alchemist', min_level=25, max_level=100,
             class_restrictions='Alchemist'),
        Item(name='Joy of Death', item_type='Weapon', value=1250000, attack_bonus=50,
             description='A deadly poison feared across the realm.', in_shop=True,
             shop_category='alchemist', min_level=30, max_level=100,
             class_restrictions='Alchemist'),
        Item(name='Devils Cure', item_type='Weapon', value=9900000, attack_bonus=95,
             description='The most lethal poison known to alchemists.', in_shop=True,
             shop_category='alchemist', min_level=50, max_level=100,
             class_restrictions='Alchemist'),

        # === HEALING HUT (Consumables) ===
        Item(name='Cure Disease Tonic', item_type='Food', value=50,
             description='Cures disease and plague.', in_shop=True,
             shop_category='healing', min_level=1, max_level=100),
        Item(name='Antidote', item_type='Food', value=30,
             description='Cures poison.', in_shop=True,
             shop_category='healing', min_level=1, max_level=100),
        Item(name='Eye Drops', item_type='Food', value=40,
             description='Cures blindness.', in_shop=True,
             shop_category='healing', min_level=1, max_level=100),
        Item(name='Greater Healing Potion', item_type='Food', value=100, hp_bonus=80,
             description='A potent healing elixir.', in_shop=True,
             shop_category='healing', min_level=5, max_level=100),
        Item(name='Full Restoration Elixir', item_type='Food', value=300, hp_bonus=200,
             description='Fully restores health.', in_shop=True,
             shop_category='healing', min_level=10, max_level=100),

        # === GENERAL STORE (Misc equipment) ===
        Item(name='Torch', item_type='Hands', value=5, armor_bonus=0,
             description='Lights your way in the dungeon.', in_shop=True,
             shop_category='general', min_level=1, max_level=100),
        Item(name='Rope', item_type='Waist', value=10, armor_bonus=0, agility_bonus=1,
             description='Useful for climbing and escaping.', in_shop=True,
             shop_category='general', min_level=1, max_level=100),
        Item(name='Traveler\'s Pack', item_type='Around Body', value=35, armor_bonus=1,
             stamina_bonus=2, description='A sturdy pack for long journeys.', in_shop=True,
             shop_category='general', min_level=1, max_level=15),
        Item(name='Silver Mirror', item_type='Face', value=80, charisma_bonus=3,
             description='A polished mirror that reveals truth.', in_shop=True,
             shop_category='general', min_level=3, max_level=20),
        Item(name='Lucky Charm', item_type='Neck', value=200, charisma_bonus=2,
             dexterity_bonus=2, description='A rabbit\'s foot on a chain.', in_shop=True,
             shop_category='general', min_level=1, max_level=100),

        # === SHADY DEALER (Dark Alley items) ===
        Item(name='Thieves\' Dagger', item_type='Weapon', value=350, attack_bonus=12,
             dexterity_bonus=3, description='A dagger favored by cutpurses.', in_shop=True,
             shop_category='shady', min_level=3, max_level=15, evil_only=True),
        Item(name='Shadow Cloak', item_type='Around Body', value=600, armor_bonus=5,
             agility_bonus=4, description='A cloak woven from shadow threads.', in_shop=True,
             shop_category='shady', min_level=5, max_level=25, evil_only=True),
        Item(name='Cursed Ring', item_type='Fingers', value=50, strength_bonus=8,
             wisdom_bonus=-3, description='Grants power at a terrible cost.', in_shop=True,
             shop_category='shady', min_level=1, max_level=100, is_cursed=True),
        Item(name='Mask of Deception', item_type='Face', value=400, charisma_bonus=5,
             description='Hides your true identity.', in_shop=True,
             shop_category='shady', min_level=5, max_level=25),
        Item(name='Assassin\'s Blade', item_type='Weapon', value=1500, attack_bonus=28,
             dexterity_bonus=4, description='A blade made for killing.', in_shop=True,
             shop_category='shady', min_level=10, max_level=100,
             class_restrictions='Assassin'),

        # === SHADY DEALER - More dark alley items ===
        Item(name='Poisoned Dagger', item_type='Weapon', value=800, attack_bonus=15,
             dexterity_bonus=2, description='A dagger with a hollow blade filled with venom.',
             in_shop=True, shop_category='shady', min_level=5, max_level=20, evil_only=True),
        Item(name='Blackguard Armor', item_type='Body', value=2000, armor_bonus=18,
             strength_bonus=3, charisma_bonus=-2,
             description='Dark armor that inspires fear.', in_shop=True,
             shop_category='shady', min_level=12, max_level=40, evil_only=True),
        Item(name='Amulet of Shadows', item_type='Neck', value=1200, armor_bonus=2,
             agility_bonus=5, dexterity_bonus=3,
             description='An amulet that bends light around the wearer.', in_shop=True,
             shop_category='shady', min_level=8, max_level=30),
        Item(name='Garrote Wire', item_type='Hands', value=250, attack_bonus=8,
             dexterity_bonus=4, description='A tool of silent assassination.', in_shop=True,
             shop_category='shady', min_level=3, max_level=15,
             class_restrictions='Assassin'),

        # === GENERAL STORE - Additional utility items ===
        Item(name='Adventurer\'s Compass', item_type='Hands', value=150, wisdom_bonus=2,
             dexterity_bonus=1, description='Helps navigate the dungeon depths.',
             in_shop=True, shop_category='general', min_level=1, max_level=20),
        Item(name='Dungeon Map', item_type='Hands', value=75, agility_bonus=1,
             description='A rough map of the upper dungeon levels.',
             in_shop=True, shop_category='general', min_level=1, max_level=10),
        Item(name='Iron Rations', item_type='Food', value=15, stamina_bonus=1,
             hp_bonus=5, description='Dried meat and hardtack for long expeditions.',
             in_shop=True, shop_category='general', min_level=1, max_level=100),
        Item(name='Waterskin', item_type='Drink', value=10, stamina_bonus=1,
             description='Fresh water for your journey.',
             in_shop=True, shop_category='general', min_level=1, max_level=100),

        # === HEALING HUT - Additional healing items ===
        Item(name='Bandages', item_type='Food', value=10, hp_bonus=10,
             description='Simple bandages to bind wounds.',
             in_shop=True, shop_category='healing', min_level=1, max_level=100),
        Item(name='Salve of Restoration', item_type='Food', value=75,
             hp_bonus=50, description='A soothing salve that mends wounds quickly.',
             in_shop=True, shop_category='healing', min_level=3, max_level=100),
        Item(name='Elixir of Mental Clarity', item_type='Drink', value=500,
             wisdom_bonus=2, mana_bonus=30,
             description='Clears the mind and restores magical energy.',
             in_shop=True, shop_category='healing', min_level=5, max_level=100),
        Item(name='Phoenix Tears', item_type='Drink', value=2000,
             hp_bonus=500, description='Legendary tears that can heal even mortal wounds.',
             in_shop=True, shop_category='healing', min_level=20, max_level=100),

        # === MAGIC SHOP - Additional magical items ===
        Item(name='Wand of Sparks', item_type='Weapon', value=400, attack_bonus=8,
             mana_bonus=10, description='A wand that crackles with minor magic.',
             in_shop=True, shop_category='magic', min_level=1, max_level=12,
             class_restrictions='Magician,Sage,Cleric,Alchemist'),
        Item(name='Crystal Ball', item_type='Hands', value=600, wisdom_bonus=5,
             mana_bonus=15, description='Enhances magical perception.',
             in_shop=True, shop_category='magic', min_level=5, max_level=25,
             class_restrictions='Magician,Sage,Cleric'),
        Item(name='Robe of the Magi', item_type='Body', value=800, armor_bonus=5,
             wisdom_bonus=6, mana_bonus=25,
             description='Robes woven with magical thread.',
             in_shop=True, shop_category='magic', min_level=5, max_level=30,
             class_restrictions='Magician,Sage,Cleric'),
        Item(name='Spellbook of Secrets', item_type='Hands', value=2500, wisdom_bonus=10,
             mana_bonus=40, description='A tome containing arcane formulas.',
             in_shop=True, shop_category='magic', min_level=15, max_level=50,
             class_restrictions='Magician,Sage,Cleric'),

        # === PALADIN/GOOD-ONLY items ===
        Item(name='Holy Avenger', item_type='Weapon', value=5000, attack_bonus=40,
             strength_bonus=5, charisma_bonus=3,
             description='A blade blessed by the gods of light.',
             in_shop=True, shop_category='weapon', min_level=20, max_level=60,
             good_only=True, class_restrictions='Paladin'),
        Item(name='Shield of Faith', item_type='Shield', value=2000, armor_bonus=12,
             defence_bonus=5, wisdom_bonus=3,
             description='A shield that gleams with divine radiance.',
             in_shop=True, shop_category='armor', min_level=10, max_level=40,
             good_only=True),
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
