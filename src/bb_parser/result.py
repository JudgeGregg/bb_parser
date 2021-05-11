from bb_parser.mappings import BLOCK, ARMOUR


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
        self.previous_dices = None
        self.current = None

    def get_team_and_turn(self, event):
        team = ""
        turn = ""
        player_id = event.findtext("PlayerId")
        if player_id:
            player_id = int(player_id)
            print("Player ID:")
            print(player_id)
            elem_id = event.getparent().xpath("./BoardState/ListTeams/TeamState/ListPitchPlayers/PlayerState/Id[text()='{}']".format(player_id))[0]
            elem_team_state = elem_id.getparent().getparent().getparent()
            turn = elem_team_state.findtext("./GameTurn")
            team = elem_team_state.findtext("./Data/Name")
            print("Turn:")
            print(turn)
            print("Team:")
            print(team)
        return Actor(team, turn)

    def get_result(self, action_res):
        # Ignore requirements on block
        rolltype = int(action_res.findtext("./RollType"))
        if rolltype == BLOCK:
            dices = action_res.find(".//ListDices").text
            if action_res.findtext("./IsOrderCompleted") == "1":
                print("=> " + dices)
                return
            else:
                print(dices)
                res = Result(dices)
                return res
        requirement = action_res.findtext("./Requirement")
        if requirement:
            requirement_init = int(requirement)
            requirement = int(requirement)
            mods = action_res.find("./ListModifiers")
            for mod in mods.getchildren():
                requirement -= int(mod.find("Value").text)
            if requirement < 2 and rolltype not in (ARMOUR,):
                requirement = 2
            elif requirement > 6 and rolltype not in (ARMOUR,):
                requirement = 6
            if requirement != requirement_init and rolltype == ARMOUR:
                requirement = str(requirement) + "*"
            print(str(requirement) + "+")

        dices = action_res.find(".//ListDices").text

        if self.previous_dices:
            if action_res.findtext("./IsOrderCompleted") == "1" and self.previous_dices == dices:
                self.previous_dices = None
                print("Ignoring, reroll not used")
                print("Ignoring, reroll not used (OR SAME DICE?")
                return
            elif action_res.findtext("./IsOrderCompleted") == "1" and dices == self.previous_dices:
                __import__('pdb').set_trace()
                print("SHOULD NOT HAPPEN")
            elif dices != self.previous_dices:
                if self.current:
                    print("FINAL CHOICE, Ignore")
                    self.current = None
                    self.previous_dices = None
                    return
                print("NEW DICES: OK")
                print("CHOICE OFFERED")
                self.current = True
        if action_res.findtext(".//Reroll") == "1":
            self.previous_dices = dices

        print(dices)
        res = Result(dices, str(requirement))
        return res
