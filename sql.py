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

# main function
def main():
    # connect to the database
    conn = sqlite3.connect('ukgames.db')
    cur = conn.cursor()

    # URL of the website to scrape
    #url = 'http://www.bigbluehistory.net/bb/Statistics/Games/19080110LexingtonYMCA.html'
    url = 'http://www.bigbluehistory.net/bb/Statistics/Games/20091113Morehead.html'

    #soup = read_html(url)
    #title = get_title(soup)
    #box_score = get_box_score(soup, title)

    #populate_database(conn, cur, box_score)
    
    #query = "WITH CTE AS (SELECT *, ROW_NUMBER() OVER (PARTITION BY Name) AS row_num FROM UKPlayerStats) DELETE FROM UKPlayerStats WHERE rowid IN (SELECT rowid FROM CTE WHERE row_num > 1);"
    query = "SELECT Name, TRB FROM UKPlayerStats WHERE TRB > 1;"
    print(run_query(conn, cur, query))
    
    
    
    # commit and close the database
    conn.commit()
    conn.close()
if __name__ == "__main__":
    main()
