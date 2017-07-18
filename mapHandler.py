import random

class MapHandler:
    ASSAULT = ["Hanamura", "Horizon Lunar Colony", "Temple of Anubis", "Volskaya Industries"]
    ESCORT = ["Dorado", "Route 66", "Watchpoint: Gibraltar"]
    HYBRID = ["Eichenwalde", "Hollywood", "King's Row", "Numbani"]
    CONTROL = ["Ilios", "Lijang Tower", "Nepal", "Oasis"]

    MODES = [ASSAULT, ESCORT, HYBRID, CONTROL]

    def __init__(self):
        return

    def getMap(self, no2CP=False):
        mapType = self.MODES[random.randint(0, len(self.MODES) - 1)] # Get mode to be played
        map = mapType[random.randint(0, len(mapType) - 1)] # Get map

        return map