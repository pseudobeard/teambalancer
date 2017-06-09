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


