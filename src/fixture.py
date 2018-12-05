import constants as cst

class Fixture:
    def __init__(self):
        self.hteam = ""
        self.ateam = ""
        self.hg = 0
        self.ag = 0

    def print(self):
        print('{0} vs {1}: {2}-{3}'.format(
            self.hteam,
            self.ateam,
            self.hg,
            self.ag))
