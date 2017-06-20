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
bot = commands.Bot(command_prefix='', description=description)
scraper = scraper.Scraper()
balancer = balancer.Balancer()
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


@bot.command(description='Updates the players stats from Bnet')
async def update(*args):
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
            p.setStatus("Active")
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
        await bot.say("Please provide a list of players to retire")
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
async def listplayers():
    active_players_list = helper.getAllActive(known_players)
    active_players_list.sort(key=lambda x: x.getSR())
    message_list = []
    for p in active_players_list:
        string = '{:>2.2}'.format(str(active_players_list.index(p)+1)) + ': ' + '{:22}'.format(p.getID()) + '{:>4.4}'.format(str(p.getSR())) + '{:>18}'.format(p.getRole())
        message_list.append(string)
    message = str(len(active_players_list)) + " players listed as Active"
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
async def startscrim(scrim_name="Active"):
    s = scrim.Scrim(scrim_name)
    scrims.append(s)
    await bot.say("Starting scrim " + scrim_name)

@bot.command(description='List scrims')
async def listscrims():
    message_list = []
    for s in scrims:
        message_list.append(s.getName())
    s_message = helper.serializeMessage(message_list)
    await bot.say(s_message)

#Use chess notation. 1 means Red wins, -1 for Blue, 0 for draw
@bot.command(description='Stop a scrim')
async def stopscrim(result: str, scrim_name="Active"):
    active_scrim = helper.getScrim(scrim_name, scrims)
    if active_scrim is not None:
        red_team, blue_team = active_scrim.getTeams()
        if result.lower() == "red":
            active_scrim.setResult("Red")
            for player in red_team:
                player.setWins(player.getWins() + 1)
                player.setStatus("Active")
            for player in blue_team:
                player.setLosses(player.getLosses() + 1)
                player.setStatus("Active")
        elif result.lower() == "blue":
            active_scrim.setResult("Blue")
            for player in red_team:
                player.setLosses(player.getLosses() + 1)
                player.setStatus("Active")
            for player in blue_team:
                player.setWins(player.getWins() + 1)
                player.setStatus("Active")
        elif result.lower() == "draw":
            active_scrim.setResult("Draw")
            for player in red_team:
                player.setDraws(player.getDraws() + 1)
                player.setStatus("Active")
            for player in blue_team:
                player.setDraws(player.getDraws() + 1)
                player.setStatus("Active")
        else:
            await bot.say("Result must be Red, Blue, or Draw")
            return #Early because I want Joe to see this
        await bot.say("Scrim concluded.")
        active_scrim.setName(str(time.time()))
        scrims.remove(active_scrim)
        helper.saveScrim(active_scrim)
    else:
        await bot.say("Scrim not found.  Are you sure you got the right name?")
    

@bot.command(description="Show the teams for the active scrim")
async def showteams(scrim_name="Active"):
    s = helper.getScrim(scrim_name, scrims)
    if s is not None:
        message_list = []
        red_team, blue_team = s.getTeams()
        message_list.append(balancer.printTeam("Red Team", red_team, "Draft"))
        message_list.append(balancer.printTeam("Blue Team", blue_team, "Draft"))
        for message in message_list:
            s_message = helper.serializeMessage(message)
            await bot.say(s_message)
    else:
        await bot.say("Scrim not found.  Are you sure you got the right name?")

@bot.command(description='Draft a player to the given team')
async def draft(p_num: int, team: str, scrim_name="Active"):
    s = helper.getScrim(scrim_name, scrims)
    active_players_list = helper.getAllActive(known_players)
    active_players_list.sort(key=lambda x: x.getSR())
    p = active_players_list[p_num-1]
    if p is not None and s is not None:
        s.addPlayer(p, team)
        p.setStatus("Drafted")
        if len(active_players_list) == 1:
            p.setFatkids(p.getFatkids() + 1)
            message = p.getName() + " is fat!"
        else:
            message = "Added " + p.getName() + " to " + team + " team."
    else:
        message = "Player or Scrim Unknown"
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
        status, red_team, blue_team = balancer.partition(active_players, weight) # TODO: convert to multi-team (>2) partition function
        await bot.say(status)
        sc.setTeams(red_team, blue_team)
        message_list.append(balancer.printTeam("Red Team", red_team, weight))
        message_list.append(balancer.printTeam("Blue Team", blue_team, weight))
        scrims.append(sc)
    for message in message_list:
        s_message = helper.serializeMessage(message)
        await bot.say(s_message)


@bot.command(description='Create a tournament')
async def tourney(*args):
    if len(args) == 0:
        await bot.say("Please provide one or more weights to balance")
        return
    active_players = []
    for p in known_players:
        if p.getStatus() == "Active":
            active_players.append(p)
    message_list = []
    for weight in args:
        status, teams = balancer.partitionMultipleTeams(active_players, weight)
        await bot.say(status)
        for t in teams:
            team_name = "Team " + str(teams.index(t) + 1)
            message_list.append(balancer.printTeam(team_name, t, weight))
    for message in message_list:
        s_message = helper.serializeMessage(message)
        await bot.say(s_message)


bot.run('MzIyMTY4MDA3NzY3ODgzNzc2.DBow4w.87CYjhnWdIPhBg7LUCrqc3eWdek')

