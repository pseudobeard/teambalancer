import random

class Player:
    # Default role to flex, and sr to 2300
    def __init__(self, id):
        self.id = id
        self.sr = 2300
        self.role = "Flex"
        self.tier = "Gold"
        self.tierWeight = 10
        self.name = id.split('#')[0]

    def getName(self):
        return self.name

    def getID(self):
        return self.id

    def setSR(self, sr):
        self.sr = sr
        self.updateTier()

    def getTier(self):
        return self.tier

    def getTierWeight(self):
        return self.tierWeight

    def getWeightedSR(self):
        return float(self.sr) * self.getWeight()

    def getSR(self):
        return self.sr

    def getRole(self):
        return self.role

    def setRole(self, role):
        self.role = role

    def getSort(self, weight):
        if weight == "Curve":
            return self.getWeightedSR()
        if weight == "Tier":
            return self.getTierWeight()
        if weight == "Role":
            return self.getSR()
        if weight == "Rand":
            return random.randint(1,5000)
        if weight == "Throw" and self.getSR() > 4000:
            return 3000
        return self.getSR()

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

    def updateTier(self):
        self.tier = "Bronze"
        self.tierWeight = 5
        if self.sr >= 1500:
           self.tier = "Silver"
           self.tierWeight = 8
        if self.sr >= 2000:
           self.tier = "Gold"
           self.tierWeight = 10
        if self.sr >= 2500:
           self.tier = "Platinum"
           self.tierWeight = 11
        if self.sr >= 3000:
           self.tier = "Diamond"
           self.tierWeight = 13
        if self.sr >= 3500:
           self.tier = "Master"
           self.tierWeight = 16
        if self.sr >= 4000:
           self.tier = "GM"
           self.tierWeight = 20
