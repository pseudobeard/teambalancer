import discord
from discord.ext import commands
import scraper
import player
import balancer
import helper
import pickle
import glob
import scrim
import time

description = 'Scrim bot generates scrims and automates drafting'
bot = commands.Bot(command_prefix='scrimbot ', description=description)
scraper = scraper.Scraper()
balancer = balancer.Balancer()
helper = helper.Helper()
active_scrim = scrim.Scrim("Active")
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
    helper.savePlayers(known_players)

@bot.command(description='Adds a player to the active scrim')
async def activate(*args):
    if len(args) == 0:
        await bot.say("Please provide a list of players to add to the scrim")
        return
    for playerid in args:
        p = helper.findPlayer(playerid, known_players)
        if p is not None:
            p.setStatus("Active")
            message = 'Adding player ' + p.getName() + ' to draft pool'
            await bot.say(helper.formatMessage(message))
    helper.savePlayers(known_players)

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
    helper.savePlayers(known_players)


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
                message_list.append(' ' + p.getID())
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
    helper.savePlayers(known_players)

@bot.command(description='Manually update role for a given player')
async def updaterole(playerid: str, role: str):
    p = helper.findPlayer(playerid, known_players)
    if p is not None:
        p.setRole(role)
        message = "Updated " + p.getName()
    else:
        message = "Player unknown (did you type the Bnet ID right?)"
    await bot.say(helper.formatMessage(message))
    helper.savePlayers(known_players)

@bot.command(description='Start a scrim')
async def startscrim(game_map: str):
    active_scrim.setMap(game_map)
    await bot.say("Starting scrim on " + game_map)

#Use chess notation. 1 means Red wins, -1 for Blue, 0 for draw
@bot.command(description='Stop a scrim')
async def stopscrim(result: int):
    red_team, blue_team = active_scrim.getTeams()
    if result == 1:
        active_scrim.setResult("Red")
        for player in red_team:
            player.setWins(player.getWins() + 1)
            player.setStatus("Active")
        for player in blue_team:
            player.setLosses(player.getLosses() + 1)
            player.setStatus("Active")
    elif result == -1:
        active_scrim.setResult("Blue")
        for player in red_team:
            player.setLosses(player.getLosses() + 1)
            player.setStatus("Active")
        for player in blue_team:
            player.setWins(player.getWins() + 1)
            player.setStatus("Active")
    elif result == 0:
        active_scrim.setResult("Draw")
        for player in red_team:
            player.setDraws(player.getDraws() + 1)
            player.setStatus("Active")
        for player in blue_team:
            player.setDraws(player.getDraws() + 1)
            player.setStatus("Active")
    else:
        await bot.say("Result must be 1, -1, or 0")
        return #Early because I want Joe to see this
    await bot.say("Scrim concluded.")
    active_scrim.setName(str(time.time()))
    helper.saveScrim(active_scrim)
    active_scrim.flush()

@bot.command(description="Show the teams for the active scrim")
async def showteams():
    message_list = []
    red_team, blue_team = active_scrim.getTeams()
    message_list.append(balancer.printTeam("Red Team", red_team, "0000", "Draft"))
    message_list.append(balancer.printTeam("Blue Team", blue_team, "0000", "Draft"))
    for message in message_list:
        s_message = helper.serializeMessage(message)
        await bot.say(s_message)
    

@bot.command(description='Draft a player to the given team')
async def draft(playerid: str, team: str):
    active_players = []
    active_players.extend(helper.getAllActive(known_players))
    p = helper.findPlayer(playerid, active_players)
    if p is not None:
        active_scrim.addPlayer(p, team)
        p.setStatus("Drafted")
        message = "Added " + p.getName() + " to " + team + " team."
    else:
        message = "Player unknown (did you type the Bnet ID right?)"
    await bot.say(helper.formatMessage(message))
    helper.savePlayers(known_players)
    return


@bot.command(description='Balance teams in scrim by a certain weight')
async def autobalance(*args):
    if len(args) == 0:
        await bot.say("Please provide one or more weights to balance")
        return
    active_players = []
    for p in known_players:
        if p.getStatus() == "Active":
            active_players.append(p)
    message_list = []
    for weight in args:
        sc = scrim.Scrim(weight)
        status, red_team, r_sum, blue_team, b_sum = balancer.partition(active_players, weight)
        await bot.say(status)
        sc.setTeams(red_team, blue_team)
        message_list.append(balancer.printTeam("Red Team", red_team, r_sum, weight))
        message_list.append(balancer.printTeam("Blue Team", blue_team, b_sum, weight))
        scrims.append(sc)
    for message in message_list:
        s_message = helper.serializeMessage(message)
        await bot.say(s_message)




bot.run('MzIyMTY4MDA3NzY3ODgzNzc2.DBow4w.87CYjhnWdIPhBg7LUCrqc3eWdek')

