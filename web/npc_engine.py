"""NPC action engine for Usurper ReLoaded.

Handles all autonomous NPC behaviors on a regular cadence, inspired by the
original game's maintenance-based NPC system but running actions continuously
so NPCs feel more alive.

NPC action categories (each runs on its own probability per tick):
  - Experience gain & leveling
  - Equipment purchasing
  - Spell learning
  - Location changes (inn, prison, beggars' wall)
  - Crime & imprisonment
  - Bounty hunting (NPC vs player/NPC combat)
  - Team formation & management
  - Throne challenges
  - Relationship & marriage
  - Health & status maintenance
"""

import random
import logging
from datetime import datetime, timezone

from models import (
    db, Player, Item, InventoryItem, NewsEntry, Mail,
    Team, TeamMember, KingRecord, Bounty, Relationship,
    RACES, CLASSES, RACE_BONUSES, CLASS_BONUSES, LEVEL_XP,
    SPELLS, SPELLCASTER_CLASSES, EQUIPMENT_SLOTS,
)

logger = logging.getLogger(__name__)

# --------------------------------------------------------------------------- #
#  NPC Battle Phrases
# --------------------------------------------------------------------------- #

NPC_BATTLECRIES = [
    "On your knees!", "Show me your stuff!", "Hehe!",
    "Prepare to die!", "You'll regret this!", "For glory!",
    "I'll crush you!", "No mercy!", "Come and get it!",
    "You don't stand a chance!", "Feel my wrath!",
    "Time to bleed!", "I've been waiting for this!",
    "Another one bites the dust!", "Your gold is mine!",
]

NPC_VICTORY_PHRASES = [
    "Too easy!", "Another fool falls!", "I barely broke a sweat.",
    "That was fun!", "Next?", "Maybe you should try knitting instead.",
]

NPC_DEFEAT_PHRASES = [
    "I'll get you next time!", "This isn't over!",
    "Curse you!", "Lucky hit...", "I'll be back!",
]

# --------------------------------------------------------------------------- #
#  NPC Names for Generation
# --------------------------------------------------------------------------- #

NPC_FIRST_NAMES_M = [
    "Aldric", "Brom", "Cedric", "Darius", "Erik", "Finn", "Gareth",
    "Hugo", "Ivan", "Jorn", "Kael", "Leoric", "Magnus", "Nolan",
    "Orin", "Pike", "Ragnar", "Sven", "Theron", "Ulric", "Viktor",
    "Wulf", "Xander", "Yorick", "Zephyr",
]

NPC_FIRST_NAMES_F = [
    "Astrid", "Brynn", "Celeste", "Dahlia", "Elara", "Freya", "Gwen",
    "Helena", "Iris", "Jessa", "Kira", "Luna", "Mira", "Nessa",
    "Ophelia", "Petra", "Quinn", "Rowena", "Sera", "Thalia", "Una",
    "Vesper", "Wren", "Xyla", "Yara", "Zara",
]

NPC_SURNAMES = [
    "Ironforge", "Darkbane", "Stormwind", "Thornwall", "Brightblade",
    "Shadowmere", "Goldhand", "Blackthorn", "Frostborne", "Firewalker",
    "Stonefist", "Dreadmore", "Silvercrest", "Ravenclaw", "Nighthollow",
    "Steelheart", "Ashwood", "Grimshaw", "Oakenshield", "Bloodworth",
]

# --------------------------------------------------------------------------- #
#  NPC Creation
# --------------------------------------------------------------------------- #

def generate_npc_name(sex):
    """Generate a unique NPC name."""
    names = NPC_FIRST_NAMES_M if sex == 1 else NPC_FIRST_NAMES_F
    for _ in range(50):
        name = f"{random.choice(names)} {random.choice(NPC_SURNAMES)}"
        if not Player.query.filter_by(name=name).first():
            return name
    # Fallback with number suffix
    base = f"{random.choice(names)} {random.choice(NPC_SURNAMES)}"
    return f"{base} {random.randint(1, 999)}"


