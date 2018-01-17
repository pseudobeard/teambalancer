import math
from random import shuffle
import team

class Balancer:
    def __init__(self):
        return

    # Supports balancing multiple teams
    # Optional param to force teamsize
    def partition(self, player_list, teamsize=None):
        teams = []
        if teamsize is None:
            ts = 6
        else:
            ts = teamsize
        number_of_teams = math.ceil(len(player_list)/ts)
        for i in range(0, number_of_teams):
            t = team.Team("Team-"+str(i+1))
            teams.append(t)
        player_list.sort(key=lambda x: x.info['sr'], reverse=True)
        for p in player_list:
            t = self.getLowestTeam(teams)
            t.addplayer(p)

        return teams

    # Partition players by their role first.  Attempt to make
    # each team have 1 DPS, 1 Healer, and 1 Tank
    def rolesort(self, player_list, teamsize=None):
        tanks= []
        dpsers = []
        healers = []
        flexers = []
        teams = []
        for p in player_list:
            if p.info['role'].upper() == "DPS":
                dpsers.append(p)
            elif p.info['role'].upper() == "HEALER":
                healers.append(p)
            elif p.info['role'].upper() == "OFFTANK":
                tanks.append(p)
            elif p.info['role'].upper() == "MAINTANK":
                tanks.append(p)
            else:
                flexers.append(p)
        if teamsize is None:
            ts = 6
        else:
            ts = teamsize
        number_of_teams = math.ceil(len(player_list)/ts)
        shuffle(dpsers)
        shuffle(healers)
        shuffle(tanks)

        # Prevent weird behavior if there are not enough roles
        if len(dpsers) < number_of_teams or len(healers) < number_of_teams or len(tanks) < number_of_teams:
            return self.partition(player_list, ts)  # CODE REVIEW PLZ

        for i in range(0, number_of_teams):  # Create each team with 1 of each role
            t = team.Team("Team-"+str(i+1))
            t.addplayer(dpsers.pop())
            t.addplayer(healers.pop())
            t.addplayer(tanks.pop())
            teams.append(t)

        for p in dpsers:
            flexers.append(p)
        for p in healers:
            flexers.append(p)
        for p in tanks:
            flexers.append(p)

        flexers.sort(key=lambda x: x.info['sr'], reverse=True)
        for p in flexers:
            t = self.getLowestTeam(teams)
            t.addplayer(p)

        return teams

    # Recursion amirite???
    def getLowestTeam(self, teams):
        teams.sort(key=lambda x: x.sum)
        return teams[0]
