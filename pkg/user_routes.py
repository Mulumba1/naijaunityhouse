import os, random, uuid, string
from uuid import uuid4
from datetime import datetime,date
import requests,json
from functools import wraps
from flask import render_template,request,redirect,flash,url_for,session,flash,jsonify,send_from_directory,abort,make_response,Response,send_file
from io import BytesIO
from flask_weasyprint import HTML, render_pdf, CSS  
from werkzeug.security import generate_password_hash, check_password_hash 
from paystackapi.transaction import Transaction as PaystackTransaction
from pkg import app
from pkg.models import db,State,Lga,Image,Admin,NewsletterSubscriber,ContactUs,User,Volunteer,Donation,Payment,Plan
from pkg.contact import ContactForm
from pkg.register_forms import RegisterForm
from pkg.contestant_forms import ContestantForm
from pkg.volunteer_forms import VolunteerForm
from pkg.upload_pics import UploadForm
from pkg.payment_forms import PaymentForm
from pkg.login_forms import LoginForm
from pkg.voting_forms import VotingForm
from pkg.reset_forms import ResetForm



def payment_required(f):
    @wraps(f) 
    def check_payment(*args, **kwargs):
        if session.get('useronline') != None:
            return f(*args, **kwargs)
        else:
            flash('Please make payment to access this page',category='error')
            return redirect(url_for('payment'))
    return check_payment


def login_required(f):
    @wraps(f) 
    def check_login(*args, **kwargs):
        if session.get('useronline') != None:
            return f(*args, **kwargs)
        else:
            flash('You must be logged in to access this page',category='error')
            return redirect(url_for('login'))
    return check_login




@app.route('/')
def home():
    return render_template("user/index.html")


@app.route('/about/')
def about():
    return render_template('user/about.html')


@app.route('/contact/', methods=['POST', 'GET'])
def contact_us():
    form = ContactForm()
    contact_form = ContactForm()
    if request.method == 'POST' and form.validate_on_submit():
        name = form.name.data
        email = form.email.data
        phone = form.phone.data
        subject = form.subject.data
        message = form.message.data
        new_contact = ContactUs(contact_name=name, contact_email=email, contact_phone=phone,contact_subject=subject, contact_message=message)
        db.session.add(new_contact)
        db.session.commit()

        flash(f'Thank you {name} for contacting us. One of our representative will contact you shortly on your Email: {email}', 'success')
        return redirect('/')
    
    return render_template('user/contact.html', form = form)


@app.route('/login/', methods = ['POST','GET'])
def login():
    form = LoginForm()
    if request.method=='POST':
        if form.validate_on_submit():
            ref = form.ref.data
            password = form.password.data
            data = db.session.query(User).filter(User.user_ref==ref).first()
            if data:
                hashed_pwd= data.user_password
                rsp = check_password_hash(hashed_pwd,password)
                if rsp:
                    id = data.user_id
                    session['useronline'] = id
                    session['name'] = data.user_fname
                    return redirect('/dashboard/')
                else:
                    flash('Invalid User Ref Code or password', category='error')
                    return render_template('user/login.html',form=form)
            else:
                flash('Invalid Login email or password',  category='error')
                return redirect('/login/')
        else:
            return redirect('/login/')   
    else:
        return render_template('user/login.html', form=form)



@app.route("/logout/")
def logout():
    session.pop("useronline",None)
    return redirect("/login/")



@app.route('/reset/password/', methods=['GET', 'POST'])
def reset_password():
    form = ResetForm()
    if request.method == 'POST' and form.validate_on_submit():
        ref = form.ref.data
        new_password = form.new_password.data
        confirm_password = form.confirm_password.data
        user = User.query.filter_by(user_ref=ref).first()
        if user:
            user.user_password = generate_password_hash(new_password)
            db.session.commit()
            flash('Password reset successfully! You can now login with your new Password', 'success')
            return redirect('/') 
        else:
            flash('Invalid Reference number', 'error')
            return redirect('/reset/password/')  
    return render_template('user/reset_password.html', form=form)






