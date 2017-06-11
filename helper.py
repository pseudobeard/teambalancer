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

    # This makes it easier to get just active players
    # Increases memory footprint of bot but who cares its 2017
    def getAllActive(self, player_list):
        active_players = []
        for p in player_list:
            if p.getStatus() == "Active":
                active_players.append(p)
        return active_players

    def savePlayers(self, player_list):
        for p in player_list:
            f = open("players/" + p.getID() + ".pk", 'wb')
            pk = pickle.Pickler(f, 3)
            pk.dump(p)
            f.close()
        return

    def getScrim(self, scrim_name, scrim_list):
       for s in scrim_list:
           if s.getName() == scrim_name:
               return s
       return None

    def saveScrim(self, sobj):
        f = open("scrims/" + sobj.getName() + ".pk", 'wb')
        pk = pickle.Pickler(f, 3)
        pk.dump(sobj)
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
