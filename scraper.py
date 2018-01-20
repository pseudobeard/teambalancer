import requests
from pprint import pprint

class Scraper:
    def __init__(self):
        self.url_base = "http://localhost:4444/api/v3/u/"
#        self.url_base = "https://owapi.net/api/v3/u/"
        self.headers = {'user-agent': 'teambalancer/0.2'}
        self.url_end = "/blob"
        self.heal_list = ['ana', 'mercy', 'zenyatta', 'lucio', 'moira']
        self.dps_list = ['bastion', 'genji', 'hanzo', 'junkrat', 'mccree', 'pharah', 'reaper', 'soldier76', 'sombra', 'tracer', 'widowmaker', 'doomfist', 'torbjorn', 'symmetra']
        self.maintank_list = ['reinhardt', 'winston', 'orisa']
        self.offtank_list = ['dva', 'roadhog', 'zarya', 'mei']
        self.playtime = {'HEALER': 0, 'DPS': 0, 'MAINTANK': 0, 'OFFTANK': 0}

    def scrape(self, player):
        player_name = player.bnetID
        if player_name is None:
            message = "No battlenetID found"
            return(message)
        url = self.url_base + player_name.replace("#","-") + self.url_end
        try:
            r = requests.get(url, headers=self.headers)
            data = r.json()
        except Exception:
            message = "Failure to get data for %s" % player.info['name']
            return(message)
        try:
            player.info['sr'] = data['us']['stats']['competitive']['overall_stats']['comprank']
        except Exception:
            message = "Failed to determine rating for player %s" % player.info['name']
            player.info['sr'] = 2500
            return(message)
        try:
            comp_playtime = data['us']['heroes']['playtime']['competitive']
            player.info['role'] = self.determineRoles(comp_playtime)
        except Exception:
            message = "Failed to determine roles for player %s" % player.info['name']
            return(message)
        try:
            player.info['heroes'] = self.determineHeroes(comp_playtime)
        except Exception:
            message = "Failed to determine top 3 heroes for player %s" % player.info['name']
            return(message)
        message = "Sr and roles updated for player %s" % player.info['name']
        return(message)
            
    def determineRoles(self, comp_playtime):
        heal_time = 0
        dps_time = 0
        maintank_time = 0
        offtank_time = 0
        for hero in self.heal_list:
            heal_time = heal_time + comp_playtime[hero]
        for hero in self.dps_list:
            dps_time = dps_time + comp_playtime[hero]
        for hero in self.maintank_list:
            maintank_time = maintank_time + comp_playtime[hero]
        for hero in self.offtank_list:
            offtank_time = offtank_time + comp_playtime[hero]
        self.playtime['HEALER'] = heal_time
        self.playtime['DPS'] = dps_time
        self.playtime['MAINTANK'] = maintank_time
        self.playtime['OFFTANK'] = offtank_time
        sortedList = sorted(self.playtime, key=self.playtime.get, reverse=True)
        return(str(sortedList[0]))

    def determineHeroes(self, heroes):
        # Only consider heroes with non-0 playime
        message = ""
        heroes = {key:val for key, val in heroes.items() if val > 0}
        sortedHeroes = sorted(heroes, key=heroes.get, reverse=True)
        top3 = sortedHeroes[:3]
        pprint(top3)
        for hero in top3:
            message = message + hero + ","
        if len(message) > 0:
            message = message[:-1] # Get rid of trailing comma
        return(message)

