from bb_parser.mappings import BLOCK, ARMOUR, CASUALTY


class Result():

    def __init__(self, dices, requirement=None):
        self.requirement = requirement
        self.dices = dices


class Actor():

    def __init__(self, team, turn, player_name=None):
        self.team = team
        self.turn = turn
        self.player_name = player_name


class Parser():

    def __init__(self):
        self.current_team = None
        self.current_turn = 0

    def get_team_and_turn(self, event):
        team = None
        turn = None
        player_name = None
        player_id = event.findtext("PlayerId")
        if player_id:
            player_id = int(player_id)
            print("Player ID:")
            print(player_id)
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
            print("Turn:")
            print(turn)
            print("Team:")
            print(team)
            print("Player:")
            print(player_name)
        return Actor(team, turn, player_name)

    def get_result(self, action_res):
        rolltype = int(action_res.findtext("./RollType"))
        if rolltype == BLOCK:
            # Ignore requirements on block
            dices = action_res.find(".//ListDices").text
            if action_res.findtext("./IsOrderCompleted") == "1":
                print("=> " + dices)
                return
            elif action_res.findtext("./RollStatus") == "2":
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

        if action_res.findtext("./RollStatus") == "2":
            print("Ignoring, reroll not used or not available")
            return

        if action_res.findtext("./SubResultType") == "22":
            print("Ignoring, break tackle used")
            return

        print(dices)
        res = Result(dices, str(requirement))
        return res
