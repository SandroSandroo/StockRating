"""User model tests."""

# run these tests like:
#
#    python -m unittest test_model.py
import os
from app import app
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Watchlist, TickersInWatchlist




# create a new TEST DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///StockRatingDB_test"
app.config['SQLALCHEMY_ECHO'] = False
# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True


db.create_all()

class UserModelTestCase(TestCase):

    """ Create test client, add sample data. """

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()

        u1 = User.register("fname_test1", "lname_test1", "email1@email.com", "user_test1", "password")
        uid1 = 1111
        u1.id = uid1

        u2 = User.register("fname_test2", "lname_test2", "email2@email.com", "user_test2", "password")
        uid2 = 2222
        u2.id = uid2

        db.session.commit()

        u1 = User.query.get(uid1)
        u2 = User.query.get(uid2)

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.client = app.test_client()

    def tearDown(self):
        res = super().tearDown()
        db.session.rollback()
        return res


    def test_user_model(self):
        """Does basic model work?"""

        u = User(
            first_name="test",
            last_name="testing",
            email="test@test.com",
            username="testuser",
            password="HASHED_PASSWORD"
        )

        db.session.add(u)
        db.session.commit()

        # User should have no Watchlist
        self.assertEqual(len(u.Watchlist), 0)
        
       
    def test_valid_register(self):
        u_test = User.register("pele","pelepele", "testtest@test.com", "forward", "password")
        uid = 99999
        u_test.id = uid
        db.session.commit()

        u_test = User.query.get(uid)
        self.assertIsNotNone(u_test)
        self.assertEqual(u_test.username, "forward")
        self.assertEqual(u_test.email, "testtest@test.com")
        self.assertNotEqual(u_test.password, "password")
        # Bcrypt strings should start with $2b$
        self.assertTrue(u_test.password.startswith("$2b$"))


    def test_invalid_username_register(self):
        invalid = User.register("pele", "pelepele", "test@test.com", None, "password")
        uid = 123456789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()


    def test_invalid_email_register(self):
        invalid = User.register("pele", "pelepele", None, "goal", "password")
        uid = 123789
        invalid.id = uid
        with self.assertRaises(exc.IntegrityError) as context:
            db.session.commit()
    

    def test_invalid_password_register(self):
        with self.assertRaises(ValueError) as context:
            User.register("pele", "pelepele", "test@test.com", "goal", "")
        
        with self.assertRaises(ValueError) as context:
            User.register("pele", "pelepele", "test@test.com", "goal", None)


    def test_valid_authentication(self):
        u = User.authenticate(self.u1.username, "password")
        self.assertIsNotNone(u)
        self.assertEqual(u.id, self.uid1)
    
    def test_invalid_username(self):
        self.assertFalse(User.authenticate("badusername", "password"))

    def test_wrong_password(self):
        self.assertFalse(User.authenticate(self.u1.username, "badpassword"))

