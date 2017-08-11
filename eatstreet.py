"""Helper functions to deal with requests from Eat Street API."""

import requests
import os
import re

# URLs and headers for interaction with EatStreet API
SEARCH_URL = "https://api.eatstreet.com/publicapi/v1/restaurant/search?"
MENU_URL = "https://api.eatstreet.com/publicapi/v1/restaurant/{}/menu"
HEADERS = {"X-Access-Token": os.environ["EAT_ACCESS_TOKEN"]}


def search_eatstreet(term, address):
    """Gets available delivery restaurants from Eat Street API.

    Args: term is string type of cuisine or restaurant
          address is user's delivery address

    Return value list of restaurant dicts that deliver to user's address."""

    params = {"street-address": address, "method": "delivery"}

    # get restaurants that meet search terms from Eat Street
    response = requests.get(SEARCH_URL, params=params, headers=HEADERS)

    result = response.json()

    restaurants = result["restaurants"]

    term = term.split(" ")
    first_word = term[0]

    matching_restaurants = []

    # check API response to see if first word of search term falls within
    # restaurant or food type category
    for restaurant in restaurants:

        food_types = restaurant["foodTypes"]
        restaurant_name = restaurant["name"]

        if re.search(first_word, restaurant_name, flags=re.IGNORECASE):

            if restaurant not in matching_restaurants:
                matching_restaurants.append(restaurant)

        for food in food_types:

            if re.search(first_word, food, flags=re.IGNORECASE):

                if restaurant not in matching_restaurants:
                    matching_restaurants.append(restaurant)

    return matching_restaurants


def get_restaurant_details(restaurant, address):
    """Gets detailed restaurant information.

       Args: restaurant is name of restaurant user is searching
             address is user's address

       Returns dict of information about specific restaurant."""

    params = {"street-address": address, "method": "delivery",
              "search": restaurant}

    # get restaurants that meet search terms from Eat Street
    response = requests.get(SEARCH_URL, params=params, headers=HEADERS)

    result = response.json()

    restaurant = result["restaurants"][0]

    return restaurant


def get_restaurant_menu(restaurant_info):
    """Get restaurant's menu from eatstreet.

       Args: restaurant_info = results of get_restaurant_details for restaurant

       Returns restaurant's menu as list of dicts"""

    api_key = restaurant_info["apiKey"]

    response = requests.get(MENU_URL.format(api_key), headers=HEADERS)

    menu = response.json()

    return menu


def get_restaurant_list(search_result):
    """Extracts restaurant info for each restaurant in search_eatstreet result.

    Args: list of restaurant dicts obtained by using search_eatstreet function

    Returns each restaurant's name and full address as a list of tuples."""

    restaurant_list = []

    # parse search result for use in other functions
    for restaurant in search_result:
        name = restaurant["name"]
        street_address = restaurant["streetAddress"]
        city = restaurant["city"]
        state = restaurant["state"]
        zipcode = restaurant["zip"]
        full_address = "{} {}, {} {}".format(street_address, city, state,
                                             zipcode)
        restaurant_list.append((name, full_address))

    return restaurant_list


def get_cuisine_count(address):
    """Searches eat street API for all restaurants that deliver to user.

       Args: address is user's full address

       Returns dict: keys are cuisine types
                     values are how many restaurants in users delivery area
                     that are listed under that cuisine type."""

    params = {"street-address": address, "method": "delivery"}

    # get restaurants that meet search terms from Eat Street
    response = requests.get(SEARCH_URL, params=params, headers=HEADERS)

    result = response.json()

    restaurants = result["restaurants"]

    cuisine_count = {}

    # count how many restaurants fall into each cuisine type
    for restaurant in restaurants:
        food_types = restaurant["foodTypes"]

        for cuisine in food_types:
            # only used first word because data from API is not consistent
            # ex: 'indian' and 'indian food' are different categories
            first_word = cuisine.split(" ")[0]

            if first_word not in cuisine_count:
                cuisine_count[first_word] = 1

            else:
                cuisine_count[first_word] += 1

    return cuisine_count


def format_chart_data(data_dict):
    """Changes information from get_cuisine_count into format for chartJS."""

    cuisine_list = data_dict.items()

    sorted_cuisines = sorted(cuisine_list, key=lambda x: x[1], reverse=True)

    top_five = sorted_cuisines[0:5]

    labels = []
    counts = []

    for cuisine in top_five:
        labels.append(cuisine[0])
        counts.append(cuisine[1])

    # format properly for use with chartJS
    data_dict = {"labels": labels,
                 "datasets": [{"data": counts,
                               "backgroundColor": [
                                   "#AE5E50", "#B67BA4", "#68B1D2", "#5BD8A7",
                                   "#F3FE72"
                               ],
                               "hoverBackgroundColor": [
                                   "#AE5E50", "#B67BA4", "#68B1D2", "#5BD8A7",
                                   "#F3FE72"]}]}

    return data_dict
