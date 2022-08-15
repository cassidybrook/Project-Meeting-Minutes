from datetime import datetime
from xml.dom import ValidationErr
from flask_wtf import FlaskForm
from wtforms import TextAreaField, PasswordField, SubmitField, DateTimeField, DateField, StringField, TimeField

from wtforms.validators import InputRequired, Length, EqualTo, ValidationError

from models import User,MinuteTake

def invalid_credentials(form,field):
    """Username and password checker"""

    username_entered = form.username.data
    password_entered = field.data

    
    user_object = User.query.filter_by(username=username_entered).first()
    if user_object is None:
        raise ValidationError("Username or Password Incorrect")
    if password_entered != user_object.password:
        raise ValidationError("Username or Password Incorrect")

#valdation of username and password
#Validation in python prevents third-party users from mishandling the code accidentally or intentionally.
#Here it is being used to check if the input data type is correct or not and being used to check if there are no invalid values in the given input.




class RegistrationForm (FlaskForm):
    """ Registration Form """

    username = StringField('username_label', validators=[
        InputRequired(message="Username Required"),
        Length(min=4,max=25, message="Username must be between 4 and 25 characters")]) #creating stringfield , length 4-25 characters or wont submit and message error will appear.
    password = PasswordField('password_label', validators=[
        InputRequired(message="Password Required"),
        Length (min=4,max=25, message="Password must be between 4 and 25 characters")])
    confirm_pswd = PasswordField('confirm_pswd_label', validators=[
        InputRequired(message="Password Required"),
        EqualTo ('password', message="Passwords must match")])
    submit_button = SubmitField('Create')

    def validate_username(self, username):
        user_object = User.query.filter_by(username=username.data).first() #if username already exists this will return user object.
        if user_object:
            raise ValidationError("Username already exists. Choose another username.") #error message pop up, gives user direction.


class LoginForm(FlaskForm):
    """Login form """

    username = StringField('username_label', 
        validators=[InputRequired("Username required")])

    password = StringField ('password_label',
         validators=[InputRequired(message="Password Required"),
         invalid_credentials])
    submit_button = SubmitField('Create')

#creating validators for the login, username and password must match database to log in.


class Exit(FlaskForm):
    """exit """

class MinuteTakerForm (FlaskForm):
    """ Minute Taker Form """

    datetime = DateTimeField('date_label', validators=[
        InputRequired(message="Date Required")]) 
    topic = TextAreaField('topic_label', validators=[
        InputRequired(message="Topic Required")])
    raisedby = TextAreaField('raised_by_label', validators=[
        InputRequired(message="Raised By Required")])
    actionsrequired = TextAreaField('actions_required_by_label', validators=[
        InputRequired(message="Actions Required")])
    tobeactionedby = TextAreaField('to_be_actioned_by_label', validators=[
        InputRequired(message="To Be Actioned By Required")])
    subsequentinformation = TextAreaField('subsequent_information_label', validators=[
        InputRequired(message="Info Required")])
    dateofcompletion = DateField('date_of_completion_label', validators=[
        InputRequired(message="Date Required")])
    absent = TextAreaField ('absent_label', validators=[
        InputRequired(message="Absent Required")])
    sub_button = SubmitField('Add Minute')

#creating the validators of the minute form, and giving an error message of text required to submit to give user direction.
#these are the fields created in the minute taker DB. 
