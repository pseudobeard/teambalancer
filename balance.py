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
def partition(player_list, weight):
    red_team = []
    red_team_sum = 0
    blue_team = []
    blue_team_sum = 0
    for p in player_list:
        print("  Sorting " + p.getName())
        if red_team_sum < blue_team_sum:
            red_team.append(p)
            red_team_sum += p.getSort(weight)
            print("    Sorted " + p.getName() + " to red team")
        else:
            blue_team.append(p)
            blue_team_sum += p.getSort(weight)
            print("    Sorted " + p.getName() + " to blue team")
    return red_team, red_team_sum, blue_team, blue_team_sum


# Gonna make it look real nice
def printTeam(team, t_sum, weight):
    print ("Team sorted with " + weight)
    print("----------------------------------------")
    string = '{:14}'.format('PlayerName') + '{:>6}'.format('Weight') + '{:>16}'.format("Sum: " + str(t_sum))
    print('| %s |' % string)
    print("|--------------------------------------|")
    for p in team:
        string = '{:14}'.format(p.getName()) + '{:>4.4}'.format(str(p.getSort(weight))) + '{:>18}'.format(p.getRole())
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
    # Initialize the players
    print("Flat weighting uses SR directly with no adjustments")
    print("Tiered weighting maps SR to their tier")
    print("Normalized weighting multiplies SR by it's location in the curve")
    weight = input("Enter weighting: ")
    players = readPlayers('players.txt', 'knownplayers.txt')
    players.sort(key=lambda x: x.getSR(), reverse=True)

    # Sort the players into two roughly balanced teams
    print("Sorting using " + weight)
    red_team, r_sum, blue_team, b_sum = partition(players, weight)
    print("Sorting complete!\n\n")

    # Print the teams
    printTeam(red_team, r_sum, weight)
    printTeam(blue_team, b_sum, weight)


    # Save players to prevent constant lookups
    savePlayers(players, 'knownplayers.txt')
