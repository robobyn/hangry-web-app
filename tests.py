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

        result = self.client.post("/login",
                                  data={"email": "dopey@dwarves.com",
                                        "password": "abc123"},
                                  follow_redirects=True)
        self.assertIn("Not sure what you want?", result.data)


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

    def test_profile_page(self):
        """Test that user cannot see profile pages while logged out."""

        result = self.client.get("/profile/1", follow_redirects=True)
        self.assertIn("You need to login to see your profile page", result.data)
        self.assertNotIn("Not sure what you want?", result.data)


if __name__ == "__main__":
    import unittest

    unittest.main()
