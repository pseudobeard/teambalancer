from keygen import *
from PIL import Image
from pytesseract import *
import pyscreenshot
from difflib import SequenceMatcher
import time

class Mover:
    TOP_LEFT = (330, 481)

    TEAM_SPACE = 680
    PLAYER_SPACE = 60

    def __init__(self):
        return

    def move_player(self, team, index):
        rightClick(self.TOP_LEFT[0] + team * self.TEAM_SPACE, self.TOP_LEFT[1] + index * self.PLAYER_SPACE)  # Right click player
        pos = cursorPos()

        time.sleep(0.5)
        clickDelay(pos[0] + 50, pos[1] + 20, 0.5)

        time.sleep(3)

    def move_teams(self, team1players, team2players):
        teamPositions = self.get_teams(team1players + team2players)
        team1pos, team2pos = teamPositions[0], teamPositions[1]

        for player in team1players:
            try:
                playerIndex = team2pos.index(player) # In wrong team, must be moved
                playerTeam = 1
                print("Moving player " + player + " from team " + str(playerTeam) + " index " + str(playerIndex))
                self.move_player(playerTeam, playerIndex)
            except ValueError:
                print(player + " not found in team 2, not moving")
            time.sleep(1)

        for player in team2players:
            try:
                playerIndex = team1pos.index(player) # In wrong team, must be moved
                playerTeam = 0
                print("Moving player " + player + " from team " + str(playerTeam) + " index " + str(playerIndex))
                self.move_player(playerTeam, playerIndex)
            except ValueError:
                print(player + " not found in team 1, not moving")
            time.sleep(1)

    def get_teams(self, playerlist):
        pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'

        team1 = pyscreenshot.grab(bbox=(50,450,530,810)) # X1, Y1, X2, Y2
        team1.save("team1screenshot.png")
        team1text = pytesseract.image_to_string(team1, config=tessdata_dir_config, lang='owf')

        team2 = pyscreenshot.grab(bbox=(800,450,1280,810)) # X1, Y1, X2, Y2
        team2.save("team2screenshot.png")
        team2text = pytesseract.image_to_string(team2, config=tessdata_dir_config, lang='owf')

        team1list = team1text.splitlines() # Split teams into players by line
        team2list = team2text.splitlines()

        team1list = list(filter(None, team1list)) # Remove empty strings from list
        team2list = list(filter(None, team2list))

        team1list = self.findPlayers(team1list, playerlist) # Match to closest known player
        team2list = self.findPlayers(team2list, playerlist)

        return (team1list, team2list)

    def findPlayers(self, teamList, playerlist):
        for index, raw_name in enumerate(teamList):
            highest_similarity = -1
            closest_match = ""
            for name in playerlist:
                similarity = self.similar(raw_name.upper(), name)
                if highest_similarity == -1 or similarity >= highest_similarity:
                    highest_similarity = similarity
                    closest_match = name

            teamList[index] = closest_match
        return teamList

    def similar(self, s1, s2):
        return SequenceMatcher(None, s1, s2).ratio()


if __name__=="__main__":
    m = Mover()

    for i in range (10, 0, -1):
        print(i)
        time.sleep(1)
    # print(cursorPos())

    # m.move_player(1, 2)

    team1players = ["TheMightyMat", "Easy McCree"]
    team2players = ["Easy Ana", "Easy Lucio"]

    m.move_teams(team1players, team2players)