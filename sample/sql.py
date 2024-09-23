import scraper
import sqlite3

# populate a database with a box score
def populate_database(cursor, box_score):
    # create a table to store Kentucky players' statistics
    cursor.execute('''CREATE TABLE IF NOT EXISTS UKPlayerStats (
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS OppPlayerStats (
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
    
    # create a table to store UK's team statistics
    cursor.execute('''CREATE TABLE IF NOT EXISTS UKTeamStats (
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
    
    # create a table to store UK's team statistics
    cursor.execute('''CREATE TABLE IF NOT EXISTS OppTeamStats (
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
    for player in box_score["UKPlayerStats"]:
        cursor.execute("INSERT INTO UKPlayerStats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", player)
    # iterate through opposing players
    for player in box_score["OppPlayerStats"]:
        cursor.execute("INSERT INTO OppPlayerStats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", player)
    
    # add Kentucky's team stats
    cursor.execute("INSERT INTO UKTeamStats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", box_score["UKTeamStats"])
    # add the opponent's team stats
    cursor.execute("INSERT INTO OppTeamStats VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)", box_score["OppTeamStats"])

# perform queries to the database
def run_query(cursor, query):
    #print(query)
    # execute the query
    cursor.execute(query)

    # return all the results
    return cursor.fetchall()

# main function
def main():
    # connect to the database
    connection = sqlite3.connect('ukgames.db')
    cur = connection.cursor()

    # add games to the database
    #add_games(cur)
    
    #query = "DELETE FROM UKPlayerStats WHERE Name = 'Team' OR Name = 'TEam' OR Name = 'team' OR Name = '';"
    #print(run_query(cur, query))

    query = "SELECT Date, PTS FROM OppTeamStats WHERE Team = 'Pennsylvania';"
    print(run_query(cur, query))
    
    # commit and close the database
    connection.commit()
    connection.close()

if __name__ == "__main__":
    main()