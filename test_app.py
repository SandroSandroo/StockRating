"""app routs & watchlist tests."""

# run these tests like:
#
#    python -m unittest test_app.py
import os
from app import app, CURR_USER_KEY
from unittest import TestCase
from sqlalchemy import exc

from models import db, User, Watchlist, TickersInWatchlist, Ticker

# create a new TEST DATABASE
app.config['SQLALCHEMY_DATABASE_URI'] = "postgresql:///StockRatingDB_test"
app.config['SQLALCHEMY_ECHO'] = False
# Make Flask errors be real errors, rather than HTML pages with error info
app.config['TESTING'] = True


db.create_all()


class UserRoutsTestCase(TestCase):
    """ Create test client, add sample data. """

    def setUp(self):
        """Create test client, add sample data."""
        db.drop_all()
        db.create_all()
        

        self.client = app.test_client()

        u1 = User.register("fname_test1", "lname_test1", "email1@email.com", "user_test1", "password")
        uid1 = 111
        u1.id = uid1

        u2 = User.register("fname_test2", "lname_test2", "email2@email.com", "user_test2", "password")
        uid2 = 222
        u2.id = uid2

        test_watchlist = Watchlist(name="gainer", description="description", user_id=uid2)
        wid2 = 12
        test_watchlist.id = wid2

        test_ticker = Ticker(name="AAPL")
        tid = 199
        test_ticker.id = tid

        
        db.session.add_all([u2, u1, test_watchlist, test_ticker])
        db.session.commit()

        test_t_in_w = TickersInWatchlist(symbol_id = test_ticker.id, watchlist_id = wid2)
        twid = 5
        test_t_in_w.id = twid
        
        db.session.add(test_t_in_w)
        db.session.commit()

        self.u1 = u1
        self.uid1 = uid1

        self.u2 = u2
        self.uid2 = uid2

        self.test_watchlist = test_watchlist
        self.wid2 = wid2

        self.test_ticker = test_ticker
        self.tid = tid

        self.test_t_in_w = test_t_in_w
        self.twid = twid

        

        db.session.commit()

    def tearDown(self):
        resp = super().tearDown()
        db.session.rollback()
        return resp   

    
    def test_register_route(self):
        """Test user registeration"""
        with self.client as client:
            res = client.get('/register')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('</form>', html)


    def test_login_route(self):
        """Test login route with valid user"""
        with self.client as client:
            res = client.get('/login')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('Username', html)
            self.assertIn('<h4 class="display-2 text-center">Login</h4>', html)


    def test_login_route_no_user(self):
        """Test login route with no user"""
        with self.client as client:
            res = client.get('/login')
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h4 class="display-2 text-center">Login</h4>', html)

    # ========================= LOGOUT ROUTE =========================

    def test_logout_route(self):
        """Test logout user route"""
        with self.client as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY] = self.uid1
            res = client.get('/logout', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertNotIn(self.uid1, session)        
                           
           
    # ========================= watchlist ROUTE =========================

    def test_watchlist_route(self):
        """Test authorized favorites route"""
        with app.test_client() as client:
            with client.session_transaction() as session:
                session[CURR_USER_KEY] = self.uid2
            res = client.get('/watchlist', follow_redirects=True)
            html = res.get_data(as_text=True)

            self.assertEqual(res.status_code, 200)
            self.assertIn('<h3 class="display-4 text-center">Watchlist</h3>', html)


    def test_watchlist_details_route(self):
        """Test recipe details route"""
        with app.test_client() as client:
            res = client.get(f"/watchlist/{12}")
            

            self.assertEqual(res.status_code, 200)
            self.assertIn("gainer", str(res.data))
            self.assertIn("AAPL", str(res.data))
            self.assertNotIn("AMZN", str(res.data))
            
    # =========================  search ticker ROUTE =========================  

    def test_search_route(self):
        """Test recipe details route"""
        with app.test_client() as client:
            res = client.get(f"/search/{199}")

            self.assertEqual(res.status_code, 200)
            self.assertIn("RECOMMENDATION", str(res.data))

    # =========================  home ROUTE =========================  
    
    def test_home_route(self):
        """Test recipe details route"""
        with app.test_client() as client:
            res = client.get("/")

            self.assertEqual(res.status_code, 200)
            self.assertIn("GAINER", str(res.data))
            self.assertIn("ACTIVE", str(res.data))
            self.assertIn("LOSER", str(res.data))


    
              
                    
            




    


  