import pickle
import glob
import discord
from pprint import pprint

class Helper:
    def __init__(self):
        return

    def serializeMessage(self, message_list):
        s_line = ''
        for line in message_list:
            s_line = s_line + line + '\n'
        s_line = '```' + s_line + '```'
        return s_line

    def chunkMessage(self, message_list):
        chunkedMessage = []
        for chunk in self.chunks(message_list):
            chunkedMessage.append(self.serializeMessage(chunk))
        pprint(chunkedMessage)
        return chunkedMessage

    def chunks(self, l):
        for i in range(0, len(l), 20):
            yield l[i:i + 20]

    def formatMessage(self, message):
        return '`' + message + '`'


    def checkAdmin(self, discordRoles):
        for role in discordRoles:
            if role.permissions.administrator:
                return True
        return False

    # This makes it easier to get just active players
    # Increases memory footprint of bot but who cares its 2018
    def getAllActive(self, player_list):
        active_players = []
        for p in player_list:
            if p.info['status'] == "Ready":
                active_players.append(p)
        return active_players

    def savePlayers(self, player_list):
        for p in player_list:
            f = open("players/" + p.info['name'] + ".pk", 'wb')
            pk = pickle.Pickler(f, 3)
            pk.dump(p)
            f.close()
        return

    def loadPlayers(self):
        player_list = []
        for filename in glob.glob('players/*.pk'):
            f = open(filename, 'rb')
            pk = pickle.Unpickler(f)
            p = pk.load()
            player_list.append(p)
            f.close()
        return player_list

    def getPlayerByDiscord(self, member: discord.Member, player_list):
        for player in player_list:
            if player.discordID == member:
                return player
        return None

    def getPlayersInVoice(self, server, c_name="Overwatch"):
        for channel in server.channels:
            if channel.name == c_name:
                return channel.voice_members
        return None

    def printPlayerRow(self, p):
        return '{:22.22}'.format(p.info['name']) +  \
                "  " + \
               '{:>4.4}'.format(str(p.info['sr'])) + \
                "  " + \
               '{:<10.10}'.format(p.info['role']) + \
                "  " + \
               '{:>30.30}'.format(p.info['heroes'])