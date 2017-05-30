#!/usr/bin/python3

import scraper
import player

def openFile(fileName):
    f = open(fileName, 'r')
    fileContents = f.readlines()
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
    for line in new_players:
        playerID = line[:-1]
        p = player.Player(playerID)
        player_info = indexIntoLine(p.getID(), known_players)
        if len(player_info) > 1:
            print("Loading " + p.getID() + " from known players")
            p.setSR(int(player_info.split(',')[1]))
            p.setRole(player_info.split(',')[2][:-1])
        else:
            print(p.getID() + " not known. Fetching info")
            s.scrape(p)
        player_list.append(p)
    return player_list

def indexIntoLine(index, line_list):
    for line in line_list:
        tokens = line.split(',')
        if index == tokens[0]:
            return line
    return ""
  

#Takes in a list of players and partitions them into two
#teams using least difference heuristic
def partition(player_list):
    red_team = []
    red_team_average_sr = 0
    red_team_weighted_sr = 0
    blue_team = []
    blue_team_average_sr = 0
    blue_team_weighted_sr = 0
    for p in player_list:
        print("  Sorting " + p.getName())
        if red_team_weighted_sr < blue_team_weighted_sr:
            red_team.append(p)
            red_team_weighted_sr += p.getWeightedSR()
            red_team_average_sr += p.getSR()
            print("    Sorted " + p.getName() + " to red team")
        else:
            blue_team.append(p)
            blue_team_weighted_sr += p.getWeightedSR()
            blue_team_average_sr += p.getSR()
            print("    Sorted " + p.getName() + " to blue team")
    return red_team, blue_team


# Gonna make it look real nice
def printTeam(team):
    for p in team:
        string = '{:14}'.format(p.getName()) + '{:4}'.format(p.getSR()) + '{:>18}'.format(p.getRole())
        print('| %s |' % string)

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
    # Initialize the players
    players = readPlayers('players.txt', 'knownplayers.txt')
    players.sort(key=lambda x: x.getSR(), reverse=True)

    # Greedy algorithm. Sort by weighted SR and pop off
    print("Begin Sorting")
    red_team, blue_team = partition(players)
    print("Sorting complete")
    print("----------------------------------------")

    # Print the teams
    printTeam(red_team)
    print("----------------------------------------")
    printTeam(blue_team)

    # Save players to prevent constant lookups
    savePlayers(players, 'knownplayers.txt')
