CASUALTY = "8"
BLOCK = "5"
ARMOUR = "3"

IGNORED_ACTIONS = [
    "fan_attendance",
    "weather",
    "halfing_chef",
    "kickoff",
    "kickoff_gust",
    "ignored",
    "foul",
    "throw_in",
    "inaccurate_pass",
]

# Rolltype -> Action
ROLL_TO_ACTION = {
    "1": "gfi",
    "2": "dodge",
    "3": "armour",
    "4": "injury",
    "5": "block",
    "6": "stand_up",
    "7": "pickup",
    "8": "casualty",
    "9": "catch",
    "10": "kickoff",
    "11": "throw_in",
    "12": "pass",
    "15": "foul",  # Useless since armour is roll on a separate event
    "16": "intercept",
    "17": "wake_up_ko",
    "20": "bone_head",
    "21": "really_stupid",
    "22": "wild_animal",
    "23": "loner",
    "24": "landing",
    "25": "regeneration",
    "26": "inaccurate_pass",  # Inaccurate Pass scatter
    "27": "always_hungry",
    "28": "snack",
    "29": "dauntless",
    "31": "jump_up",
    "32": "shadowing",
    "34": "stab",
    "36": "leap",
    "39": "chainsaw",
    "37": "foul_appearance",
    "38": "tentacles",
    "40": "take_root",
    "41": "ignored",  # Fanatic Movement
    "44": "ignored",  # FIXME Diving Tackle?
    "45": "pro",
    "46": "hypnotic_gaze",
    "49": "animosity",
    "50": "bloodlust",
    "52": "bribe",
    "53": "halfing_chef",
    "54": "fireball",
    "55": "lightning_bolt",
    "56": "throw_team_mate",
    "58": "kickoff_gust",
    "59": "ignored",  # FIXME Piling On Armour?
    "60": "ignored",  # FIXME Piling On Injury?
    "61": "ignored",  # FIXME Diving Catch?
    "62": "ignored",  # FIXME DS -> P through Dodge?
    "63": "ignored",  # FIXME Stand Firm?
    "64": "ignored",  # FIXME Juggernaut?
    "69": "fan_attendance",
    "70": "weather",
    "72": "impact_of_the_bomb",
    "71": "sweltering_heat",
    "73": "ignored",  # FIXME Chainsaw armour roll
}

BLOCK_SYMBOL = {
    "0": "AD",
    "1": "BD",
    "2": "P",
    "3": "DS",
    "4": "DD",
}

# Not used
SKILLS = {
    "30": "block",
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
