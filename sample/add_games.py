import scraper
from sql import *

# create a cursor connected to the database
# will create the database if it doesn't exist
cursor = sqlite3.connect('ukgames.db').cursor()

# the game we start with
game = '20091113Morehead.html'

# iterate over however many consecutive games you want to add
for i in range(0, 532):
    # build a soup out of this game's webpage
    soup = scraper.read_html(f"http://www.bigbluehistory.net/bb/Statistics/Games/{game}")
    
    # get the title of this game
    title = scraper.get_title(soup)
    
    # make the box score
    box_score = scraper.get_box_score(soup, title)

    # populate the database with this box score
    populate_database(cursor, box_score)

    print(f"Added: {game}")
    
    # get the next game
    game = scraper.next_game(soup)