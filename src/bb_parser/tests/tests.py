import unittest
from io import StringIO

from lxml import etree

from bb_parser.main import Replayer, Parser

import bb_parser.tests.fixtures as fixtures


class TestGameInfos(unittest.TestCase):

    def setUp(self):
        self.replayer = Replayer()
        self.text = StringIO(fixtures.GAME_INFO_FIXTURE)
        self.root = etree.fromstring(self.text.read())

    def test_gameinfos(self):
        teams = self.replayer.parse_game_infos(self.root)
        self.assertEqual(len(teams), 2)


class TestFansWeather(unittest.TestCase):

    def setUp(self):
        self.replayer = Replayer()
        self.text = StringIO(fixtures.WEATHER_FANS_FIXTURE)
        self.root = etree.fromstring(self.text.read())

    def test_fans_weather(self):
        self.replayer.parse_fans_and_weather(self.root)


class TestDodge(unittest.TestCase):

    def setUp(self):
        self.replayer = Replayer()
        self.replayer.parser = Parser()
        self.text = StringIO(fixtures.DODGE_FIXTURE)
        self.root = etree.fromstring(self.text.read())

    def test_upper(self):
        for event in self.root.iter("BoardActionResult"):
            self.replayer.dodge(event, 1)


if __name__ == '__main__':
    unittest.main()
