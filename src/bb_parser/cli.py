#!/usr/bin/python
import sys
import pprint
import json
from pathlib import Path
import logging
import getopt

from .main import Replayer

# Options
options = "hdp"

# Long options
long_options = ["help", "debug", "pretty"]

help_message = """
Usage:
bb2_parser [-d] [-p] [-h] path_to_replay_file1_bbrz path_to_replay_file2_bbrz …

Outputs stats as a json object

-d, --debug adds debugging info
-p, --pretty pretty prints stats dict
-h, --help shows this message and exits
"""


def main():
    argument_list = sys.argv[1:]
    pretty = False
    log = logging.getLogger("bb_parser")
    try:
        arguments, values = getopt.getopt(argument_list, options, long_options)
        for argument, value in arguments:
            if argument in ("-h", "--help"):
                print(help_message)
                sys.exit(0)
            elif argument in ("-d", "--debug"):
                logging.basicConfig(level=logging.DEBUG)
            if argument in ("-p", "--pretty"):
                pretty = True
    except getopt.error as err:
        print(err)
        print(help_message)
        sys.exit(1)
    for file_ in values:
        log.debug("FILENAME:")
        log.debug(file_)
        file_path = Path(file_)
        replayer = Replayer()
        stats = replayer.parse_replay(file_path)
        if pretty:
            pprint.pprint(stats, compact=True, width=179)
        else:
            print(json.dumps(stats))


def display_stats(stats):
    for team in stats:
        if team == "date":
            continue
        print("=" * 77)
        print(team)
        print("=" * 77)
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
