import scraper
import sqlite3

# populate a database with a box score
def populate_database(conn, cur, box_score):
    # create a table to store Kentucky players' statistics
    cur.execute('''CREATE TABLE IF NOT EXISTS UKPlayerStats (
                Name TEXT,
                Date TEXT,
                Opponent TEXT,
                Minutes INT,
                FGM INT,
                FGA INT,
                TFGM INT,
                TFGA INT,
                FTM INT,
                FTA INT,
                ORB INT,
                DRB INT,
                TRB INT,
                PF INT,
                AST INT,
                STL INT,
                BLK INT,
                TOV INT,
                PTS INT
                )''')
    
    # create a table to store opposing players' statistics
    cur.execute('''CREATE TABLE IF NOT EXISTS OppPlayerStats (
                Name TEXT,
                Date TEXT,
                Team TEXT,
                Minutes INT,
                FGM INT,
                FGA INT,
                TFGM INT,
                TFGA INT,
                FTM INT,
                FTA INT,
                ORB INT,
                DRB INT,
                TRB INT,
                PF INT,
                AST INT,
                STL INT,
                BLK INT,
                TOV INT,
                PTS INT
                )''')
    
    # iterate through each player, updating the correct table
    # iterate through Kentucky players
    for player in box_score[0]:
        cur.execute("INSERT INTO UKPlayerStats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", player)
    # iterate through opposing players
    for player in box_score[1]:
        cur.execute("INSERT INTO OppPlayerStats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", player)

# perform queries to the database
def run_query(conn, cur, query):
    # execute the query
    cur.execute(query)

    # return all the results
    return cur.fetchall()

# add multiple games to the database
def add_games(conn, cur):
    # the game we start with
    game = '20091113Morehead.html'
    # iterate over however many consecutive games you want to add
    for i in range(0, 38):
        # build a soup out of this game's webpage
        soup = scraper.read_html(f"http://www.bigbluehistory.net/bb/Statistics/Games/{game}")
        
        # get the title of this game
        title = scraper.get_title(soup)
        
        # make the box score
        box_score = scraper.get_box_score(soup, title)

        # populate the database with this box score
        populate_database(conn, cur, box_score)

        print(f"Added: {game}")
        
        # get the next game
        game = scraper.next_game(soup)

# main function
def main():
    # connect to the database
    conn = sqlite3.connect('ukgames.db')
    cur = conn.cursor()

    # add games to the database
    #add_games(conn, cur)
   
    #query = "DELETE FROM OppPlayerStats;"
    
    query = "SELECT Name, Team, PTS FROM OppPlayerStats WHERE PTS > 23 AND Name != 'Team' AND Name != 'Totals';"
    print(run_query(conn, cur, query))    
    
    # commit and close the database
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
