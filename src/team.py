class Team:
    def __init__(self, name):
        self.name = name
        self.points = 0
        self.scored = 0
        self.conceeded = 0
        self.gd = 0
        self.played = 0

    def print(self):
        print('{0}: {1} points, {2} for, {3} against, played {4}'
                .format(
                self.name,
                self.points,
                self.scored,
                self.conceeded,
                self.played))

