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

@bot.command(pass_context=True, description='Manually update heroes for a given player')
async def updatenotes(ctx, heroes: str=None):
    p = helper.getPlayerByDiscord(ctx.message.author, known_players)
    if p is not None and heroes is not None:
        p.info['heroes'] = heroes
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
        message_list.append(" Heroes: " + p.info['heroes'])
        message_list.append(p.info['name'] + " has been fat kid " + str(p.info['fat']) + " times")
        await bot.say(helper.serializeMessage(message_list))
    else:
        message = "Player unknown (ready up or correctly identify player by Discord ID)"
        await bot.say(helper.formatMessage(message))

@bot.command(description='List players by status')
async def list():
    active_players_list = helper.getAllActive(known_players)
    active_players_list.sort(key=lambda x: x.info['sr'], reverse=True)
    message_list = []
    for p in active_players_list:
        message_list.append(helper.printPlayerRow(p))
    message = str(len(active_players_list)) + " players listed as Ready"
    await bot.say(message)
    s_message = helper.chunkMessage(message_list)
    for m in s_message:
        await bot.say(m)

@bot.command(pass_context=True, description='List players in the voice channel')
async def listvoice(ctx):
    server = ctx.message.server
    members = helper.getPlayersInVoice(server, "Overwatch")
    message_list = []
    for member in members:
        p = helper.getPlayerByDiscord(member, known_players)
        message_list.append(helper.printPlayerRow(p))
    s_message = helper.chunkMessage(message_list)
    for m in s_message:
        await bot.say(m)


@bot.command(description='List players by role')
async def listrole(role: str=None):
    active_players_list = helper.getAllActive(known_players)
    active_players_list.sort(key=lambda x: x.info['sr'], reverse=True)
    message_list = []
    for p in active_players_list:
        if role.upper() in p.info['role']:
            message_list.append(helper.printPlayerRow(p))
    message = "Players listed as " + role + ":"
    await bot.say(message)
    s_message = helper.chunkMessage(message_list)
    for m in s_message:
        await bot.say(m)


@bot.command(pass_context=True, description='Retire all players')
async def retireall(ctx):
    if not helper.checkAdmin(ctx.message.author.roles):
        await bot.say("You must be an admin to do this")
        return
    for player in known_players:
        player.info['status'] = 'Inactive'
    message = "Set all players to inactive"
    await bot.say(helper.formatMessage(message))

@bot.command(pass_context=True, description='Ready all players')
async def readyall(ctx):
    if not helper.checkAdmin(ctx.message.author.roles):
        await bot.say("You must be an admin to do this")
        return
    for player in known_players:
        player.info['status'] = 'Ready'
    message = "Set all players to ready"
    await bot.say(helper.formatMessage(message))

@bot.command(pass_context=True, description='Ready all players in voice')
async def readyvoice(ctx):
    if not helper.checkAdmin(ctx.message.author.roles):
        await bot.say("You must be an admin to do this")
        return
    server = ctx.message.server
    members = helper.getPlayersInVoice(server, "Overwatch")
    for member in members:
        p = helper.getPlayerByDiscord(member, known_players)
        if p is not None:
            p.info['status'] = 'Ready'
    message = "Set all players in voice chat to ready"
    await bot.say(helper.formatMessage(message))


@bot.command(pass_context=True, description='Check on stuff')
async def playercheck(ctx):
    if not helper.checkAdmin(ctx.message.author.roles):
        await bot.say("You must be an admin to do this")
        return
    message_list = []
    known_players.sort(key=lambda x: x.info['sr'])
    for p in known_players:
        message_list.append(helper.printPlayerRow(p))
    message_list.reverse()
    s_message = helper.chunkMessage(message_list)
    for m in s_message:
        await bot.say(m)


@bot.command(pass_context=True, description='Clean')
async def clean(ctx, teamsize=6):
    for p in known_players:
        p.info['status'] = 'Inactive'
    server = ctx.message.server
    players = []
    members = helper.getPlayersInVoice(server)
    for member in members:
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


@bot.command(pass_context=True, description='Repair')
async def repair(ctx):
    if not helper.checkAdmin(ctx.message.author.roles):
        await bot.say("You must be an admin to do this")
        return
    roles = ["DPS", "OFFTANK", "MAINTANK", "HEALER", "FLEX"]
    for p in known_players:
        sr = p.info['sr'] # Returns none, if unset
        if p.info['sr'] is None or p.info['role'] not in roles or p.info['heroes'] == "JeffKaplan":
            scraper.scrape(p)
            if sr is not None: # Keep over-written sr, if it exists
                p.info['sr'] = sr
            elif p.info['sr'] is None: # Player hasn't placed, or api down
                p.info['sr'] = 2500
            await bot.say("Repairs made for " + p.info['name'])
    await bot.say("Repairs completed")

@bot.command(pass_context=True, description="Summon the people playing overwatch to scrim")
@commands.cooldown(1, 3600, commands.BucketType.server)
async def summon(ctx):
    role = await bot.create_role(ctx.message.server, name="Playing_Overwatch")
    for m in ctx.message.server.members:
        if m.game is not None:
           if m.game.name == "Overwatch":
                await bot.add_roles(m, role)
                print("Role added to " + m.name)
    await bot.say(role.mention)
    await bot.delete_role(ctx.message.server, role)
    print("Deleted the role")



bot.run('MzIyMTY4MDA3NzY3ODgzNzc2.DT8Ixw.m6LISJNK0zuWt32jgmPEKVm9bsM')

