import requests
from pprint import pprint

class Webapp:
    def __init__(self, url, token):
        self.url = url
        self.headers = {'user-agent': 'teambalancer/0.2', 'content-type': 'application/json'}
        self.headers['Authorization'] = "Token ATastySnack#1553 " + token

    def getTeams(self, blob):
        try:
            r = requests.post(self.url + "/teams", headers=self.headers, data=blob)
            if str(r.status_code) == "201":
                data = r.json()
                return data['team']['url']
            else:
                return "The webapp returned with error code " + r.status_code
        except Exception:
            print("Nope")
            return "The webapp failed to respond"