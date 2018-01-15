import discord

class Player:
    def __init__(self, did: discord.Member, bid=None):
        self.info = {}
        self.bnetID = bid
        self.discordID = did
        self.info['sr'] = 2500
        self.info['role'] = "Flex"
        self.info['status'] = "Inactive"
        self.info['name'] = self.discordID.name
        self.info['fat'] = 0
