CASUALTY = 8
BLOCK = 5
ARMOUR = 3
DODGE = 2

# Rolltype -> Action
ROLL_TO_ACTION = {
    1: "gfi",
    15: "foul",  # Useless since armour is roll on a separate event
    22: "wild_animal",
    2: "dodge",
    69: "fan_attendance",
    70: "weather",
    53: "halfing_chef",
    10: "kickoff",
    5: "block",
    3: "armour",
    4: "injury",
    6: "stand_up",
    7: "pickup",
    8: "casualty",
    9: "catch",
    12: "pass_",
    16: "intercept",
    21: "really_stupid",
    23: "loner",
    26: "inaccurate_pass",  # Inaccurate Pass scatter
    17: "wake_up_ko",
    11: "throw_in",
    56: "throw_team_mate",
    24: "landing",
    58: "kickoff_gust",
    20: "bone_head",
    29: "dauntless",
    31: "jump_up",
    36: "leap",
    40: "take_root",
    72: "impact_of_the_bomb",
    25: "regeneration",
    49: "animosity",
    54: "fireball",
    55: "lightning_bolt",
    27: "always_hungry",
    32: "shadowing",
    34: "stab",
    37: "foul_appearance",
    38: "tentacles",
    46: "hypnotic_gaze",
    50: "bloodlust",
    39: "chainsaw",
    52: "bribe",
    71: "sweltering_heat",
    45: "pro",
    41: "ignored",  # Fanatic Movement
    44: "ignored",  # FIXME Diving Tackle?
    59: "ignored",  # Piling On Armour
    60: "ignored",  # Piling On Injury
    61: "ignored",  # Diving Catch
    73: "ignored",  # Chainsaw armour roll
    62: "ignored",  # FIXME DS -> P through Dodge?
    63: "ignored",  # FIXME???
    64: "ignored",  # FIXME???
}

BLOCK_SYMBOL = {
    "0": "AD",
    "1": "BD",
    "2": "P",
    "3": "DS",
    "4": "DD",
}


SKILLS = {
    30: "block",
}

ID_RACE_TO_NAME = {
    "1": "Humans",
    "2": "Dwarfs",
    "3": "Skavens",
    "4": "Orcs",
    "5": "Lizardmen",
    "6": "Goblins",
    "7": "Wood Elves",
    "8": "Chaos",
    "9": "Dark Elves",
    "10": "Undead",
    "11": "Halflings",
    "12": "Norse",
    "13": "Amazons",
    "14": "Elven Union",
    "15": "High Elves",
    "16": "Khemri",
    "17": "Necromantic",
    "18": "Nurgle",
    "19": "Ogres",
    "20": "Vampires",
    "21": "Chaos Dwarfs",
    "22": "Underworld Denizens",
    "24": "Bretonnians",
    "25": "Kislev Circus",
}
