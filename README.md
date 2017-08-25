# Hangry

Hangry is an API centric aggregator that collects and displays food delivery and
ratings information using the Eatstreet and Yelp Fusion APIs.  Hangry aims to
streamline the process of ordering food delivery by making more information
accessible in one place including restaurant names and Yelp reviews, menus, 
photos, whether or not the restaurant is open, and a link to place your order.
Future goals include adding more food delivery services to the site, publicly
deploying the service, and improving timeliness of API calls.

## Getting Started

Download files from Github

If you don't have PostgreSQL installed on your machine, download [here](https://www.postgresql.org/download/).

Create and activate a virtual environment:
```
$virtualenv env
$source env/bin/activate
```
Pip install requirements
```
$pip install -r requirements.txt
```

Create a Postgres database for user data
```
$createdb hangry
```

Enter data_model.py interactively to create database tables
```
$python -i data_model.py
```

Create all tables
```
>>>db.create_all()
```

Check db for users table
```
$psql hangry

# SELECT * FROM USERS;
```

The SQL query above should return the following if the database is set up properly
```
 user_id | username | email | password | st_address | city | state | zipcode | fav_cuisine 
---------+----------+-------+----------+------------+------+-------+---------+-------------
(0 rows)
```

Get API user tokens from Yelp Fusion and Eatstreet (see yelp.py in this repo for
a function that requests an oauth token using Yelp client id and secret key -
Oauth token required for Yelp Fusion API requests)

Source necessary environmental variables into your virtual env.  These include
CLIENT_ID, CLIENT_SECRET, YELP_ACCESS_TOKEN from Yelp Fusion API,
EAT_ACCESS_TOKEN from eatstreet API, and SECRET_KEY for Flask session use.
One way to do this is to create a shell file including the following scripts.

```
export CLIENT_ID="Replace with Yelp client id"
export CLIENT_SECRET="Replace with Yelp secret key"
export YELP_ACCESS_TOKEN="Replace with Yelp Oauth access token"
export EAT_ACCESS_TOKEN="Replace with Eatstreet access token"
export SECRET_KEY="Any string will do here"
```

Then from the command line
```
$source secrets.sh
```

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

Program written in Python 2.7 and created using Vagrant virtual machine running Ubuntu.  Please see requirements.txt for a full list of requirements.


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
* [PostgreSQL](https://www.postgresql.org/download/) - Database for storing user
information
* [Vagrant](https://www.vagrantup.com/intro/getting-started/) - Virtual machine for running Ubuntu
