#!/usr/bin/python
import sys
import zipfile
from pathlib import Path
from io import TextIOWrapper

from lxml import etree

from bb_parser.result import Parser
from bb_parser.mappings import ROLL_TO_ACTION
from bb_parser.stats import Stats


def main():
    for file_ in sys.argv[1:]:
        print("FILENAME:")
        print(file_)
        file_path = Path(file_)
        with zipfile.ZipFile(file_path) as bb_zip:
            with bb_zip.open(file_path.stem) as bb_file:
                text = TextIOWrapper(bb_file, encoding="utf-8")
                replayer = Replayer()
                replayer.parse_replay(text)


class Replayer():

    def parse_replay(self, replay_file):
        self.parser = Parser()
        root = etree.fromstring(replay_file.read())
        teams = self.parse_game_infos(root)
        self.stats = Stats(teams)
        self.parse_events(root)
        self.display_stats()

    def parse_events(self, root):
        for event in root.iter(
                "RulesEventBoardAction", "RulesEventKickOffTable"):
            if event.tag == "RulesEventKickOffTable":
                pass
            else:
                self.parse_board_action(event)

    def parse_game_infos(self, root):
        game_infos = root.find("./ReplayStep/GameInfos")
        coaches_infos = game_infos.findall("CoachesInfos/CoachInfos")
        print("Coaches:")
        for coach in coaches_infos:
            print(coach.findtext(".//Login"))
        teams = []
        teams_elem = game_infos.getparent().findall(".//TeamState/Data/Name")
        for team in teams_elem:
            teams.append(team.text)
        print(teams)
        return teams

    def display_stats(self):
        for team in self.stats.stats:
            print("="*77)
            print(team)
            print("="*77)
            print("GFI")
            print(self.stats.stats[team]["gfi"])
            print("ARMOUR")
            print(self.stats.stats[team]["armour"])
            print("TOTAL ARMOURS:")
            total_armours = []
            for rolls in self.stats.stats[team]["armour"].values():
                for roll in rolls:
                    total_armours.append(roll)
            print(len(total_armours))
            print("INJURY")
            print(self.stats.stats[team]["injury"])
            print("CASUALTY")
            print(self.stats.stats[team]["casualty"])
            print("WAKE UP KO")
            print(self.stats.stats[team]["wake_up_ko"])
            print("DODGE")
            print(self.stats.stats[team]["dodge"])
            print("PICKUP")
            print(self.stats.stats[team]["pickup"])
            print("PASS")
            print(self.stats.stats[team]["pass"])
            print("CATCH")
            print(self.stats.stats[team]["catch"])
            print("INTERCEPT")
            print(self.stats.stats[team]["intercept"])
            print("LANDING")
            print(self.stats.stats[team]["landing"])
            print("TTM")
            print(self.stats.stats[team]["throw_team_mate"])
            print("BLOCK DICE")
            print(self.stats.stats[team]["block"])
            print("BLOCK DICE DISTRIBUTION")
            print(self.stats.stats[team]["blocks"])
            print("TOTAL BLOCKS")
            total_blocks = 0
            for rolls in self.stats.stats[team]["blocks"].values():
                total_blocks += rolls
            print(total_blocks)
            print("BLOCKS PER PLAYER")
            for player_name, roll_hist in self.stats.stats[team]["players"].items():
                print(player_name, roll_hist)
            print("D6 DICE DISTRIBUTION")
            print(self.stats.stats[team]["dice"])

    def parse_board_action(self, event):
        # Is there a dice roll in this action?
        for action_res in event.iter("BoardActionResult"):
            dices = action_res.find(".//ListDices")
            if dices is not None:
                actor = self.parser.get_team_and_turn(event)
                rolltype = action_res.find("./RollType")
                rolltype = int(rolltype.text)
                self.__getattribute__(ROLL_TO_ACTION[rolltype])(
                    action_res, actor)

    def dodge(self, action_res, actor):
        print("dodge")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_dodge(result, actor)

    def fan_attendance(self, action_res, player_id):
        print("fan_attendance")
        _ = self.parser.get_result(action_res)

    def weather(self, action_res, player_id):
        print("weather")
        _ = self.parser.get_result(action_res)

    def halfing_chef(self, action_res, player_id):
        print("halfing_chef")
        _ = self.parser.get_result(action_res)

    def kickoff(self, action_res, player_id):
        print("kickoff")
        _ = self.parser.get_result(action_res)

    def block(self, action_res, actor):
        print("block")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_block(result, actor)

    def pickup(self, action_res, actor):
        print("pickup")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_pickup(result, actor)

    def foul(self, action_res, actor):
        print("foul")
        # Ignore foul, since armour and injury have regular rolls

    def armour(self, action_res, actor):
        print("armour")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_armour(result, actor)

    def injury(self, action_res, actor):
        print("injury")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_injury(result, actor)

    def casualty(self, action_res, actor):
        print("casualty")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_casualty(result, actor)

    def gfi(self, action_res, actor):
        print("gfi")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_gfi(result, actor)

    def pass_(self, action_res, actor):
        print("pass")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_pass(result, actor)

    def catch(self, action_res, actor):
        print("catch")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_catch(result, actor)

    def throw_team_mate(self, action_res, actor):
        print("throw_team_mate")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_throw_team_mate(result, actor)

    def landing(self, action_res, actor):
        print("landing")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_landing(result, actor)

    def intercept(self, action_res, actor):
        print("intercept")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_intercept(result, actor)

    def jump_up(self, action_res, actor):
        print("jump up")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_jump_up(result, actor)

    def leap(self, action_res, actor):
        print("leap")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_leap(result, actor)

    def loner(self, action_res, actor):
        print("loner")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_loner(result, actor)

    def wake_up_ko(self, action_res, actor):
        print("wake_up_ko")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_wake_up_ko(result, actor)

    def throw_in(self, action_res, player_id):
        pass

    def kickoff_gust(self, action_res, player_id):
        pass

    def ignored(self, action_res, player_id):
        pass

    def bone_head(self, action_res, actor):
        print("bone_head")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_bone_head(result, actor)

    def wild_animal(self, action_res, actor):
        print("wild_animal")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_wild_animal(result, actor)

    def really_stupid(self, action_res, actor):
        print("really_stupid")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_really_stupid(result, actor)

    def take_root(self, action_res, actor):
        print("take_root")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_take_root(result, actor)

    def dauntless(self, action_res, actor):
        print("dauntless")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_dauntless(result, actor)

    def impact_of_the_bomb(self, action_res, actor):
        print("impact_of_the_bomb")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_impact_of_the_bomb(result, actor)

    def regeneration(self, action_res, actor):
        print("regeneration")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_regeneration(result, actor)

    def fireball(self, action_res, actor):
        print("fireball")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_fireball(result, actor)

    def lightning_bolt(self, action_res, actor):
        print("lightning_bolt")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_lightning_bolt(result, actor)

    def stand_up(self, action_res, player_id):
        pass

    def inaccurate_pass(self, action_res, actor):
        # These are recorded in game whereas they're 8 sided rolls??
        pass


if __name__ == "__main__":
    main()
