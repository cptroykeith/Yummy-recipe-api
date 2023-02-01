from sqlalchemy import Column, ForeignKey, Integer, String
from sqlalchemy import create_engine
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from sqlalchemy.orm import relationship
from app import db


class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(60))
    last_name = db.Column(db.String(60))
    email = db.Column(db.String(60), unique=True)
    password_hash = db.Column(db.String(300))
    category_id = db.Column(db.Integer, db.ForeignKey('categories.id'))
    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password
    @property
    def password(self):
        #keep password private
        raise AttributeError('password is not a readable attribute.')  
   
    @password.setter  
    def password(self, password):
       #generate password_hash
        self.password_hash = generate_password_hash(password) 
		
    def verify_password(self, password):
        #check password with password_hash
        return check_password_hash(self.password_hash, password)

    def __repr__(self):
        return '{}'.format(self.first_name)
  
    #setup user loader  
    @login_manager.user_loader
    def get_user(id):
        return User.query.get(int(id))
 
class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(60), nullable=False)
    description = db.Column(db.String(200), nullable=False)
    recipe_id=db.Column(db.Integer, ForeignKey('recipes.id'))
    user = db.relationship('User', backref='categories',
                                 lazy='dynamic')
    def __init__(self, name, description):
        self.name = name
        self.description = description
    def __repr__(self):
        return '{} {}'.format(self.name, self.description)
		
class Recipe(db.Model):
    __tablename__ = 'recipes'	
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(500), nullable=False)
    category = db.relationship('Category', backref='recipes', \
	                               lazy='dynamic')
    def __init__(self, name, description):
        self.name = name 
        self.description = description
    def __repr__(self):
        return '{}'.format(self.name)	

    #create engine to store data in local non-persistent database directory   

db.Model.metadata.bind = create_engine('sqlite:///api_db') 

db.create_all()