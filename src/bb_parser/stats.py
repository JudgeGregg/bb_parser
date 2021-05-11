from collections import defaultdict


class Stats():

    def __init__(self, teams):
        self.stats = {}
        self.teams = set()
        for team in teams:
            self.teams.add(team)
            self.stats[team] = {}
            self.stats[team]["armour"] = defaultdict(list)
            self.stats[team]["injury"] = list()
            self.stats[team]["casualty"] = list()
            self.stats[team]["dodge"] = defaultdict(list)
            self.stats[team]["block"] = list()

    def add_armour(self, result, actor):
        dices = result.dices
        opposing_team = self.teams.difference(set([actor.team])).pop()
        requirement = result.requirement
        self.stats[opposing_team]["armour"][requirement].append(dices)

    def add_injury(self, result, actor):
        dices = result.dices
        opposing_team = self.teams.difference(set([actor.team])).pop()
        self.stats[opposing_team]["injury"].append(dices)

    def add_casualty(self, result, actor):
        dices = result.dices
        opposing_team = self.teams.difference(set([actor.team])).pop()
        self.stats[opposing_team]["casualty"].append(dices)

    def add_dodge(self, result, actor):
        dices = result.dices
        requirement = result.requirement
        self.stats[actor.team]["dodge"][requirement].append(dices)

    def add_block(self, result, actor):
        dices = result.dices
        self.stats[actor.team]["block"].append(dices)
