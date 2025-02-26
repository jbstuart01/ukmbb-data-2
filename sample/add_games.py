import box_score_scraper
import sql

# create a cursor connected to the database
# will create the database if it doesn't exist
cursor = sql.sqlite3.connect('ukgames2.db').cursor()
# start from scratch
#cursor.execute('''DROP TABLE IF EXISTS PlayerStats''')
#cursor.execute('''DROP TABLE IF EXISTS TeamStats''')

# the game we start with
game = '19050222KentuckyUniversity.html'
# iterate until the last game, exclusive
while game == '19050222KentuckyUniversity.html':
    # build a soup out of this game's webpage
    soup = box_score_scraper.read_html(f"http://www.bigbluehistory.net/bb/Statistics/Games/{game}")
    
    # get the title of this game
    title = box_score_scraper.get_title(soup)
    
    # make the box score
    box_score = box_score_scraper.get_box_score(soup, title)

    # populate the database with this box score
    sql.populate_boxscore(cursor, box_score)
    
    # get the next game
    try:
        #game = box_score_scraper.next_game(soup)
        game = ""
    except IndexError:
        print("AAHHH INDEX ERROR!")
        print(game)
        break
    
# Commit the changes
cursor.connection.commit()
cursor.connection.close()