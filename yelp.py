"""Helper functions to deal with requests from Yelp API."""


import requests
import os


def get_access_token():
    """Uses client id & secret key to get access token for Yelp API."""

    token_url = 'https://api.yelp.com/oauth2/token'

    payload = {'grant_type': 'client_credentials',
               'client_id': os.environ["CLIENT_ID"],
               'client_secret': os.environ["CLIENT_SECRET"]}  # get client id and secret from environment after sourcing secrets.sh

    response = requests.post(token_url, data=payload)

    token = response.json()

    access_token = token['access_token']

    return access_token


def get_yelp_rating(restaurant, location):
    """Gets Yelp rating for restaurant.

    Args: restaurant is a tuple with restaurant name at index 0 and full
          restaurant address at index 1.  get_yelp_rating function to be
          used in conjunction with search_eatstreet and get_restaurant_info
          functions from eatstreet.py file.


    Return value is float between 1 and 5."""

    # headers contain authentication information
    headers = {"Authorization": "Bearer " + os.environ["YELP_ACCESS_TOKEN"]}

    # search params limit response to one restaurant
    params = {"term": restaurant, "location": location, "limit": 1}

    # get first restaurant that matches search terms from Yelp API
    response = requests.get("https://api.yelp.com/v3/businesses/search",
                            params=params,
                            headers=headers)

    result = response.json()

    # get restaurant rating from API response
    rating = result["businesses"][0]["rating"]

    print rating
    return rating
