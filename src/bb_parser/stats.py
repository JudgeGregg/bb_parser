from collections import defaultdict

from .mappings import BLOCK_SYMBOL, ID_RACE_TO_NAME


class Stats():

    def __init__(self, teams):
        self.stats = {}
        self.teams = set()
        for team, race, coach in teams:
            self.teams.add(team)
            self.stats[team] = {}
            self.stats[team]["race"] = ID_RACE_TO_NAME.get(race, race)
            self.stats[team]["coach"] = coach
            # All D6 dices (histogram)
            self.stats[team]["dice"] = {
                "1": 0, "2": 0, "3": 0, "4": 0, "5": 0, "6": 0}
            # Injuries
            self.stats[team]["armour"] = defaultdict(list)
            self.stats[team]["injury"] = list()
            self.stats[team]["casualty"] = list()
            self.stats[team]["wake_up_ko"] = defaultdict(list)
            # Blocks + histogram
            self.stats[team]["block"] = list()
            self.stats[team]["blocks"] = {
                "AD": 0, "BD": 0, "P": 0, "DS": 0, "DD": 0}
            self.stats[team]["players"] = defaultdict(list)
            # Movement
            self.stats[team]["gfi"] = defaultdict(list)
            self.stats[team]["dodge"] = defaultdict(list)
            # Ball handling
            self.stats[team]["pickup"] = defaultdict(list)
            self.stats[team]["pass"] = defaultdict(list)
            self.stats[team]["catch"] = defaultdict(list)
            self.stats[team]["intercept"] = defaultdict(list)
            # TTM
            self.stats[team]["throw_team_mate"] = defaultdict(list)
            self.stats[team]["landing"] = defaultdict(list)
            # Negatraits
            self.stats[team]["bone_head"] = defaultdict(list)
            self.stats[team]["wild_animal"] = defaultdict(list)
            self.stats[team]["really_stupid"] = defaultdict(list)
            self.stats[team]["take_root"] = defaultdict(list)
            self.stats[team]["loner"] = defaultdict(list)

    def get_stats(self):
        return self.stats

    def parse_d6_dice(self, dice):
        return [
            elem for elem in dice if elem in ("1", "2", "3", "4", "5", "6")]

    def parse_casualty_dice(self, dice):
        dice = dice.split(",")
        if len(dice) > 2:
            # Apo used
            return "({})".format(dice[1][0])
        else:
            return "({})".format(dice[0][1])

    def parse_block_dice(self, dice):
        filtered_dice = [
            elem for elem in dice if elem in (
                "0", "1", "2", "3", "4", "5", "6")]
        if len(filtered_dice) > 1:
            dice = filtered_dice[:int(len(filtered_dice)/2)]
        else:
            dice = filtered_dice
        result = []
        for die in dice:
            result.append(BLOCK_SYMBOL[die])
        return result

    def add_dice(self, dice, team):
        dice = self.parse_d6_dice(dice)
        for elem in dice:
            self.stats[team]["dice"][elem] += 1

    def add_armour(self, result, actor):
        dice = result.dices
        requirement = result.requirement
        opposing_team = self.teams.difference(set([actor.team])).pop()
        # self.add_dice(dice, actor.team)
        self.add_dice(dice, opposing_team)
        self.stats[opposing_team]["armour"][requirement].append(dice)

    def add_injury(self, result, actor):
        dice = result.dices
        opposing_team = self.teams.difference(set([actor.team])).pop()
        # self.add_dice(dice, actor.team)
        self.add_dice(dice, opposing_team)
        self.stats[opposing_team]["injury"].append(dice)

    def add_casualty(self, result, actor):
        dice = result.dices
        parsed_casualty_dice = self.parse_casualty_dice(dice)
        opposing_team = self.teams.difference(set([actor.team])).pop()
        # self.add_dice(parsed_casualty_dice, actor.team)
        self.add_dice(parsed_casualty_dice, opposing_team)
        self.stats[opposing_team]["casualty"].append(dice)

    def add_wake_up_ko(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
        requirement = result.requirement
        self.stats[actor.team]["wake_up_ko"][requirement].append(dice)

    def add_pickup(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
        requirement = result.requirement
        self.stats[actor.team]["pickup"][requirement].append(dice)

    def add_pass(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
        requirement = result.requirement
        self.stats[actor.team]["pass"][requirement].append(dice)

    def add_catch(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
        requirement = result.requirement
        self.stats[actor.team]["catch"][requirement].append(dice)

    def add_intercept(self, result, actor):
        dice = result.dices
        requirement = result.requirement
        opposing_team = self.teams.difference(set([actor.team])).pop()
        self.add_dice(dice, opposing_team)
        self.stats[opposing_team]["intercept"][requirement].append(dice)

    def add_throw_team_mate(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
        requirement = result.requirement
        self.stats[actor.team]["throw_team_mate"][requirement].append(dice)

    def add_landing(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
        requirement = result.requirement
        self.stats[actor.team]["landing"][requirement].append(dice)

    def add_dodge(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
        requirement = result.requirement
        self.stats[actor.team]["dodge"][requirement].append(dice)

    def add_block(self, result, actor):
        player_name = actor.player_name
        dice = result.dices
        dice = self.parse_block_dice(dice)
        self.stats[actor.team]["block"].append(dice)
        self.stats[actor.team]["players"][player_name].append(dice)
        for block in dice:
            self.stats[actor.team]["blocks"][block] += 1

    def add_gfi(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
        requirement = result.requirement
        self.stats[actor.team]["gfi"][requirement].append(dice)

    def add_bone_head(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
        requirement = result.requirement
        self.stats[actor.team]["bone_head"][requirement].append(dice)

    def add_wild_animal(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
        requirement = result.requirement
        self.stats[actor.team]["wild_animal"][requirement].append(dice)

    def add_really_stupid(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
        requirement = result.requirement
        self.stats[actor.team]["really_stupid"][requirement].append(dice)

    def add_take_root(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
        requirement = result.requirement
        self.stats[actor.team]["take_root"][requirement].append(dice)

    def add_loner(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
        requirement = result.requirement
        self.stats[actor.team]["loner"][requirement].append(dice)

    def add_jump_up(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_leap(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_dauntless(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_impact_of_the_bomb(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_regeneration(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_fireball(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_lightning_bolt(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_stand_up(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_animosity(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_always_hungry(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_shadowing(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_stab(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_foul_appearance(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_tentacles(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_hypnotic_gaze(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_bloodlust(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_bribe(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_chainsaw(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_sweltering_heat(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)

    def add_pro(self, result, actor):
        dice = result.dices
        self.add_dice(dice, actor.team)
