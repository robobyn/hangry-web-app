"""Sample of code used to get responses from Yelp API."""


import requests
import os
import json


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


headers = {'Authorization': 'Bearer ' + os.environ["ACCESS_TOKEN"]}  # authentication information will be in header

params = dict(term='coffee', latitude=37.786882, longitude=-122.399972)  # search conditions

response = requests.get('https://api.yelp.com/v3/businesses/search',
                        params=params,
                        headers=headers)  # get businesses from keyword search

result = response.json()


# f = open('data.json', 'w')

# for business in result['businesses']: # for each business, get details and dump into a file, one JSON per line
#     _id =  business['id']
#     url = 'https://api.yelp.com/v3/businesses/' + _id
#     print url
#     data = requests.get(url, headers=headers).json()
#     line = json.dumps(data)
#     f.write(line+'\n')

# f.close()
