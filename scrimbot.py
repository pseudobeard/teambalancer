import discord
from discord.ext import commands
import scraper
import player
import balancer
import helper
import pickle
import glob
import scrim
import mapHandler
import time
from getter import *

description = 'Scrim bot generates scrims and automates drafting'
bot = commands.Bot(command_prefix='~', description=description)
scraper = scraper.Scraper()
balancer = balancer.Balancer()
mapHandler = mapHandler.MapHandler()
helper = helper.Helper()
known_players = []
scrims = []

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    print('Loading players from pickles')
    known_players.extend(helper.loadPlayers())
    print('SCRIMBOT READY')


# @bot.command(description='Updates the players stats from Bnet')
# async def update(*args):
#     if len(args) == 0:
#         await bot.say("Please provide a list of players to update")
#         return
#     else:
#         await bot.say("Updating provided players")
#     for playerid in args:
#         p = helper.findPlayer(playerid, known_players)
#         if p is None:
#             p = player.Player(playerid)
#             known_players.append(p)
#         message = 'Updating player ' + playerid + ' from BattleNet'
#         await bot.say(helper.formatMessage(message))
#         status = scraper.scrape(p)
#         p.setStatus(status)
#     await bot.say("Update complete")
#     helper.savePlayers(known_players)
#
#
# @bot.command(description='Gets players from KarQ StreamElements store who have pending viewertickets')
# async def updateViewerTicket():
#     g = Getter()
#     battletags = g.getViewerGameParticipants()
#
#     for playerid in battletags:
#         p = helper.findPlayer(playerid, known_players)
#         if p is None:
#             p = player.Player(playerid)
#             known_players.append(p)
#         message = 'Updating player ' + playerid + ' from BattleNet'
#         await bot.say(helper.formatMessage(message))
#         scraper.scrape(p)
#         p.setStatus("Active")
#     await bot.say("All players loaded from Stream Elements Store")
#     helper.savePlayers(known_players)
#
# @bot.command(decription='Generate a random map. Add --no2CP to disable 2CP maps')
# async def randomMap(*args):
#     if(len(args) != 0):
#         if (args[0] == "--no2CP"):
#             await bot.say("Map: '" + mapHandler.getMap(True) + "'")
#             return
#     await bot.say("Map: '" + mapHandler.getMap(False) + "'")

# @bot.command(description="Show the teams for the active scrim")
# async def showteams(scrim_name="Active"):
#     s = helper.getScrim(scrim_name, scrims)
#     if s is not None:
#         message_list = []
#         red_team, blue_team = s.getTeams()
#         message_list.append(balancer.printTeam("Red Team", red_team, "Draft"))
#         message_list.append(balancer.printTeam("Blue Team", blue_team, "Draft"))
#         for message in message_list:
#             s_message = helper.serializeMessage(message)
#             await bot.say(s_message)
#     else:
#         await bot.say("Scrim not found.  Are you sure you got the right name?")

# @bot.command(description='Balance teams in scrim by a certain weight')
# async def autobalance(*args):
#     if len(args) == 0:
#         await bot.say("Please provide one or more weights to balance")
#         return
#
#     args = list(args) # convert args to list (was tuple) for easy removal of "--no2CP" arg
#
#     no2CP = False
#     if "--no2CP" in args:
#         no2CP = True
#         args.remove("--no2CP") # Remove "--no2CP" so it does not get treated as a weight name later
#
#     active_players = []
#     for p in known_players:
#         if p.info['status'] == "Active":
#             active_players.append(p)
#     message_list = []
#     for weight in args:
#         sc = scrim.Scrim(weight)
#         status, red_team, blue_team = balancer.partition(active_players, weight) # TODO: convert to multi-team (>2) partition function
#         await bot.say(status)
#         sc.setTeams(red_team, blue_team)
#         message_list.append(balancer.printTeam("Red Team", red_team, weight))
#         message_list.append(balancer.printTeam("Blue Team", blue_team, weight))
#         scrims.append(sc)
#     for message in message_list:
#         s_message = helper.serializeMessage(message)
#         await bot.say(s_message)
#     await bot.say("```Random map: '" + mapHandler.getMap(no2CP) + "'```")


