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
            string = '{:22.22}'.format(p.info['name']) +  \
                "  " + \
               '{:>4.4}'.format(str(p.info['sr'])) + \
                "  " + \
               '{:<10.10}'.format(p.info['role']) + \
                "  "
            if p.bnetID is not None:
                string = string + '{:>20.20}'.format(p.bnetID)
            else:
                string = string + '{:>20.20}'.format("No bnetID linked")
            message.append('  %s  ' % string)
        message.append(self.name + " Average SR: " + '{:>4.4}'.format(str(self.average)))
        message.reverse()
        return message

    def toJSON(self):
        json_dict = {}
        json_dict['players'] = []
        json_dict['team'] = self.name
        json_dict['average'] = self.average
        for p in self.players:
            player_dict = {}
            player_dict['name'] = p.info['name']
            player_dict['sr'] = p.info['sr']
            player_dict['role'] = p.info['role']
            if p.bnetID is not None:
                player_dict['battlenetID'] = p.bnetID
            else:
                player_dict['battlenetID'] = "No-bnet-id"
            json_dict['players'].append(player_dict)
        return json_dict