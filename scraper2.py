from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re
import requests
import sqlite3

# read data from an HTML webpage
def read_html(url):
    # read data from the webpage
    response = requests.get(url)

    # create and return a beautifulsoup object
    return BeautifulSoup(response.text, 'html.parser')

# make the box score given soup
def get_box_score(soup, title):
    tables = soup.find_all('table')

    # get the title of the webpage
    title = get_title(soup)

    # get the title and game information of this webpage, to be used later
    info = get_game_info(soup)

    # initialize the box score
    all_player_stats = []

    # iterate through each table
    for table in tables:
        # find all rows
        rows = table.find_all('tr')

        # iterate through each row (player), skipping the header
        for row in rows[1:]:
            # get data from each cell in the row
            cells = row.find_all('td')

            # extract text from each cell and remove whitespace
            player_stats = [cell.get_text() for cell in cells]

            # append player statistics to the list
            all_player_stats.append(player_stats)

    # use the null entry in between teams to separate the two teams in the list
    separator_index = next(i for i, row in enumerate(all_player_stats) if row[0] == 'Totals') + 1

    # split the data into separate teams
    team1_data = all_player_stats[:separator_index]
    team2_data = all_player_stats[separator_index:-1]

    # compile the box score based on whether or not UK was shown first
    box_score = [team1_data, team2_data] if uk_first(title) else [team2_data, team1_data]

    # add the game's date and opponent to each player
    # iterate through both teams
    for team in box_score:
        # iterate through all players in this team
        for player in team:
            # insert the date
            player.insert(1, info[0])
            # insert the opponent
            player.insert(2, info[1])
            # insert the team identifier
            player.insert(3, 1 if team is team1_data else 0)

    # declare a list of invalid names to delete
    invalid_names = ['', "Team", "TEam", "team"]

    # delete out bad data, including miscellaneous Team totals
    team1_data = [player for player in team1_data if player[0] not in invalid_names]
    team2_data = [player for player in team2_data if player[0] not in invalid_names]

    # remove any ' (*)' links from opponents
    # this indicates that the player is "significant" but we don't care about that
    team2_data = [[player[0].replace(' (*)', '')] + player[1:] for player in team2_data]

    # return the box score as a dictionary
    # trim the Totals value off the player stats
    return {"PlayerStats" : team1_data[:-1] + team2_data[:-1], "TeamStats" : [box_score[0][-1], box_score[1][-1]]}

# given the webpage's title, figure out if Kentucky is listed first
def uk_first(title):
    # in neutral games, "vs." is the separator and Kentucky is always first
    if "vs." in title:
        return True
    
    # determine if Kentucky is the away team or not
    elif " at " in title:
        teams = title.split(" at ")
        return teams[0] == "Kentucky"
    
# given a soup, pull opponent and YYYY-MM-DD out of the title
def get_game_info(soup):
    # get the title of this webpage
    title = get_title(soup)

    # Split the string based on delimiters ' at ', ' vs. ', and ' (' or ' )'
    if ' at ' in title:
        team1, team2 = title.split(' at ')
    else:
        team1, team2 = title.split(' vs. ')
    
    # trim the date off of team2
    team2_nodate = team2.split(' (')[0]
    
    # build the date from the given data between parentheses
    date_match = re.search(r'\(([^)]{3,})\)', title)
    if date_match:
        raw_date = date_match.group(1)
        date_object = datetime.strptime(raw_date, "%B %d, %Y")
        formatted_date = date_object.strftime("%Y-%m-%d")
    
    # return the opponent and formatted date
    return [formatted_date, team2_nodate if team1 == 'Kentucky' else team1]

# given a soup, return the title
def get_title(soup):
    if soup is not None and soup.title is not None:
        return soup.title.get_text()
    else:
        print("Error! Soup is None.")
        return None
    
# find the URL of the next game
def next_game(soup):
    # find the last of all the tables if possible
    last_table = soup.find_all('table')[-1]

    # find all 'a' tags (links) within this table
    links = last_table.find_all('a')

    # extract the HREF attribute value from each 'a' tag
    href_values = [link['href'] for link in links]

    return href_values[-1]