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
    for arg in args:
        playerFound = False
        for i in known_players:
            if arg == i.getID():
                p = i
                playerFound = True
                break
        if not playerFound:
            p = player.Player(arg) 
            active_players.append(p)
        message = 'Updating player ' + arg + ' from BattleNet'
        await bot.say(helper.formatMessage(message))
        scraper.scrape(p)
    await bot.say("Update complete")

@bot.command(description='List active players')
async def listplayers():
    message_list = []
    for p in active_players:
        message_list.append(p.getName())
    s_message = helper.serializeMessage(message)

@bot.command(description='Add a player to active roster')

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
        message_list.append(balancer.printTeam(red_team, r_sum, weight))
        message_list.append(balancer.printTeam(blue_team, b_sum, weight))
    for message in message_list:
        s_message = helper.serializeMessage(message)
        await bot.say(s_message)




bot.run('MzIyMTY4MDA3NzY3ODgzNzc2.DBow4w.87CYjhnWdIPhBg7LUCrqc3eWdek')

