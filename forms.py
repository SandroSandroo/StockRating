""" Forms for inveRaisting """ 

from wtforms import StringField, PasswordField, TextAreaField, SelectField
from wtforms.validators import InputRequired, Length, Email, EqualTo, DataRequired, Optional
from flask_wtf import FlaskForm


class RegisterForm(FlaskForm):
    """User registration form."""

    first_name = StringField(
        "First Name",
        validators=[InputRequired(), Length(max=45)]
        )

    last_name = StringField(
        "Last Name",
        validators=[InputRequired(), Length(max=45)]
        )

    email =  StringField(
        "Email",
        validators=[InputRequired(), Email(), Length(max=50)]
        )

    username = StringField(
        "Username",
        validators=[InputRequired(), Length(min=1, max=25)]
        )

    password = PasswordField(
        "Password", 
        validators=[InputRequired(message="Please enter a password"), 
        EqualTo('confirm', message='Passwords must match'), Length(min=6)]
        )

    confirm = PasswordField(
        'Confirm Password'
        )    



class LoginForm(FlaskForm):
    """Login form."""

    username = StringField(
        "Username",
        validators=[DataRequired()],
    )
    password = PasswordField(
        "Password",
        validators=[DataRequired()],
    )
    
    


class UserEditForm(FlaskForm):
    """ to update user info form"""

    first_name = StringField(
        "First Name",
        validators=[DataRequired(), Length(max=45)]
        )

    last_name = StringField(
        "Last Name",
        validators=[DataRequired(), Length(max=45)]
        )

    email =  StringField(
        "Email",
        validators=[DataRequired(), Email(), Length(max=50)]
        )



class WatchlistForm(FlaskForm):
    """Form for create new watchlist"""

    name = StringField('Watchlist Name', validators=[Length(min=1, max=30), InputRequired()], )
    description = TextAreaField('Watchlist Description', validators=[Length(min=1, max=55), Optional()])



class NewTickerForWatchlisForm(FlaskForm):
    """Form for adding ticker in watchlist"""

    ticker = SelectField('Add', coerce=int)
