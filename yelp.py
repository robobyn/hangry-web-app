"""Helper functions to deal with requests from Yelp API."""


import requests
import os

# API endpoint URLs and headers for Oauth
SEARCH_URL = "https://api.yelp.com/v3/businesses/search"
BUSINESS_URL = "https://api.yelp.com/v3/businesses/{}"
REVIEWS_URL = "https://api.yelp.com/v3/businesses/{}/reviews"
HEADERS = {"Authorization": "Bearer " + os.environ["YELP_ACCESS_TOKEN"]}


def get_access_token():
    """Uses client id & secret key to get access token for Yelp API.

       Access token valid for 180 days - only need this function for new key."""

    token_url = 'https://api.yelp.com/oauth2/token'

    # get client id and secret from environment after sourcing secrets.sh
    payload = {'grant_type': 'client_credentials',
               'client_id': os.environ["CLIENT_ID"],
               'client_secret': os.environ["CLIENT_SECRET"]}

    response = requests.post(token_url, data=payload)

    token = response.json()

    access_token = token['access_token']

    return access_token


def get_yelp_rating(restaurant, location):
    """Gets Yelp rating for restaurant.

    Args: restaurant - name of restaurant
          location - restaurant address

    get_yelp_rating function to be used in conjunction with search_eatstreet
    and get_restaurant_info functions from eatstreet.py file.

    Return value is float between 1 and 5."""

    # search params limit response to one restaurant
    params = {"term": restaurant, "location": location, "limit": 1}

    # get first restaurant that matches search terms from Yelp API
    response = requests.get(SEARCH_URL, params=params, headers=HEADERS)

    result = response.json()

    # get restaurant rating from API response
    rating = result["businesses"][0]["rating"]

    return rating


def get_business_id(restaurant, location):
    """Get Yelp business id to use in other API calls.

    Args: restaurant is restaurant name
          location is user's city

    Returns Yelp business id as a string."""

    # search params limit response to one restaurant
    params = {"term": restaurant, "location": location, "limit": 1}

    # get first restaurant that matches search terms from Yelp API
    response = requests.get(SEARCH_URL, params=params, headers=HEADERS)

    result = response.json()

    business_id = result["businesses"][0]["id"]

    return business_id


def get_photos(business_id):
    """Gets URLs for 3 Yelp restaurant photos based on business id."""

    response = requests.get(BUSINESS_URL.format(business_id), headers=HEADERS)

    result = response.json()

    photo_urls = result["photos"]

    return photo_urls


def get_reviews(business_id):
    """Gets top 3 Yelp reviews & exerpts based on business id."""

    response = requests.get(REVIEWS_URL.format(business_id), headers=HEADERS)

    result = response.json()

    reviews = result["reviews"]

    return reviews
