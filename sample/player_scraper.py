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
def get_players(soup):
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

# get the player's name
def get_name(soup):
    # Find the img tag that contains the player's image
    img_tag = soup.find('img', {'src': re.compile(r'Players/.*\.jpg')})

    # Extract the filename and split it to get the name "john_adams"
    if img_tag:
        img_src = img_tag['src']
        # Extract "john_adams" from the file path
        name = img_src.split('/')[-1].split('.')[0]  # Splitting by / and .
        # Replace underscores with spaces and capitalize the name
        return ' '.join(name.split('_')).title()  
        
    else:
        return None

# get the jersey number
def get_number(soup):
    # Extract the jersey number (from the anchor tag with the format '# 45')
    jersey_number_tag = soup.find('a', href=re.compile("playersjersey.html"))
    
    # return the number if it's found, None if not
    return jersey_number_tag.string.strip()[2:] if jersey_number_tag else None

# get the home city
def get_city(soup):
    # Find the 'b' tag containing "Hometown: "
    hometown_tag = soup.find('b', string = "Hometown: ")
    
    # Split by ',' and take the first part
    return hometown_tag.next_sibling.strip().split(',')[0] if hometown_tag else None

# get the home state
def get_state(soup):
    # Find the 'b' tag containing "Hometown: "
    hometown_tag = soup.find('b', string = "Hometown: ")
    
    # Find the <a> tag that contains the state
    return hometown_tag.find_next('a').string.strip() if hometown_tag else None

# convert month to number
def month_to_number(month_name):
    months = {
        'January': '01',
        'February': '02',
        'March': '03',
        'April': '04',
        'May': '05',
        'June': '06',
        'July': '07',
        'August': '08',
        'September': '09',
        'October': '10',
        'November': '11',
        'December': '12'
    }
    return months.get(month_name, None)  # Returns None if month_name is not found

# get the date of birth
def get_dob(soup):
    # Find the <b> tag containing 'Date of Birth: '
    dob_tag = soup.find('b', string='Date of Birth: ')
    
    if dob_tag:
        # The month is in the next <a> tag
        dob_month = dob_tag.find_next('a').text.strip()  # The month is in an <a> tag
        
        # The day and year are in the next text node after the <a> tag
        # Move to the next sibling after the <a> tag, and then get the text
        dob_day_year = dob_tag.find_next('a').find_next_sibling(string=True).strip()
        
        dob_day, dob_year = dob_day_year.split()
        
        return dob_year, month_to_number(dob_month), dob_day[:-1]
    else:
        return None, None, None

def get_height_weight(soup, ind):
    # Find the <b> tag containing 'Playing Height: '
    height_tag = soup.find('b', string = f"Playing {ind}: ")

    # Extract the height following the <b> tag
    if height_tag:
        # Get the next sibling and then navigate through any other nodes
        next_nodes = height_tag.find_next_siblings(string=True)
        for node in next_nodes:
            # Strip any whitespace and check if the text is not empty
            if node.strip():
                return node.strip()  # Return the first non-empty text found
    
    return None

# scrape data from a given player's webpage
def scrape_player(soup):    
    # create a list of all <p> sections of this webpage
    links = soup.find_all('p')
    # create list to hold information about the player
    player_info = []
    
    # check this player for a name
    player_info.append(get_name(soup))
    
    # check this player for a jersey number
    player_info.append(get_number(soup))
    
    # check this player for a home city
    player_info.append(get_city(soup))
    
    # check this player for a home state
    player_info.append(get_state(soup))
    
    # check this player for height
    player_info.append(get_height_weight(soup, "Height"))
    
    # check this player for weight
    player_info.append(get_height_weight(soup, "Weight"))
    
    # check this player for a birth date
    player_info.extend(get_dob(soup))
    
    return player_info