def create_npc(level=None):
    """Create a new NPC character with random race/class/stats.

    If *level* is given the NPC is fast-levelled to that level so it has
    appropriate stats for the game world.
    """
    import game as game_logic

    sex = random.choice([1, 2])
    race = random.choice(RACES)
    player_class = random.choice(CLASSES)

    name = generate_npc_name(sex)

    npc = Player(
        user_id=None,  # NPCs have no real user account
        name=name,
        race=race,
        player_class=player_class,
        sex=sex,
        is_npc=True,
    )
    db.session.add(npc)
    db.session.flush()  # get id

    game_logic.create_character(npc, name, race, player_class, sex)

    # Fast-level if requested
    target_level = level or 1
    while npc.level < target_level and npc.level < 30:
        # Grant enough XP, then level
        npc.experience = LEVEL_XP.get(npc.level + 1, 0)
        game_logic.level_up(npc)

    # Set NPC phrases
    npc.battlecry = random.choice(NPC_BATTLECRIES)
    npc.phrase_attacked = random.choice(NPC_DEFEAT_PHRASES)
    npc.phrase_victory = random.choice(NPC_VICTORY_PHRASES)
    npc.phrase_defeat = random.choice(NPC_DEFEAT_PHRASES)

    # Give starting gold based on level
    npc.gold = npc.level * random.randint(100, 300)
    npc.bank_gold = npc.level * random.randint(500, 1500)

    # Healing potions
    npc.healing_potions = max(5, npc.level)

    # Random alignment
    if random.random() < 0.5:
        npc.chivalry = random.randint(0, npc.level * 5)
    else:
        npc.darkness = random.randint(0, npc.level * 5)

    # NPC-specific defaults
    npc.npc_location = random.choice(['dormitory', 'inn', 'dormitory', 'dormitory'])
    npc.npc_buy_strategy = random.randint(1, 5)
    npc.npc_last_action = datetime.now(timezone.utc)

    return npc


def equip_npc_for_level(npc):
    """Give an NPC appropriate equipment for their level."""
    # Find best affordable items for each slot
    for slot in ['weapon', 'body', 'shield', 'head', 'hands', 'feet', 'arms',
                 'legs', 'waist', 'neck', 'face', 'around_body']:
        item_type_map = {
            'weapon': 'Weapon', 'body': 'Body', 'shield': 'Shield',
            'head': 'Head', 'hands': 'Hands', 'feet': 'Feet',
            'arms': 'Arms', 'legs': 'Legs', 'waist': 'Waist',
            'neck': 'Neck', 'face': 'Face', 'around_body': 'Around Body',
        }
        item_type = item_type_map.get(slot)
        if not item_type:
            continue

        # Find best item for this level
        items = Item.query.filter(
            Item.item_type == item_type,
            Item.min_level <= npc.level,
        ).order_by(
            (Item.attack_bonus + Item.armor_bonus).desc()
        ).all()

        for item in items:
            if item.can_be_used_by(npc):
                setattr(npc, f'equipped_{slot}', item.id)
                break

    npc.recalculate_equipment_power()


# --------------------------------------------------------------------------- #
#  Individual NPC Action Functions
# --------------------------------------------------------------------------- #

def npc_gain_experience(npc):
    """NPC gains experience from daily activities."""
    import game as game_logic

    xp_gain = random.randint(10, 200) * npc.level + random.randint(100, 500)
    npc.experience += xp_gain

    # Auto level-up
    leveled = False
    while npc.can_level_up() and npc.level < 30:
        game_logic.level_up(npc)
        leveled = True

    if leveled:
        news = NewsEntry(
            player_id=npc.id,
            category='general',
            message=f"{npc.name} has reached level {npc.level}!"
        )
        db.session.add(news)

    return leveled


