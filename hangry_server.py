"""Server holds routes for Flask app."""

from flask import Flask, jsonify, render_template
from flask import redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from data_model import connect_to_db, db, User
from eatstreet import search_eatstreet, get_restaurant_list
from yelp import get_yelp_rating


app = Flask(__name__)

app.secret_key = "ABCD"  # need to create secret key & fill this in

ADDRESS_FORMAT = "{} {}, {} {}"
COMMON_SEARCH_TERMS = ["Pizza", "Sandwiches", "Italian", "Sushi", "Chinese",
                       "Burgers", "Wings", "Indian", "Mexican", "Desserts",
                       "Thai", "Salads"]
US_STATES = us_state_abbrev = {
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


@app.route("/")
def homepage():
    """Homepage shows user login or acct creation link."""

    if "user_id" in session:

        user_id = session["user_id"]
        user = User.query.get(user_id)

        return render_template("homepage.html",
                               user=user,)

    else:

        return render_template("homepage.html")


@app.route("/create-account")
def show_acct_form():
    """Display form to create Hangry account."""

    return render_template("create-account.html",
                           all_states=US_STATES,)


@app.route("/create-account", methods=["POST"])
def create_acct():
    """Sends user's account creation form to database.

    Checks database for existing user with same email
    If user exists, prompts user to login
    If user does not exist, creates new user & adds to database."""

    username = request.form.get("username")
    email = request.form.get("email")
    password = request.form.get("password")
    st_address = request.form.get("st_address")
    city = request.form.get("city")
    state = request.form.get("state")
    zipcode = request.form.get("zipcode")
    cuisine = request.form.get("cuisine")

    existing_user = User.query.filter(User.email == email).first()

    if not existing_user:

        new_user = User(username=username,
                        email=email,
                        password=password,
                        st_address=st_address,
                        city=city,
                        state=state,
                        zipcode=zipcode,
                        fav_cuisine=cuisine,)

        db.session.add(new_user)
        db.session.commit()

        session["user_id"] = new_user.user_id

        flash("You successfully created an account, start your search below!")
        return redirect("/profile/{}".format(new_user.user_id))

    else:
        flash("That e-mail address is already in use!  Login at our homepage or try a different email.")
        return redirect("/create-account")


@app.route("/update-account", methods=["GET"])
def show_update_form():
    """Shows user form to update account info."""

    return render_template("update-account.html")


@app.route("/update-account", methods=["POST"])
def update_user_info():
    """Changes user's profile DB to reflect info from form."""

    user_id = session["user_id"]
    user = User.query.get(user_id)

    user.user_id = user.user_id
    user.username = request.form.get("username")
    user.email = request.form.get("email")
    user.password = user.password
    user.st_address = request.form.get("address")
    user.city = request.form.get("city")
    user.state = request.form.get("state")
    user.zipcode = request.form.get("zipcode")
    user.fav_cuisine = request.form.get("cuisine")

    db.session.commit()

    full_address = ADDRESS_FORMAT.format(user.st_address,
                                         user.city,
                                         user.state,
                                         user.zipcode)

    return render_template("profile.html",
                           user=user,
                           address=full_address,
                           all_states=US_STATES,)


@app.route("/profile/<int:user_id>")
def show_user(user_id):
    """Shows user's profile page."""

    if "user_id" not in session:

        flash("You need to login to see your profile page.")

        return redirect("/")

    elif session["user_id"] != user_id:

        flash("Woops!  You don't have access to that page.")

        return redirect("/")

    else:

        user = User.query.get(user_id)
        address = user.st_address
        city = user.city
        state = user.state
        zipcode = user.zipcode
        full_address = ADDRESS_FORMAT.format(address, city, state, zipcode)

        return render_template("profile.html",
                               user=user,
                               address=full_address,
                               all_states=US_STATES,)


# @app.route("/search")
# def search():
#     """Display search form - search by cuisine or restaurant name."""

#     pass

# may or may not need search route - search form currently on home and prof page


@app.route("/search-results")
def show_results():
    """Show results of user's search - factor in user location."""

    search_term = request.args.get("search")
    user_id = session["user_id"]
    user = User.query.get(user_id)
    address = user.st_address
    city = user.city
    state = user.state
    zipcode = user.zipcode
    full_address = ADDRESS_FORMAT.format(address, city, state, zipcode)

    eatstreet_json = search_eatstreet(search_term, full_address)
    eatstreet_options = get_restaurant_list(eatstreet_json)

    restaurant_list = []

    for restaurant in eatstreet_options:
        restaurant_name = restaurant[0]
        restaurant_address = restaurant[1]
        yelp_rating = get_yelp_rating(restaurant_name, restaurant_address)
        restaurant_list.append((restaurant_name, yelp_rating))

    return render_template("search-results.html",
                           search_term=search_term,
                           user=user,
                           restaurant_list=restaurant_list,
                           cuisines=COMMON_SEARCH_TERMS,)


@app.route("/login", methods=["POST"])
def log_user_in():
    """Logs user into account based on form input."""

    email = request.form.get("email")
    form_password = request.form.get("password")

    existing_user = User.query.filter(User.email == email).first()
    user_id = existing_user.user_id

    if not existing_user:

        flash("You must create an account first")
        return redirect("/")

    else:

        user_password = existing_user.password

        if form_password != user_password:

            flash("The password you entered does not match your account")
            return redirect("/")

        else:

            session["user_id"] = user_id

            flash("You've successfully logged in")
            return redirect("/profile/{}".format(user_id))


@app.route("/logout")
def logout():
    """Log user out"""

    del session["user_id"]
    flash("You've logged out, but we'll be here next time you're Hangry.")
    return redirect("/")


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # DebugToolbarExtension(app)

    app.run(port=5000, host="0.0.0.0")
