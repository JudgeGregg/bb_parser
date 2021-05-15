from bb_parser.mappings import BLOCK, ARMOUR, CASUALTY


class Result():

    def __init__(self, dices, requirement=None):
        self.requirement = requirement
        self.dices = dices


class Actor():

    def __init__(self, team, turn):
        self.team = team
        self.turn = turn


class Parser():

    def __init__(self):
        self.current_team = None
        self.current_turn = 0

    def get_team_and_turn(self, event):
        team = ""
        turn = ""
        player_id = event.findtext("PlayerId")
        if player_id:
            player_id = int(player_id)
            print("Player ID:")
            print(player_id)
            if player_id == -1:  # Wizard
                return Actor(self.current_team, self.current_turn)
            elem_id = event.getparent().xpath("./BoardState/ListTeams/TeamState/ListPitchPlayers/PlayerState/Id[text()='{}']".format(player_id))[0]
            elem_team_state = elem_id.getparent().getparent().getparent()
            turn = elem_team_state.findtext("./GameTurn")
            if turn and int(turn) >= int(self.current_turn):
                self.current_turn = turn
            team = elem_team_state.findtext("./Data/Name")
            self.current_team = team
            print("Turn:")
            print(turn)
            print("Team:")
            print(team)
        return Actor(team, turn)

    def get_result(self, action_res):
        rolltype = int(action_res.findtext("./RollType"))
        if rolltype == BLOCK:
            # Ignore requirements on block
            dices = action_res.find(".//ListDices").text
            if action_res.findtext("./IsOrderCompleted") == "1":
                print("=> " + dices)
                return
            elif action_res.find("./RollStatus") is not None and action_res.findtext("./RollStatus") == "2":
                print("REROLL NOT AVAILABLE!")
                return
            else:
                print(dices)
                res = Result(dices)
                return res

        if rolltype == CASUALTY:
            if action_res.findtext("./RollStatus") == "1" and action_res.findtext("./IsOrderCompleted") == "1":
                print("Ignoring, casualty choice")
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
            print(str(requirement) + "+")

        dices = action_res.find(".//ListDices").text

        if action_res.find("./RollStatus") is not None and action_res.findtext("./RollStatus") == "2":
            print("Ignoring, reroll not used or not available")
            return

        print(dices)
        res = Result(dices, str(requirement))
        return res
