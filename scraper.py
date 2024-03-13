from bs4 import BeautifulSoup
import csv
from datetime import datetime
import re
import requests

# fetch HTML data from the website
def get_html(url):
    response = requests.get(url)
    return response.text

# make the box score given soup
def get_box_score(soup, uk_first):
    tables = soup.find_all('table')

    # initialize a list of 17 empty elements to hold statistics
    # 17 is the full amount of stats, so box scores from early seasons without certain statistics will still be same size
    all_player_stats = []

    # iterate through each table
    for table in tables:
        # find all rows
        rows = table.find_all('tr')

        # iterate through each row (player), skipping the header
        for i in range(0, len(rows)):
            # get data from each cell in the row
            cells = rows[i].find_all('td')

            # extract text from each cell and remove whitespace
            player_stats = [cell.get_text().strip() for cell in cells]

            # append player statistics to the list
            all_player_stats.append(player_stats)
    
    # return a box score of the game with the headers and footers trimmed off
    return all_player_stats[1:-2]

# read data from HTML
def read_html(html, csv_filename):
    # create a beautifulsoup object
    soup = BeautifulSoup(html, 'html.parser')
    
    # find the title of the webpage
    # this tells us the date of the game and if Kentucky is first or second box score
    title = soup.title.get_text()

    # get the date of the game
    date = get_date(title)

    # make the box score
    get_box_score(soup, uk_first(title))

    data = []
    paragraphs = soup.find_all('a')
    for p in paragraphs[:-15]:
        data.append(p.get_text())   
       
    # return the HTML data
    return data

# given the webpage's title, figure out if Kentucky is listed first
def uk_first(title):
    # in neutral games, "vs." is the separator and Kentucky is always first
    if "vs." in title:
        return True
    
    # determine if Kentucky is the away team or not
    elif " at " in title:
        teams = title.split(" at ")
        return teams[0] == "Kentucky"


# clean up data from HTML
def clean_data(data):
    # this dictionary will hold the cleaned data
    new_data = {}

    # assign this game's date
    new_data["date"] = get_date(data[1])
    print(new_data["date"])

# pull the date out of the title
def get_date(title):
    # extract the characters between the parentheses
    date_match = re.search(r'\(([^)]+)\)', title)

    # if it worked, do the following
    if date_match:
        # make the data between the parentheses raw_date
        raw_date = date_match.group(1)
        # format the date
        date_object = datetime.strptime(raw_date, "%B %d, %Y")
        formatted_date = date_object.strftime("%Y-%m-%d")
    else:
        formatted_date = "ERROR"

    return formatted_date

# write data to CSV
def write_csv(data, csv_filename):
    with open(csv_filename, 'w', newline = '', encoding = 'utf-8') as csvfile:
        writer = csv.writer(csvfile)
        for item in data:
            writer.writerow([item])

# URL of the website to scrape
url = 'http://www.bigbluehistory.net/bb/Statistics/Games/19891128Ohio.html'

# filename of the CSV to create
csv_filename = '19030206GeorgetownCollege.csv'

# fetch HTML data
html = get_html(url)

# extract data and write to CSV
html_data = read_html(html, csv_filename)

# clean the data
#clean_data(html_data)

# write the data to a CSV
#write_csv(html_data, csv_filename)