def npc_buy_equipment(npc):
    """NPC purchases equipment from shops based on buy strategy.

    Strategy 1 = rarely buys, 5 = always buys.
    """
    if random.randint(1, 5) > npc.npc_buy_strategy:
        return False

    bought_something = False
    slot_order = ['weapon', 'body', 'shield', 'head', 'hands', 'feet',
                  'arms', 'legs', 'waist', 'neck', 'face', 'around_body']

    for slot in slot_order:
        if random.randint(0, 2) != 0:  # 1/3 chance per slot
            continue

        item_type_map = {
            'weapon': 'Weapon', 'body': 'Body', 'shield': 'Shield',
            'head': 'Head', 'hands': 'Hands', 'feet': 'Feet',
            'arms': 'Arms', 'legs': 'Legs', 'waist': 'Waist',
            'neck': 'Neck', 'face': 'Face', 'around_body': 'Around Body',
        }
        item_type = item_type_map.get(slot)
        if not item_type:
            continue

        current_item_id = getattr(npc, f'equipped_{slot}', None)
        current_power = 0
        if current_item_id:
            current_item = db.session.get(Item, current_item_id)
            if current_item:
                current_power = current_item.attack_bonus + current_item.armor_bonus

        # Find a better shop item
        candidates = Item.query.filter(
            Item.item_type == item_type,
            Item.in_shop == True,
            Item.min_level <= npc.level,
            Item.value <= npc.gold + npc.bank_gold,
        ).order_by(
            (Item.attack_bonus + Item.armor_bonus).desc()
        ).all()

        for item in candidates:
            item_power = item.attack_bonus + item.armor_bonus
            if item_power > current_power and item.can_be_used_by(npc):
                # Pay for it - withdraw from bank if needed
                cost = item.value
                if npc.gold < cost:
                    deficit = cost - npc.gold
                    if npc.bank_gold >= deficit:
                        npc.bank_gold -= deficit
                        npc.gold += deficit
                    else:
                        continue

                npc.gold -= cost
                setattr(npc, f'equipped_{slot}', item.id)
                bought_something = True

                news = NewsEntry(
                    player_id=npc.id,
                    category='general',
                    message=f"{npc.name} purchased a {item.name} from the shop."
                )
                db.session.add(news)
                break

    if bought_something:
        npc.recalculate_equipment_power()
    return bought_something


def npc_learn_spells(npc):
    """NPC learns spells appropriate for their class and level."""
    if npc.player_class not in SPELLCASTER_CLASSES:
        return False

    learned = False
    for spell_id, spell in SPELLS.items():
        if (spell['min_level'] <= npc.level and
                npc.player_class in spell['classes'] and
                not npc.knows_spell(spell_id)):
            npc.learn_spell(spell_id)
            # Also ensure NPC has enough mana
            npc.max_mana = max(npc.max_mana, npc.level * 30)
            npc.mana = npc.max_mana
            learned = True

    return learned


def npc_change_location(npc):
    """NPC randomly moves between town locations."""
    if npc.npc_location == 'prison':
        npc.npc_days_in_prison -= 1
        if npc.npc_days_in_prison <= 0:
            npc.npc_location = 'dormitory'
            npc.is_imprisoned = False
            npc.npc_days_in_prison = 0
            news = NewsEntry(
                player_id=npc.id,
                category='general',
                message=f"{npc.name} has been released from prison."
            )
            db.session.add(news)
        return

    # Random location changes
    roll = random.randint(1, 20)
    if roll <= 3:  # 15% chance to go to inn
        npc.npc_location = 'inn'
    elif roll == 4:  # 5% chance to go to beggars' wall
        npc.npc_location = 'beggar_wall'
    else:
        npc.npc_location = 'dormitory'

    # Random crime (for evil-leaning NPCs)
    if npc.darkness > npc.chivalry and random.randint(1, 15) == 1:
        crimes = ['vagrancy', 'theft', 'drunkenness', 'witchcraft', 'fraud']
        crime = random.choice(crimes)
        days = random.randint(1, 3)
        npc.npc_location = 'prison'
        npc.is_imprisoned = True
        npc.npc_days_in_prison = days

        news = NewsEntry(
            player_id=npc.id,
            category='general',
            message=f"{npc.name} has been arrested for {crime} and sentenced to {days} day(s) in prison!"
        )
        db.session.add(news)


