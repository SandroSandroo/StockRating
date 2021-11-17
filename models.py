"""SQLAlchemy models for inveRai$ting."""


from enum import unique

from flask_bcrypt import Bcrypt
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import backref

from datetime import datetime

bcrypt = Bcrypt()
db = SQLAlchemy()


class User(db.Model):
    """User in the system."""

    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True)

    first_name = db.Column(db.Text, nullable=False)

    last_name = db.Column(db.Text, nullable=False)

    email = db.Column(db.Text, nullable=False, unique=True)

    username = db.Column(db.Text, nullable=False, unique=True)

    password = db.Column(db.Text, nullable=False)


    ########## relationship ###########
    
    Watchlist = db.relationship('Watchlist')


    ########## methods #########

    def __repr__(self):
        return f"<User #{self.id}: {self.username}, {self.email}>"
    


    ######### class methods ##########

    @classmethod
    def register(cls, first_name, last_name,  email, username, password ):
        """Sign up user.

        Hashes password and adds user to system.
        """
        hashed = bcrypt.generate_password_hash(password).decode("utf8")

        user = User(

            first_name=first_name,
            last_name=last_name,
            email=email,
            username=username,
            password=hashed
            
        )

        db.session.add(user)
        return user

    @classmethod
    def authenticate(cls, username, password):
        """Validate that user exists & password is correct.

        Return user if valid; else return False.
        """

        user = cls.query.filter_by(username=username).first()

        if user:
            is_auth = bcrypt.check_password_hash(user.password, password)
            if is_auth:
                return user

        return False


""" class for company stock symbol"""

class Ticker(db.Model):
    """ tickers in the systems """
    __tablename__ = 'ticker'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    name = db.Column(
        db.String,
        nullable=False
     )


""" class for castum made watchlists """

class Watchlist(db.Model):
     """A watchlists in the system."""

     __tablename__ = 'watchlist'

     id = db.Column(
        db.Integer,
        primary_key=True
     )

     name = db.Column(
        db.String,
        nullable=False
     )

     description = db.Column(
        db.String,
        nullable=False
     )   

     user_id = db.Column(
         db.Integer,
         db.ForeignKey('users.id', ondelete='CASCADE'),
         nullable=False
     )

     user = db.relationship('User')
     tickers = db.relationship('Ticker', secondary='tickersinwatchlist', backref="watchlist")



""" class for symbols add in watchlist """

class TickersInWatchlist(db.Model):
    
    """An individual watchlist."""

    __tablename__ = 'tickersinwatchlist'

    id = db.Column(
        db.Integer,
        primary_key=True
    )

    symbol_id = db.Column(
        db.Integer,
        db.ForeignKey('ticker.id', ondelete='CASCADE'),
        nullable=False
    )

    watchlist_id = db.Column(
        db.Integer,
        db.ForeignKey('watchlist.id', ondelete='CASCADE'),
        nullable=False
    )
    
""" DB connector"""   

def connect_db(app):
    """Connect to database."""

    db.app = app
    db.init_app(app)

