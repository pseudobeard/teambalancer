#!/usr/bin/python3
import time
import os
from getter import Getter
from mapHandler import MapHandler
import scraper
import player

if os.name == 'nt': # If Windows
    from inviter import Inviter
    from mover import Mover

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
    player_list.sort(key=lambda x: x.getSR(), reverse=True)
    teams = []
    sums = []
    for i in range(0, number_of_teams): # Create array for each team
        teams.append([])
        sums.append(0);

    for p in player_list:
        lowest_sum = -1
        lowest_index = 0
        for i, team in enumerate(teams): # Get team with lowest sum
            if (sums[i] < lowest_sum) or (lowest_sum == -1):
                lowest_sum = sums[i]
                lowest_index = i
        teams[lowest_index].append(p) # Add player to lowest sum team
        sums[lowest_index] += p.getSort(weight)
    if not all([len(team) == len(teams[0]) for team in teams]): # If not all teams are the same length
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
    print("----------------------------------------")
    if len(team) != 0:
        print("Average SR: " + str(int(t_sum / len(team))) + "\n")

def savePlayers(player_list, known_player_file):
    players_to_save = []
    known_players = openFile(known_player_file)
    for p in player_list:
        line = indexIntoLine(p.getID(), known_players)
        if len(line) < 1:
            players_to_save.append(p.getID() + ',' + str(p.getSR()) + ',' + p.getRole())
    writeFile(known_player_file, players_to_save)
    return

def autoinvite():
    print("\n\nAuto invite players to custom game? (WINDOWS ONLY) (Y/N) ")
    response = input()
    if response.lower() == "y":
        print("For auto-invite to work, you must have Overwatch in 1920x1080 and in fullscreen mode.")
        print(
            "Start a custom game, then tab back to this program and press enter to start. Tab back into Overwatch within 10 seconds, and leave the keyboard/mouse until completed.")
        input()

        time.sleep(1)

        inviter = Inviter()

        print("\n\nOpen custom game lobby!")
        for i in range(10, 0, -1):
            print("Starting in", i)
            time.sleep(1)

        inviter.invite_players(players)

def automove(team1, team2):
    team1names = []
    team2names = []

    for team1player in team1:
        team1names.append(team1player.getName())

    for team2player in team2:
        team2names.append(team2player.getName())

    print("\n\nAuto move players in custom game? (WINDOWS ONLY) (Y/N) ")
    response = input()
    if response.lower() == "y":
        m = Mover()

        print("\n\nTab into Overwatch!")
        for i in range(10, 0, -1):
            print("Starting in", i)
            time.sleep(1)

        m.move_teams(team1names, team2names)

def addPlayerPrompt(players):
    s = scraper.Scraper()
    newPlayer = input("Add additional player battletag (or type 'continue' to start balancing): ")
    p = player.Player(newPlayer)
    p.setStatus(s.scrape(p))

    if p.getStatus() == "Active": players.append(p)

def generateRandomMap():
    mh = MapHandler()
    print("Map: '" + mh.getMap(False) + "'")

def retirePlayerPrompt(players):
    battletag = input("Enter player name: ")
    for p in players:
        if p.getName == battletag:
            p.setStatus("Inactive")
            print("Retired " + p.getName())

def retireAllPlayers(players):
    print("Retiring " + len(players) + " players")
    for p in players:
        p.setStatus("Inactive")

def listPlayers(players):
    print("Players: ")
    for p in players:
        print(p.getName() + " - " + str(p.getSR()) + "SR")

def importPlayersFromStreamElements(players):
    g = Getter()
    s = scraper.Scraper()
    loadedPlayers = g.getViewerGameParticipants()
    for pID in loadedPlayers:
        p = player.Player(pID)
        p.setStatus(s.scrape(p))
        if p.getStatus() == "Active": players.append(p)
    return players

def balancePlayers(players):
    mh = MapHandler()
    players.sort(key=lambda x: x.getSR(), reverse=True)
    weights = ['Curve', 'Flat', 'Tier', 'Rand', 'Throw']
    teams, sums = partition(players, 'Flat', 2)
    for index, team in enumerate(teams):
        print("Team %s" % str(index + 1))
        printTeam(team, sums[index], 'Flat')
    print("Map: '" + mh.getMap(False) + "'")
    return teams

def runConsole(players):
    userInput = input(">>>>>").lower()

    if userInput == "update":
        addPlayerPrompt(players)
    if userInput == "streamelementsimport" or userInput == "streamelements" or userInput == "updateViewerTicket":
        importPlayersFromStreamElements(players)
    if userInput == "randommap":
        generateRandomMap();
    if userInput == "retire":
        retirePlayerPrompt(players);
    if userInput == "retireAll":
        retireAllPlayers(players)
    if userInput == "listplayers":
        listPlayers(players)
    if userInput == "autobalance":
        balancePlayers(players)

    runConsole(players)

if __name__ == "__main__":
    # Input number of teams to produce
    # number_of_teams = int(input("Enter number of teams: "))
    #
    # getFromStreamElements = input(
    #     "Would you like to import all players who bought 'Viewer Game Sunday Ticket' on StreamElements? (Y/N)")
    #
    # s = scraper.Scraper()
    # mh = MapHandler()

    players = []

    runConsole(players)

    # if getFromStreamElements.lower() == "y":
    #     importPlayersFromStreamElements(players)
    # else:
    #     # Initialize the players
    #     players = readPlayers('players.txt', 'knownplayers.txt')
    #
    # addPlayerPrompt(players)
    #
    # teams = balancePlayers(players)
    #
    # # Auto-invite players
    # autoinvite()
    #
    # # Auto-move players
    # automove(teams[0], teams[1])
    #
    # # Save players to prevent constant lookups
    # savePlayers(players, 'knownplayers.txt')
