import scraper
import sql

# create a cursor connected to the database
# will create the database if it doesn't exist
cursor = sql.sqlite3.connect('ukgames.db').cursor()
# start from scratch
#cursor.execute('''DROP TABLE IF EXISTS PlayerStats''')
#cursor.execute('''DROP TABLE IF EXISTS TeamStats''')

# the game we start with
game = '20240321Oakland.html'

# iterate until the last game, exclusive
while game == '20240321Oakland.html':
    # build a soup out of this game's webpage
    soup = scraper.read_html(f"http://www.bigbluehistory.net/bb/Statistics/Games/{game}")
    
    # get the title of this game
    title = scraper.get_title(soup)
    
    # make the box score
    box_score = scraper.get_box_score(soup, title)

    # populate the database with this box score
    sql.populate_database(cursor, box_score)
    
    print(f"Added: {game}")
    
    # get the next game
    try:
        #game = scraper.next_game(soup)
        game = ""
    except IndexError:
        print("AAHHH INDEX ERROR!")
        break
    
# Commit the changes
cursor.connection.commit()
cursor.connection.close()