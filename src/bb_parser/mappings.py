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
    54: "fireball",
    55: "lightning_bolt",
    27: "ignored",  # Always Hungry
    32: "ignored",  # Shadowing
    34: "ignored",  # Stab
    37: "ignored",  # Foul Appearance
    38: "ignored",  # Tentacles
    39: "ignored",  # Chainsaw
    41: "ignored",  # Fanatic Movement
    44: "ignored",  # FIXME Diving Tacle?
    45: "ignored",  # Pro
    46: "ignored",  # Hypnotic Gaze
    50: "ignored",  # Bloodlust
    52: "ignored",  # Bribe
    59: "ignored",  # Piling On Armour
    60: "ignored",  # Piling On Injury
    61: "ignored",  # Diving Catch
    71: "ignored",  # Sweltering Heat
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
