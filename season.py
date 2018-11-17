import urllib2
#response = urllib2.urlopen('http://www.example.com/')
#html = response.read()

START_DATA_URL = "http://www.football-data.co.uk/mmz4281/"
END_DATA_URL = "/EC.csv"

class Season:
    def __init__(self, season):
        data_url = START_DATA_URL + season + END_DATA_URL
        response = urllib2.urlopen(data_url)
        csv = response.read()
        print(csv)
        #print(data_url)


if __name__ == "__main__":
    main()