@app.route('/dashboard/')
@login_required
def dashboard():
    user_id = session.get('useronline')
    user = User.query.get(user_id)
    contestant_link = url_for('voting', user_id=user_id, _external=True)
    confirm_registration_url = url_for('confirm_registration', user_id=user_id)
    return render_template('user/profile.html', user=user, contestant_link=contestant_link, user_id=user_id, confirm_registration_url=confirm_registration_url)



@app.route('/other/contestants')
@login_required
def other_contestants():
    user = User.query.order_by(User.user_vote.desc()).all()  
    return render_template('user/other_contestants.html', user=user)


@app.route("/user/exit/")
def user_exit():
    return redirect("/dashboard/")



def generate_pdf(html_content):
    pdf_bytes = HTML(string=html_content).write_pdf()
    pdf_io = BytesIO(pdf_bytes)  
    return pdf_io 




# @app.route('/checkme/')
# def checkme():
#     user = User.query.all()
#     return render_template('user/contestant_dash.html', user=user)

# @app.route('/user/checkme/')
# def checkme2():
#     user = User.query.all()
#     return render_template('user/reg_summary.html', user=user)

@app.route('/team/')
def our_team ():
    return render_template('user/team.html')


def generate_ref_number(year, serial_number):
    year_str = str(year).zfill(4)
    serial_str = str(serial_number).zfill(4)
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))
    ref_number = year_str + serial_str + letters
    return ref_number

    
@app.route('/confirmation/')
def confirm():
    return render_template('user/confirmation.html')


@app.route('/volunteer/', methods=['POST', 'GET'])
def volunteer ():
    form = VolunteerForm()
    states = db.session.query(State).all()
    form.state.choices = [(state.state_id, state.state_name) for state in State.query.all()]
    form.lga.choices = [(lga.lga_id, lga.lga_name) for lga in Lga.query.all()]
    if request.method == 'GET':
        return render_template('user/volunteer.html', states=states, form=form)
    else:
        if form.validate_on_submit():
            name = form.name.data
            email = form.email.data
            phone = form.phone.data
            address = form.address.data
            state = form.state.data
            lga = form.lga.data
            new_volunteer = Volunteer(volunteer_name=name,volunteer_address=address, volunteer_phone=phone,volunteer_email=email,volunteer_state=state, volunteer_lga=lga)
            
            db.session.add(new_volunteer)
            db.session.commit()
            flash('Registration Successful!', category='success')
            return render_template('user/confirmation.html')
    return render_template('user/volunteer.html', states=states, form=form)






# @app.route("/contestant/", methods=['POST', 'GET'])
# def register_contestant():
#     form = ContestantForm()
#     states = db.session.query(State).all()
#     form.state.choices = [(state.state_id, state.state_name) for state in State.query.all()]
#     form.lga.choices = [(lga.lga_id, lga.lga_name) for lga in Lga.query.all()]
#     if request.method == 'GET':
#         return render_template('user/contestantreg.html', states=states, form=form)
#     else:
#         if form.validate_on_submit():
#             fname = form.fname.data
#             lname = form.lname.data 
#             othername = form.othername.data
#             dob = form.dob.data
#             email = form.email.data
#             phone = form.phone.data
#             address = form.address.data
#             state = form.state.data
#             lga = form.lga.data
#             bio = form.bio.data
#             pics = form.pics.data
#             password = form.password.data
#             confirm_password = form.confirm_password.data
#             hashed_password = generate_password_hash(password)

#             age = calculate_age(dob)
#             if age < 18:
            
#                 flash(f'You must be 18 or older to Participate (Your current age is {age}).', category='error')
#                 return render_template('user/contestantreg.html', states=states, form=form)

#             current_year = datetime.now().year
#             user_id = User.query.count() + 1
#             serial_number = user_id
#             user_ref = generate_ref_number(current_year, serial_number)

#             new_user = User(user_fname=fname, user_lname=lname, user_othername=othername,user_dob=dob,user_address=address, user_phone=phone,user_email=email,user_pics=pics, user_password=hashed_password,user_state=state, user_lga=lga,user_bio=bio, user_ref=user_ref)
            
