import math
from pprint import pprint

class Team:
    def __init__(self, name):
        self.players = []
        self.name = name
        self.sum = 0
        self.average = 0

    def addplayer(self, player):
        self.players.append(player)
        self.sum = self.sum + player.info['sr']
        self.average = math.floor(self.sum/len(self.players))

# Gonna make it look real nice
    def printTeam(self):
        message = []
        self.players.sort(key=lambda x: x.info['sr'])
        for p in self.players:
            sr = str(p.info['sr'])
            string = '{:22}'.format(p.info['name']) + '{:>4.4}'.format(sr) + '{:>18}'.format(p.info['role'])
            message.append('  %s  ' % string)
        message.append(self.name + " Average SR: " + '{:>4.4}'.format(str(self.average)))
        message.reverse()
        return message
