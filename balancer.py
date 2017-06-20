class Balancer:
    def __init__(self):
        return

    def partition(self, player_list, weight):
        player_list.sort(key=lambda x: x.getSR(), reverse=True)
        red_team = []
        red_team_sum = 0
        blue_team = []
        blue_team_sum = 0
        for p in player_list:
            if red_team_sum < blue_team_sum:
                red_team.append(p)
                red_team_sum += p.getSort(weight)
            else:
                blue_team.append(p)
                blue_team_sum += p.getSort(weight)
        if (len(red_team) != len(blue_team)):
            message = "No balanced partition found for " + weight
        else:
            message = "Created balanced partition for " + weight
        return message, red_team, blue_team

    # Supports balancing multiple teams
    def partitionMultipleTeams(self, player_list, weight, number_of_teams): # TODO: Phase out regular partition function, replace with this
        player_list.sort(key=lambda x: x.getSR(), reverse=True)
        teams = []
        sums = []
        for i in range(0, number_of_teams):  # Create array for each team
            teams.append([])
            sums.append(0);

        for p in player_list:
            lowest_sum = -1
            lowest_index = 0
            for i, team in enumerate(teams):  # Get team with lowest sum
                if (sums[i] < lowest_sum) or (lowest_sum == -1):
                    lowest_sum = sums[i]
                    lowest_index = i
            teams[lowest_index].append(p)  # Add player to lowest sum team
            sums[lowest_index] += p.getSort(weight)
        if not all([len(team) == len(teams[0]) for team in teams]):  # If not all teams are the same length
            message = "No balanced partition found for " + weight
        else :
            message = "Created balanced partition for " + weight
        return message, teams, sums

# Gonna make it look real nice
    def printTeam(self, t_name, team, weight):
        message = []
        message.append(t_name + " sorted with " + weight)
        for p in team:
            if weight == "Tier":
                display = str(p.getTier())
            elif weight == "Rand":
                display = str('????')
            else:
                display = str(p.getSort(weight))
            string = '{:14}'.format(p.getName()) + '{:>4.4}'.format(display) + '{:>18}'.format(p.getRole())
            message.append('  %s  ' % string)
        return message
