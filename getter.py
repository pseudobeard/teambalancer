import json
import requests

jwtToken = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJfaWQiOiI1OTNiOTEzNjQ5YzVlYTczMzA1ZDkzYWYiLCJ1c2VybmFtZSI6ImthcmtldyIsInRva2VuIjoiR2ZmMExGT21xYjJqeXBsd3lBMFMiLCJpYXQiOjE0OTc4NjE3NTQsImlzcyI6IlN0cmVhbUVsZW1lbnRzIn0.fzv9g4zsGVW2DbI0YKh5mQj4jT_s8EVoofhKhfRN04k"
id = "593b913649c5ea73305d93af" # Find these on https://streamelements.com/dashboard/account/information

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
        for redemption in json: # Iterate throgh redemptions
            item = redemption.get("item") # Get item
            if item is not None:
                itemName = item.get("name")
                if itemName == "Viewer Game Sunday Ticket": # If it is a viewer ticket, add the battletag to the list
                    inputs = redemption.get("input")
                    battletags.append(inputs[0])

        return battletags

if __name__=="__main__":
    g = Getter()
    battletags = g.getViewerGameParticipants()
    for battletag in battletags:
        print(battletag)