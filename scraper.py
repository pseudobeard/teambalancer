import requests
from pprint import pprint

class Scraper:
    def __init__(self):
        self.url_base = "https://owapi.net/api/v3/u/"
        self.headers = {'user-agent': 'teambalancer/0.1'}
        self.url_end = "/blob"

    def scrape(self, player):
        url = self.url_base + player.getID().replace("#","-") + self.url_end
        try:
            r = requests.get(url, headers=self.headers)
            data = r.json()
            player.setSR(data['us']['stats']['competitive']['overall_stats']['comprank'])
            pprint(data['us']['heroes']['playtime']['competitive'])
        except Exception:
            print("-->Rating not found for %s, using %d" % (player.name, player.sr))
