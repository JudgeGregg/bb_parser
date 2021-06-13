import logging

from lxml import etree

from .mappings import BLOCK, ARMOUR, CASUALTY

log = logging.getLogger("bb_parser")


class Result():

    def __init__(self, dices, requirement=None):
        self.requirement = requirement
        self.dices = dices


class Actor():

    def __init__(self, team, turn, player_name=None):
        self.team = team
        self.turn = turn
        self.player_name = player_name

class Action():

    def __init__(self, rolltype, action_res, actor):
        self.type = "action"
        self.rolltype = rolltype
        self.action_res = action_res
        self.actor = actor

class MatchResult():

    def __init__(self, date, home_team_name, home_score, away_team_name, away_score):
        self.type = "match_result"
        self.date = date
        self.home_team_name = home_team_name
        self.home_score = home_score
        self.away_team_name = away_team_name
        self.away_score = away_score


class Parser():

    def __init__(self):
        self.current_team = None
        self.current_turn = 0

    def parse_game_infos(self, text):
        game_infos = None
        for event, elem in etree.iterparse(text):
            if elem.tag == "GameInfos":
                game_infos = elem
                teams_state = elem.getparent()
                break
        coaches_infos = game_infos.findall("CoachesInfos/CoachInfos")
        log.debug("COACHES:")
        coaches = []
        for coach in coaches_infos:
            log.debug(coach.findtext(".//Login"))
            coaches.append(coach.findtext(".//Login"))
        teams = []
        teams_elem = teams_state.findall(".//TeamState/Data")
        for index, team in enumerate(teams_elem):
            teams.append((team.findtext(".//Name"),
                          team.findtext(".//IdRace"), coaches[index]))
        log.debug("TEAMS:")
        log.debug(teams)
        return teams

    def parse_events(self, text):
        for _, step in etree.iterparse(text, tag="ReplayStep"):
            for event in step.iter("RulesEventBoardAction", "RulesEventGameFinished"):
                if event.tag == "RulesEventBoardAction":
                    for rolltype, action_res, actor in self.parse_board_action(event):
                        yield Action(rolltype, action_res, actor)
                elif event.tag == "RulesEventGameFinished":
                    match_result = self.parse_endgame(event)
                    yield match_result
                event.clear(keep_tail=True)
            step.clear(keep_tail=True)

    def parse_board_action(self, event):
        # Is there a dice roll in this action?
        for action_res in event.iter("BoardActionResult"):
            dices = action_res.find(".//ListDices")
            if dices is not None:
                actor = self.get_team_and_turn(event)
                rolltype = action_res.findtext("./RollType")
                yield rolltype, action_res, actor

    def parse_endgame(self, match_result):
        home_team_name = match_result.findtext("./MatchResult/Row/TeamHomeName")
        home_score = match_result.findtext("./MatchResult/Row/HomeScore")
        away_team_name = match_result.findtext("./MatchResult/Row/TeamAwayName")
        away_score = match_result.findtext("./MatchResult/Row/AwayScore")
        if not home_score:
            home_score = "0"
        if not away_score:
            away_score = "0"
        date = match_result.findtext("./MatchResult/Row/Finished").split(".")[0]
        return MatchResult(date, home_team_name, home_score, away_team_name, away_score)

    def get_team_and_turn(self, event):
        team = None
        turn = None
        player_name = None
        player_id = event.findtext("PlayerId")
        if player_id:
            player_id = int(player_id)
            log.debug("Player ID:")
            log.debug(player_id)
            if player_id == -1:  # Wizard
                return Actor(self.current_team, self.current_turn)
            elem_id = event.getparent().xpath("./BoardState/ListTeams/TeamState/ListPitchPlayers/PlayerState/Id[text()='{}']".format(player_id))[0]
            elem_team_state = elem_id.getparent().getparent().getparent()
            elem_player = elem_id.getparent()
            player_name = elem_player.findtext("./Data/Name")
            turn = elem_team_state.findtext("./GameTurn")
            if turn and int(turn) >= int(self.current_turn):
                self.current_turn = turn
            team = elem_team_state.findtext("./Data/Name")
            self.current_team = team
            log.debug("Turn:")
            log.debug(turn)
            log.debug("Team:")
            log.debug(team)
            log.debug("Player:")
            log.debug(player_name)
        return Actor(team, turn, player_name)

    def get_result(self, action_res):
        rolltype = action_res.findtext("./RollType")
        if rolltype == BLOCK:
            # Ignore requirements on block
            dices = action_res.find(".//ListDices").text
            if action_res.findtext("./IsOrderCompleted") == "1":
                log.debug("=> " + dices)
                return
            elif action_res.findtext("./RollStatus") == "2":
                log.debug("Ignoring, reroll not used or not available")
                return
            elif action_res.findtext("./RequestType") == "4":
                log.debug("Ignoring, skill used")
                return
            else:
                log.debug(dices)
                res = Result(dices)
                return res

        if rolltype == CASUALTY:
            if action_res.findtext("./RollStatus") == "1" and action_res.findtext("./IsOrderCompleted") == "1":
                log.debug("Ignoring, casualty choice")
                return

        requirement = action_res.findtext("./Requirement")

        if requirement:
            requirement_init = int(requirement)
            requirement = int(requirement)
            mods = action_res.find("./ListModifiers")
            for mod in mods.getchildren():
                if mod.find("Value") is not None:
                    requirement -= int(mod.find("Value").text)
            if requirement < 2 and rolltype not in (ARMOUR,):
                requirement = 2
            elif requirement > 6 and rolltype not in (ARMOUR,):
                requirement = 6
            if requirement != requirement_init and rolltype == ARMOUR:
                requirement = str(requirement) + "*"
            log.debug(str(requirement) + "+")

        dices = action_res.find(".//ListDices").text

        if action_res.findtext("./RollStatus") == "2":
            log.debug("Ignoring, reroll not used or not available")
            return

        if action_res.findtext("./SubResultType") == "22":
            log.debug("Ignoring, break tackle used")
            return

        log.debug(dices)
        res = Result(dices, str(requirement))
        return res
