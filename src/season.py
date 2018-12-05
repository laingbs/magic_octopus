import constants as cst
from week import Week
from team import Team

class Season:
    def __init__(self, raw_data):

        print("Load the teams")
        self.teams = []
        for team_name in set(raw_data[cst.HOME_TEAM]):
            self.teams.append(Team(team_name))

        if (len(self.teams) != 20):
            print('Error: there are {0} teams, should be 20'.format(len(self.teams)))
            return
        else:
            print('{0} teams successfully created'
                    .format(len(self.teams)))

        print("Create the weeks")
        self.weeks = []
        starting_fixture_index = 0
        for i in range(0,38):
            self.weeks.append(
                Week(raw_data,
                     starting_fixture_index,
                     self.teams))
            starting_fixture_index += 10
        print("Fixtures all used?: " + str(starting_fixture_index ==
            len(raw_data[cst.HOME_TEAM])))



