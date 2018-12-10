import wget
import os
import csv
import random
import numpy as np
from copy import deepcopy

from season import Season
import constants as cst

DATAFILE = 'current_data.csv'

HOME_TEAM = 'HomeTeam'
AWAY_TEAM = 'AwayTeam'
HG = 'FTHG'
AG = 'FTAG'
TAGS = [HOME_TEAM, AWAY_TEAM, HG, AG]

def download_file(url):
    if os.path.exists(DATAFILE):
        print('Removing ' + DATAFILE)
        os.remove(DATAFILE)
    #print('Beginning file download')
    print(url)
    wget.download(url, DATAFILE)
    print('')

def load_data():
    #print('Load data from CSV file')
    f = open(DATAFILE, 'rt', encoding="latin-1")
    reader = csv.reader(f)

    #print('Get headers from CSV file')
    headers = next(reader, None)
    try:
        for tag in cst.TAGS:
            if tag not in headers:
                value_index = headers.index(tag)
    except:
        print(tag + ' not found :(')

    column = {}
    for h in headers:
        column[h] = []
    for row in reader:
        for h, v in zip(headers, row):
            column[h].append(v)
    return column


###############################################################################
# Loading in Season Data
###############################################################################
# Index for table - sorts from 0 - 5
TAB_POINTS = 0
TAB_GD = 1
TAB_FOR = 2
TAB_AGAINST = 3
TAB_PLAYED = 4
TAB_TEAM = 5
WEEKS_PER_SEASON = 38
MATCHES_PER_WEEK = 10

def create_starting_table(team_names):
    table = []
    for team in team_names:
        table.append([0,0,0,0,0,team])
    return sorted(table, reverse = True)

def get_new_table(old_table, week):
    new_table = deepcopy(old_table)
    for fixture in week:
        home_index = get_team_index_from_table(new_table, fixture[0])
        away_index = get_team_index_from_table(new_table, fixture[1])

        if fixture[2] > fixture[3]:
            hpoints = 3
            apoints = 0
        elif fixture[3] > fixture[2]:
            hpoints = 0
            apoints = 3
        else:
            hpoints = 1
            apoints = 1

        new_table[home_index][TAB_POINTS] += hpoints
        new_table[home_index][TAB_GD] += fixture[2] - fixture[3]
        new_table[home_index][TAB_FOR] += fixture[2]
        new_table[home_index][TAB_AGAINST] += fixture[3]
        new_table[home_index][TAB_PLAYED] += 1

        new_table[away_index][TAB_POINTS] += apoints
        new_table[away_index][TAB_GD] += fixture[3] - fixture[2]
        new_table[away_index][TAB_FOR] += fixture[3]
        new_table[away_index][TAB_AGAINST] += fixture[2]
        new_table[away_index][TAB_PLAYED] += 1

    return sorted(new_table, reverse = True)

def print_table(table):
    table_string = "||Team                   ||Points|| GD  ||Played||\n"
    for team in table:
        table_string += ("|| {0:20}  || {1:3}  ||{2:3}  ||{3:3}   ||\n"
                .format(
                    team[TAB_TEAM],
                    team[TAB_POINTS],
                    team[TAB_GD],
                    team[TAB_PLAYED]))
    print(table_string)

def get_team_index_from_table(table, team):
    index = 0
    while table[index][TAB_TEAM] != team:
        index += 1
        if index > len(table):
            print("Aaa can't find {0} in {1}".format(team, table))
    return index

def get_league_tables(weeks, team_names):
    # Create initial empty table for week 0
    tables = [create_starting_table(team_names)]
    for week in weeks:
        tables.append(get_new_table(tables[-1],week))
    return tables

def get_weeks_array(data):
    weeks = []
    starting_fixture_index = 0
    for week in range(WEEKS_PER_SEASON):
        weeks.append(get_fixtures_for_week(starting_fixture_index, data))
        starting_fixture_index += MATCHES_PER_WEEK
    return weeks

FIXTURE_HOME = 0
FIXTURE_AWAY = 1
FIXTURE_HG = 2
FIXTURE_AG = 3

def get_fixtures_for_week(start_index, data):
    fixtures = []
    for i in range(start_index, start_index+10):
        fixtures.append([
            data[HOME_TEAM][i],
            data[AWAY_TEAM][i],
            int(data[HG][i]),
            int(data[AG][i])])
    return fixtures


def get_team_result(team, match_index, week_index, weeks):
    form = []
    number_found = 0
    m = match_index
    w = week_index
    while number_found < WEEKS_INCLUDED_IN_FORM:
        m = (m-1) % MATCHES_PER_WEEK
        if m == MATCHES_PER_WEEK -1:
            w = w - 1
        fixture = weeks[w][m]
        if fixture[FIXTURE_HOME] == team:
            form.append([fixture[FIXTURE_HG], fixture[FIXTURE_AG], 1])
            number_found += 1
        if fixture[FIXTURE_AWAY] == team:
            form.append([fixture[FIXTURE_AG], fixture[FIXTURE_HG], 0])
            number_found += 1
    return form


