from datetime import datetime
from sqlalchemy import Index, ForeignKeyConstraint,Enum 
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
    user_phone = db.Column(db.String(20), nullable=False)
    user_bio = db.Column(db.Text, nullable=False)
    user_pics = db.Column(db.String(120),nullable=True)
    user_email = db.Column(db.String(120), nullable=False, unique=True)
    user_password = db.Column(db.String(200), nullable=False)
    user_datereg = db.Column(db.DateTime(), default=datetime.utcnow)
    user_state = db.Column(db.Integer(), db.ForeignKey('state.state_id'))
    user_lga = db.Column(db.Integer, db.ForeignKey('lga.lga_id'))
    user_vote = db.Column(db.Integer, nullable=False, default=0)
    userstate = db.relationship('State',backref='user', lazy=True)
    userlga = db.relationship('Lga', backref='user',lazy=True)
    user_ref = db.Column(db.String(10),nullable=False, unique=True)


class Volunteer(db.Model):
    volunteer_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    volunteer_name = db.Column(db.String(200), nullable=False)
    volunteer_address = db.Column(db.Text, nullable=False)
    volunteer_phone = db.Column(db.String(20), nullable=False, unique=True)
    volunteer_email = db.Column(db.String(120), nullable=False, unique=True)
    volunteer_datereg = db.Column(db.DateTime(), default=datetime.utcnow)
    volunteer_state = db.Column(db.Integer(), db.ForeignKey('state.state_id'))
    volunteer_lga = db.Column(db.Integer, db.ForeignKey('lga.lga_id'))
    volstate = db.relationship('State',backref='volunteer', lazy=True)
    vollga = db.relationship('Lga', backref='volunteer',lazy=True)

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
    contact_name = db.Column(db.String(100), nullable=False)
    contact_email = db.Column(db.String(120), nullable=False)
    contact_subject = db.Column(db.String(120), nullable=False)
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




class Plan(db.Model):
    plan_id = db.Column(db.Integer, autoincrement=True,primary_key=True)
    plan_name = db.Column(db.String(120),nullable=False)
    plan_amount = db.Column(db.Float,nullable=False)
    



PAYMENT_STATUS_PENDING = 'pending'
PAYMENT_STATUS_PAID = 'paid'
PAYMENT_STATUS_FAILED = 'failed'

class Payment(db.Model):  
    payment_id = db.Column(db.Integer, autoincrement=True, primary_key=True)
    payment_fname = db.Column(db.String(120), nullable=False)
    payment_lname = db.Column(db.String(120), nullable=False)
    payment_email = db.Column(db.String(120), nullable=False)
    payment_phone = db.Column(db.String(120), nullable=False)
    payment_plan = db.Column(db.Integer, db.ForeignKey('plan.plan_id'))
    payplan = db.relationship('Plan', backref='payment', lazy=True)
    payment_amt = db.Column(db.Float, nullable=False)
    payment_date = db.Column(db.DateTime, default=datetime.utcnow)
    payment_status = db.Column(Enum('pending', 'paid', 'failed', name='payment_status_enum'), nullable=False, default='pending')
    payment_ref = db.Column(db.String(200), nullable=True)
    payplan = db.relationship('Plan',backref='payment', lazy=True)
    

    def __init__(self, payment_fname, payment_lname, payment_email, payment_phone, payment_plan, payment_amt, payment_ref):
        self.payment_fname = payment_fname
        self.payment_lname = payment_lname
        self.payment_email = payment_email
        self.payment_phone = payment_phone
        self.payment_plan = payment_plan
        self.payment_amt = payment_amt
        self.payment_ref = payment_ref

    def mark_as_paid(self):
        self.payment_status = 'paid'

    def mark_as_failed(self):
        self.payment_status = 'failed'

    
    
     


    
    

    