#             db.session.add(new_user)
#             db.session.commit()
#             name = new_user.user_fname
#             session['user_name'] = name
#             session['useronline'] = new_user.user_id

#             contestant_link = url_for('voting', user_id=new_user.user_id, _external=True)

#             flash('Registration Successful!', category='success')
#             return render_template('user/confirmation.html',contestant_link=contestant_link) 
    
#         else:
#             flash('Registration is not successful. Please check your input.', category='error')
#             return render_template('user/contestantreg.html', states=states, form=form)
        

@app.route("/contestant/", methods=['POST', 'GET'])
def register_contestant():
    form = ContestantForm()
    states = db.session.query(State).all()
    form.state.choices = [(state.state_id, state.state_name) for state in State.query.all()]
    form.lga.choices = [(lga.lga_id, lga.lga_name) for lga in Lga.query.all()]

    if request.method == 'GET':
        return render_template('user/contestantreg.html', states=states, form=form)
    else:
        if form.validate_on_submit():
            fname = form.fname.data
            lname = form.lname.data 
            othername = form.othername.data
            dob = form.dob.data
            email = form.email.data
            phone = form.phone.data
            address = form.address.data
            state = form.state.data
            lga = form.lga.data
            bio = form.bio.data
            pics = form.pics.data
            password = form.password.data
            confirm_password = form.confirm_password.data
            hashed_password = generate_password_hash(password)

            age = calculate_age(dob)
            if age < 18:
                flash(f'You must be 18 or older to participate (Your current age is {age}).', category='error')
                return render_template('user/contestantreg.html', states=states, form=form)

           
            if not check_payment(email):
                flash('Please purchase our book to complete your registration.', category='error')
                return redirect(url_for('make_payment'))  

            current_year = datetime.now().year
            user_id = User.query.count() + 1
            serial_number = user_id
            user_ref = generate_ref_number(current_year, serial_number)

            new_user = User(user_fname=fname, user_lname=lname, user_othername=othername,
                            user_dob=dob, user_address=address, user_phone=phone,
                            user_email=email, user_pics=pics, user_password=hashed_password,
                            user_state=state, user_lga=lga, user_bio=bio, user_ref=user_ref)
            
            db.session.add(new_user)
            db.session.commit()

            name = new_user.user_fname
            session['user_name'] = name
            session['useronline'] = new_user.user_id

            contestant_link = url_for('voting', user_id=new_user.user_id, _external=True)

            flash('Registration Successful!', category='success')
            return render_template('user/confirmation.html', contestant_link=contestant_link) 
    
        else:
            flash('Registration is not successful. Please check your input.', category='error')
            return render_template('user/contestantreg.html', states=states, form=form)




def check_payment(email):
    payment = Payment.query.filter_by(payment_email=email, payment_status='paid').first()
    return payment is not None


   
def calculate_age(user_dob):
    if isinstance(user_dob, str):
        dob_date = datetime.strptime(user_dob, '%d/%m/%Y').date()
    elif isinstance(user_dob, date):
        dob_date = user_dob
    else:
        raise ValueError("Invalid user_dob format. Expected str or datetime.date.")

    today = date.today()
    age = today.year - dob_date.year - ((today.month, today.day) < (dob_date.month, dob_date.day))
    return age




@app.route('/uploadpics/', methods=['GET', 'POST'])
def upload_pics():
    form = UploadForm()
    user_id = session.get('useronline')
    user = User.query.get(user_id)
    user_ref = user.user_ref

    if form.validate_on_submit():  
        pics = form.pics.data  
        if pics:  
            filename = pics.filename 
            if filename == "":
                flash('Please select a file', category='error')
                return redirect('/uploadpics/')
            else:
                name, ext = os.path.splitext(filename)
                allowed = ['.jpg', '.png', '.jpeg']
                if ext.lower() in allowed:
                    final_name = user_ref + ext
                    pics.save(os.path.join('pkg/static/pictures', final_name))
                    user.user_pics = final_name
                    db.session.commit()
                    flash('Image uploaded successfully', category='success')
                    # return redirect(url_for('confirm_registration', user_id=user_id))  
                    return redirect('/dashboard/')

    return render_template('user/upload_pics.html', form=form, user=user)





