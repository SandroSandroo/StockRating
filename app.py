from crypt import methods
from distutils.log import ERROR
from lib2to3 import refactor
import os
import re
from urllib.error import HTTPError
from flask import Flask, render_template, request, flash, redirect, session, g

from helpers import APIFunctions



from flask_debugtoolbar import DebugToolbarExtension
from sqlalchemy.exc import IntegrityError, InvalidRequestError
from sqlalchemy.orm import query
from werkzeug.wrappers import response

from forms import RegisterForm, LoginForm, UserEditForm, WatchlistForm, NewTickerForWatchlisForm
from models import db, connect_db, User, Ticker, Watchlist, TickersInWatchlist




CURR_USER_KEY = "curr_user"

app = Flask(__name__)

# Get DB_URI from environ variable (useful for production/testing) or,
# if not set there, use development local db.


app.config['SQLALCHEMY_DATABASE_URI'] = os.environ.get(
               'DATABASE_URL', 'postgres:///investStockRaiting_DB').replace("://", "ql://", 1)

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['DEBUG_TB_INTERCEPT_REDIRECTS'] = False
app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', "it's a secret")

app.debug = False
toolbar = DebugToolbarExtension(app)


connect_db(app)


# #################### TO DO BEFORE REQUEST ####################


@app.before_request
def add_user_to_g():
    """If we're logged in, add curr user to Flask global."""

    if CURR_USER_KEY in session:
        g.user = User.query.get(session[CURR_USER_KEY])

    else:
        g.user = None


def do_login(user):
    """Log in user."""

    session[CURR_USER_KEY] = user.id


def do_logout():
    """Logout user."""

    if CURR_USER_KEY in session:
        del session[CURR_USER_KEY]


#==================================================================
#                           USER ROUTES
#==================================================================

# ################### SIGN UP FORM ####################

@app.route('/register', methods=["GET", "POST"])
def register():
    """Handle user signup.

    Create new user and add to DB. Redirect to home page.

    If form not valid, present form.

    If the there already is a user with that username: flash message
    and re-present form.
    """

    form = RegisterForm()

    if form.validate_on_submit():
        try:
            user = User.register(
                first_name = form.first_name.data,
                last_name = form.last_name.data,
                email=form.email.data,
                username=form.username.data,
                password=form.password.data,
               
            )
            db.session.commit()

        except IntegrityError:
            flash("Username already taken", 'danger')
            return render_template('users/register.html', form=form)

        do_login(user)

        return redirect("/")

    else:
        return render_template('users/register.html', form=form)

    

@app.route('/login', methods=["GET", "POST"])
def login():
    """Handle user login."""

    form = LoginForm()

    if form.validate_on_submit():
        user = User.authenticate(form.username.data,
                                 form.password.data)

        if user:
            do_login(user)
            return redirect("/")

        flash('Invalid credentials', 'danger')

    return render_template('users/login.html', form=form)


@app.route('/logout')
def logout():
    """Handle logout of user."""
    do_logout()

    return redirect("/login")




######## user route ##########


@app.route('/users/<int:user_id>')
def show_user(user_id):
    """ show user profile"""

    user=User.query.get_or_404(user_id)

    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")

    if g.user:
        
        return render_template("users/profile.html", user=user)

    else:

        flash("Invalid credentials.", 'danger')

        return redirect('/')


@app.route('/users/<int:user_id>/edit', methods=["GET", "POST"])
def update_profile(user_id):
    """Update profile for current user."""
    
    user = User.query.get_or_404(user_id)

   
    form = UserEditForm(obj=user)
    
    if not user:
        flash("User does not exist.", "danger")
        return redirect('/')
   
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect("/")
    

    if g.user.id == user.id:

        if form.validate_on_submit():

            user.first_name = form.first_name.data
            user.last_name= form.last_name.data
            user.email = form.email.data 

            db.session.commit()
        
            return redirect(f"/users/{user.id}")


    return render_template('users/edit.html', form=form, user=user.id)    


