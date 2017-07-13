#!/usr/bin/python3
import time
from inviter import Inviter
from getter import Getter
from mover import Mover
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

if __name__ == "__main__":
    # Input number of teams to produce
    number_of_teams = int(input("Enter number of teams: "))

    getFromStreamElements = input(
        "Would you like to import all players who bought 'Viewer Game Sunday Ticket' on StreamElements? (Y/N)")

    players = []
    if getFromStreamElements.lower() == "y":
        g = Getter()
        scraper = scraper.Scraper()
        loadedPlayers = g.getViewerGameParticipants()

        for pID in loadedPlayers:
            p = player.Player(pID)
            scraper.scrape(p)
            players.append(p)
    else:
        # Initialize the players
        players = readPlayers('players.txt', 'knownplayers.txt')

    while True:
        scraper = scraper.Scraper()
        newPlayer = input("Add additional player battletag (or type 'continue' to start balancing): ")
        if newPlayer.lower() == 'continue':
            break
        else:
            p = player.Player(newPlayer)
            scraper.scrape(p)
            players.append(p)

    players.sort(key=lambda x: x.getSR(), reverse=True)
    weights = ['Curve', 'Flat', 'Tier', 'Rand', 'Throw']

    teams, sums = partition(players, 'Flat', number_of_teams)
    for index, team in enumerate(teams):
        print("Team %s" % str(index + 1))
        printTeam(team, sums[index], 'Flat')

    # Auto-invite players
    autoinvite()

    # Auto-move players
    automove(teams[0], teams[1])

    print("Automove sometimes needs to be run a second time to work fully")
    automove(teams[0], teams[1])

    # Save players to prevent constant lookups
    savePlayers(players, 'knownplayers.txt')
