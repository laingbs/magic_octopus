import constants as cst

class Table:

    def __init__(self,teams):
        self.teams = teams
        self.teams.sort(key=lambda x : (x.points, x.gd, x.points),
                reverse=True)


    def add_fixture(self, fixture):
        if fixture.hg > fixture.ag:
            hpoints = 3
            apoints = 0
        elif fixture.ag > fixture.hg:
            hpoints = 0
            apoints = 3
        else:
            hpoints = 1
            apoints = 1
        for i in range(0,20):
            if self.teams[i].name == fixture.hteam:
                self.teams[i].points += hpoints
                self.teams[i].scored += fixture.hg
                self.teams[i].conceeded += fixture.ag
                self.teams[i].gd = self.teams[i].scored - self.teams[i].conceeded
                self.teams[i].played += 1
            if self.teams[i].name == fixture.ateam:
                self.teams[i].points += apoints
                self.teams[i].scored += fixture.ag
                self.teams[i].conceeded += fixture.hg
                self.teams[i].gd = self.teams[i].scored - self.teams[i].conceeded
                self.teams[i].played += 1
                self.teams[i].played += 1
        self.teams.sort(key=lambda x : (x.points, x.gd, x.points),
                reverse=True)

    def print(self):
        table_string = "||Team                   ||Points|| GD  ||\n"
        for team in self.teams:
            table_string += ("|| {0:20}  || {1:3}  ||{2:3}  ||\n"
                .format(team.name, team.points, team.gd))
        print(table_string)
