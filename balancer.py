import math

class Balancer:
    def __init__(self):
        return

    # Supports balancing multiple teams
    def partition(self, player_list):
        player_list.sort(key=lambda x: x.info['sr'], reverse=True)
        number_of_teams = math.ceil(len(player_list)/6)
        teams = []
        sums = []
        for i in range(0, number_of_teams):  # Create array for each team
            teams.append([])
            sums.append(0)

        for p in player_list:
            lowest_sum = -1
            lowest_index = 0
            for i, team in enumerate(teams):  # Get team with lowest sum
                if (sums[i] < lowest_sum) or (lowest_sum == -1):
                    lowest_sum = sums[i]
                    lowest_index = i
            teams[lowest_index].append(p)  # Add player to lowest sum team
            sums[lowest_index] += p.info['sr']
        if not all([len(team) == len(teams[0]) for team in teams]):  # If not all teams are the same length
            message = "No balanced partition found"
        else:
            message = "Created balanced partition"
        return message, teams

# Gonna make it look real nice
    def printTeam(self, t_name, team):
        message = []
        team_sum = 0
        message.append(t_name + " sorted")
        for p in team:
            display = str(p.info['sr'])
            team_sum = team_sum + p.info['sr']
            string = '{:22}'.format(p.info['name']) + '{:>4.4}'.format(display) + '{:>18}'.format(p.info['role'])
            message.append('  %s  ' % string)
        message.append("Team Average SR: " + '{:>4.4}'.format(str(math.floor(team_sum/len(team)))))
        return message