@app.route('/users/<int:user_id>/delete', methods=["POST"])
def delete_profile(user_id):
    """Deletes profile of signed in user."""

    user = User.query.get_or_404(user_id)
    watchlist = Watchlist.query.filter(Watchlist.user_id == user.id).all()

    if not user:
        flash("User does not exist.", "danger")
        return redirect('/')
    
    if not g.user:
        flash("Access unauthorized.", "danger")
        return redirect('/')

    if g.user and g.user.id == user.id:
        do_logout()

        db.session.delete(g.user)
        for w in watchlist:
            db.session.delete(w)
        db.session.commit()

        flash("You have successfully deleted your account.", "success")
        return redirect('/')



#==================================================================
#                           VIEW ROUTES
#==================================================================

 #############  watchlist ############### 

@app.route('/watchlist/create', methods = ["GET", "POST"])
def create_watchlist():
     
    """ create watchlist (kind of portfolio)"""

    form = WatchlistForm()

    if g.user:
    
        if form.validate_on_submit():

            name = form.name.data
            description = form.description.data
            new_watchlist = Watchlist(name=name, description=description, user_id=g.user.id)

            db.session.add(new_watchlist)
            db.session.commit()
            return redirect('/watchlist')
    
    return render_template('tickers/new_watchlist.html', form=form)


@app.route('/watchlist')
def show_watchlist():

    """ show watchlist"""
    watchlist = Watchlist.query.filter(Watchlist.user_id == g.user.id).all()
    

    return render_template("tickers/watchlist.html", watchlist=watchlist)


@app.route('/watchlist/<int:watchlist_id>')
def watchlist_detailsn(watchlist_id):

    """show watchlist details"""
    watchlist_id = Watchlist.query.get_or_404(watchlist_id)
    
    return render_template("tickers/watchlist_detail.html", watchlist_id=watchlist_id)


@app.route('/watchlist/<int:watchlist_id>/delete', methods=["POST"])
def delete_watchlist(watchlist_id):
    """delete watchlist by id"""

    watchlist_id = Watchlist.query.get_or_404(watchlist_id)

    if g.user:

        try:
            db.session.delete(watchlist_id)
            db.session.commit()
            return redirect('/watchlist')
        

        except Exception:
            flash("Can not delate")
            return redirect('/watchlist')



#==================================================================
#                           SEARCH TICKER ROUTES
#==================================================================

############## search compnay ticker ###############


@app.route('/search', methods = ["GET", "POST"])
def search_company():

    """company Search form. On submit, 
        API is called and response is returned in JSON format, 
        company information"""
   
    s = request.args.get("query", type=str)
    
    """ Tickers on the NYSE range from one to five characters long! """
    if s is None or len(s)>5:
        flash("pleas enter valid company Symbol", "danger")
        return render_template("error.html") 

    else:
        try:
            search_query = str(s).strip().upper()
            obj = APIFunctions()

            """ call method get_ticker()"""   
            data = obj.get_ticker(search_query) 
            
            """ call method get_rating and loop data"""
            dataRating = obj.get_rating(search_query)
            
            """ call method get_statement """
            st = obj.get_statement(search_query)
            
            if data and dataRating and st == None :
                flash("API response ERROR (under CONSTRUCTION sorry)", "danger")
                return redirect("/")
                
            else:
                for c in dataRating:
                    ratingScore = c.get("ratingScore")
                    rating = c.get("rating")
                    ratingRecommendation = c.get("ratingRecommendation")
                
                """ add simbol in DB if ther is no curr symbol """
                
                symbol = data.get("symbol")
                ticker = Ticker.query.all()
            
                symbol_in_DB = [t.name for t in ticker]
            
                if symbol not in symbol_in_DB:

                    add_ticker = Ticker(name=symbol)
                    db.session.add(add_ticker)
                    db.session.commit()
           
                curr_ticker = Ticker.query.filter_by(name=symbol).first()    

            return render_template("tickers/ticker.html", data=data, ratingScore=ratingScore, rating=rating, 
                                                          ratingRecommendation=ratingRecommendation, st=st, curr_ticker=curr_ticker)

        except (ValueError, TypeError, IntegrityError, AttributeError ):
            flash(" ERROR company symbol does not exist", 'danger')
            return redirect('/')


