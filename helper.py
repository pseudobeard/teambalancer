import pickle
import glob

class Helper:
    def __init__(self):
        return

    def serializeMessage(self, message_list):
        s_line = ''
        for line in message_list:
            s_line = s_line + line + '\n'
        s_line = '```' + s_line + '```'
        return s_line

    def formatMessage(self, message):
        return '`' + message + '`'

    # Returns a player object if that player is found in a list, otherwise none
    def findPlayer(self, playerid, player_list):
        for p in player_list:
            if p.getID() == playerid:
                return p
        return None

    def savePlayers(self, player_list):
        for p in player_list:
            f = open("players/" + p.getID() + ".pk", 'wb')
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
