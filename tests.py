from unittest import TestCase
from data_model import connect_to_db, db, create_example_data
from hangry_server import app
from flask import session


class FlaskTestsDatabase(TestCase):
    """Flask tests that use database from data model."""

    def setUp(self):
        """Set up test client and test db before each test."""

        self.client = app.test_client()
        app.config['TESTING'] = True

        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        create_example_data()

    def tearDown(self):
        """Tear down test client and test db when tests finish."""

        db.session.close()
        db.drop_all()

    def test_login(self):
        """Test login page."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

            result = self.client.post("/login",
                                      data={"email": "dopey@dwarves.com",
                                            "password": "abc123"},
                                      follow_redirects=True)

            self.assertIn("Not sure what you want?", result.data)
            self.assertEqual(sess["user_id"], 1)

    def test_create_account_post(self):
        """Test account creation post route for new user."""

        result = self.client.post("/create-account",
                                  data={"username": "person",
                                        "email": "person@address.com",
                                        "password": "password1",
                                        "st_address": "450 Sutter St.",
                                        "city": "San Francisco",
                                        "state": "CA",
                                        "zipcode": "94108",
                                        "cuisine": "pizza"},
                                  follow_redirects=True)

        self.assertIn("You successfully created an account", result.data)
        self.assertNotIn("That e-mail address is already in use!", result.data)

    def test_create_dup_account(self):
        """Test attempting to create duplicate acct for email already in db."""

        result = self.client.post("/create-account",
                                  data={"username": "dopey",
                                        "email": "dopey@dwarves.com",
                                        "password": "password1",
                                        "st_address": "450 Sutter St.",
                                        "city": "San Francisco",
                                        "state": "CA",
                                        "zipcode": "94108",
                                        "cuisine": "pizza"},
                                  follow_redirects=True)

        self.assertIn("That e-mail address is already in use!", result.data)
        self.assertNotIn("You successfully created an account", result.data)


class FlaskTestsLoggedOut(TestCase):
    """Flask tests with user not logged in to session."""

    def setUp(self):
        """Set up test client and test db before each test."""

        self.client = app.test_client()
        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "key"

    def test_homepage(self):
        """Test homepage while logged out."""

        result = self.client.get("/")
        self.assertIn("Login", result.data)
        self.assertNotIn("What are you craving?", result.data)

    def test_profile_page(self):
        """Test that user cannot see profile pages while logged out."""

        result = self.client.get("/profile/1", follow_redirects=True)
        self.assertIn("You need to login to see your profile page", result.data)
        self.assertNotIn("Not sure what you want?", result.data)

    def test_search_page(self):
        """Test that user cannot get to search-results page while logged out."""

        result = self.client.get("/search-results?search=sushi",
                                 follow_redirects=True)
        self.assertIn("You must be logged in to search.", result.data)
        self.assertNotIn("Get ready to eat", result.data)

    def test_create_account(self):
        """Test create account page."""

        result = self.client.get("/create-account")
        self.assertIn("Create your Account", result.data)


class FlaskTestsLoggedIn(TestCase):
    """Flask tests for pages when user logged in to session."""

    def setUp(self):
        """Set up test client and test db before each test."""

        app.config["TESTING"] = True
        app.config["SECRET_KEY"] = "key"
        self.client = app.test_client()
        connect_to_db(app, "postgresql:///testdb")

        db.create_all()
        create_example_data()

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

    def tearDown(self):
        """Tear down test client and test db when tests finish."""

        db.session.close()
        db.drop_all()

    def test_home_page(self):
        """Test homepage while user logged in."""

        result = self.client.get("/")
        self.assertIn("What are you craving?", result.data)
        self.assertNotIn("Login", result.data)

    def test_profile_page(self):
        """Test profile page while logged in."""

        result = self.client.get("/profile/1", follow_redirects=True)
        self.assertNotIn("You need to login to see your profile page",
                         result.data)
        self.assertIn("Not sure what you want?", result.data)

    def test_search_results(self):
        """Test search results while user logged in."""

        result = self.client.get("http://localhost:5000/search-results?search=sushi",
                                 follow_redirects=True)

        self.assertIn("Get ready to eat", result.data)
        self.assertNotIn("You must be logged in to search.", result.data)

    def test_update_account(self):
        """Test update-account post route."""

        result = self.client.post("/update-account",
                                  data={"username": "fancy",
                                        "email": "dopey@dwarves.com",
                                        "address": "450 Sutter St.",
                                        "city": "San Francisco",
                                        "state": "CA",
                                        "zipcode": "94108",
                                        "cuisine": "pizza"},
                                  follow_redirects=True)

        self.assertIn("successfully updated your account.", result.data)

    def test_logout(self):
        """Test logout route."""

        with self.client as c:
            with c.session_transaction() as sess:
                sess["user_id"] = 1

            result = self.client.get("/logout", follow_redirects=True)
            self.assertIn("logged out", result.data)
            self.assertNotIn("user_id", session)

    def test_cuisine_chart(self):
        """Test /cuisine-count.json route for chartJS on profile page."""

        result = self.client.get("/cuisine-count.json", follow_redirects=True)
        self.assertIn("datasets", result.data)

    def test_show_more(self):
        """Test /show-more route in hangry server."""

        result = self.client.get("/show-more",
                                 data={"name": "DJ Sushi"},
                                 follow_redirects=True)

        self.assertIn("photos", result.data)
        self.assertIn("reviews", result.data)

    def test_show_menu(self):
        """Test /show-menu route in hangry server."""

        result = self.client.get("show-menu",
                                 data={"name": "DJ Sushi"},
                                 follow_redirects=True)

        self.assertIn("menu", result.data)
        self.assertIn("items", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
