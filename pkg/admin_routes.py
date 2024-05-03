import os, random, uuid, string
from uuid import uuid4
from datetime import datetime
from functools import wraps
from flask import render_template,request,redirect,flash,url_for,make_response,session,flash,jsonify,send_file
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
from flask_weasyprint import HTML, render_pdf  
from flask_mail import  Message
from pkg import app, mail
from pkg.models import db,State,Lga,Image,Admin,ContactUs,User,Volunteer, NewsletterSubscriber,Payment,Plan
from pkg.adminlogin_forms import AdminloginForm



def admin_login_required(f):
    @wraps(f) 
    def check_login(*args, **kwargs):
        if session.get('useronline') != None:
            return f(*args, **kwargs)
        else:
            flash('You must be logged in to access this page',category='error')
            return redirect(url_for('admin_login'))
    return check_login


@app.route('/admin/dashboard/')
@admin_login_required
def admin_dashboard():
    admin_id = session.get('useronline')
    admin = Admin.query.get(admin_id)
    return render_template('admin/admin_dashboard.html', admin=admin)

@app.route('/users/profile/')
@admin_login_required
def users_profile():
    user = User.query.all()  
    return render_template('admin/display_contestants.html', user=user)

@app.route('/contact/details/')
@admin_login_required
def contact_details():
    contact = ContactUs.query.all()  
    return render_template('admin/contact_details.html', contact=contact)

@app.route('/volunteer/details/')
@admin_login_required
def volunteer_details():
    volunteer = Volunteer.query.all()  
    return render_template('admin/display_volunteers.html', volunteer=volunteer)

@app.route('/newsletter/subscribers/')
@admin_login_required
def newsletter_subscribers():
    subscribers = NewsletterSubscriber.query.all()  
    return render_template('admin/newsletter_subscribers.html', subscribers=subscribers)

@app.route('/admin/login/', methods = ['POST','GET'])
def admin_login():
    form = AdminloginForm()
    if request.method=='POST':
        if form.validate_on_submit():
            username = form.username.data
            password = form.password.data
            data = db.session.query(Admin).filter(Admin.admin_username==username).first()
            if data:
                password= data.admin_password
                rsp = password
                if rsp:
                    id = data.admin_id
                    session['useronline'] = id
                    session['name'] = data.admin_username
                    return redirect('/admin/dashboard/')
                else:
                    flash('Invalid Login Credentials', 'error')
                    return render_template('admin/adminlogin.html',form=form)
            else:
                flash('Please enter valid credentials', 'error')
                return redirect('/admin/login/')
        else:
            return redirect('/admin/login/')   
    else:
        return render_template('admin/adminlogin.html', form=form)






@app.route("/admin/logout/")
def admin_logout():
    session.pop("useronline",None)
    return redirect("/admin/login/")

 
@app.route("/exit/")
@admin_login_required
def exit():
    return redirect("/admin/dashboard/")

@app.route('/contestants/votes/')
@admin_login_required
def contestants_votes():
    user = User.query.order_by(User.user_vote.desc()).all()  
    return render_template('admin/contestants_votes.html', user=user)

@app.route('/payment/list/')
@admin_login_required
def payment_list():
    payment = Payment.query.all()  
    return render_template('admin/payment_list.html', payment=payment)





@app.route('/contestant/search/')
def search_contestant():
    search_query = request.args.get('q')  
    users = []

    if search_query:
        users = User.query.filter(
            (User.user_ref.ilike(f'%{search_query}%')) |
            (User.user_email.ilike(f'%{search_query}%')) |
            (User.user_fname.ilike(f'%{search_query}%')) |
            (User.user_lname.ilike(f'%{search_query}%'))
        ).all()
    else:
        users = User.query.all()

    if not users:
        message = f"No contestants found with the details provided: {search_query}"
        return render_template('admin/no_contestant_found.html', message=message)

    return render_template('admin/contestant_search_result.html', users=users)



@app.route('/payment/search/')
def search_payment():
    search_query = request.args.get('q')  
    payments = []

    if search_query:
        payments = Payment.query.join(Payment.payplan).filter(
            (Plan.plan_name.ilike(f'%{search_query}%')) |
            (Payment.payment_ref.ilike(f'%{search_query}%')) |
            (Payment.payment_fname.ilike(f'%{search_query}%')) |
            (Payment.payment_lname.ilike(f'%{search_query}%'))
        ).all()
    else:
        payments = Payment.query.all()

    if not payments:
        message = f"No payment found with the details provided: {search_query}"
        return render_template('admin/no_payment_found.html', message=message)

    return render_template('admin/payment_search_result.html', payments=payments)



@app.route('/volunteer/search/')
def search_volunteer():
    search_query = request.args.get('q')  
    volunteers = []

    if search_query:
        volunteers = Volunteer.query.join(Volunteer.volstate).filter(
            (State.state_name.ilike(f'%{search_query}%')) |
            (Volunteer.volunteer_email.ilike(f'%{search_query}%')) |
            (Volunteer.volunteer_name.ilike(f'%{search_query}%'))
        ).all()
        
    else:
        volunteers = Volunteer.query.all()

    if not volunteers:
        message = f"No Volunteers found with the details provided: {search_query}"
        return render_template('admin/no_volunteers_found.html', message=message)

    return render_template('admin/volunteers_search.html', volunteers=volunteers)

