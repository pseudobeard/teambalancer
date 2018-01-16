import requests
from pprint import pprint

class Scraper:
    def __init__(self):
#        self.url_base = "http://localhost:4444/api/v3/u/"
        self.url_base = "https://owapi.net/api/v3/u/"
        self.headers = {'user-agent': 'teambalancer/0.2'}
        self.url_end = "/blob"
        self.heal_list = ['ana', 'mercy', 'zenyatta', 'lucio', 'moira']
        self.dps_list = ['bastion', 'genji', 'hanzo', 'junkrat', 'mccree', 'pharah', 'reaper', 'soldier76', 'sombra', 'tracer', 'widowmaker', 'doomfist']
        self.maintank_list = ['reinhardt', 'winston', 'orisa']
        self.offtank_list = ['dva', 'roadhog', 'zarya']
        self.weird_list = ['mei', 'symmetra', 'torbjorn']
        self.playtime = {'Healer': 0, 'DPS': 0, 'Tank': 0, 'Weird': 0}

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
        message = "Sr and roles updated for player %s" % player.info['name']
        return(message)
            
    def determineRoles(self, comp_playtime):
        heal_time = 0
        dps_time = 0
        tank_time = 0
        weird_time = 0
        for hero in self.heal_list:
            heal_time = heal_time + comp_playtime[hero]
        for hero in self.dps_list:
            dps_time = dps_time + comp_playtime[hero]
        for hero in self.maintank_list:
            maintank_time = maintank_time + comp_playtime[hero]
        for hero in self.offtank_list:
            offtank_time = offtank_time + comp_playtime[hero]
        for hero in self.weird_list:
            weird_time = weird_time + comp_playtime[hero]
        self.playtime['Healer'] = heal_time
        self.playtime['DPS'] = dps_time
        self.playtime['MainTank'] = maintank_time
        self.playtime['OffTank'] = offtank_time
        self.playtime['Weird'] = weird_time
        pprint(self.playtime)
        sortedList = sorted(self.playtime, key=self.playtime.get, reverse=True)
        return (str(sortedList[0]) + '/' + str(sortedList[1]))
