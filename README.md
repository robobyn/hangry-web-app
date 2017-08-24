# Project Title

Hangry is an API centric aggregator that collects and displays food delivery and
ratings information using the Eatstreet and Yelp Fusion APIs.  Hangry aims to
streamline the process of ordering food delivery by making more information
accessible in one place including restaurant names and Yelp reviews, menus, 
photos, whether or not the restaurant is open, and a link to place your order.
Future goals include adding more food delivery services to the site, publicly
deploying the service, and improving timeliness of API calls.

## Getting Started

Download files from Github
Create and activate a virtual environment:
```
$virtualenv env
$source env/bin/activate
```
Pip install requirements
```
$pip install -r requirements.txt
```
Get API user tokens from Yelp Fusion and Eatstreet (see yelp.py in this repo for
a function that requests an oauth token using Yelp client id and secret key -
Oauth token required for Yelp Fusion API requests)

Run tests.py to ensure all components working properly
```
$python tests.py
```
Start the Hangry server
```
$python hangry-server.py
```
Run in browser using localhost:5000

### Prerequisites

Program written in Python 2.7.  Please see requirements.txt for a full list of requirements.


## Running the tests

From the command line:
```
$python tests.py
```

## Built With

* [Flask](http://flask.pocoo.org/docs/0.12/) - The web framework used
* [Yelp Fusion](https://www.yelp.com/fusion) - API for restaurant reviews
* [Eatstreet](https://developers.eatstreet.com/endpoint/search) - Public
food delivery app API
