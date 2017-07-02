"""Helper functions to deal with requests from Eat Street API."""

import requests
import os
import json


def search_eatstreet(term, address):
    """Gets available delivery restaurants from Eat Street API.

    Args: term is string type of cuisine or restaurant
          address is user's delivery address

    Return value list of restaurant dicts that deliver to user's address."""

    # headers contain authentication information
    headers = {"X-Access-Token": os.environ["EAT_ACCESS_TOKEN"]}

    params = {"street-address": address, "method": 'delivery', "search": term}

    # get restaurants that meet search terms from Eat Street
    response = requests.get("https://api.eatstreet.com/publicapi/v1/restaurant/search?",
                            params=params,
                            headers=headers)

    result = response.json()

    restaurants = result["restaurants"]

    return restaurants


def get_restaurant_list(search_result):
    """Extracts restaurant info for each restaurant in search_eatstreet result.

    Args: list of restaurant dicts obtained by using search_eatstreet function

    Returns each restaurant's name and full address as a list of tuples."""

    restaurant_list = []

    for restaurant in search_result:
        name = restaurant['name']
        street_address = restaurant['streetAddress']
        city = restaurant['city']
        state = restaurant['state']
        zipcode = restaurant['zip']
        full_address = street_address + ' ' + city + ' ' + state + ' ' + zipcode
        restaurant_list.append((name, full_address))

    return restaurant_list
