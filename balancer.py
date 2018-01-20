import math
from random import shuffle
import team

class Balancer:
    def __init__(self):
        self.team_names = ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']
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
            if len(self.team_names) > 0:
                team_name = self.team_names.pop() # Pop-pop magnitude
            else:
                team_name = "Team-" + str(i+1)
            t = team.Team(team_name)
            teams.append(t)
        player_list.sort(key=lambda x: x.info['sr'], reverse=True)
        for p in player_list:
            t = self.getLowestTeam(teams)
            t.addplayer(p)

        self.resetTeamNames()
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
        shuffle(self.team_names)

        # Prevent weird behavior if there are not enough players of each role to
        # meet the minimum requirements.  Kick it to regular partition.
        if len(dpsers) < number_of_teams or len(healers) < number_of_teams or len(tanks) < number_of_teams:
            print('Could not meet minimum role requirements')
            return self.partition(player_list, ts)  # CODE REVIEW PLZ

        for i in range(0, number_of_teams):  # Create each team with 1 of each role
            if len(self.team_names) > 0:
                team_name = self.team_names.pop() # Pop-pop magnitude
            else:
                team_name = "Team-" + str(i+1)
            t = team.Team(team_name)
            t.addplayer(dpsers.pop())
            t.addplayer(healers.pop())
            t.addplayer(tanks.pop())
            teams.append(t)

        # Now that 1 of each role has been added to each team, we proceed normally
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

        self.resetTeamNames()
        return teams

    # Recursion amirite???
    def getLowestTeam(self, teams):
        teams.sort(key=lambda x: x.sum)
        return teams[0]

    def resetTeamNames(self):
        self.team_names.clear()
        for item in ['Gryffindor', 'Hufflepuff', 'Ravenclaw', 'Slytherin']:
            self.team_names.append(item)
