### Magic_Octopus Design ###

## Description of program ##

This program will use machine learning to predict the results to English Premier
League fixtures.

Historic Premier League data can be download in CSV format from
http://www.football-data.co.uk/englandm.php. The training data will be the
seasons 95/6 to 16/7, with 17/8 being used for the verfication data. Seasons
93/4 - 94/5 are omitted as there were 22 teams in the league during that year.

The CSV file contains the full time result of each game in a seasons. For later
seasons, more stats such as half-time results are available - I propose to
ignore these.

Inputs to the neural network will be:

* The two teams playing, ordered home and then away
* The position that each team finished in during the previous season, with teams
  that were promoted all marked as 18th.
* The premier league table at the time that they play, including
  - Points of each team
  - Won/Drawn of each team (assume lost can be infered)
  - Goals for/against
* The score om each team's last three games  - note that this
* The teams current posistion (though this may be infered)

The outputs will be:
* A 0 ,1 or 2 for home win, away win or draw

Additional optional outputs will be
* Home team score
* Away team score

The program will use tensor flow for the nueral network.

## Classes of the program ##

* Fixture
* League table
* Form - contains the teams last three games
- Result - contains th

## Potential future enhancements ##

## High Level Design ##



