import csv
from sql import *

# create a cursor connected to the database
# will create the database if it doesn't exist
connection = sqlite3.connect('ukgames.db')
cursor = connection.cursor()

cursor.execute('''CREATE TABLE IF NOT EXISTS GameInfo (
            Date DATE,
            Season TEXT,
            Opponent TEXT,
            Result TEXT,
            Location TEXT,
            UKScore INT,
            OppScore INT,
            Notes TEXT,
            Arena TEXT,
            Attendnance INT,
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
        
        for row in reader:
            cursor.execute('''
                INSERT INTO GameInfo (
                    Date, Season, Opponent, Result, Location, UKScore, OppScore, Notes, Arena, Attendnance, City, UKHalfScore, OppHalfScore, OTS, UKRank, OppRank, OppCoach, OppConference, LeadScorer, LeadScorerPoints, LeadRebounder, LeadRebounderRebs, LeadAssister, LeadAssisterAsts, LeadStealer, LeadStealerSteals, LeadBlocker, LeadBlockerBlocks)
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);
                    ''', row)
            
        # commit and close the connection
        connection.commit()
        connection.close()


if __name__ == "__main__":
    main()