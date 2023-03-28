from bs4 import BeautifulSoup
import requests
import re
from config import URL, blacklist

# scrape the data and return a list of restaurants represented as dict objects
def get_restaurants():

    try:
        response = requests.get(URL)
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
        restaurants.append(restaurant)
    return restaurants