# @app.route('/confirm_registration/<int:user_id>/')
# def confirm_registration(user_id):
#     user = User.query.get(user_id)
#     if not user:
#         return "User not found", 404

#     details = {
#         'user_fname': user.user_fname,
#         'user_lname': user.user_lname,
#         'user_othername': user.user_othername,
#         'user_email': user.user_email,
#         'user_phone': user.user_phone,
#         'user_ref': user.user_ref
#     }

#     rendered_html = render_template('user/reg_summary.html', details=details, user=user)
#     pdf_io = generate_pdf(rendered_html)
#     filename = f'registration_confirmation_{user.user_fname}.pdf'
    
#     redirect_home = redirect(url_for('home'))
#     (redirect_home)

#     response = send_file(
#         pdf_io,
#         mimetype='application/pdf',
#         as_attachment=True,
#         download_name=filename
#     )

#     response.autocorrect_location_header = False
#     response.headers['Location'] = url_for('home')
#     return response


@app.route('/confirm_registration/<int:user_id>/', methods=['GET', 'POST'])
def confirm_registration(user_id):
    user = User.query.get(user_id)
    if not user:
        return "User not found", 404

    details = {
        'user_fname': user.user_fname,
        'user_lname': user.user_lname,
        'user_othername': user.user_othername,
        'user_email': user.user_email,
        'user_phone': user.user_phone,
        'user_ref': user.user_ref
    }

    rendered_html = render_template('user/reg_summary.html', details=details, user=user)
    pdf_io = generate_pdf(rendered_html)
    filename = f'registration_confirmation_{user.user_fname}.pdf'
    
    redirect_home = redirect(url_for('home'))
    (redirect_home)

    response = send_file(
        pdf_io,
        mimetype='application/pdf',
        as_attachment=True,
        download_name=filename
    )

    response.autocorrect_location_header = False
    response.headers['Location'] = url_for('home')
    return response




@app.route("/newsletter/", methods = ['POST','GET'])
def newsletter():
    email = request.form.get('email')
    if not email:
        flash('You need to enter your email address to subscribe', category='error')
        return redirect('/')
    else:
        subscriber = NewsletterSubscriber(email=email)
        db.session.add(subscriber)
        db.session.commit()
        
        flash('Thank you for subscribing for our monthly newsletter', category='success')
        return redirect('/')





@app.route('/state/lgas/', methods=['POST'])
def get_lgas_by_state():
    state_id = request.form.get("state_id")
    state = State.query.get(state_id)  
    if state is None:
        return jsonify(error="State not found"), 404
    lgas = state.lga_id
    lga_data = [{"lga_id": lga.lga_id, "lga_name": lga.lga_name} for lga in lgas]
    return jsonify(lga_data)





@app.route('/download/<filename>')
def download_file(filename):
    directory = app.config['UPLOAD_FOLDER']
    return send_from_directory(directory, filename, as_attachment=True)

        


@app.route('/voting/', methods=['GET', 'POST'])
def voting():
    form = VotingForm()
    if request.method == 'POST' and form.validate_on_submit():
        ref = form.ref.data
        data = db.session.query(User).filter(User.user_ref == ref).first()
       
        if data:
            user_id = data.user_id
            return redirect(url_for('voter', user_id=user_id))
        else:
            flash('Invalid contestant reference number. Please try again.', 'error')
            return redirect('/voting/')
    return render_template('user/voting.html', form=form)



         


@app.route('/voter/<int:user_id>/', methods=['GET', 'POST'])
def voter(user_id):
    user = User.query.get_or_404(user_id)
    contestant_link = url_for('vote', user_id=user_id, _external=True)
    
    if request.method == 'POST':
        user.user_vote += 1
        db.session.commit()
        flash(f'You successfully voted for {user.user_fname} {user.user_lname}. Thank you for contributing to the campaign for peace in our country Nigeria', 'success')
        return redirect('/')
    
    return render_template('user/voter.html', user=user, contestant_link=contestant_link)



