import zipfile
from pathlib import Path
from io import TextIOWrapper
import logging

from lxml import etree


from .mappings import ROLL_TO_ACTION
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
                self.__getattribute__(
                    ROLL_TO_ACTION[rolltype])(action_res, actor)
            except KeyError as e:
                log.error("ERROR: Missing key: {}".format(e))

    def dodge(self, action_res, actor):
        log.debug("dodge")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_dodge(result, actor)

    def fan_attendance(self, action_res, player_id):
        log.debug("fan_attendance")
        _ = self.parser.get_result(action_res)

    def weather(self, action_res, player_id):
        log.debug("weather")
        _ = self.parser.get_result(action_res)

    def halfing_chef(self, action_res, player_id):
        log.debug("halfing_chef")
        _ = self.parser.get_result(action_res)

    def kickoff(self, action_res, player_id):
        log.debug("kickoff")
        _ = self.parser.get_result(action_res)

    def block(self, action_res, actor):
        log.debug("block")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_block(result, actor)

    def pickup(self, action_res, actor):
        log.debug("pickup")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_pickup(result, actor)

    def foul(self, action_res, actor):
        log.debug("foul")
        # Ignore foul, since armour and injury have regular rolls

    def armour(self, action_res, actor):
        log.debug("armour")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_armour(result, actor)

    def injury(self, action_res, actor):
        log.debug("injury")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_injury(result, actor)

    def casualty(self, action_res, actor):
        log.debug("casualty")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_casualty(result, actor)

    def gfi(self, action_res, actor):
        log.debug("gfi")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_gfi(result, actor)

    def pass_(self, action_res, actor):
        log.debug("pass")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_pass(result, actor)

    def catch(self, action_res, actor):
        log.debug("catch")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_catch(result, actor)

    def throw_team_mate(self, action_res, actor):
        log.debug("throw_team_mate")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_throw_team_mate(result, actor)

    def landing(self, action_res, actor):
        log.debug("landing")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_landing(result, actor)

    def intercept(self, action_res, actor):
        log.debug("intercept")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_intercept(result, actor)

    def jump_up(self, action_res, actor):
        log.debug("jump up")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_jump_up(result, actor)

    def leap(self, action_res, actor):
        log.debug("leap")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_leap(result, actor)

    def loner(self, action_res, actor):
        log.debug("loner")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_loner(result, actor)

    def wake_up_ko(self, action_res, actor):
        log.debug("wake_up_ko")
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
        log.debug("bone_head")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_bone_head(result, actor)

    def wild_animal(self, action_res, actor):
        log.debug("wild_animal")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_wild_animal(result, actor)

    def really_stupid(self, action_res, actor):
        log.debug("really_stupid")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_really_stupid(result, actor)

    def take_root(self, action_res, actor):
        log.debug("take_root")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_take_root(result, actor)

    def dauntless(self, action_res, actor):
        log.debug("dauntless")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_dauntless(result, actor)

    def impact_of_the_bomb(self, action_res, actor):
        log.debug("impact_of_the_bomb")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_impact_of_the_bomb(result, actor)

    def regeneration(self, action_res, actor):
        log.debug("regeneration")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_regeneration(result, actor)

    def fireball(self, action_res, actor):
        log.debug("fireball")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_fireball(result, actor)

    def lightning_bolt(self, action_res, actor):
        log.debug("lightning_bolt")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_lightning_bolt(result, actor)

    def stand_up(self, action_res, actor):
        log.debug("stand up")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_stand_up(result, actor)

    def inaccurate_pass(self, action_res, actor):
        # These are recorded in game whereas they're 8 sided rolls??
        pass

    def animosity(self, action_res, actor):
        log.debug("animosity")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_animosity(result, actor)

    def always_hungry(self, action_res, actor):
        log.debug("always_hungry")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_always_hungry(result, actor)

    def snack(self, action_res, actor):
        log.debug("snack")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_snack(result, actor)

    def shadowing(self, action_res, actor):
        log.debug("shadowing")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_shadowing(result, actor)

    def stab(self, action_res, actor):
        log.debug("stab")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_stab(result, actor)

    def foul_appearance(self, action_res, actor):
        log.debug("foul_appearance")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_foul_appearance(result, actor)

    def tentacles(self, action_res, actor):
        log.debug("tentacles")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_tentacles(result, actor)

    def hypnotic_gaze(self, action_res, actor):
        log.debug("hypnotic_gaze")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_hypnotic_gaze(result, actor)

    def bloodlust(self, action_res, actor):
        log.debug("bloodlust")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_bloodlust(result, actor)

    def bribe(self, action_res, actor):
        log.debug("bribe")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_bribe(result, actor)

    def chainsaw(self, action_res, actor):
        log.debug("chainsaw")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_chainsaw(result, actor)

    def sweltering_heat(self, action_res, actor):
        log.debug("sweltering_heat")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_sweltering_heat(result, actor)

    def pro(self, action_res, actor):
        log.debug("pro")
        result = self.parser.get_result(action_res)
        if result:
            self.stats.add_pro(result, actor)
