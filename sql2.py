import scraper2
import sqlite3

# populate a database with a box score
def populate_database(cur, box_score):
    # create a table to store players' statistics
    cur.execute('''CREATE TABLE IF NOT EXISTS PlayerStats (
                Name TEXT,
                Date TEXT,
                Opponent TEXT,
                TeamInd INT,
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
    
    # create a table to store team statistics
    cur.execute('''CREATE TABLE IF NOT EXISTS TeamStats (
                Name TEXT,
                Date TEXT,
                Opponent TEXT,
                TeamInd INT,
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
    for player in box_score["PlayerStats"]:
        cur.execute("INSERT INTO PlayerStats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", player)
    
    # add the opponent's team stats
    cur.execute("INSERT INTO TeamStats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", box_score["OppTeamStats"])

# perform queries to the database
def run_query(cur, query):
    #print(query)
    # execute the query
    cur.execute(query)

    # return all the results
    return cur.fetchall()

# add multiple games to the database
def add_games(cur):
    # the game we start with
    game = '20091113Morehead.html'
    # iterate over however many consecutive games you want to add
    for i in range(0, 532):
        # build a soup out of this game's webpage
        soup = scraper2.read_html(f"http://www.bigbluehistory.net/bb/Statistics/Games/{game}")
        
        # get the title of this game
        title = scraper2.get_title(soup)
        
        # make the box score
        box_score = scraper2.get_box_score(soup, title)

        # populate the database with this box score
        populate_database(cur, box_score)

        print(f"Added: {game}")
        
        # get the next game
        game = scraper2.next_game(soup)

# main function
def main():
    # connect to the database
    conn = sqlite3.connect('ukgames2.db')
    cur = conn.cursor()

    # add games to the database
    add_games(cur)
    
    #query = "DELETE FROM UKPlayerStats WHERE Name = 'Team' OR Name = 'TEam' OR Name = 'team' OR Name = '';"
    #print(run_query(cur, query))

    query = "SELECT Date, Name, Team, PTS FROM PlayerStats WHERE PTS > 34;"
    print(run_query(cur, query))
    
    # commit and close the database
    conn.commit()
    conn.close()

if __name__ == "__main__":
    main()
