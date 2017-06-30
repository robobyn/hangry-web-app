"""Helper functions to deal with requests from Eat Street API."""

import requests
import os


def search_eatstreet(term, address):
    """Gets available delivery restaurants from Eat Street API.

    Args: term is string type of cuisine or restaurant
          address is user's delivery address

    Return value dictionary of restaurants that deliver to user's address."""

    # headers contain authentication information
    headers = {'X-Access-Token': os.environ["EAT_ACCESS_TOKEN"]}

    params = {"street-address": address, "method": 'delivery', "search": term}

    # get restaurants that meet search terms from Eat Street
    response = requests.get('https://api.eatstreet.com/publicapi/v1/restaurant/search?',
                            params=params,
                            headers=headers)

    result = response.json()

    restaurants = result['restaurants']

    print restaurants
    return restaurants
