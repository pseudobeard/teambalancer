from keygen import *
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
        time.sleep(0.3)
        click(self.VIA_BATTLETAG_BUTTON[0], self.VIA_BATTLETAG_BUTTON[1]) # Click on "Via Battletag"
        time.sleep(0.3)

        for character in battletag:
            if(character.isupper()): # Press shift when letter is uppercase
                pressKey(0x10)

            if(not (getKeyCode(character) is None)):
                typeKey(getKeyCode(character)) # Type each letter of the battletag

            releaseKey(0x10) # Release shift

            time.sleep(0.01)

        time.sleep(0.1)

        click(self.INVITE_BUTTON[0], self.INVITE_BUTTON[1]) # Click on the "Invite" button

        click(self.BACK_BUTTON[0], self.BACK_BUTTON[1]) # Click "Back" button (in case battletag did not work)

        time.sleep(0.3)

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