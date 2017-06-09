import discord
from discord.ext import commands
import random
import scraper
import player
import balancer
import helper

description = 'Scrim bot generates scrims and automates drafting'
bot = commands.Bot(command_prefix='!', description=description)
scraper = scraper.Scraper()
balancer = balancer.Balancer()
helper = helper.Helper()
known_players = []
active_players = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

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
async def addplayer(*args):
    if len(args) == 0:
        await bot.say("Please provide a list of players to add to the scrim")
        return
    for playerid in args:
        p = helper.findPlayer(playerid, known_players)
        if p is not None:
            active_players.append(p)
            message = 'Adding player ' + p.getName() + ' to scrim'
            await bot.say(helper.formatMessage(message))

@bot.command(desciption='List player information')
async def playerstats(playerid: str):
    message_list = []
    p = helper.findPlayer(playerid, known_players)
    if p is not None:
        message_list.append("Stats for " + p.getName()) 
        message_list.append(" SR:   " + str(p.getSR()))
        message_list.append(" Role: " + p.getRole())
        message_list.append(" Tier: " + p.getTier())
        await bot.say(helper.serializeMessage(message_list))
    else:
        message = "Player unknown (did you type the Bnet ID right?)"
        await bot.say(helper.formatMessage(message))
        

@bot.command(description='List active players')
async def listplayers():
    message_list = []
    for p in active_players:
        message_list.append(p.getName())
    s_message = helper.serializeMessage(message_list)
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
        

@bot.command(description='Start a scrim')
async def scrim():
    return

@bot.command(description='Balance teams in scrim by a certain weight')
async def balance(*args):
    if len(args) == 0:
        await bot.say("Please provide one or more weights to balance")
        return
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

