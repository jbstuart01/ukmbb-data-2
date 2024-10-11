import player_scraper
import sql


def main():
    # URL of the webpage to scrape
    names_url = "http://www.bigbluehistory.net/bb/Statistics/players.html"
    player_url = "http://www.bigbluehistory.net/bb/Statistics/Players/"

    # Call the scrape_webpage function
    players = player_scraper.get_players(player_scraper.get_soup(names_url))
    
    # create a connection to the database
    cursor = sql.sqlite3.connect('ukgames2.db').cursor()
    
    # iterate through all players, skipping footer value
    for player in players[:-1]:
        # scrape this player's webpage for data    
        player_to_insert = player_scraper.scrape_player(player_scraper.get_soup(player_url + player))

        # insert this player into the database
        sql.populate_player(cursor, player_to_insert)
        
    # commit the changes and close the connection to the database
    cursor.connection.commit()
    cursor.connection.close()

if __name__ == "__main__":
    main()