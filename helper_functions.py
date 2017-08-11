"""Functions to use in server routes."""

from yelp import get_yelp_rating

ADDRESS_FORMAT = "{} {}, {} {}"
COMMON_SEARCH_TERMS = ["Pizza", "Sandwiches", "Italian", "Sushi", "Chinese",
                       "Burgers", "Indian", "Mexican", "Desserts",
                       "Thai", "Salads"]
US_STATES = {
    'Alabama': 'AL',
    'Alaska': 'AK',
    'Arizona': 'AZ',
    'Arkansas': 'AR',
    'California': 'CA',
    'Colorado': 'CO',
    'Connecticut': 'CT',
    'Delaware': 'DE',
    'Florida': 'FL',
    'Georgia': 'GA',
    'Hawaii': 'HI',
    'Idaho': 'ID',
    'Illinois': 'IL',
    'Indiana': 'IN',
    'Iowa': 'IA',
    'Kansas': 'KS',
    'Kentucky': 'KY',
    'Louisiana': 'LA',
    'Maine': 'ME',
    'Maryland': 'MD',
    'Massachusetts': 'MA',
    'Michigan': 'MI',
    'Minnesota': 'MN',
    'Mississippi': 'MS',
    'Missouri': 'MO',
    'Montana': 'MT',
    'Nebraska': 'NE',
    'Nevada': 'NV',
    'New Hampshire': 'NH',
    'New Jersey': 'NJ',
    'New Mexico': 'NM',
    'New York': 'NY',
    'North Carolina': 'NC',
    'North Dakota': 'ND',
    'Ohio': 'OH',
    'Oklahoma': 'OK',
    'Oregon': 'OR',
    'Pennsylvania': 'PA',
    'Rhode Island': 'RI',
    'South Carolina': 'SC',
    'South Dakota': 'SD',
    'Tennessee': 'TN',
    'Texas': 'TX',
    'Utah': 'UT',
    'Vermont': 'VT',
    'Virginia': 'VA',
    'Washington': 'WA',
    'West Virginia': 'WV',
    'Wisconsin': 'WI',
    'Wyoming': 'WY',
}


def list_with_yelp(eatstreet_options):
    """Gets list of restaurants that will deliver to user - lists yelp rating

       Args: From get_restaurant_list in eatstreet - have list of tuples
             with restaurant names and addresses.

       Function loops over tuples and gets Yelp rating for each restaurant.

       Returns list of tuples showing restaurant names and Yelp ratings."""

    restaurant_list = []

    for restaurant in eatstreet_options:

        restaurant_name = restaurant[0]
        restaurant_address = restaurant[1]
        yelp_rating = get_yelp_rating(restaurant_name, restaurant_address)
        restaurant_list.append((restaurant_name, yelp_rating))

    return restaurant_list
