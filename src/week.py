import constants as cst
from table import Table
from fixture import Fixture

class Week:
    def __init__(self, fixture_data, start_index, teams):
       fixture_index = start_index
       self.table = Table(teams)
       self.fixtures = []
       self.number = int(start_index / 10.0)
       for i in range(start_index, start_index+10):
           current_fixture = Fixture()
           current_fixture.hteam = fixture_data[cst.HOME_TEAM][i]
           current_fixture.ateam = fixture_data[cst.AWAY_TEAM][i]
           current_fixture.hg = int(fixture_data[cst.HG][i])
           current_fixture.ag = int(fixture_data[cst.AG][i])

           self.fixtures.append(current_fixture)
           self.table.add_fixture(current_fixture)

       if len(self.fixtures) != 10:
           print('Error - should be 10 fixtures, there are {0}'
               .format(len(self.fixtures)))
           return

    def print(self):
        print('Week number {0}'.format(self.number))

