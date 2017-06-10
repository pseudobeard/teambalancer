import random

class Scrim:
    # Start a scrim baby
    def __init__(self, name):
        self.name = name
        self.red_team = []
        self.blue_team = []
        self.game_map = "No map chosen"
        self.result = "N/A"

    def addPlayer(self, team, player):
        if team == "Red":
            red_team.append(player)
        elif team == "Blue":
            blue_team.append(player)
        else:
            return "Team must be Red or Blue"
        return

    def setMap(self, m):
        self.game_map = m

    def setResult(self, result):
        self.result = result

    def getResult(self):
        return result

    def getTeams(self):
        return red_team, blue_team

    #Clobbers the teams. Only should be used by autobalancer
    def setTeams(self, rt, bt):
        self.red_team = rt
        self.blue_team = bt