@app.route('/vote/<int:user_id>/', methods=['GET', 'POST'])
def vote(user_id):
    ref = request.form.get('ref')
    logged_in_user_id = session.get('useronline')
    if logged_in_user_id == user_id:
        flash("You cannot vote for yourself.", category='error')
        return redirect('/dashboard/')
    else:
        
        user = User.query.get_or_404(user_id)
        user.user_vote += 1
        db.session.commit()
        # flash(f'You successfully voted for {user.user_fname} {user.user_lname}. Thank you for contributing to the campaign for peace in our country Nigeria', 'success')
        return redirect('/payment/')




@app.route('/flash/messages/')
def flash_messages():
    return render_template('user/flash_messages.html')


# @app.route('/payment/', methods=['GET', 'POST'])
# def payment():
#     form = PaymentForm()
#     if request.method == 'POST' and form.validate_on_submit():
#         fname = form.fname.data
#         lname = form.lname.data
#         email = form.email.data
#         phone = form.phone.data
#         amount = form.amount.data
        

#         paystack_transaction = PaystackTransaction.initialize(
#             email=email,
#             amount=int(amount) * 100, 
#             reference=f"{fname}-{lname}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
#         )

#         payment = Payment(
#             payment_fname=fname,
#             payment_lname=lname,
#             payment_email=email,
#             payment_phone=phone,
#             payment_amt=amount,
#             payment_ref=paystack_transaction['data']['reference']
#         )
#         db.session.add(payment)
#         db.session.commit()
#         return redirect(paystack_transaction['data']['authorization_url'])

#     return render_template('user/payment.html', form = form)


# @app.route('/paystack/webhook', methods=['POST'])
# def paystack_webhook():
#     return '', 200










# @app.route('/payment/', methods=['GET', 'POST'])
# def payment():
#     form = PaymentForm()
#     plans = Plan.query.all()
#     form.plan.choices = [(plan.plan_id, plan.plan_name) for plan in plans]
    
#     if request.method == 'POST' and form.validate_on_submit():
#         plan_id = form.plan.data
#         fname = form.fname.data
#         lname = form.lname.data
#         email = form.email.data
#         phone = form.phone.data
        
#         plan = Plan.query.get(plan_id)
#         if not plan:
#             flash('Invalid plan selected.', 'error')
#             return redirect(url_for('payment'))
        
#         plan_amount = plan.plan_amount
        
#         paystack_transaction = PaystackTransaction.initialize(
#             email=email,
#             amount=int(plan_amount * 100),  
#             reference=f"{fname}-{lname}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
#         )
        
      
#         payment = Payment(
#             payment_fname=fname,
#             payment_lname=lname,
#             payment_email=email,
#             payment_phone=phone,
#             payment_plan=plan_id,
#             payment_amt=plan_amount,
#             payment_ref=paystack_transaction['data']['reference']
#         )
        
   
#         db.session.add(payment)
#         db.session.commit()
        
        
#         flash('Payment successful. Thank you for helping us to do more', category='success')
#         return redirect(paystack_transaction['data']['authorization_url'])
    
#     return render_template('user/payment.html', form=form)




# @app.route('/payment/', methods=['GET', 'POST'])
# def make_payment():
#     form = PaymentForm()
#     plans = Plan.query.all()
#     form.plan.choices = [(plan.plan_id, plan.plan_name) for plan in plans]
    
#     if request.method == 'POST' and form.validate_on_submit():
#         plan_id = form.plan.data
#         fname = form.fname.data
#         lname = form.lname.data
#         email = form.email.data
#         phone = form.phone.data
        
#         plan = Plan.query.get(plan_id)
#         if not plan:
#             flash('Invalid plan selected.', 'error')
#             return redirect(url_for('payment'))
        
#         plan_amount = plan.plan_amount
        
#         paystack_transaction = PaystackTransaction.initialize(
#             email=email,
#             amount=int(plan_amount * 100),  
#             reference=f"{fname}-{lname}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
#         )
      
