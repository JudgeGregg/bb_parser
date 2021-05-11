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
    file_path = Path(sys.argv[1])
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
        self.parse_fans_and_weather(root)
        for event in root.iter("RulesEventBoardAction", "RulesEventKickOffTable"):
            if event.tag == "RulesEventKickOffTable":
                pass
            else:
                self.parse_board_action(event)
        self.display_stats()

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

    def parse_fans_and_weather(self, root):
        fans_infos = root.xpath("./ReplayStep/RulesEventBoardAction/ActionType[text()='46']/..//ListDices")
        weather_infos = root.xpath("./ReplayStep/RulesEventBoardAction/ActionType[text()='47']/..//ListDices")
        print("Fans:")
        for fans_info in fans_infos:
            print(fans_info.text)
        print("Weather:")
        print(weather_infos[0].text)

    def display_stats(self):
        for team in self.stats.stats:
            print(team)
            print("ARMOUR")
            print(self.stats.stats[team]["armour"])
            print("INJURY")
            print(self.stats.stats[team]["injury"])
            print("CASUALTY")
            print(self.stats.stats[team]["casualty"])
            print("DODGE")
            print(self.stats.stats[team]["dodge"])
            print("BLOCK")
            print(self.stats.stats[team]["block"])

    def parse_board_action(self, event):
        # Is there a dice roll in this action?
        for action_res in event.iter("BoardActionResult"):
            dices = action_res.find(".//ListDices")
            if dices is not None:
                actor = self.parser.get_team_and_turn(event)
                rolltype = action_res.find("./RollType")
                rolltype = int(rolltype.text)
                # player_id = step.findtext("./PlayerId")
                self.__getattribute__(ROLL_TO_ACTION[rolltype])(action_res, actor)

    def dodge(self, action_res, actor):
        print("dodge")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_dodge(result, actor)
        pass

    def fan_attendance(self, action_res, player_id):
        print("fan_attendance")
        result = self.parser.get_result(action_res)
        pass

    def weather(self, action_res, player_id):
        print("weather")
        result = self.parser.get_result(action_res)
        pass

    def halfing_chef(self, action_res, player_id):
        print("halfing_chef")
        result = self.parser.get_result(action_res)
        pass

    def kickoff(self, action_res, player_id):
        print("kickoff")
        result = self.parser.get_result(action_res)

    def block(self, action_res, actor):
        print("block")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_block(result, actor)

    def pickup(self, action_res, player_id):
        pass

    def armour(self, action_res, actor):
        print("armour")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_armour(result, actor)
        pass

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

    def gfi(self, action_res, player_id):
        pass

    def wild_animal(self, action_res, player_id):
        pass

    def pass_(self, action_res, player_id):
        pass

    def catch(self, action_res, player_id):
        pass

    def intercept(self, action_res, player_id):
        pass

    def really_stupid(self, action_res, player_id):
        pass

    def loner(self, action_res, player_id):
        print("loner")
        result = self.parser.get_result(action_res)
        pass

    def wake_up_ko(self, action_res, player_id):
        pass

    def throw_in(self, action_res, player_id):
        pass

    def kickoff_gust(self, action_res, player_id):
        pass

    def unknown(self, action_res, player_id):
        pass

    def bone_head(self, action_res, player_id):
        pass


# def parse_dodge(root):
    # dodges = root.xpath("./ReplayStep/RulesEventBoardAction/Results/BoardActionResult/RollType[text()='2']/../../..")
    # print("Dodges:")
    # for dodge in dodges:
        # player_id = dodge.find("./PlayerId").text
        # requirement = int(dodge.find(".//Requirement").text)
        # mods = dodge.find(".//ListModifiers")
        # for mod in mods.getchildren():
            # requirement -= int(mod.find("Value").text)
        # result = dodge.find(".//ListDices").text
        # print(player_id)
        # if requirement < 2:
            # requirement = 2
        # elif requirement > 6:
            # requirement = 6

        # print(str(requirement) + "+")
        # print(result)


# def parse_pickup(root):
    # pickups = root.xpath("./ReplayStep/RulesEventBoardAction/Results/BoardActionResult/RollType[text()='7']/../../..")
    # print("Pickups:")
    # for pickup in pickups:
        # player_id = pickup.find("./PlayerId").text
        # results = pickup.findall("./Results/BoardActionResult")
        # for result in results:
            # requirement = int(result.find(".//Requirement").text)
            # mods = result.find(".//ListModifiers")
            # for mod in mods.getchildren():
                # requirement -= int(mod.find("Value").text)
            # dices = result.find(".//ListDices").text
            # print(player_id)
            # if requirement < 2:
                # requirement = 2
            # elif requirement > 6:
                # requirement = 6

            # print(str(requirement) + "+")
            # print(dices)


if __name__ == "__main__":
    main()
