from keygen import *
from clipboard import *
import time

class Inviter:
    ADD_BUTTON = (1660, 320)
    VIA_BATTLETAG_BUTTON = (1200, 300)
    INVITE_BUTTON = (1000, 870)
    BACK_BUTTON = (865, 865)

    def __init__(self):
        return

    def invite_player(self, battletag):
        click(self.ADD_BUTTON[0], self.ADD_BUTTON[1])  # Click on "Invite Players"
        time.sleep(0.5)
        click(self.VIA_BATTLETAG_BUTTON[0], self.VIA_BATTLETAG_BUTTON[1]) # Click on "Via Battletag"
        time.sleep(0.5)

        copyToClipboard(battletag) # Copy battletag to clipboard

        pressKey(0x11) # CTRL + V
        pressKey(getKeyCode('v'))

        time.sleep(0.05)
        
        releaseKey(0x11)
        releaseKey(getKeyCode('v'))

        time.sleep(0.2)

        click(self.INVITE_BUTTON[0], self.INVITE_BUTTON[1]) # Click on the "Invite" button

        time.sleep(0.1)

        click(self.BACK_BUTTON[0], self.BACK_BUTTON[1]) # Click "Back" button (in case battletag did not work)

        time.sleep(0.4)

    def invite_players(self, player_list):
        for p in player_list:
            self.invite_player(p.getID())



if __name__=="__main__":
    inviter = Inviter()

    # time.sleep(5)
    # print(cursorPos())

    print("Open custom game lobby!")
    for i in range(5, 0, -1):
        print("Starting in", i)
        time.sleep(1)
    inviter.invite_player("TheMightyMat#2228")