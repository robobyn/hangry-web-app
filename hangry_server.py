"""Server holds routes for Flask app."""

from flask import Flask, jsonify, render_template
from flask import redirect, request, flash, session
from flask_debugtoolbar import DebugToolbarExtension

from data_model import connect_to_db, db, User, Cuisine


app = Flask(__name__)

app.secret_key = "ABCD"  # need to create secret key & fill this in


@app.route("/")
def homepage():
    """Homepage shows user login or acct creation link."""

    return render_template("homepage.html")


@app.route("/create-account")
def show_acct_form():
    """Display form to create Hangry account."""

    return render_template("create-account.html")


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

    existing_user = User.query.filter(User.email == email).first()

    if not existing_user:

        new_user = User(username=username,
                        email=email,
                        password=password,
                        st_address=st_address,
                        city=city,
                        state=state,
                        zipcode=zipcode)

        db.session.add(new_user)
        db.session.commit()

        flash("You successfully created an account")
        return redirect("/")

    else:
        flash("That e-mail address is already in use!  Login at the homepage or try a different email.")
        return redirect("/create-account")


@app.route("/profile")  # will need route to go to specific user page
def show_user():
    """Shows user's profile page."""

    pass


@app.route("/search")
def search():
    """Display search form - search by cuisine or restaurant name."""

    pass


@app.route("/search-results")  # need route to show results specific to search
def show_results():
    """Show results of user's search - factor in user location."""

    pass


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
            return redirect("/")


if __name__ == "__main__":

    app.debug = True
    app.jinja_env.auto_reload = app.debug

    connect_to_db(app)

    # Use the DebugToolbar
    # DebugToolbarExtension(app)  # need secret key for this to work

    app.run(port=5000, host="0.0.0.0")
