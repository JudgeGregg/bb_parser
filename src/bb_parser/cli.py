#!/usr/bin/python
import sys
import pprint
from pathlib import Path
import logging

from .main import Replayer


def main():
    logging.basicConfig(level=logging.DEBUG)
    for file_ in sys.argv[1:]:
        print("FILENAME:")
        print(file_)
        file_path = Path(file_)
        replayer = Replayer()
        stats = replayer.parse_replay(file_path)
        pprint.pprint(stats, compact=True, width=179)


def display_stats(stats):
    for team in stats:
        print("="*77)
        print(team)
        print("="*77)
        print("GFI")
        print(stats[team]["gfi"])
        print("ARMOUR")
        print(stats[team]["armour"])
        print("TOTAL ARMOURS:")
        total_armours = []
        for rolls in stats[team]["armour"].values():
            for roll in rolls:
                total_armours.append(roll)
        print(len(total_armours))
        print("INJURY")
        print(stats[team]["injury"])
        print("CASUALTY")
        print(stats[team]["casualty"])
        print("WAKE UP KO")
        print(stats[team]["wake_up_ko"])
        print("DODGE")
        print(stats[team]["dodge"])
        print("PICKUP")
        print(stats[team]["pickup"])
        print("PASS")
        print(stats[team]["pass"])
        print("CATCH")
        print(stats[team]["catch"])
        print("INTERCEPT")
        print(stats[team]["intercept"])
        print("LANDING")
        print(stats[team]["landing"])
        print("TTM")
        print(stats[team]["throw_team_mate"])
        print("BLOCK DICE")
        print(stats[team]["block"])
        print("BLOCK DICE DISTRIBUTION")
        print(stats[team]["blocks"])
        print("TOTAL BLOCKS")
        total_blocks = 0
        for rolls in stats[team]["blocks"].values():
            total_blocks += rolls
        print(total_blocks)
        print("BLOCKS PER PLAYER")
        for player_name, roll_hist in stats[team]["players"].items():
            print(player_name, roll_hist)
        print("D6 DICE DISTRIBUTION")
        print(stats[team]["dice"])