############## search ticker by id from DB ###############    
@app.route('/search/<int:ticker_id>')
def search_ticker(ticker_id):
    """serach ticker from watchlist"""

    ticker_id = Ticker.query.get_or_404(ticker_id)
    try: 
        obj = APIFunctions()

        """ call method get_ticker()"""   
        data = obj.get_ticker(ticker_id.name) 
            
        """ call method get_rating and loop data"""
        dataRating = obj.get_rating(ticker_id.name)
        for c in dataRating:

            ratingScore = c.get("ratingScore")
            rating = c.get("rating")
            ratingRecommendation = c.get("ratingRecommendation")

        """ call method get_statement """
        st = obj.get_statement(ticker_id.name)
        symbol = data.get("symbol")
        curr_ticker = Ticker.query.filter_by(name=symbol).first()  

        return render_template("tickers/ticker.html", data=data, ratingScore=ratingScore, rating=rating, 
                                                          ratingRecommendation=ratingRecommendation, st=st, curr_ticker=curr_ticker)

    except (ValueError, TypeError, IntegrityError, AttributeError):

        flash("company symbol does not exist", 'danger')
        return redirect('/')       




############## add ticker in watchlist  ###############

@app.route('/watchlist_choose/<int:ticker_id>')
def choose_ticker(ticker_id):
    """ display watchlist where user wants to add ticker"""

    tickerid = Ticker.query.get_or_404(ticker_id)
    watchlist = Watchlist.query.filter(Watchlist.user_id == g.user.id).all()
    

    return render_template("tickers/watchlist_ticker_id.html", watchlist=watchlist, tickerid=tickerid)


@app.route('/watchlist_choose/<int:ticker_id>/<int:watchlist_id>')
def add_ticker(ticker_id, watchlist_id):
    """ add ticker in watchlist """

    t_id = Ticker.query.get_or_404(ticker_id)
    w_id = Watchlist.query.get_or_404(watchlist_id)
     
    
    watchlist_ticker = TickersInWatchlist(symbol_id=t_id.id,
                                  watchlist_id=w_id.id)
    db.session.add(watchlist_ticker)
    db.session.commit()

    return redirect(f"/watchlist/{watchlist_id}")



@app.route('/watchlist/<int:watchlist_id>/add_ticker', methods=["GET", "POST"])
def add_in_watchlist(watchlist_id): 
    """ add more ticker from DB"""
    
    watchlist = Watchlist.query.get_or_404(watchlist_id)
    form = NewTickerForWatchlisForm()
    
    ticker_on_watchlist = [s.id for s in watchlist.tickers]
    tickers = Ticker.query.filter(Ticker.id.notin_(ticker_on_watchlist)).all()
    form.ticker.choices = [(x.id, x.name) for x in tickers ]
   
    
    if form.validate_on_submit():
        
        watchlist_ticker = TickersInWatchlist(symbol_id=form.ticker.data,
                                  watchlist_id=watchlist_id)
        db.session.add(watchlist_ticker)
        db.session.commit()

        return redirect(f"/watchlist/{watchlist_id}")

    return render_template("/tickers/add_ticker_to_watchlist.html", watchlist=watchlist, form=form)    




#==================================================================
#                           HOME ROUTE
#==================================================================
####### home route ###########

@app.route('/')
def homepage():
    """Show homepage."""
    
    if g.user:
        
        obj = APIFunctions()
        """ show gainer"""
        try:
            data_gainer = obj.get_most_gainers()
            data_active = obj.get_most_actives()
            data_loser = obj.get_most_losers()
            
            if data_gainer == None or data_active == None or data_loser == None:
                return render_template("error.html")
            else:
                """ show gainer"""  
                gainer = data_gainer.get('mostGainerStock')
                """ show active"""
                active = data_active.get('mostActiveStock')
                """ show loser"""
                loser = data_loser.get('mostLoserStock')
                return render_template("home.html",gainer=gainer, active=active, loser=loser)
       
        except(HTTPError):
            return render_template("error.html")
        
    return render_template("base.html")







     
   
    



