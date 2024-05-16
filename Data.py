class PlayerData:

    def __init__(self, x, y, name):
        self.x = x
        self.y = y
        self.sprite_name = "idle_left"
        self.die = False
        self.restart = False
        self.respawn = False
        self.name = name
        self.connected = -1
        self.saws = []
        self.isSawSend = False
        self.isSawReceive = False
        self.lasers = []
        self.isLaserSend = False
        self.isLaserReceive = False

    def setVal(self, x, y, sprite_name, die):
        self.x = x
        self.y = y
        self.sprite_name = sprite_name
        self.die = die


class Game:

    def __init__(self, id):
        self.p1Die = False
        self.p2Die = False
        self.ready = False
        self.id = id
        self.playerData = [None, None]

    def getPlayerData(self, p):
        return self.playerData[p]

    def die(self, player, die):
        self.playerData[player].die = die
        if player == 0:
            self.p1Die = True
        else:
            self.p2Die = True

    def connected(self):
        return self.ready

    def bothDie(self):
        return self.p1Die and self.p2Die

    def resetDie(self):
        self.p1Die = False
        self.p2Die = False

