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
        screen = pyscreenshot.grab()

        pytesseract.tesseract_cmd = 'C:/Program Files (x86)/Tesseract-OCR/tesseract'
        tessdata_dir_config = '--tessdata-dir "C:\\Program Files (x86)\\Tesseract-OCR\\tessdata"'

        text = pytesseract.image_to_string(screen, config=tessdata_dir_config)

        print(text)


if __name__=="__main__":
    m = Mover()

    time.sleep(5)
    # print(cursorPos())

    m.move_player(0, 0)