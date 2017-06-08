class Helper:
    def __init__(self):
        return

    def serializeMessage(self, message):
        s_line = ''
        for line in message:
            s_line = s_line + line + '\n'
        s_line = '```' + s_line + '```'
        return s_line

    def formatMessage(self, message):
        return '`' + message + '`'
