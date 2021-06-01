import zipfile
from pathlib import Path
from io import TextIOWrapper
import logging

from lxml import etree


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
            text_file = TextIOWrapper(bb_file, encoding="utf-8")
            root = etree.fromstring(text_file.read())
            self.parser = Parser()
            teams = self.parser.parse_game_infos(root)
            date = self.parser.parse_game_date(root)
            self.stats = Stats(teams)
            self.stats.stats["date"] = date
            self.parse_events(root)
            home_team_name, home_score, away_team_name, away_score = self.parser.parse_endgame(root)
            self.stats.stats[home_team_name]["score"] = home_score
            self.stats.stats[away_team_name]["score"] = away_score
            return self.stats.get_stats()

    def parse_events(self, root):
        for rolltype, action_res, actor in self.parser.parse_events(root):
            try:
                self.handle_event(ROLL_TO_ACTION[rolltype], action_res, actor)
            except KeyError as e:
                log.error("ERROR:Missing key: {}".format(e))

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
