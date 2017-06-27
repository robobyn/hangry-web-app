"""Models and database functions for Hangry project"""

from flask_sqlalchemy import SQLalchemy

# data-model.py connects to PostgreSQL database through flask-sqlalchemy
# tables/classes include User, Cuisine, and Delivery Services
# Upon account creation User chooses favorite cuisine type - will be foreign
# key that references Cuisines table - Delivery Services is independent of
# other 2 tables/classes

db = SQLalchemy()


class Cuisine(db.Model):
    """Type of cuisine available for User to search or favorite."""

    __tablename__ = "cuisines"

    cuisine_id = db.Column(db.Integer,
                           autoincrement=True,
                           primary_key=True)
    cuisine_name = db.Column(db.String(30), nullable=False)


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
    fav_cuisine = db.Column(db.Integer,
                            db.ForeignKey("cuisines.cuisine_id"),
                            nullable=True)

    def __repr__(self):
        """Provide representation of User when printed."""

        return "<User user_id={} username={}".format(self.user_id,
                                                     self.username)


def connect_to_db(app):
    """Connect the database to Hangry Flask app."""

    # Configure to use PostgreSQL database
    app.config["SQLALCHEMY_DATABASE_URI"] = "postgresql:///hangry"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
    db.app = app
    db.init_app(app)

