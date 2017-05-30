class Player:
    # Default role to flex, and sr to 2300
    def __init__(self, id):
        self.id = id
        self.sr = 2300
        self.role = "Flex"
        self.name = id.split('#')[0]

    def getName(self):
        return self.name

    def getID(self):
        return self.id

    def setSR(self, sr):
        self.sr = sr

    def getWeightedSR(self):
        return float(self.sr) * self.getWeight()

    def getSR(self):
        return self.sr

    def getRole(self):
        return self.role

    def setRole(self, role):
        self.role = role

    def getWeight(self):
        weight = 0.2
        if self.sr >= 1000:
            weight = 0.4
        if self.sr >= 1500:
            weight = 0.6
        if self.sr >= 2000:
            weight = 1
        if self.sr >= 3000:
            weight = 1.2
        if self.sr >= 3500:
            weight = 1.4
        if self.sr >= 4000:
            weight = 1.6
        return weight
