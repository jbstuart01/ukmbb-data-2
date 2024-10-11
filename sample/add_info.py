import csv
from sql import *

# create a cursor connected to the database
connection = sqlite3.connect('ukgames2.db')
cursor = connection.cursor()

# start from scratch
cursor.execute('''DROP TABLE IF EXISTS GameInfo''')
cursor.execute('''CREATE TABLE GameInfo (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            Date DATE,
            Day TEXT,
            Season TEXT,
            Opponent TEXT,
            Result TEXT,
            Location TEXT,
            UKScore INT,
            OppScore INT,
            Notes TEXT,
            Arena TEXT,
            Attendance INT,
            City TEXT,
            UKHalfScore INT,
            OppHalfScore INT,
            OTS INT,
            UKRank INT,
            OppRank INT,
            OppCoach TEXT,
            OppConference TEXT,
            LeadScorer TEXT,
            LeadScorerPoints INT,
            LeadRebounder TEXT,
            LeadRebounderRebs INT,
            LeadAssister TEXT,
            LeadAssisterAsts INT,
            LeadStealer TEXT,
            LeadStealerSteals INT,
            LeadBlocker TEXT,
            LeadBlockerBlocks INT           
            )''')

def main():
    # open the CSV
    with open('data/fullgames.csv', mode = 'r') as file:
        reader = csv.reader(file)
        # skip the header
        next(reader)
        
        # iterate through rows in the CSV
        for row in reader:
            cursor.execute('''
                INSERT INTO GameInfo (
                    Date, Day, Season, Opponent, Result, Location, UKScore, OppScore, Notes, Arena, Attendance, City, UKHalfScore, OppHalfScore, OTS, UKRank, OppRank, OppCoach, OppConference, LeadScorer, LeadScorerPoints, LeadRebounder, LeadRebounderRebs, LeadAssister, LeadAssisterAsts, LeadStealer, LeadStealerSteals, LeadBlocker, LeadBlockerBlocks)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    ''', row)
            
        # commit and close the connection
        connection.commit()
        connection.close()


if __name__ == "__main__":
    main()