#         payment = Payment(
#             payment_fname=fname,
#             payment_lname=lname,
#             payment_email=email,
#             payment_phone=phone,
#             payment_plan=plan_id,
#             payment_amt=plan_amount,
#             payment_ref=paystack_transaction['data']['reference']
#         )
        
#         db.session.add(payment)
#         db.session.commit()
        
#         flash('Payment successful. Thank you for helping us to do more', category='success')
#         return redirect(paystack_transaction['data']['authorization_url'])
    
#     return render_template('user/payment.html', form=form)


@app.route('/payment/', methods=['GET', 'POST'])
def make_payment():
    form = PaymentForm()
    plans = Plan.query.all()
    form.plan.choices = [(plan.plan_id, plan.plan_name) for plan in plans]
    
    if request.method == 'POST' and form.validate_on_submit():
        plan_id = form.plan.data
        fname = form.fname.data
        lname = form.lname.data
        email = form.email.data
        phone = form.phone.data
        
        plan = Plan.query.get(plan_id)
        if not plan:
            flash('Invalid plan selected.', 'error')
            return redirect(url_for('payment'))
        
        plan_amount = plan.plan_amount
        
        paystack_transaction = PaystackTransaction.initialize(
            email=email,
            amount=int(plan_amount * 100),  
            reference=f"{fname}-{lname}-{datetime.now().strftime('%Y%m%d%H%M%S')}"
        )
      
        payment = Payment(
            payment_fname=fname,
            payment_lname=lname,
            payment_email=email,
            payment_phone=phone,
            payment_plan=plan_id,
            payment_amt=plan_amount,
            payment_ref=paystack_transaction['data']['reference']
        )
        
        db.session.add(payment)
        db.session.commit()
        
        flash('Payment successful. Thank you for helping us to do more', category='success')
        return redirect(paystack_transaction['data']['authorization_url'])
    
    return render_template('user/payment.html', form=form)



# @app.route('/paystack/webhook', methods=['POST'])
# def paystack_webhook():
#     data = request.get_json(force=True)  
#     payment_ref = data.get('reference')
#     payment_status = data.get('status')
#     payment = Payment.query.filter_by(payment_ref=payment_ref).first()
    
#     if payment:
#         if payment_status == 'success':
#             payment.payment_status = 'paid'
#         elif payment_status == 'failed':
#             payment.payment_status = 'failed'
#         db.session.commit()
        
        
#     else:
#         return jsonify({'error': 'Payment not found'}), 404

@app.route('/paystack/webhook', methods=['POST'])
def paystack_webhook():
    data = request.get_json(force=True)  
    payment_ref = data.get('reference')
    payment_status = data.get('status')
    payment = Payment.query.filter_by(payment_ref=payment_ref).first()
    
    if payment:
        if payment_status == 'success':
            payment.payment_status = 'paid'
            db.session.commit()
            
            return redirect(url_for('home'))
        elif payment_status == 'failed':
            payment.payment_status = 'failed'
            db.session.commit()
    else:
        return jsonify({'error': 'Payment not found'}), 404



# @app.route('/paystack/webhook', methods=['POST'])
# def paystack_webhook():
#     data = request.get_json(force=True)  
#     payment_ref = data.get('reference')
#     payment_status = data.get('status')
#     payment = Payment.query.filter_by(payment_ref=payment_ref).first()
    
#     if payment:
#         if payment_status == 'success':
#             payment.payment_status = 'paid'
#             db.session.commit()
#             return redirect(url_for('voting'))  
#         elif payment_status == 'failed':
#             payment.payment_status = 'failed'
#             db.session.commit()
#             return redirect('/payment/failed')
#     else:
#         return jsonify({'error': 'Payment not found'}), 404




# @app.route("/paylanding/")
# def paylanding():
#     payment_id = session.get('useronline')  
#     trxref = request.args.get('trxref') 
#     if session.get('reference') is not None and str(trxref) == str(session.get('reference')):
#         url = "https://api.paystack.co/transaction/verify/" + str(session.get('reference'))
#         headers = {
#             "Content-Type": "application/json",
#             "Authorization": "Bearer sk_test_ead50eacadfcfa37f1e5f65f95551db34e36513b"
#         }

