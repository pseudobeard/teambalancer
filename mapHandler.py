import random

class MapHandler:
    ASSAULT = ["Hanamura", "Horizon Lunar Colony", "Temple of Anubis", "Volskaya Industries"]
    ESCORT = ["Dorado", "Route 66", "Watchpoint: Gibraltar"]
    HYBRID = ["Eichenwalde", "Hollywood", "King's Row", "Numbani"]
    CONTROL = ["Ilios", "Lijang Tower", "Nepal", "Oasis"]

    def __init__(self):
        return

    def getMap(self, no2CP=False):
        if (no2CP):
            modes = [self.ESCORT, self.HYBRID, self.CONTROL]
        else:
            modes = [self.ASSAULT, self.ESCORT, self.HYBRID, self.CONTROL]

        mapType = modes[random.randint(0, len(self.modes) - 1)] # Get mode to be played
        map = mapType[random.randint(0, len(mapType) - 1)] # Get map

        return map