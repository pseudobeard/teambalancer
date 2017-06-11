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
