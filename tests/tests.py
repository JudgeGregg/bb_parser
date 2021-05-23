import unittest
from io import StringIO

from lxml import etree

from bb_parser.main import Replayer, Parser, Stats, display_stats

from . import fixtures


class TestGameInfos(unittest.TestCase):

    def setUp(self):
        self.replayer = Replayer()
        self.parser = Parser()

    def test_parse(self):
        text = StringIO(fixtures.GAME_INFO_FIXTURE)
        stats = self.replayer.parse_replay(text)
        display_stats(stats)

    def test_gameinfos(self):
        self.text = StringIO(fixtures.GAME_INFO_FIXTURE)
        self.root = etree.fromstring(self.text.read())
        teams = self.parser.parse_game_infos(self.root)
        self.assertEqual(len(teams), 2)


class TestFansWeather(unittest.TestCase):

    def setUp(self):
        self.replayer = Replayer()
        self.parser = Parser()
        self.text = StringIO(fixtures.WEATHER_FANS_FIXTURE)
        self.root = etree.fromstring(self.text.read())

    def test_fans_weather(self):
        self.parser.parse_events(self.root)


class TestDodge(unittest.TestCase):

    def setUp(self):
        self.replayer = Replayer()
        self.replayer.parser = Parser()
        self.replayer.stats = Stats(
            (("Team1", "Bar", "Foo"), ("Team2", "Baz", "Eggs")))

    def test_dodge_success(self):
        self.text = StringIO(fixtures.DODGE_SUCCESS_FIXTURE)
        self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.root)
        stats = self.replayer.get_stats()
        self.assertEqual(len(stats["Team1"]["dodge"]), 1)
        self.assertEqual(stats["Team1"]["dodge"]["3"], ["(5)"])

    def test_dodge_failure_despite_rr(self):
        self.text = StringIO(fixtures.DODGE_FAILURE_DESPITE_RR_FIXTURE)
        self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.root)
        stats = self.replayer.get_stats()
        self.assertEqual(len(stats["Team1"]["dodge"]), 1)
        self.assertEqual(stats["Team1"]["dodge"]["3"], ["(1)", "(2)"])

    def test_dodge_failure_no_rr(self):
        self.text = StringIO(fixtures.DODGE_FAILURE_NO_RR_FIXTURE)
        self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.root)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["dodge"]), 1)
        self.assertEqual(stats["Team1"]["dodge"]["2"], ["(1)"])

    def test_dodge_success_with_skill(self):
        self.text = StringIO(fixtures.DODGE_SUCCESS_WITH_SKILL_FIXTURE)
        self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.root)
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
        self.text = StringIO(fixtures.BLOCK_WITH_RR_FIXTURE)
        self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.root)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["block"]), 2)
        self.assertEqual(stats["Team1"]["blocks"]["P"], 1)
        self.assertEqual(stats["Team1"]["blocks"]["AD"], 3)

    def test_block_no_rr(self):
        self.text = StringIO(fixtures.BLOCK_NO_RR_FIXTURE)
        self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.root)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["block"]), 1)
        self.assertEqual(stats["Team1"]["blocks"]["P"], 1)
        self.assertEqual(stats["Team1"]["blocks"]["BD"], 1)

    def test_block_rr_loner(self):
        self.text = StringIO(fixtures.BLOCK_RR_LONER_FIXTURE)
        self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.root)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["block"]), 1)
        self.assertEqual(stats["Team1"]["blocks"]["BD"], 1)

    def test_1d_block_with_rr(self):
        self.text = StringIO(fixtures.BLOCK_ONE_DIE_WITH_RR_FIXTURE)
        self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.root)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["block"]), 2)
        self.assertEqual(stats["Team1"]["blocks"]["BD"], 1)

    def test_1d_block_no_rr(self):
        self.text = StringIO(fixtures.BLOCK_ONE_DIE_NO_RR_FIXTURE)
        self.root = etree.fromstring(self.text.read())
        self.replayer.parse_events(self.root)
        stats = self.replayer.stats.stats
        self.assertEqual(len(stats["Team1"]["block"]), 1)
        self.assertEqual(stats["Team1"]["blocks"]["DS"], 1)
