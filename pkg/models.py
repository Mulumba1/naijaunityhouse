from datetime import datetime
from sqlalchemy import Index, ForeignKeyConstraint
from flask_sqlalchemy import SQLAlchemy



db = SQLAlchemy()




class State(db.Model):
    state_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    state_name = db.Column(db.String(120),index=True, nullable=False)
    lga_id = db.relationship('Lga', backref='state', lazy=True)
    

    

class Lga(db.Model):
    lga_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    lga_name = db.Column(db.String(120),index=True, nullable=False)
    state_id = db.Column(db.Integer, db.ForeignKey('state.state_id'), nullable=False)
    




class User(db.Model):
    user_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    user_fname = db.Column(db.String(200), nullable=False)
    user_lname = db.Column(db.String(200), nullable=False)
    user_othername = db.Column(db.String(200), nullable=True)
    user_dob = db.Column(db.Date)
    user_address = db.Column(db.Text, nullable=False)
    user_phone = db.Column(db.String(20), nullable=False, unique=True)
    user_nin = db.Column(db.String(20), nullable=False, unique=True)
    user_pics = db.Column(db.String(120),nullable=True)
    user_email = db.Column(db.String(120), nullable=False, unique=True)
    user_password = db.Column(db.String(200), nullable=False)
    user_datereg = db.Column(db.DateTime(), default=datetime.utcnow)
    user_state = db.Column(db.Integer(), db.ForeignKey('state.state_id'))
    user_lga = db.Column(db.Integer, db.ForeignKey('lga.lga_id'))
    images = db.relationship('Image', backref='user_relation', lazy=True)
    userstate = db.relationship('State',backref='user', lazy=True)
    userlga = db.relationship('Lga', backref='user',lazy=True)
    user_ref = db.Column(db.String(10),nullable=False, unique=True)

    




class Image(db.Model):
    image_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    image_name = db.Column(db.String(100), nullable=False)
    user_id = db.Column(db.Integer(), db.ForeignKey('user.user_id'))  
    user = db.relationship('User', backref='users', lazy=True)


class Admin(db.Model):
    admin_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    admin_name = db.Column(db.String(100), nullable=False)
    admin_username = db.Column(db.String(100), nullable=False)
    admin_password = db.Column(db.String(100), nullable=False)
    admin_lastlogin = db.Column(db.DateTime(), default=datetime.utcnow)


class NewsletterSubscriber(db.Model):
    subscriber_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    email = db.Column(db.String(120), nullable=False, unique=True)
    date_subscribed = db.Column(db.DateTime(), default=datetime.utcnow)

class ContactUs(db.Model):
    contact_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    contact_fname = db.Column(db.String(100), nullable=False)
    contact_lname =db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    contact_phone = db.Column(db.String(20), nullable=False)
    contact_message = db.Column(db.Text, nullable=False)
    contact_date = db.Column(db.DateTime(), default=datetime.utcnow)


class Donation(db.Model):  
    donate_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    donate_amt = db.Column(db.Float,nullable=False)
    donate_date=db.Column(db.DateTime(), default=datetime.utcnow)
    donate_status = db.Column(db.Enum('pending','paid','failed'),nullable=False)
    donate_email = db.Column(db.String(120),nullable=False)
    donate_donor = db.Column(db.String(200),nullable=False)
    donate_paygate=db.Column(db.String(200), nullable=True)
    donate_ref = db.Column(db.String(200), nullable=True)
    
    
     


    
    

    






