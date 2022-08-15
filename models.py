from time import time
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin
from flask import Flask
#Configure App
app = Flask(__name__, static_folder="StaticFiles", template_folder="templates")
app.secret_key = 'replace later'
file = open("password.txt")
passwordString=file.read()
file.close()
connString = 'postgresql+psycopg2://postgres:' + passwordString + '@localhost:5432/MeetingMinutes'
# creating connection Object which will contain SQL Server Connection    

#confiure databs

app.config['SQLALCHEMY_DATABASE_URI']= connString
db = SQLAlchemy(app)



#info we want to store in database from reg page,
#username, password - saving password in plane text,
# not good for security in future ! 

#define the class 
#inherit from the model SQL database

#first property of the class is the name of the table
class User(db.Model, UserMixin):
    """User model"""
    __tablename__='users' #each collum in data base is a property of class users
    id = db.Column(db.Integer, primary_key =True)
    username =  db.Column (db.String(25), unique=True,nullable=False) #string,25 characters, unique so no duplicate usernames, and field cant be empty.
    password = db.Column (db.String(), nullable=False)
    
class MinuteTake(db.Model): 
    """"Minute Model"""
    __tablename__='minutetaker' #table created as minutetaker
    __table_args__ = {'quote': False, 'extend_existing': True}
    userid = db.Column(db.Integer, db.ForeignKey ("users.id"))
    id = db.Column(db.Integer, primary_key=True)
    timestamp =  db.Column (db.Integer, nullable=False)
    topic = db.Column (db.String(100), nullable=False)
    raisedby = db.Column (db.String(25), nullable=False)
    actionsrequired = db.Column (db.String(150), nullable=False)
    tobeactionedby = db.Column (db.String(50), nullable=False)
    subsequentinformation = db.Column (db.String(100))
    dateofcompletion = db.Column (db.Integer, nullable=False)
    absent = db.Column (db.Integer, nullable=False)

#the above code is the collums in my database, the numbers in the () = the amount of characters allowed. nullable = cannot be empty