@bot.command(description='Create a tournament')
async def tourney(teamsize=6):
    active_players = []
    for p in known_players:
        if p.info['status'] == "Ready":
            active_players.append(p)
    message_list = []
    teams = balancer.partition(active_players, teamsize)
    for t in teams:
        message_list.append(t.printTeam())
    for message in message_list:
        s_message = helper.serializeMessage(message)
        await bot.say(s_message)

@bot.command(description='Create a tournament')
async def rolesort(teamsize=6):
    active_players = []
    for p in known_players:
        if p.info['status'] == "Ready":
            active_players.append(p)
    message_list = []
    teams = balancer.rolesort(active_players, teamsize)
    for t in teams:
        message_list.append(t.printTeam())
    for message in message_list:
        s_message = helper.serializeMessage(message)
        await bot.say(s_message)


@bot.command(pass_context=True, description='Ready player for drafting')
async def ready(ctx, bnetID=None):
    p = helper.getPlayerByDiscord(ctx.message.author, known_players)
    if p is None:
        p = player.Player(ctx.message.author, bnetID)
        known_players.append(p)
    if bnetID is not None:
        await bot.say(scraper.scrape(p))
    p.info['status'] = "Ready"
    message = p.info['name'] + " is now ready"
    await bot.say(helper.formatMessage(message))

@bot.command(pass_context=True, description='Link BattleNetID to Discord Account')
async def link(ctx, bnetID=None):
    p = helper.getPlayerByDiscord(ctx.message.author, known_players)
    if p is None:
        p = player.Player(ctx.message.author, bnetID)
        known_players.append(p)
    if bnetID is not None:
        p.bnetID = bnetID
        message = (scraper.scrape(p))
    else:
        message = "No BattleNetID provided.  Failed to link"
    await bot.say(helper.formatMessage(message))


@bot.command(pass_context=True, description='Draft player by discord name')
async def draft(ctx, member: discord.Member, team="Lads"):
    p = helper.getPlayerByDiscord(member, known_players)
    if p is not None:
        p.info['status'] = "Drafted"+": "+team
        message = "Drafted " + p.info['name'] + " to " + team
    else:
        message = "Player unknown"
    await bot.say(helper.formatMessage(message))

@bot.command(pass_context=True, description='Manually update SR for a given player')
async def updatesr(ctx, sr: int=None):
    p = helper.getPlayerByDiscord(ctx.message.author, known_players)
    if p is not None and sr is not None:
        if sr < 1 or sr > 5000:
            message = "Your sr must be between 1 and 5000"
        else:
            p.info['sr'] = sr
            message = "Updated " + p.info['name']
    else:
        message = "Player unknown"
    await bot.say(helper.formatMessage(message))
    helper.savePlayers(known_players)

@bot.command(pass_context=True, description='Manually update role for a given player')
async def updaterole(ctx, role: str=None):
    p = helper.getPlayerByDiscord(ctx.message.author, known_players)
    roles = ["DPS", "OFFTANK", "MAINTANK", "HEALER", "FLEX"]
    if p is not None and role is not None:
        role_mod = role.upper()
        if role_mod not in roles:
            message = "Your role must be dps, offtank, maintank, healer, or flex"
        else:
            p.info['role'] = role_mod
            message = "Updated " + p.info['name']
    else:
        message = "Player unknown or role not specified"
    await bot.say(helper.formatMessage(message))
    helper.savePlayers(known_players)


@bot.command(pass_context=True, desciption='List player information')
async def stats(ctx, member: discord.Member=None):
    if member is not None:
        p = helper.getPlayerByDiscord(member, known_players)
    else:
        p = helper.getPlayerByDiscord(ctx.message.author, known_players)
    message_list = []
    if p is not None:
        message_list.append("Statistics for " + p.info['name'])
        message_list.append(" Status: " + p.info['status'])
        message_list.append(" SR:     " + str(p.info['sr']))
        message_list.append(" Role:   " + p.info['role'])
        message_list.append(p.info['name'] + " has been fat kid " + str(p.info['fat']) + " times")
        await bot.say(helper.serializeMessage(message_list))
    else:
        message = "Player unknown (ready up or correctly identify player by Discord ID)"
        await bot.say(helper.formatMessage(message))

