import random

class Scrim:
    # Start a scrim baby
    def __init__(self, name):
        self.name = name
        self.red_team = []
        self.blue_team = []
        self.game_map = "No map chosen"
        self.result = "N/A"

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def addPlayer(self, player, team):
        if team == "Red":
            self.red_team.append(player)
        elif team == "Blue":
            self.blue_team.append(player)
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
        return self.red_team, self.blue_team

    def getRedTeam(self):
        return self.red_team

    def getBlueTeam(self):
        return self.blue_team

    #Clobbers the teams. Only should be used by autobalancer
    def setTeams(self, rt, bt):
        self.red_team.extend(rt)
        self.blue_team.extend(bt)

    #Because GC is a thing, I guess I can resue the same object over and over
    def flush(self):
        self.red_team[:] = []
        self.blue_team[:] = []
        self.game_map = "No map chosen"
        self.result = "N/A"
        self.name = "Active"