def npc_hunt_bounty(npc):
    """NPC attempts to collect bounties on wanted players."""
    if npc.is_imprisoned or npc.hp < npc.max_hp // 2:
        return False

    # Find unclaimed bounties worth pursuing
    bounties = Bounty.query.filter_by(claimed=False).filter(
        Bounty.amount >= 100,
        Bounty.target_id != npc.id
    ).all()

    if not bounties:
        return False

    # Pick a random bounty to pursue
    if random.randint(1, 5) != 1:  # 20% chance to pursue
        return False

    bounty = random.choice(bounties)
    target = db.session.get(Player, bounty.target_id)
    if not target or target.is_imprisoned:
        return False

    # Level difference check - NPC won't attack much stronger targets
    if target.level > npc.level + 5:
        return False

    # Simulate NPC vs target combat
    winner, loser, log = _npc_vs_player_combat(npc, target)

    if winner and winner.id == npc.id:
        # NPC collects bounties
        total_bounty = 0
        target_bounties = Bounty.query.filter_by(
            target_id=target.id, claimed=False
        ).all()
        for b in target_bounties:
            b.claimed = True
            b.claimed_by_id = npc.id
            total_bounty += b.amount

        npc.bank_gold += total_bounty

        news = NewsEntry(
            player_id=npc.id,
            category='combat',
            message=f"Bounty hunter {npc.name} tracked down {target.name} and collected {total_bounty} gold in bounties!"
        )
        db.session.add(news)

        # Notify target via mail
        mail = Mail(
            sender_id=npc.id,
            receiver_id=target.id,
            subject="Bounty Collected!",
            message=f"{npc.name} hunted you down and collected the bounty on your head!"
        )
        db.session.add(mail)
        return True

    return False


def npc_manage_team(npc):
    """NPC joins or creates teams."""
    if npc.is_imprisoned:
        return False

    membership = TeamMember.query.filter_by(player_id=npc.id).first()

    if membership:
        # Already in a team - small chance to leave if team is struggling
        team = membership.team
        if team.losses > team.wins * 2 and random.randint(1, 10) == 1:
            db.session.delete(membership)
            npc.team_name = ''
            # Check if team needs cleanup
            remaining = TeamMember.query.filter_by(team_id=team.id).count()
            if remaining == 0:
                db.session.delete(team)
            elif team.leader_id == npc.id:
                new_leader = TeamMember.query.filter_by(team_id=team.id).first()
                if new_leader:
                    team.leader_id = new_leader.player_id
            return True
        return False

    # Not in a team - consider joining or creating one
    if random.randint(1, 8) != 1:  # Low chance per tick
        return False

    # Try to join an existing NPC-friendly team
    available_teams = Team.query.all()
    for team in available_teams:
        if team.member_count() < 5:
            member = TeamMember(team_id=team.id, player_id=npc.id)
            db.session.add(member)
            npc.team_name = team.name

            news = NewsEntry(
                player_id=npc.id,
                category='social',
                message=f"{npc.name} has joined the team '{team.name}'."
            )
            db.session.add(news)
            return True

    # No teams to join - maybe create one
    if random.randint(1, 3) == 1:
        team_prefixes = ["The", "Clan", "Order of", "Brotherhood of", "Band of"]
        team_suffixes = [
            "Wolves", "Dragons", "Shadows", "Thorns", "Iron",
            "Serpents", "Ravens", "Lions", "Vipers", "Phoenix",
        ]
        team_name = f"{random.choice(team_prefixes)} {random.choice(team_suffixes)}"

        existing = Team.query.filter_by(name=team_name).first()
        if not existing:
            team = Team(name=team_name, leader_id=npc.id)
            db.session.add(team)
            db.session.flush()
            member = TeamMember(team_id=team.id, player_id=npc.id)
            db.session.add(member)
            npc.team_name = team_name

            news = NewsEntry(
                player_id=npc.id,
                category='social',
                message=f"{npc.name} has founded the team '{team_name}'!"
            )
            db.session.add(news)
            return True

    return False