@bot.command(description='List players by status')
async def list():
    active_players_list = helper.getAllActive(known_players)
    drafted_players_list = helper.getAllDrafted(known_players)
    active_players_list.sort(key=lambda x: x.info['sr'])
    message_list = []
    for p in active_players_list:
        string = '{:22}'.format(p.info['name']) + '{:>4.4}'.format(str(p.info['sr'])) + '{:>18}'.format(p.info['role'])
        message_list.append(string)
    message = str(len(active_players_list)) + " players listed as Ready"
    message_list.append(message)
    s_message = helper.serializeMessage(reversed(message_list))
    await bot.say(s_message)

    message_list = []
    for p in drafted_players_list:
        string = '{:22}'.format(p.info['name']) + '{:>4.4}'.format(str(p.info['sr'])) + '{:>30}'.format(p.info['status'])
        message_list.append(string)
    message = str(len(drafted_players_list)) + " players listed as Drafted"
    message_list.append(message)
    s_message = helper.serializeMessage(reversed(message_list))
    await bot.say(s_message)

    message_list = []
    for p in known_players:
        if p not in active_players_list and p not in drafted_players_list:
            string = '{:22}'.format(p.info['name']) + '{:>18}'.format(p.info['status'])
            message_list.append(string)
    message = str(len(message_list)) + " non-active players"
    message_list.append(message)
    s_message = helper.serializeMessage(reversed(message_list))
    await bot.say(s_message)

@bot.command(description='List players by role')
async def listrole(role: str=None):
    active_players_list = helper.getAllActive(known_players)
    active_players_list.sort(key=lambda x: x.info['sr'])
    message_list = []
    for p in active_players_list:
        if p.info['role'] == role.upper():
            string = '{:22}'.format(p.info['name']) + '{:>4.4}'.format(str(p.info['sr'])) + '{:>18}'.format(p.info['role'])
            message_list.append(string)
    message = "Players listed as " + role + ":"
    message_list.append(message)
    s_message = helper.serializeMessage(reversed(message_list))
    await bot.say(s_message)


@bot.command(description='Retire all players')
async def retireall():
    for player in known_players:
        player.info['status'] = 'Inactive'
    message = "Set all players to inactive"
    await bot.say(helper.formatMessage(message))

@bot.command(description='Ready all players')
async def readyall():
    for player in known_players:
        player.info['status'] = 'Ready'
    message = "Set all players to ready"
    await bot.say(helper.formatMessage(message))

@bot.command(pass_context=True, description='Clean')
async def clean(ctx, teamsize=6):
    for p in known_players:
        p.info['status'] = 'Inactive'
    server = ctx.message.server
    players = []
    for channel in server.channels:
        if channel.name == "Overwatch":
            for member in channel.voice_members:
                p = helper.getPlayerByDiscord(member, known_players)
                if p is None:
                    p = player.Player(member)
                    known_players.append(p)
                p.info['status'] = "Ready"
                players.append(p)
    # Take the new player list and partition it
    message_list = []
    teams = balancer.rolesort(players, teamsize)
    for t in teams:
        message_list.append(t.printTeam())
    for message in message_list:
        s_message = helper.serializeMessage(message)
        await bot.say(s_message)

@bot.command(pass_context=True, description="Marks a player as 'inactive'")
async def retire(ctx):
    p = helper.getPlayerByDiscord(ctx.message.author, known_players)
    if p is not None:
        p.info['status'] = "Inactive"
        message = 'Removing player ' + p.info['name'] + ' from draft pool'
        await bot.say(helper.formatMessage(message))
    else:
        await bot.say("Can't retire a player that doesn't exist you nerd")
    helper.savePlayers(known_players)

@bot.command(description='Fat')
async def fat(member: discord.Member=None):
    p = helper.getPlayerByDiscord(member, known_players)
    if p is not None:
        p.info['fat'] = p.info['fat'] + 1
    message = "Someone eats too many pies"
    await bot.say(helper.formatMessage(message))


@bot.command(description='Repair')
async def repair():
    roles = ["DPS", "OFFTANK", "MAINTANK", "HEALER", "FLEX"]
    for p in known_players:
        sr = p.info['sr']
        if p.info['role'] not in roles:
            scraper.scrape(p)
            await bot.say("Repaired role for " + p.info['name'])
        p.info['sr'] = sr
    await bot.say("Repairs completed")


bot.run('MzIyMTY4MDA3NzY3ODgzNzc2.DT8Ixw.m6LISJNK0zuWt32jgmPEKVm9bsM')

