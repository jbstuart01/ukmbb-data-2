import re
import requests
from bs4 import BeautifulSoup

# given a URL, return a BeautifulSoup object to parse the HTML
def get_soup(url):
    # Send a GET request to fetch the webpage content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

    # Create a BeautifulSoup object to parse the HTML
    return BeautifulSoup(response.text, 'html.parser')

# scrape the webpage containing all player names
def get_names(soup):
    # Extract specific content (in this case, all the <a> tags)
    links = soup.find_all('a')
    
    # initialize a list to hold the player URLs
    players = []
    
    # for each link, add it to the list
    for link in links:
        # filter out everything that isn't a name
        if '_' in str(link) and 'gbg' not in str(link):
            players.append(str(link.get('href'))[8:])        

    # return the list of players
    return players

# get the jersey number
def get_number(soup):
    # Extract the jersey number (from the anchor tag with the format '# 45')
    jersey_number_tag = soup.find('a', href=re.compile("playersjersey.html"))
    
    # return the number if it's found, None if not
    return jersey_number_tag.text.strip()[2:] if jersey_number_tag else None

# get the home city
def get_city(soup):
    # Find the 'b' tag containing "Hometown: "
    hometown_tag = soup.find('b', text="Hometown: ")
    
    # Split by ',' and take the first part
    return hometown_tag.next_sibling.strip().split(',')[0]

# get the home state
def get_state(soup):
    # Find the 'b' tag containing "Hometown: "
    hometown_tag = soup.find('b', text="Hometown: ")
    
    # Find the <a> tag that contains the state
    return hometown_tag.find_next('a').text.strip() if hometown_tag else None
    
 # scrape data from a given player's webpage
def scrape_player(soup):    
    # create a list of all <p> sections of this webpage
    links = soup.find_all('p')
    # create dictionary to hold information about the player
    player_info = {}
    
    # check this player for a jersey number
    player_info['number'] = get_number(soup)
    
    # check this player for a home city
    player_info['home_city'] = get_city(soup)
    
    # check this player for a home state
    player_info['home_state'] = get_state(soup)
    print(links)
    print(player_info)     

def main():
    # URL of the webpage to scrape
    names_url = "http://www.bigbluehistory.net/bb/Statistics/players.html"
    player_url = "http://www.bigbluehistory.net/bb/Statistics/Players/"

    # Call the scrape_webpage function
    players = get_names(get_soup(names_url))
    
    scrape_player(get_soup(player_url + players[500]))
        

if __name__ == "__main__":
    main()