#         response = requests.get(url, headers=headers)
#         rsp = response.json()

#         return jsonify(rsp)
#     else:
#         return "Transaction verification failed. Please start again."









@app.route('/plan/', methods=['POST'])
def get_plan():
    plan_id = request.form.get("plan_id")
    plan = Plan.query.get(plan_id)
    
    if not plan:
        return jsonify(error="Plan not found"), 404
    
    return jsonify({
        'plan_amount': plan.plan_amount
    })


# @app.route("/topaystack/", methods=['POST','GET'])
# def topaystack():
#     form = PaymentForm()
#     plans = Plan.query.all()
#     form.plan.choices = [(plan.plan_id, plan.plan_name) for plan in plans]
    
#     if request.method == 'POST' and form.validate_on_submit():
#         plan_id = form.plan.data
#         fname = form.fname.data
#         lname = form.lname.data
#         email = form.email.data
#         phone = form.phone.data
        
        
#         plan = Plan.query.get(plan_id)
#         if not plan:
#             flash('Invalid plan selected.', 'error')
#             return redirect(url_for('payment'))
        
        
#         ref = session.get('ref')
#         if not ref:
#             flash("Start the payment process again.", 'error')
#             return redirect('/payment/')
        
        
#         payment = Payment.query.filter(Payment.payment_ref == ref).first()
#         if not payment:
#             flash("Payment details not found.", 'error')
#             return redirect('/payment/')
        
        
#         url = "https://api.paystack.co/transaction/initialize"
#         headers = {
#             "Content-Type": "application/json",
#             "Authorization": "Bearer sk_test_ead50eacadfcfa37f1e5f65f95551db34e36513b"
#         }
#         data = {
#             'email': payment.payment_email,
#             'amount': int(payment.payment_amt * 100),
#             'reference': ref
#         }
        
        
#         response = requests.post(url, headers=headers, data=json.dumps(data))
#         rspjson = response.json()
        
#         if rspjson and rspjson.get('status') == True:
#             authurl = rspjson['data']['authorization_url']
#             return redirect(authurl)
#         else:
#             flash(rspjson.get('message', 'Failed to initialize payment.'), 'error')
#             return redirect('/payment/')
    
#     return redirect('/payment/')


# @app.route('/toconfirm/')
# def to_confirm():
#     id = session.get('useronline')
#     ref = session.get('ref')
    
#     if ref:
#         payment = Payment.query.filter(Payment.payment_ref == ref).first()
        
#         if payment:
#             return render_template('user/contestantreg.html', payment=payment)
#         else:
#             flash('Payment details not found. Please start the transaction again.', 'error')
#             return redirect('/payment/')
#     else:
#         flash('Please start the transaction again.', 'error')
#         return redirect('/payment/')


@app.errorhandler(ValueError)
def handle_value_error(error):
    return "Invalid input: " + str(error), 400


@app.errorhandler(404)
def page_not_found(error):
    return render_template('user/error.html'), 404

@app.errorhandler(500)
def internal_server_error(error):
    return render_template('user/error.html'), 500


@app.route('/news/')
def news():
    return render_template('user/news.html')

@app.route('/user/gallary/')
def user_gallary():
    return render_template('user/gallary_test.html')



@app.route('/buy/book/', methods=['GET', 'POST'])
def buy_book():
    if request.method == 'POST':
        email = request.form.get('email')
        if not email:
            flash('Please provide an email address.', category='error')
            return redirect(url_for('buy_book')) 
        
        payment = db.session.query(Payment).filter(Payment.payment_email == email, Payment.payment_status == 'paid').first()
        
        if payment:
            flash('Proceed with your registration.', category='success')
            return render_template('user/book_download.html')  
        else:
            flash('Please buy our book to proceed.', category='error')
            return redirect(url_for('make_payment'))  

    return render_template('user/buy_book.html')
    



@app.route('/registration/steps/')
def reg_steps():
    return render_template('user/register_steps.html')