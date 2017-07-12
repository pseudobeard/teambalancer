# This program should simulate a keystroke.
import ctypes
import time

MOUSE_LEFTDOWN = 0x0002     # left button down
MOUSE_LEFTUP = 0x0004       # left button up
MOUSE_RIGHTDOWN = 0x0008    # right button down
MOUSE_RIGHTUP = 0x0010      # right button up
MOUSE_MIDDLEDOWN = 0x0020   # middle button down
MOUSE_MIDDLEUP = 0x0040     # middle button up

SendInput = ctypes.windll.user32.SendInput

# C struct redefinitions
PUL = ctypes.POINTER(ctypes.c_ulong)

class KeyBdInput(ctypes.Structure):
    _fields_ = [("wVk", ctypes.c_ushort),
                ("wScan", ctypes.c_ushort),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class HardwareInput(ctypes.Structure):
    _fields_ = [("uMsg", ctypes.c_ulong),
                ("wParamL", ctypes.c_short),
                ("wParamH", ctypes.c_ushort)]


class MouseInput(ctypes.Structure):
    _fields_ = [("dx", ctypes.c_long),
                ("dy", ctypes.c_long),
                ("mouseData", ctypes.c_ulong),
                ("dwFlags", ctypes.c_ulong),
                ("time", ctypes.c_ulong),
                ("dwExtraInfo", PUL)]


class Input_I(ctypes.Union):
    _fields_ = [("ki", KeyBdInput),
                ("mi", MouseInput),
                ("hi", HardwareInput)]


class Input(ctypes.Structure):
    _fields_ = [("type", ctypes.c_ulong),
                ("ii", Input_I)]


class POINT(ctypes.Structure):
    _fields_ = [("x", ctypes.c_ulong), ("y", ctypes.c_ulong)]

# Actual Functions

def getKeyCode(character): # See https://msdn.microsoft.com/en-us/library/windows/desktop/dd375731(v=vs.85).aspx
    if (character.isalpha()):
        return ord(character.upper())
    elif (character.isdigit()):
        return ord(character)
    elif (character == "#"):
        return 0xDE
    else:
        return ord(0) # Return a 0 character if invalid character is provided


def pressKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0x48, 0, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))


def releaseKey(hexKeyCode):
    extra = ctypes.c_ulong(0)
    ii_ = Input_I()
    ii_.ki = KeyBdInput(hexKeyCode, 0x48, 0x0002, 0, ctypes.pointer(extra))
    x = Input(ctypes.c_ulong(1), ii_)
    SendInput(1, ctypes.pointer(x), ctypes.sizeof(x))

def typeKey(hexKeyCode):
    pressKey(hexKeyCode)
    time.sleep(0.01)
    releaseKey(hexKeyCode)

def moveMouse(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)

def cursorPos():
    point = POINT()
    ctypes.windll.user32.GetCursorPos(ctypes.pointer(point))
    return (point.x, point.y)

def click(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)
    ctypes.windll.user32.mouse_event(MOUSE_LEFTDOWN, x, y, 0, 0)
    ctypes.windll.user32.mouse_event(MOUSE_LEFTUP, x, y, 0, 0)

def rightClick(x, y):
    ctypes.windll.user32.SetCursorPos(x, y)
    ctypes.windll.user32.mouse_event(MOUSE_RIGHTDOWN, x, y, 0, 0)
    ctypes.windll.user32.mouse_event(MOUSE_RIGHTUP, x, y, 0, 0)


if __name__ == "__main__":
    print("keygen library 1.0")


