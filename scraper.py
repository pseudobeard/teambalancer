import requests
from pprint import pprint

class Scraper:
    def __init__(self):
#        self.url_base = "http://localhost:4444/api/v3/u/"
        self.url_base = "http://ec2-52-35-61-178.us-west-2.compute.amazonaws.com/api/v3/u/"
        self.headers = {'user-agent': 'teambalancer/0.1'}
        self.url_end = "/blob"
        self.heal_list = ['ana', 'mercy', 'zenyatta', 'lucio']
        self.dps_list = ['bastion', 'genji', 'hanzo', 'junkrat', 'mccree', 'pharah', 'reaper', 'soldier76', 'sombra', 'tracer', 'widowmaker']
        self.tank_list = ['dva', 'orisa', 'reinhardt', 'winston']
        self.offtank_list = ['roadhog', 'mei', 'zarya', 'symmetra', 'torbjorn']
        self.playtime = {'Healer': 0, 'DPS': 0, 'Main-Tank': 0, 'Off-Tank': 0} 

    def scrape(self, player):
        url = self.url_base + player.getID().replace("#","-") + self.url_end
        try:
            r = requests.get(url, headers=self.headers)
            data = r.json()
        except Exception:
            print("Failure to get data for %s" % player.getID())
            return
        try:
            player.setSR(data['us']['stats']['competitive']['overall_stats']['comprank'])
        except Exception:
            print("Failed to determine rating for player %s" % player.getID())
            player.setSR(1000)
        try:
            comp_playtime = data['us']['heroes']['playtime']['competitive']
            quick_playtime = data['us']['heroes']['playtime']['quickplay']
            player.setRole(self.determineRoles(comp_playtime, quick_playtime))
        except Exception:
            print("Failed to determine roles for player %s" % player.getID())
            
    def determineRoles(self, comp_playtime, quick_playtime):
        heal_time = 0
        dps_time = 0
        tank_time = 0
        offtank_time = 0
        quick_weight = 0.5
        for hero in self.heal_list:
            heal_time = heal_time + comp_playtime[hero] + quick_playtime[hero]
        for hero in self.dps_list:
            dps_time = dps_time + comp_playtime[hero] + quick_playtime[hero]
        for hero in self.tank_list:
            tank_time = tank_time + comp_playtime[hero] + quick_playtime[hero]
        for hero in self.offtank_list:
            offtank_time = offtank_time + comp_playtime[hero] + quick_playtime[hero]
        self.playtime['Healer'] = heal_time
        self.playtime['DPS'] = dps_time
        self.playtime['Main-Tank'] = tank_time
        self.playtime['Off-Tank'] = offtank_time
        pprint(self.playtime)
        sortedList = sorted(self.playtime, key=self.playtime.get, reverse=True)
        return (str(sortedList[0]) + '/' + str(sortedList[1]))
