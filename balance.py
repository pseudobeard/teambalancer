#!/usr/bin/python3
import time
import os

import math

from getter import Getter
from mapHandler import MapHandler
import scraper
import player
import re

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

# Supports balancing multiple teams
def partitionMultipleTeams(self, player_list, weight):
    player_list.sort(key=lambda x: x.getSR(), reverse=True)
    number_of_teams = math.ceil(len(player_list)/6)
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

def addPlayerPrompt(players, userInput):
    s = scraper.Scraper()

    replacementCriteria = re.compile("update ", re.IGNORECASE)
    userInput = replacementCriteria.sub("", userInput)

    params = userInput.split(" ")

    for battletag in params:
        p = player.Player(battletag)
        p.setStatus(s.scrape(p))

        if p.getStatus() == "Active": players.append(p)
    return players

def generateRandomMap():
    mh = MapHandler()
    print("Map: '" + mh.getMap(False) + "'")

def retirePlayers(players, userInput):
    replacementCriteria = re.compile("retire ", re.IGNORECASE)
    userInput = replacementCriteria.sub("", userInput)

    params = userInput.split(" ")
    newplayers = []

    for battletag in params:
        for p in players:
            if p.getID() == battletag:
                p.setStatus("Inactive")
                print("Retired " + p.getName())
            else:
                newplayers.append(p)
    return newplayers

def retireAllPlayers(players):
    print("Retiring " + len(players) + " players")
    for p in players:
        p.setStatus("Inactive")

def listPlayers(players):
    print("Players: ")
    for p in players:
        print(p.getID() + " - " + str(p.getSR()) + "SR")

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

def tournamentBalance(players):
    mh = MapHandler()
    players.sort(key=lambda x: x.getSR(), reverse=True)
    weights = ['Curve', 'Flat', 'Tier', 'Rand', 'Throw']
    teams, sums = partitionMultipleTeams(players, 'Flat')
    for index, team in enumerate(teams):
        print("Team %s" % str(index + 1))
        printTeam(team, sums[index], 'Flat')
    print("Map: '" + mh.getMap(False) + "'")
    return teams

def displayCommands():
    print("---- Available commands: ----")
    print("update {battletags} - Add specified players to active players (case sensitive)")
    print("streamelements - Import players from streamelements store who bought viewerticket")
    print("randommap - Generates a random map")
    print("retire {battletags} - Remove specified battletags from active players (case sensitive)")
    print("retireall - Remove all players from list of active players")
    print("listplayers - List all active players who will be balanced")
    print("autobalance - Sort active players into two balanced teams")
    print("tournament - Sort players into balanced teams of 6 (more than 2 teams)")
    print("\n")

def runConsole(players):
    userInput = input(">>>>>")
    inputLower = userInput.lower()

    if "update" in inputLower:
        players = addPlayerPrompt(players, userInput)
    if "streamelementsimport" in inputLower or "streamelements" in inputLower or "updateViewerTicket" in inputLower:
        players = importPlayersFromStreamElements(players)
    if "randommap" in inputLower:
        generateRandomMap();
    if "retire" in inputLower:
        players = retirePlayers(players, userInput);
    if "retireAll" in inputLower:
        players = retireAllPlayers(players)
    if "listplayers" in inputLower:
        listPlayers(players)
    if "autobalance" in inputLower:
        balancePlayers(players)
    if "tournament" in inputLower:
        tournamentBalance(players)

    runConsole(players)

if __name__ == "__main__":
    players = []
    displayCommands()
    runConsole(players)
