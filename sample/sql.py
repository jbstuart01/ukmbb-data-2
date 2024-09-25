import sample.box_score_scraper as box_score_scraper
import sqlite3

# populate a database with a box score
def populate_database(cursor, box_score):    
    # create a table to store Kentucky players' statistics
    cursor.execute('''CREATE TABLE IF NOT EXISTS PlayerStats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                Date TEXT,
                Team TEXT,
                Name TEXT,
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
    cursor.execute('''CREATE TABLE IF NOT EXISTS TeamStats (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
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
    
    # iterate through players, updating the table
    for player in box_score["PlayerStats"]:
        # if it's a game with every statistic
        if len(player) == 19:
            cursor.execute('''INSERT INTO PlayerStats (
                    Date, Team, Name, Minutes, FGM, FGA, TFGM, TFGA, FTM, FTA, ORB, DRB, TRB, PF, AST, STL, BLK, TOV, PTS) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', player)
        # if it's a game without distinct ORB/DRB totals
        elif len(player) == 17:
            cursor.execute('''INSERT INTO PlayerStats (
                Date, Team, Name, Minutes, FGM, FGA, TFGM, TFGA, FTM, FTA, ORB, DRB, TRB, PF, AST, STL, BLK, TOV, PTS) 
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, NULL, NULL, ?, ?, ?, ?, ?, ?, ?)''', player)
    
        # if it's a game before the 3 point line
        elif len(player) == 15:
            cursor.execute('''INSERT INTO PlayerStats (
                Date, Team, Name, Minutes, FGM, FGA, TFGM, TFGA, FTM, FTA, ORB, DRB, TRB, PF, AST, STL, BLK, TOV, PTS) 
                VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, ?, ?, NULL, NULL, ?, ?, ?, ?, ?, ?, ?)''', player)
        
        # early 70s with minutes
        elif len(player) == 12:
            cursor.execute('''INSERT INTO PlayerStats (
                Date, Team, Name, Minutes, FGM, FGA, TFGM, TFGA, FTM, FTA, ORB, DRB, TRB, PF, AST, STL, BLK, TOV, PTS) 
                VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, ?, ?, NULL, NULL, ?, ?, ?, NULL, NULL, NULL, ?)''', player)    

        elif len(player) == 11:
            # early 70s no minutes
            if player[0] > '1970':
                cursor.execute('''INSERT INTO PlayerStats (
                    Date, Team, Name, Minutes, FGM, FGA, TFGM, TFGA, FTM, FTA, ORB, DRB, TRB, PF, AST, STL, BLK, TOV, PTS) 
                    VALUES (?, ?, ?, NULL, ?, ?, NULL, NULL, ?, ?, NULL, NULL, ?, ?, ?, NULL, NULL, NULL, ?)''', player)
            # pre-70s minutes but no assists
            else:
                cursor.execute('''INSERT INTO PlayerStats (
                    Date, Team, Name, Minutes, FGM, FGA, TFGM, TFGA, FTM, FTA, ORB, DRB, TRB, PF, AST, STL, BLK, TOV, PTS) 
                    VALUES (?, ?, ?, ?, ?, ?, NULL, NULL, ?, ?, NULL, NULL, ?, ?, NULL, NULL, NULL, NULL, ?)''', player)

        # early 70s no assists
        elif len(player) == 10:
            cursor.execute('''INSERT INTO PlayerStats (
                Date, Team, Name, Minutes, FGM, FGA, TFGM, TFGA, FTM, FTA, ORB, DRB, TRB, PF, AST, STL, BLK, TOV, PTS) 
                VALUES (?, ?, ?, NULL, ?, ?, NULL, NULL, ?, ?, NULL, NULL, ?, ?, NULL, NULL, NULL, NULL, ?)''', player)    

        # 1930s-1950s, some 1920s
        elif len(player) == 8:
            cursor.execute('''INSERT INTO PlayerStats (
                Date, Team, Name, Minutes, FGM, FGA, TFGM, TFGA, FTM, FTA, ORB, DRB, TRB, PF, AST, STL, BLK, TOV, PTS) 
                VALUES (?, ?, ?, NULL, ?, NULL, NULL, NULL, ?, ?, NULL, NULL, NULL, ?, NULL, NULL, NULL, NULL, ?)''', player)    
    
        # 1920s 
        elif len(player) == 4:
            cursor.execute('''INSERT INTO PlayerStats (
                Date, Team, Name, Minutes, FGM, FGA, TFGM, TFGA, FTM, FTA, ORB, DRB, TRB, PF, AST, STL, BLK, TOV, PTS) 
                VALUES (?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, ?)''', player)    
        # 1910s
        elif len(player) == 6:
            cursor.execute('''INSERT INTO PlayerStats (
                Date, Team, Name, Minutes, FGM, FGA, TFGM, TFGA, FTM, FTA, ORB, DRB, TRB, PF, AST, STL, BLK, TOV, PTS) 
                VALUES (?, ?, ?, NULL, ?, NULL, NULL, NULL, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, ?)''', player)    

        # 1900s
        elif len(player) == 3:
             cursor.execute('''INSERT INTO PlayerStats (
                Date, Team, Name, Minutes, FGM, FGA, TFGM, TFGA, FTM, FTA, ORB, DRB, TRB, PF, AST, STL, BLK, TOV, PTS) 
                VALUES (?, ?, ?, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL, NULL)''', player)    

             
            
    
    
    
    
    
    
    # add the team stats
    for team in box_score["TeamStats"]:
        if len(team) == 19:
            cursor.execute('''INSERT INTO TeamStats (
                    Date, Team, Minutes, FGM, FGA, TFGM, TFGA, FTM, FTA, ORB, DRB, TRB, PF, AST, STL, BLK, TOV, PTS) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', team)
        elif len(team) == 17:
            cursor.execute('''INSERT INTO TeamStats (
                    Date, Team, Minutes, FGM, FGA, TFGM, TFGA, FTM, FTA, ORB, DRB, TRB, PF, AST, STL, BLK, TOV, PTS) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)''', team)
            
            

# perform queries on the database
def run_query(cursor, query):
    # execute the query
    cursor.execute(query)

    # return all the results
    return cursor.fetchall()