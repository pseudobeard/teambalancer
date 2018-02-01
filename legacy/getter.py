import json
import requests

with open('properties.json') as data_file:
    data = json.load(data_file)

jwtToken = data["jwtToken"]
id = data["id"]
ITEM_NAME = data["item_name"]

headers = {"authorization" : "Bearer " + jwtToken}

baseurl = "https://api.streamelements.com/kappa/v1/store/"
end = "/redemptions?limit=100&pending=true"


class Getter:
    def __init__(self):
        return

    def getJSON(self):
        res = requests.get(baseurl + id + end, headers=headers)
        data = json.loads(res.text)
        return data

    def getViewerGameParticipants(self):
        battletags = []

        json = self.getJSON()
        redemptions = json.get("docs")
        for redemption in redemptions: # Iterate throgh redemptions
            item = redemption.get("item") # Get item
            if item is not None:
                itemName = item.get("name")
                if itemName == ITEM_NAME: # If it is a viewer ticket, add the battletag to the list
                    inputs = redemption.get("input")
                    battletags.append(inputs[0])

        return battletags

if __name__=="__main__":
    g = Getter()
    battletags = g.getViewerGameParticipants()
    for battletag in battletags:
        print(battletag)