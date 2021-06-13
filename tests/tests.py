import unittest
from io import StringIO, BytesIO
import zipfile
import logging

from lxml import etree

from bb_parser.main import Replayer, Parser, Stats
from bb_parser.cli import display_stats

from . import fixtures

logging.basicConfig(level=logging.DEBUG)


class TestGameInfos(unittest.TestCase):

    def setUp(self):
        self.replayer = Replayer()
        self.parser = Parser()

    def test_parse(self):
        text = BytesIO(fixtures.GAME_INFO_FIXTURE)
        mem_zip = BytesIO()
        with zipfile.ZipFile(
                mem_zip, mode="w", compression=zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("foo", text.read())
            stats = self.replayer.parse_replay(zf)
        display_stats(stats)

    def test_gameinfos(self):
        self.text = BytesIO(fixtures.GAME_INFO_FIXTURE)
        # self.root = self.text.read()
        teams = self.parser.parse_game_infos(self.text)
        self.assertEqual(len(teams), 2)


class TestDodge(unittest.TestCase):

    def setUp(self):
        self.replayer = Replayer()
        self.replayer.parser = Parser()
        self.replayer.stats = Stats(
            (("Team1", "Bar", "Foo"), ("Team2", "Baz", "Eggs")))

    def test_dodge_success(self):
        self.text = BytesIO(fixtures.DODGE_SUCCESS_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.get_stats()
        self.assertEqual(len(stats["Team1"]["dodge"]), 1)
        self.assertEqual(stats["Team1"]["dodge"]["3"], ["(5)"])

    def test_dodge_failure_despite_rr(self):
        self.text = BytesIO(fixtures.DODGE_FAILURE_DESPITE_RR_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.get_stats()
        self.assertEqual(len(stats["Team1"]["dodge"]), 1)
        self.assertEqual(stats["Team1"]["dodge"]["3"], ["(1)", "(2)"])

    def test_dodge_failure_no_rr(self):
        self.text = BytesIO(fixtures.DODGE_FAILURE_NO_RR_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["dodge"]), 1)
        self.assertEqual(stats["Team1"]["dodge"]["2"], ["(1)"])

    def test_dodge_success_with_skill(self):
        self.text = BytesIO(fixtures.DODGE_SUCCESS_WITH_SKILL_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["dodge"]), 2)
        self.assertEqual(stats["Team1"]["dodge"]["3"], ["(5)"])
        self.assertEqual(stats["Team1"]["dodge"]["None"], ["(1)"])


class TestBlock(unittest.TestCase):

    def setUp(self):
        self.replayer = Replayer()
        self.replayer.parser = Parser()
        self.replayer.stats = Stats(
            (("Team1", "Bar", "Foo"), ("Team2", "Baz", "Eggs")))

    def test_block_with_rr(self):
        self.text = BytesIO(fixtures.BLOCK_WITH_RR_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["block"]), 2)
        self.assertEqual(stats["Team1"]["blocks"]["P"], 1)
        self.assertEqual(stats["Team1"]["blocks"]["AD"], 3)

    def test_block_no_rr(self):
        self.text = BytesIO(fixtures.BLOCK_NO_RR_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["block"]), 1)
        self.assertEqual(stats["Team1"]["blocks"]["P"], 1)
        self.assertEqual(stats["Team1"]["blocks"]["BD"], 1)

    def test_block_rr_loner(self):
        self.text = BytesIO(fixtures.BLOCK_RR_LONER_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["block"]), 1)
        self.assertEqual(stats["Team1"]["blocks"]["BD"], 1)

    def test_1d_block_with_rr(self):
        self.text = BytesIO(fixtures.BLOCK_ONE_DIE_WITH_RR_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["block"]), 2)
        self.assertEqual(stats["Team1"]["blocks"]["BD"], 1)

    def test_1d_block_no_rr(self):
        self.text = BytesIO(fixtures.BLOCK_ONE_DIE_NO_RR_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["block"]), 1)
        self.assertEqual(stats["Team1"]["blocks"]["DS"], 1)

    def test_2d_block_no_rr_tackle(self):
        self.text = BytesIO(fixtures.BLOCK_2D_NO_RR_TACKLE_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["block"]), 1)
        self.assertEqual(stats["Team1"]["blocks"]["DS"], 1)
        self.assertEqual(stats["Team1"]["blocks"]["BD"], 1)


class TestArmour(unittest.TestCase):

    def setUp(self):
        self.replayer = Replayer()
        self.replayer.parser = Parser()
        self.replayer.stats = Stats(
            (("Team1", "Bar", "Foo"), ("Team2", "Baz", "Eggs")))

    def test_armour(self):
        self.text = BytesIO(fixtures.ARMOUR_ROLL_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team2"]["armour"]), 1)
        self.assertEqual(stats["Team2"]["armour"]["9"], ["(2,5)"])
        self.assertEqual(stats["Team2"]["dice"]["2"], 1)
        self.assertEqual(stats["Team2"]["dice"]["5"], 1)

    def test_injury(self):
        self.text = BytesIO(fixtures.INJURY_ROLL_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team2"]["injury"]), 1)
        self.assertEqual(stats["Team2"]["injury"], ["(2,4)"])
        self.assertEqual(stats["Team2"]["dice"]["2"], 1)
        self.assertEqual(stats["Team2"]["dice"]["4"], 1)

    def test_casualty(self):
        self.text = BytesIO(fixtures.CASUALTY_ROLL_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team2"]["casualty"]), 1)
        self.assertEqual(stats["Team2"]["casualty"], ["(15,1)"])
        self.assertEqual(stats["Team2"]["dice"]["1"], 1)

    def test_casualty_apo(self):
        self.text = BytesIO(fixtures.CASUALTY_APO_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.stats.stats
        self.assertEqual(stats["Team2"]["casualty"], ["(62,63,18,18)"])
        self.assertEqual(stats["Team2"]["dice"]["6"], 1)

    def test_casualty_reroll(self):
        self.text = BytesIO(fixtures.CASUALTY_CHOICE_FIXTURE)
        # self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.text)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team2"]["casualty"]), 0)
