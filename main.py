from datetime import datetime
from flask import Flask, render_template,redirect, url_for, flash
from wtform_fields import RegistrationForm,LoginForm,Exit,MinuteTake,MinuteTakerForm
from flask_sqlalchemy import SQLAlchemy
from flask_login import  login_user, LoginManager, login_required, current_user
import pypyodbc
from models import *

#importing all required imports from downloaded packages. 

#bind with the server at the beginning:
login_manager = LoginManager()
login_manager.init_app(app)
#define login_view: tell Flask the URL of the landing that we are dealing with
login_manager.login_view = 'login'

#By specifying user_loader, we can query who the current login user is.In this way, we will judge whether the user can login or not.
@login_manager.user_loader
def load_user(user_id):
   return User.query.filter_by(id=user_id).first()


#creating app route for sign up user
@app.route("/", methods=['GET', 'POST'])
@app.route ("/index", methods=['GET', 'POST'])
def index():
 #getting function from models.py
   reg_form = RegistrationForm()

   #update database if successful reg

   if reg_form.validate_on_submit():
      username = reg_form.username.data
      password = reg_form.password.data

   #add user to db
      
      user = User (username=username, password=password)
      db.session.add(user)
      db.session.commit()

      return redirect(url_for('login'))

   return render_template("index.html", form=reg_form)
#refresh the page and take us to index

@app.route ("/login", methods=['GET', 'POST'])

def login():

   login_form = LoginForm()

   if login_form.validate_on_submit():
      user_object = User.query.filter_by(username=login_form.username.data).first() #ensure login details are correct
      if user_object is None:
         flash('wrong username')
      elif login_form.password.data != user_object.password: #password incorrect
         flash('incorrect password')
      else: 
         login_user(user_object)
         flash ('logged in :) ') #log in user

         return redirect (url_for('home'))
   return render_template("login.html", form=login_form)
#render_template is a Flask function from the flask.templating package.
#render_template is used to generate output from a template file based on the Jinja2 engine that is found in the application's templates folder.


@app.route ("/exit", methods=['GET', 'POST'])
@login_required
def exit():

   exit_form = Exit()

   
   return render_template("login.html", form=exit_form)
#returns user to login

@app.route ('/deleteminute/<int:id>', methods = ['POST','GET']) #<int:id = the minutes id from the database
def delete(id):
   record = MinuteTake.query.filter_by(id=id).first()
   db.session.delete(record)
   db.session.commit() #commit changes
   return redirect (url_for('home'))
#deletes the data from the db

@app.route ("/home", methods=['GET', 'POST'])
@login_required
def home():
   minute_form = MinuteTakerForm()
   #update database if successful 

   if minute_form.validate_on_submit(): 
      datetime = minute_form.datetime.data
      topic = minute_form.topic.data
      raisedby = minute_form.raisedby.data
      actionsrequired = minute_form.actionsrequired.data
      tobeactionedby = minute_form.tobeactionedby.data
      subsequentinformation = minute_form.subsequentinformation.data
      dateofcompletion = minute_form.dateofcompletion.data
      absent = minute_form.absent.data

   #add minutes to db
      
      minutetaker = MinuteTake (timestamp=datetime,topic=topic, raisedby=raisedby, 
      actionsrequired=actionsrequired, tobeactionedby=tobeactionedby,subsequentinformation=subsequentinformation,
      dateofcompletion=dateofcompletion, absent=absent, userid=current_user.id)
      db.session.add(minutetaker) #add the information to the db
      db.session.commit() #comit changes


      return redirect(url_for('home')) #refresh page and clear the table
   if current_user:
      currentUser = current_user 
   else:
      currentUser = None
   
   minutesList = MinuteTake.query.filter_by(userid=currentUser.id) #filtering the id
   return render_template("home.html", form=minute_form, current_user=current_user,minutesList=minutesList) 
   #return to home


if __name__ == "__main__":
   app.run(host='0.0.0.0',port=81)
 #deploy app on local host on port 81  