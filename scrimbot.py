import discord
from discord.ext import commands
import random
import scraper
import player
import balancer
import helper
import pickle
import glob

description = 'Scrim bot generates scrims and automates drafting'
bot = commands.Bot(command_prefix='scrimbot ', description=description)
scraper = scraper.Scraper()
balancer = balancer.Balancer()
helper = helper.Helper()
known_players = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print('Loading players from pickles')
    for filename in glob.glob('players/*.pk'):
        f = open(filename, 'rb')
        pk = pickle.Unpickler(f)
        p = pk.load()
        known_players.append(p)
        f.close()
    print('SCRIMBOT READY')

@bot.command(description='Updates the players stats from Bnet')
async def updateplayer(*args):
    if len(args) == 0:
        await bot.say("Please provide a list of players to update")
        return
    else:
        await bot.say("Updating provided players")
    for playerid in args:
        p = helper.findPlayer(playerid, known_players)
        if p is None:
            p = player.Player(playerid)
            known_players.append(p)
        message = 'Updating player ' + playerid + ' from BattleNet'
        await bot.say(helper.formatMessage(message))
        scraper.scrape(p)
    await bot.say("Update complete")

@bot.command(description='Adds a player to the active scrim')
async def activate(*args):
    if len(args) == 0:
        await bot.say("Please provide a list of players to add to the scrim")
        return
    for playerid in args:
        p = helper.findPlayer(playerid, known_players)
        if p is not None:
            p.setStatus("Available")
            message = 'Adding player ' + p.getName() + ' to draft pool'
            await bot.say(helper.formatMessage(message))

@bot.command(description="Marks a player as 'inactive'")
async def retire(*args):
    if len(args) == 0:
        await bot.say("Please provide a list of players to add to the scrim")
        return
    for playerid in args:
        p = helper.findPlayer(playerid, known_players)
        if p is not None:
            p.setStatus("Inactive")
            message = 'Removing player ' + p.getName() + ' from draft pool'
            await bot.say(helper.formatMessage(message))


@bot.command(desciption='List player information')
async def playerstats(playerid: str):
    message_list = []
    p = helper.findPlayer(playerid, known_players)
    if p is not None:
        message_list.append("Statistics for " + p.getName()) 
        message_list.append(" Status: " + p.getStatus())
        message_list.append(" SR:     " + str(p.getSR()))
        message_list.append(" Role:   " + p.getRole())
        message_list.append(" Tier:   " + p.getTier())
        message_list.append(" Record: " + p.getRecord())
        message_list.append(p.getName() + " has been fat kid " + str(p.getFatkids()) + " times")
        await bot.say(helper.serializeMessage(message_list))
    else:
        message = "Player unknown (did you type the Bnet ID right?)"
        await bot.say(helper.formatMessage(message))
        

@bot.command(description='List players by status')
async def listplayers(*args):
    if len(args) == 0:
        await bot.say("Please provide the list criteria")
        return
    for status in args:
        message_list = []
        for p in known_players:
            if p.getStatus() == status:
                message_list.append(' ' + p.getName())
        message = str(len(message_list)) + " players listed as " + status
        message_list.append(message)  
        s_message = helper.serializeMessage(reversed(message_list))
        await bot.say(s_message)

@bot.command(description='Manually update SR for a given player')
async def updatesr(playerid: str, sr: int):
    p = helper.findPlayer(playerid, known_players)
    if p is not None:
        p.setSR(sr)
        message = "Updated " + p.getName()
    else:
        message = "Player unknown (did you type the Bnet ID right?)"
    await bot.say(helper.formatMessage(message))

@bot.command(description='Manually update role for a given player')
async def updaterole(playerid: str, role: str):
    p = helper.findPlayer(playerid, known_players)
    if p is not None:
        p.setRole(role)
        message = "Updated " + p.getName()
    else:
        message = "Player unknown (did you type the Bnet ID right?)"
    await bot.say(helper.formatMessage(message))

@bot.command(description='Start, finish, or cancel a scrim')
async def scrim(*args):
    active_players = []
    await bot.say("Starting scrim")
    for p in known_players:
        if p.getStatus() == "Available":
            active_players.append(p)
    await bot.say("There are " + str(len(active_players)) + " available for drafting")

@bot.command(description='Draft a player to the given team')
async def draft(playerid: str, team: str):
    return


@bot.command(description='Save the players')
async def saveplayers():
    for p in known_players:
        f = open("players/" + p.getID() + ".pk", 'wb')
        pk = pickle.Pickler(f, 3)
        pk.dump(p)
        f.close()
    await bot.say("Pickled players")

@bot.command(description='Balance teams in scrim by a certain weight')
async def autobalance(*args):
    if len(args) == 0:
        await bot.say("Please provide one or more weights to balance")
        return
    active_players = []
    for p in known_players:
        if p.getStatus() == "Available":
            active_players.append(p)
            p.setStatus("Drafted")
    message_list = []
    for weight in args:
        status, red_team, r_sum, blue_team, b_sum = balancer.partition(active_players, weight)
        await bot.say(status)
        message_list.append(balancer.printTeam("Red Team", red_team, r_sum, weight))
        message_list.append(balancer.printTeam("Blue Team", blue_team, b_sum, weight))
    for message in message_list:
        s_message = helper.serializeMessage(message)
        await bot.say(s_message)




bot.run('MzIyMTY4MDA3NzY3ODgzNzc2.DBow4w.87CYjhnWdIPhBg7LUCrqc3eWdek')