###############################################################################
# Do stuff
###############################################################################

TEAM_NAMES = 0
WEEKS = 1
LEAGUE_TABLES = 2
LAST_TABLE = 3
SEASON = 4

def create_season(year, last_table):
    # Download dat for a season
    url = 'http://www.football-data.co.uk/mmz4281/{0}/E0.csv'.format(year)
    download_file(url)
    raw_data = load_data()

    # Make a list of team names and create a starting table
    list_of_team_names = list(set(raw_data[cst.HOME_TEAM]))

    # Create an array of weeks that contain 10 arrays of fixtures
    weeks = get_weeks_array(raw_data)

    # Create a league table for each week
    league_tables = get_league_tables(weeks, list_of_team_names)

    return [list_of_team_names, weeks, league_tables, last_table, year]

def get_seasons(start_year, end_year):
    seasons = []

    # Load first sacrifical year to get the form
    year_string = ('{0:02}{1:02}'.format(start_year % 100, (start_year + 1) % 100))
    sacrificial_year = create_season(year_string, {})
    prev_table = sacrificial_year[LAST_TABLE]

    for year in range(start_year, end_year + 1):
#        if year == 2004:
#            pass
        year_string = ('{0:02}{1:02}'.format(year % 100, (year + 1) % 100))
        #print('Getting season {0} (year string {1}'.format(year_string, year))
        seasons.append(create_season(year_string, prev_table))
        prev_table = seasons[-1][LAST_TABLE]
    seasons = seasons[1:]
    return seasons

def make_dict_from_table(table):
    prev_position = {}
    for i in range(0, len(table)):
        prev_position[table[i][TAB_TEAM]] = i
    return prev_position

def get_prev_post(team, season):
    if team in season[LAST_TABLE]:
        return int(season[LAST_TABLE][team])
    # If not found then probably promoted.
    else:
        return 20


###############################################################################
# Getting form and results
##############################################################################
WEEKS_INCLUDED_IN_FORM = 3

def get_form_and_results(season):
    form_collection = []
    results = []
    for week_index in range(WEEKS_INCLUDED_IN_FORM, WEEKS_PER_SEASON):
        for match_index in range(0, MATCHES_PER_WEEK):
            match = season[WEEKS][week_index][match_index]
            result =  [match[FIXTURE_HG], match[FIXTURE_AG]]
            results.append(result)
            # Add some form
            form = np.array([match[FIXTURE_HOME], match[FIXTURE_AWAY]])
            form = np.append(form,
                    get_prev_post(match[FIXTURE_HOME], season))
            form = np.append(form,
                    get_prev_post(match[FIXTURE_AWAY], season))
            form = np.append(form, get_team_result(
                match[FIXTURE_HOME],
                match_index,
                week_index,
                season[WEEKS]))
            form = np.append(form, get_team_result(
                match[FIXTURE_AWAY],
                match_index,
                week_index,
                season[WEEKS]))
            form = np.append(form, season[LEAGUE_TABLES])
            form.flatten()
            form_collection.append(form)
            #print('----')
            #print(form)
            #print(result)

    return form_collection, results


if __name__ == '__main__':
    #loaded_data = get_seasons(1994, 2016)
    #s1516 = loaded_data[1]
    #print('----------------')
    #print('Example week {0}'.format(s1516[WEEKS][23]))
    #print('Example week {0}'.format(s1516[WEEKS][0]))
    #print('----------------')
    #print_table(s1516[LEAGUE_TABLES][10])
    #print('Example week {0}'.format(s1516[WEEKS][10]))
    #print_table(s1516[LEAGUE_TABLES][11])
    #example_form, example_results = get_form_and_results(s1516)
    #print(example_form[12])
    #print(example_results[12])
    #print(example_form[13])
    #print('-------------')
    print('Create training data')
    training_data = get_seasons(1993,2015)
    training_data_form = []
    training_data_results = []
    for i in range(0, 14):
        print('Getting form/results from {0}'.format(training_data[i][SEASON]))
        a, b = get_form_and_results(training_data[i] )
        training_data_form.append(a)
        training_data_results.append(b)

    print('Create testing data')
    testing_data = get_seasons(2015, 2017)
    testing_data_form = []
    testing_data_results = []
    for i in range(0, 2):
        print('Getting form/results from {0}'.format(testing_data[i][SEASON]))
        a, b = get_form_and_results(testing_data[i] )
        testing_data_form.append(a)
        testing_data_results.append(b)
    print('Start the machine learning')
    print('Length of input data: {0}'.format(len(testing_data_form[0])))
    print('Length of output data: {0}'.format(len(testing_data_results[0])))
