"""Models and database functions for Hangry project"""

from flask_sqlalchemy import SQLAlchemy
from helper_functions import ADDRESS_FORMAT

# data-model.py connects to PostgreSQL database through flask-sqlalchemy
# only table/class is User

db = SQLAlchemy()


class User(db.Model):
    """User of Hangry website."""

    __tablename__ = "users"

    user_id = db.Column(db.Integer,
                        autoincrement=True,
                        primary_key=True)
    username = db.Column(db.String(25), nullable=False)
    email = db.Column(db.String(64), nullable=False)
    password = db.Column(db.String(15), nullable=False)
    st_address = db.Column(db.String(64), nullable=False)
    city = db.Column(db.String(45), nullable=False)
    state = db.Column(db.String(2), nullable=False)
    zipcode = db.Column(db.String(5), nullable=False)
    fav_cuisine = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        """Provide representation of User when printed."""

        return "<User user_id={} username={}>".format(self.user_id,
                                                      self.username)

    # return formatted address for use in API calls
    def get_full_address(self):
        """Concatenates st_address, city, state, zipcode.
           Returns full address for user"""

        address = self.st_address
        city = self.city
        state = self.state
        zipcode = self.zipcode

        full_address = ADDRESS_FORMAT.format(address, city, state, zipcode)

        return full_address


def create_example_data():
    """Creates sample data for use in tests.py."""

    # Delete existing sample data in case this function runs more than once
    User.query.delete()

    # add sample users to test database
    dopey = User(username="dopey", email="dopey@dwarves.com", password="abc123",
                 st_address="450 Sutter", city="San Francisco", state="CA",
                 zipcode="94108", fav_cuisine="pizza")
    happy = User(username="happy", email="happy@dwarves.com", password="123abc",
                 st_address="450 Sutter", city="San Francisco", state="CA",
                 zipcode="94108", fav_cuisine="sushi")
    grumpy = User(username="grumpy", email="grumpy@dwarves.com", password="cats",
                  st_address="450 Sutter", city="San Francisco", state="CA",
                  zipcode="94108", fav_cuisine="Indian")

    db.session.add_all([dopey, happy, grumpy])
    db.session.commit()


def connect_to_db(app, db_uri="postgresql:///hangry"):
    """Connect the database to Hangry Flask app."""

    # Configure to use PostgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = db_uri
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from hangry_server import app
    connect_to_db(app)
    print "Connected to DB."
