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
    response = requests.get(
        "https://api.eatstreet.com/publicapi/v1/restaurant/search?",
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

    # headers contain authentication information
    headers = {"X-Access-Token": os.environ["EAT_ACCESS_TOKEN"]}

    params = {"street-address": address, "method": "delivery"}

    # get restaurants that meet search terms from Eat Street
    response = requests.get(
        "https://api.eatstreet.com/publicapi/v1/restaurant/search?",
        params=params,
        headers=headers)

    result = response.json()

    restaurants = result["restaurants"]

    cuisine_count = {}

    for restaurant in restaurants:
        food_types = restaurant['foodTypes']

        for cuisine in food_types:
            first_word = cuisine.split(' ')[0]

            if first_word not in cuisine_count:
                cuisine_count[first_word] = 1

            else:
                cuisine_count[first_word] += 1

    return cuisine_count
