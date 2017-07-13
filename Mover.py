from keygen import *
from PIL import Image
from pytesseract import *
import pyscreenshot
import time

class Mover:
    TOP_LEFT = (330, 481)

    TEAM_SPACE = 680
    PLAYER_SPACE = 60

    def __init__(self):
        return

    def move_player(self, team, index):
        # rightClick(self.TOP_LEFT[0] + team * self.TEAM_SPACE, self.TOP_LEFT[1] + index * self.PLAYER_SPACE)  # Right click player
        # pos = cursorPos()
        #
        # time.sleep(0.5)
        # clickDelay(pos[0] + 50, pos[1] + 20, 0.5)
        #
        # time.sleep(3)

        pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'

        team1 = pyscreenshot.grab(bbox=(50,450,530,810)) # X1, Y1, X2, Y2
        team1.save("team1screenshot.png")
        team1text = pytesseract.image_to_string(team1, config=tessdata_dir_config, lang='owf')

        team2 = pyscreenshot.grab(bbox=(800,450,1280,810)) # X1, Y1, X2, Y2
        team2.save("team2screenshot.png")
        team2text = pytesseract.image_to_string(team2, config=tessdata_dir_config, lang='owf')

        print(team1text)
        print("------------------")
        print(team2text)


if __name__=="__main__":
    m = Mover()

    time.sleep(5)
    # print(cursorPos())

    m.move_player(0, 0)