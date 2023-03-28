from bs4 import BeautifulSoup
import requests
import re
from config import LOUNAAT_INFO_URL, POR_URL, POR_HEADERS, TELLUS_URL, blacklist

def is_blacklisted(restaurant_name):
    for blacklisted_name in blacklist:
            if (blacklisted_name.casefold() in restaurant_name.casefold()):
                return True
    return False

def get_lounaat_info_restaurants():
    try:
        response = requests.get(LOUNAAT_INFO_URL)
    except Exception as e:
        print("fail")
        print(e)
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')

    content = soup.find("div", class_="item-container masonry") # get the blob of data of all restaurants

    restaurants = []

    for element in content.find_all("div", class_=re.compile("^menu item category")): # for each restaurant do the following

        restaurant = {"name": "",
                    "address": "",
                    "distance": "",
                    "dishes": []}

        name = element.find("a", href=re.compile("^/lounas/")).text
        if name: restaurant["name"] = name

        address = element.find("p", class_="dist")["title"]
        if address: restaurant["address"] = address

        distance = element.find("p", class_="dist").text.strip()
        if distance: restaurant["distance"] = distance

        menu_content = element.find("div", class_="item-body")
        for dish in menu_content.find_all("li", class_=re.compile("^menu-item")):

            price_tag = dish.find("p", class_="price")
            if price_tag:
                price_tag.extract()

            restaurant["dishes"].append(dish.text)

        if name and not is_blacklisted(name):
            restaurants.append(restaurant)

    return restaurants

def get_por_restaurants():
    try:
        response = requests.get(POR_URL, headers=POR_HEADERS)
    except Exception as e:
        print("fail")
        print(e)
        return []
    
    soup = BeautifulSoup(response.text, 'html.parser')
    content = soup.find("div", class_="kt-tab-inner-content-inner") # get the blob of data containing the menu
    starting_tag = content.find("h2", string=re.compile("^Viikko")) # find the tag before today's menu
    menu_element = starting_tag.find_next_sibling()
    menu_element.find("strong").extract() # filter out and discard the date string
    matched_dishes = re.findall(r"[A-Z].*?(?=\d)", menu_element.text) # list dishes with some regex magic

    restaurants = []

    restaurant = {"name": "POR",
                "address": "Strömbergintie 1, 00380 Helsinki",
                "distance": "0m",
                "dishes": matched_dishes}
    
    restaurants.append(restaurant)
    return restaurants

def get_tellus_restaurants():
    # missing implementation
    try:
        response = requests.get(TELLUS_URL)
    except Exception as e:
        print("fail")
        print(e)
        return []
    
    soup = BeautifulSoup(response.text, features='xml')
    content = soup.find("description").find_next("description") # get the blob of data containing the menu
    matched_dishes = re.split(r"<br>\s*", content.text.replace('\n', '')) # list dishes with some regex magic

    restaurants = []

    restaurant = {"name": "Tellus",
                "address": "Valimopolku 4, 00380 Helsinki",
                "distance": "0m",
                "dishes": [x.replace(')', ') ') for x in matched_dishes if x != '']}
    
    restaurants.append(restaurant)
    return restaurants

# scrape the data and return a list of restaurants represented as dict objects
def get_restaurants():
    return get_por_restaurants() + get_tellus_restaurants() + get_lounaat_info_restaurants()