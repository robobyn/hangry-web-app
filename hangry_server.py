"""Server holds routes for Flask app."""

from flask import Flask, jsonify, render_template
from flask import redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from data_model import connect_to_db, db, User
from eatstreet import search_eatstreet, get_restaurant_list, get_cuisine_count
from eatstreet import format_chart_data, get_restaurant_details
from eatstreet import get_restaurant_menu
from yelp import get_yelp_rating, get_business_id, get_reviews, get_photos
from helper_functions import COMMON_SEARCH_TERMS, US_STATES
from helper_functions import list_with_yelp

app = Flask(__name__)

app.secret_key = "ABCD"  # need to create secret key & fill this in


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

    full_address = user.get_full_address()

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
        full_address = user.get_full_address()

        return render_template("profile.html",
                               user=user,
                               address=full_address,
                               all_states=US_STATES,)


@app.route("/cuisine-count.json")
def count_cuisines():
    """Counts number of restaurants in each category for user's address.

        Uses function get_cuisine_count from eatstreet.py - output is
        json string to be used in AJAX call to display chart on profile page."""

    user_id = session["user_id"]
    user = User.query.get(user_id)
    full_address = user.get_full_address()

    cuisine_dict = get_cuisine_count(full_address)

    formatted_dict = format_chart_data(cuisine_dict)

    return jsonify(formatted_dict)


@app.route("/search-results")
def show_results():
    """Show results of user's search - factor in user location."""

    search_term = request.args.get("search")
    user_id = session["user_id"]
    user = User.query.get(user_id)
    full_address = user.get_full_address()

    eatstreet_json = search_eatstreet(search_term, full_address)
    eatstreet_options = get_restaurant_list(eatstreet_json)
    restaurant_list = list_with_yelp(eatstreet_options)

    return render_template("search-results.html",
                           search_term=search_term,
                           user=user,
                           restaurant_list=restaurant_list,
                           cuisines=COMMON_SEARCH_TERMS,)


@app.route("/show-more")
def show_more_info():
    """Shows more info for restaurant upon clicking restaurant name.

       JSON response passes to AJAX route in forms.js"""

    restaurant = request.args.get("name")
    user_id = session["user_id"]
    user = User.query.get(user_id)
    city = user.city

    yelp_id = get_business_id(restaurant, city)
    reviews = get_reviews(yelp_id)
    photos = get_photos(yelp_id)

    response = {"status": "success", "name": restaurant, "reviews": reviews,
                "photos": photos}

    return jsonify(response)


@app.route("/show-menu")
def show_menu():
    """Shows restaurant menu on clicking restaurant's menu button."""

    restaurant = request.args.get("menuName")
    user_id = session["user_id"]
    user = User.query.get(user_id)
    city = user.city

    eatstreet_details = get_restaurant_details(restaurant, city)
    menu = get_restaurant_menu(eatstreet_details)

    response = {"status": "success", "menu": menu}

    return jsonify(response)


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
