import wget
import os
import csv
import random

from season import Season
import constants as cst

DATAFILE = 'current_data.csv'

def download_file(url):
    if os.path.exists(DATAFILE):
        print('Removing ' + DATAFILE)
        os.remove(DATAFILE)
    print('Beginning file download')
    wget.download(url, DATAFILE)

def load_data():
    print('Load data from CSV file')
    f = open(DATAFILE, 'rt')
    reader = csv.reader(f)

    print('Get headers from CSV file')
    headers = next(reader, None)
    try:
        for tag in cst.TAGS:
            if tag not in headers:
                value_index = headers.index(tag)
                print(tag + ' found in csv file')
    except:
        print(tag + ' not found :(')

    column = {}
    for h in headers:
        column[h] = []
    for row in reader:
        for h, v in zip(headers, row):
            column[h].append(v)
    return column

if __name__ == '__main__':
    url = 'http://www.football-data.co.uk/mmz4281/1516/E0.csv'
    download_file(url)
    raw_data = load_data()
    season = Season(raw_data)

    print('----------------')
    print('Example team:')
    season.teams[random.randint(0,20)].print()
    print('Example week:')
    season.weeks[random.randint(0,20)].print()
    print('Example fixture:')
    season.weeks[random.randint(0,38)].fixtures[random.randint(0,10)].print()
    print('Example table:')
    season.weeks[random.randint(0,20)].table.print()
