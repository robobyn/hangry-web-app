"""Models and database functions for Hangry project"""

from flask_sqlalchemy import SQLAlchemy

# data-model.py connects to PostgreSQL database through flask-sqlalchemy
# tables/classes include User, Cuisine
# Upon account creation User chooses favorite cuisine type - will be foreign
# key that references Cuisines table

db = SQLAlchemy()


# probably will delete Cuisine class from model
# may want to use if decide to track most popular user searches etc.

# class Cuisine(db.Model):
#     """Type of cuisine available for User to search or favorite."""

#     __tablename__ = "cuisines"

#     cuisine_id = db.Column(db.Integer,
#                            autoincrement=True,
#                            primary_key=True)
#     cuisine_name = db.Column(db.String(30), nullable=False)

#     def __repr__(self):
#         """Provide representation of object when printed"""

#         return "<Cuisine cuisine_id={} cuisine_name={}>".format(self.cuisine_id,
#                                                                 self.cuisine_name)


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
    city = db.Column(db.String(45), nullable=False, default="San Francisco")
    state = db.Column(db.String(2), nullable=False, default="CA")
    zipcode = db.Column(db.String(5), nullable=False)
    fav_cuisine = db.Column(db.String(30), nullable=False)

    def __repr__(self):
        """Provide representation of User when printed."""

        return "<User user_id={} username={}>".format(self.user_id,
                                                      self.username)


def connect_to_db(app):
    """Connect the database to Hangry Flask app."""

    # Configure to use PostgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///hangry"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

if __name__ == "__main__":
    # As a convenience, if we run this module interactively, it will leave
    # you in a state of being able to work with the database directly.

    from hangry_server import app
    connect_to_db(app)
    print "Connected to DB."