def npc_challenge_throne(npc):
    """NPC attempts to challenge and usurp the throne."""
    if npc.is_imprisoned or npc.is_king:
        return False

    if npc.level < 5:
        return False

    if npc.hp < npc.max_hp // 2:
        return False

    # Low probability per tick
    if random.randint(1, 20) != 1:
        return False

    king_record = KingRecord.query.filter_by(is_current=True).first()

    if not king_record:
        # No king - claim the throne
        npc.is_king = True
        record = KingRecord(
            player_id=npc.id,
            moat_guards=5,
            tax_rate=5,
            treasury=0
        )
        db.session.add(record)

        title = 'King' if npc.sex == 1 else 'Queen'
        news = NewsEntry(
            player_id=npc.id,
            category='royal',
            message=f"All hail {npc.name}, the new {title} of the realm!"
        )
        db.session.add(news)
        return True

    king = db.session.get(Player, king_record.player_id)
    if not king:
        return False

    # Don't attack spouse
    if npc.married and npc.spouse_id == king.id:
        return False

    # Check if NPC is strong enough relative to king
    if npc.level < king.level - 3:
        return False

    # Fight through moat guards
    npc_hp = npc.max_hp
    guards = king_record.moat_guards

    for _ in range(guards):
        guard_hp = 30 + king.level * 5
        while guard_hp > 0 and npc_hp > 0:
            # NPC attacks guard
            from game import calculate_attack, calculate_defense
            atk = calculate_attack(npc.strength, npc.weapon_power, npc.level)
            guard_def = 5 + king.level * 2
            dmg = max(1, atk - guard_def)
            guard_hp -= dmg

            if guard_hp <= 0:
                break

            # Guard attacks NPC
            guard_atk = 8 + king.level * 3
            pdef = calculate_defense(npc.defence, npc.armor_power)
            gdmg = max(1, guard_atk - pdef)
            npc_hp -= gdmg

    if npc_hp <= 0:
        news = NewsEntry(
            player_id=npc.id,
            category='royal',
            message=f"{npc.name} attempted to storm the castle but was defeated by the moat guards!"
        )
        db.session.add(news)
        npc.hp = max(1, npc.max_hp // 4)
        return False

    # Fight the king
    king_hp = king.max_hp
    rounds = 0
    while king_hp > 0 and npc_hp > 0 and rounds < 20:
        rounds += 1
        from game import calculate_attack, calculate_defense

        # NPC attacks
        atk = calculate_attack(npc.strength, npc.weapon_power, npc.level)
        kdef = calculate_defense(king.defence, king.armor_power)
        dmg = max(1, atk - kdef)
        king_hp -= dmg

        if king_hp <= 0:
            break

        # King attacks
        katk = calculate_attack(king.strength, king.weapon_power, king.level)
        ndef = calculate_defense(npc.defence, npc.armor_power)
        kdmg = max(1, katk - ndef)
        npc_hp -= kdmg

    if king_hp <= 0:
        # NPC wins the throne!
        from game import dethrone_king
        dethrone_king(king, king_record)

        npc.is_king = True
        new_record = KingRecord(
            player_id=npc.id,
            moat_guards=5,
            tax_rate=5,
            treasury=0
        )
        db.session.add(new_record)
        npc.hp = max(1, npc_hp)

        title = 'King' if npc.sex == 1 else 'Queen'
        news = NewsEntry(
            player_id=npc.id,
            category='royal',
            message=f"{npc.name} has defeated {king.name} and claimed the throne! All hail {title} {npc.name}!"
        )
        db.session.add(news)

        # Notify dethroned king
        if not king.is_npc:
            mail = Mail(
                sender_id=npc.id,
                receiver_id=king.id,
                subject="You have been dethroned!",
                message=f"{npc.name} has challenged you for the throne and won! You are no longer the ruler."
            )
            db.session.add(mail)

        return True
    else:
        npc.hp = max(1, npc.max_hp // 4)
        news = NewsEntry(
            player_id=npc.id,
            category='royal',
            message=f"{npc.name} challenged {king.name} for the throne and lost!"
        )
        db.session.add(news)
        return False


def npc_manage_relationships(npc):
    """NPC forms relationships and potentially marries."""
    if npc.is_imprisoned:
        return False

    if random.randint(1, 12) != 1:
        return False

    if npc.married:
        # Small chance of divorce
        if random.randint(1, 50) == 1:
            spouse = db.session.get(Player, npc.spouse_id)
            if spouse:
                spouse.married = False
                spouse.spouse_id = None

                if not spouse.is_npc:
                    mail = Mail(
                        sender_id=npc.id,
                        receiver_id=spouse.id,
                        subject="Divorce",
                        message=f"{npc.name} has divorced you."
                    )
                    db.session.add(mail)

            npc.married = False
            old_name = spouse.name if spouse else "unknown"
            npc.spouse_id = None

            Relationship.query.filter(
                ((Relationship.player1_id == npc.id) | (Relationship.player2_id == npc.id)),
                Relationship.rel_type == 'married'
            ).delete(synchronize_session=False)

            news = NewsEntry(
                player_id=npc.id,
                category='social',
                message=f"{npc.name} and {old_name} have divorced!"
            )
            db.session.add(news)
            return True
        return False

    # Try to marry another NPC
    candidates = Player.query.filter(
        Player.is_npc == True,
        Player.id != npc.id,
        Player.married == False,
        Player.is_imprisoned == False,
    ).all()

    if not candidates:
        return False

    target = random.choice(candidates)

    # Check no existing relationship conflict
    existing = Relationship.query.filter(
        ((Relationship.player1_id == npc.id) & (Relationship.player2_id == target.id)) |
        ((Relationship.player1_id == target.id) & (Relationship.player2_id == npc.id))
    ).first()
    if existing:
        return False

    # NPC-NPC marriage happens instantly
    npc.married = True
    npc.spouse_id = target.id
    target.married = True
    target.spouse_id = npc.id

    rel = Relationship(
        player1_id=npc.id,
        player2_id=target.id,
        rel_type='married'
    )
    db.session.add(rel)

    news = NewsEntry(
        player_id=npc.id,
        category='social',
        message=f"{npc.name} and {target.name} have been married!"
    )
    db.session.add(news)
    return True


def npc_heal_and_maintain(npc):
    """NPC heals, cures diseases, manages gold."""
    # Heal to full between actions
    if npc.hp < npc.max_hp:
        npc.hp = npc.max_hp
    if npc.mana < npc.max_mana:
        npc.mana = npc.max_mana

    # Cure diseases
    npc.is_poisoned = False
    npc.is_blind = False
    npc.has_plague = False

    # Ensure NPC has enough gold
    if npc.gold <= 0:
        npc.gold = npc.level * 200

    # Replenish potions
    if npc.healing_potions < 5:
        npc.healing_potions = max(5, npc.level)

    # Bank interest
    if npc.bank_gold > 0:
        interest = max(1, npc.bank_gold // 100)
        npc.bank_gold += interest

    # Reset daily limits
    npc.fights_remaining = 20
    npc.player_fights = 3
    npc.brawls_remaining = 2
    npc.thefts_remaining = 2


def npc_initiate_pvp(npc):
    """NPC may randomly attack other players (human or NPC) in dormitory combat."""
    if npc.is_imprisoned or npc.hp < npc.max_hp // 2:
        return False

    if random.randint(1, 10) != 1:  # 10% chance per tick
        return False

    # Find potential targets (not self, not imprisoned, not spouse)
    targets = Player.query.filter(
        Player.id != npc.id,
        Player.is_imprisoned == False,
        Player.level >= max(1, npc.level - 5),
        Player.level <= npc.level + 5,
    ).all()

    if not targets:
        return False

    target = random.choice(targets)

    # Don't fight spouse
    if npc.married and npc.spouse_id == target.id:
        return False

    winner, loser, log = _npc_vs_player_combat(npc, target)

    if winner and loser:
        # Transfer gold
        gold_stolen = min(loser.gold, max(1, loser.gold // 5 + random.randint(0, 50)))
        winner.gold += gold_stolen
        loser.gold = max(0, loser.gold - gold_stolen)

        # XP for winner
        xp_gain = max(10, loser.level * 20)
        winner.experience += xp_gain
        winner.player_kills += 1
        loser.player_defeats += 1

        news = NewsEntry(
            player_id=winner.id,
            category='combat',
            message=f"{winner.name} defeated {loser.name} in combat!"
        )
        db.session.add(news)

        # Notify human players via mail
        if loser and not loser.is_npc:
            mail = Mail(
                sender_id=winner.id,
                receiver_id=loser.id,
                subject="You were attacked!",
                message=f"{winner.name} attacked you and won, stealing {gold_stolen} gold!"
            )
            db.session.add(mail)

        return True

    return False


# --------------------------------------------------------------------------- #
#  NPC Combat Simulation (NPC vs Player/NPC)
# --------------------------------------------------------------------------- #

def _npc_vs_player_combat(attacker, defender):
    """Simulate combat between two characters (NPC-initiated).

    Returns (winner, loser, combat_log).  Winner/loser may be *None* on draw.
    """
    from game import calculate_attack, calculate_defense

    log = []
    atk_hp = attacker.max_hp
    def_hp = defender.max_hp
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
            log.append(f"**Critical!** {attacker.name} strikes for {dmg} damage!")
        else:
            log.append(f"{attacker.name} attacks for {dmg} damage.")
        def_hp -= dmg

        if def_hp <= 0:
            log.append(f"{defender.name} has been defeated!")
            break

        # Defender strikes
        datk = calculate_attack(defender.strength, defender.weapon_power, defender.level)
        adef = calculate_defense(attacker.defence, attacker.armor_power)
        ddmg = max(1, datk - adef)

        if random.randint(1, 100) <= 5 + defender.dexterity // 3:
            ddmg = int(ddmg * 1.5)
            log.append(f"**Critical!** {defender.name} strikes for {ddmg} damage!")
        else:
            log.append(f"{defender.name} attacks for {ddmg} damage.")
        atk_hp -= ddmg

        if atk_hp <= 0:
            log.append(f"{attacker.name} has been defeated!")
            break

    if def_hp <= 0:
        return attacker, defender, log
    elif atk_hp <= 0:
        return defender, attacker, log
    else:
        return None, None, log


# --------------------------------------------------------------------------- #
#  Main Tick Function  –  called by the scheduler
# --------------------------------------------------------------------------- #

def run_npc_tick():
    """Execute one tick of NPC actions for all active NPCs.

    This is the main entry point called by the scheduler on a regular cadence
    (e.g., every 5 minutes).  Each NPC has a probability-weighted chance to
    perform various actions each tick, simulating the original game's daily
    maintenance but spread across the day.
    """
    npcs = Player.query.filter_by(is_npc=True).all()

    if not npcs:
        return

    actions_taken = 0

    for npc in npcs:
        try:
            # Always heal/maintain first
            npc_heal_and_maintain(npc)

            # Weighted random actions - not all happen every tick
            if random.randint(1, 3) == 1:
                if npc_gain_experience(npc):
                    actions_taken += 1

            if random.randint(1, 4) == 1:
                if npc_buy_equipment(npc):
                    actions_taken += 1

            if random.randint(1, 6) == 1:
                npc_learn_spells(npc)

            if random.randint(1, 4) == 1:
                npc_change_location(npc)

            if random.randint(1, 6) == 1:
                if npc_hunt_bounty(npc):
                    actions_taken += 1

            if random.randint(1, 8) == 1:
                if npc_manage_team(npc):
                    actions_taken += 1

            if random.randint(1, 12) == 1:
                if npc_challenge_throne(npc):
                    actions_taken += 1

            if random.randint(1, 10) == 1:
                if npc_manage_relationships(npc):
                    actions_taken += 1

            if random.randint(1, 8) == 1:
                if npc_initiate_pvp(npc):
                    actions_taken += 1

            npc.npc_last_action = datetime.now(timezone.utc)

        except Exception:
            logger.exception("Error processing NPC %s (id=%s)", npc.name, npc.id)
            continue

    try:
        db.session.commit()
    except Exception:
        logger.exception("Error committing NPC tick")
        db.session.rollback()

    if actions_taken > 0:
        logger.info("NPC tick complete: %d actions taken across %d NPCs",
                     actions_taken, len(npcs))
