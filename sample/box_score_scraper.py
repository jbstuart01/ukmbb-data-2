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

def get_box_score(soup, title):
    tables = soup.find_all('table')

    # Get the title and game information (date and opponent)
    title = get_title(soup)
    info = get_game_info(soup)

    # Initialize the box score
    all_player_stats = []

    # Iterate through each table
    for table in tables:
        # Find all rows
        rows = table.find_all('tr')

        # Iterate through each row (player), skipping the header
        for i in range(0, len(rows)):
            # Get data from each cell in the row
            cells = rows[i].find_all('td')

            # Extract text from each cell and remove whitespace
            player_stats = [cell.get_text() for cell in cells]

            # Append player statistics to the list
            all_player_stats.append(player_stats)

    # Strip leading null entry and trailing information
    all_player_stats = all_player_stats[1:-2]

    # Use the null entry in between teams to separate the teams in the list
    separator_index = next((i for i, row in enumerate(all_player_stats) if not row), None)

    # get the first team's information
    team1_data = all_player_stats[:separator_index]
    # iterate through the players in team1
    for player in team1_data:
        # label this player as a Kentucky player if Kentucky is the first team
        player.insert(0, "Kentucky" if uk_first(title) else info[1])
    # get the second team's information 
    team2_data = all_player_stats[separator_index + 1:]
    # iterate through the players in team2
    for player in team2_data:
        # label this player as the opponent if Kentucky is the first team
        player.insert(0, info[1] if uk_first(title) else "Kentucky")

    # Combine player stats from both teams into one list
    player_stats = team1_data[:-1] + team2_data[:-1]

    # Add the game's date and opponent to each player
    for player in player_stats:
        # insert the date at the beginning of each player
        player.insert(0, info[0])

    # Remove any ' (*)' links from opponent players
    player_stats = [[player[0].replace(' (*)', '')] + player[1:] for player in player_stats]

    # Get team stats (the last row for each team)
    team_stats = [team1_data[-1], team2_data[-1]]
    for team in team_stats:
        team.insert(0, info[0])
        del(team[2])
    # Return the combined player stats and team stats as a dictionary
    return {
        "PlayerStats": player_stats,
        "TeamStats": team_stats
    }

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
    date_match = re.search(r'\(([A-Za-z]+ \d{1,2}, \d{4})\)', title)
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

# soup = read_html("http://www.bigbluehistory.net/bb/statistics/Games/20120111Auburn.html")
# title = get_title(soup)
# print(get_box_score(soup, title))