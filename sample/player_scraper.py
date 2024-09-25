import requests
from bs4 import BeautifulSoup

# scrape the webpage containing all player names
def gather_urls(url):
    # Send a GET request to fetch the webpage content
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code != 200:
        print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
        return None

    # Create a BeautifulSoup object to parse the HTML
    soup = BeautifulSoup(response.text, 'html.parser')

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

def main():
    # URL of the webpage to scrape
    url = "http://www.bigbluehistory.net/bb/Statistics/players.html"

    # Call the scrape_webpage function
    players = gather_urls(url)
    print(players)
    

if __name__ == "__main__":
    main()