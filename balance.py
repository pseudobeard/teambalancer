#!/usr/bin/python3

import scraper
import player

def openFile(fileName):
    f = open(fileName, 'r')
    fileContents= []
    for line in f:
        fileContents.append(line.strip())
    f.close()
    return fileContents

def writeFile(fileName, fileContents):
    f = open(fileName, 'a')
    for line in fileContents:
        f.write(line + '\n')
    f.close()
    return

def readPlayers(new_players_file, known_players_file):
    new_players = openFile(new_players_file)
    known_players = openFile(known_players_file)
    player_list = []
    s = scraper.Scraper()
    for playerID in new_players:
        if len(playerID) > 1:
            p = player.Player(playerID)
            player_info = indexIntoLine(p.getID(), known_players)
            if len(player_info) > 1:
                print("Loading " + p.getID() + " from known players")
                p.setSR(int(player_info.split(',')[1]))
                p.setRole(player_info.split(',')[2])
            else:
                print(p.getID() + " not known. Fetching info")
                s.scrape(p)
            player_list.append(p)
    return player_list

def indexIntoLine(index, line_list):
    for line in line_list:
        if index == line.split(',')[0]:
            return line
    return ""

#Takes in a list of players and partitions them into two
#teams using least difference heuristic
def partition(player_list, weight, number_of_teams):
    teams = []
    sums = []
    for i in range(0, number_of_teams): # Create array for each team
        teams.append([])
        sums.append(0);

    for p in player_list:
        shortest_len = -1
        shortest_index = 0
        for i, team in enumerate(teams):
            if (len(team) < shortest_len) or (shortest_len == -1):
                shortest_len = len(team)
                shortest_index = i
        teams[shortest_index].append(p)
        sums[shortest_index] += p.getSort(weight)
    if not all([len(team) == len(teams[0]) for team in teams]):
        print ("No balanced partition found for %s!" % weight)
    return teams, sums



# Gonna make it look real nice
def printTeam(team, t_sum, weight):
    display_sum = str(t_sum)
    print ("Team sorted with " + weight)
    print("----------------------------------------")
    string = '{:14}'.format('PlayerName') + '{:>5}'.format(weight) + '{:>17.6}'.format(display_sum)
    print('| %s |' % string)
    print("|--------------------------------------|")
    for p in team:
        if weight == "Tier":
            display = str(p.getTier())
        elif weight == "Rand":
            display = str('????')
        else:
            display = str(p.getSort(weight))
        string = '{:14}'.format(p.getName()) + '{:>4.4}'.format(display) + '{:>18}'.format(p.getRole())
        print('| %s |' % string)
    print("----------------------------------------\n")

def savePlayers(player_list, known_player_file):
    players_to_save = []
    known_players = openFile(known_player_file)
    for p in player_list:
        line = indexIntoLine(p.getID(), known_players)
        if len(line) < 1:
            players_to_save.append(p.getID() + ',' + str(p.getSR()) + ',' + p.getRole())
    writeFile(known_player_file, players_to_save)
    return

if __name__ == "__main__":
    # Input number of teams to produce
    number_of_teams = int(input("Enter number of teams: "))

    # Initialize the players
    players = readPlayers('players.txt', 'knownplayers.txt')
    players.sort(key=lambda x: x.getSR(), reverse=True)
    weights = ['Curve', 'Flat', 'Tier', 'Rand', 'Throw']
    
    for weight in weights:
        print("\n\n")
        teams, sums = partition(players, weight, number_of_teams)
        for index, team in enumerate(teams):
            print("Team %s" % str(index + 1))
            printTeam(team, sums[index], weight)

    # Save players to prevent constant lookups
    savePlayers(players, 'knownplayers.txt')
