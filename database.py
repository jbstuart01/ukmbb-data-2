import sqlite3

# connect to the database
connection = sqlite3.connect('data\\fullgames.db')
print("Opened database")

# example query
cursor = connection.execute("SELECT * FROM FullGames WHERE lead_scorer LIKE 'Chris Livingston'")

# print each entry
for row in cursor:
    print(row)