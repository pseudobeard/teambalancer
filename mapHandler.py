import random

class MapHandler:
    ASSAULT = ["Hanamura", "Horizon", "Anubis", "Volskaya"]
    ESCORT = ["Dorado", "Route66", "Gibraltar", "Junkertown"]
    HYBRID = ["Eichenwalde", "Hollywood", "Kings-Row", "Numbani", "Blizz-World"]
    CONTROL = ["Ilios", "Lijang", "Nepal", "Oasis"]

    def __init__(self):
        return

    def getMap(self, no2CP=False):
        if (no2CP):
            modes = [self.ESCORT, self.HYBRID, self.CONTROL]
        else:
            modes = [self.ASSAULT, self.ESCORT, self.HYBRID, self.CONTROL]

        mapType = modes[random.randint(0, len(modes) - 1)] # Get mode to be played
        map = mapType[random.randint(0, len(mapType) - 1)] # Get map

        return map