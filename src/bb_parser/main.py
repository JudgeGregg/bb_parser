import zipfile
from pathlib import Path
import logging


from .mappings import ROLL_TO_ACTION, IGNORED_ACTIONS
from .stats import Stats
from .parser import Parser

# Disable logging by default
log = logging.getLogger("bb_parser")
log.addHandler(logging.NullHandler())


class Replayer():

    def get_stats(self):
        return self.stats.get_stats()

    def parse_replay(self, file_or_zip):
        if isinstance(file_or_zip, Path):
            bb_zip = zipfile.ZipFile(file_or_zip)
        else:
            bb_zip = file_or_zip
        bb_file = bb_zip.namelist()[0]
        with bb_zip.open(bb_file) as bb_file:
            self.parser = Parser()
            teams = self.parser.parse_game_infos(bb_file)
            bb_file.seek(0)
            self.stats = Stats(teams)
            self.parse_events(bb_file)
            return self.stats.get_stats()

    def parse_events(self, text):
        for event in self.parser.parse_events(text):
            if event.type == "action":
                rolltype = event.rolltype
                action_res = event.action_res
                actor = event.actor
                try:
                    self.handle_event(ROLL_TO_ACTION[rolltype], action_res, actor)
                except KeyError as e:
                    log.error("ERROR:Missing key: {}".format(e))
            elif event.type == "match_result":
                date = event.date
                home_team_name = event.home_team_name
                home_score = event.home_score
                away_team_name = event.away_team_name
                away_score = event.away_score
                self.stats.stats["date"] = date
                self.stats.stats[home_team_name]["score"] = home_score
                self.stats.stats[away_team_name]["score"] = away_score

    def handle_event(self, action_name, action_res, actor):
        log.debug(action_name)
        result = self.parser.get_result(action_res)
        # Ignored actions:
        if action_name in IGNORED_ACTIONS:
            return
        if result:
            try:
                self.stats.__getattribute__("add_" + action_name)(result, actor)
            except AttributeError as e:
                log.error("ERROR:Missing attribute: {}".format(e))
