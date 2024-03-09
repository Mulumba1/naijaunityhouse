import os, random, uuid, string
from uuid import uuid4
from datetime import datetime
from functools import wraps
from flask import render_template,request,redirect,flash,url_for,make_response,session,flash,jsonify,send_file
from werkzeug.security import generate_password_hash, check_password_hash
from flask_weasyprint import HTML, render_pdf  
from flask_mail import  Message
from pkg import app, mail
from pkg.models import db,State,Lga,Image,Admin,NewsletterSubscriber,ContactUs,User
from pkg.contact import ContactForm
from pkg.register_forms import RegisterForm







@app.route('/')
def home():
    return render_template("user/index.html")


@app.route('/about/')
def about():
    return render_template('user/about.html')

@app.route('/bases/')
def bases():
    return render_template('user/bases.html')



@app.route('/volunteer/')
def volunteer ():
    return render_template('user/volunteer.html')

@app.route('/contestant/')
def contenstant_reg ():
    return render_template('user/contestantreg.html')


# @app.route('/reset/password/', methods=['GET', 'POST'])
# def reset_password():
#     reset = ResetForm()
#     if request.method == 'POST' and reset.validate_on_submit():
#         email = reset.email.data
#         new_password = reset.new_password.data
#         confirm_password = reset.confirm_password.data
#         user = User.query.filter_by(user_email=email).first()
#         if user:
#             user.user_password = generate_password_hash(new_password)
#             db.session.commit()
#             flash('Password reset successfully! You can now login with your new Password', 'success')
#             return redirect('/') 
#         else:
#             flash('Invalid email address', 'error')
#             return redirect('/reset/password/')  
#     return render_template('user/reset_password.html', reset=reset)
            


# @app.route('/login/', methods = ['POST','GET'])
# def login():
#     form = LoginForm()
#     if request.method=='POST':
#         if form.validate_on_submit():
#             email = form.email.data
#             password = form.password.data
#             data = db.session.query(User).filter(User.user_email==email).first()
#             if data:
#                 hashed_pwd= data.user_password
#                 rsp = check_password_hash(hashed_pwd,password)
#                 if rsp:
#                     id = data.user_id
#                     session['useronline'] = id
#                     session['name'] = data.user_fname
#                     return redirect('/dashboard/')
#                 else:
#                     flash('Invalid Login Credentials', 'error')
#                     return render_template('user/login.html',form=form)
#             else:
#                 flash('Please enter valid credentials', 'error')
#                 return redirect('/login/')
#         else:
#             return redirect('/login/')   
#     else:
#         return render_template('user/login.html', form=form)






# @app.route("/logout/")
# def logout():
#     session.pop("useronline",None)
#     return redirect("/")


# @app.route('/dashboard/')
# def dashboard():
#     user_id = session.get('useronline')
#     user = User.query.get(user_id)
#     return render_template('user/dashboard/dashboard.html', user=user)
     




# @app.route('/profile/')
# def user_profiles():
#     user = User.query.all()
#     return render_template('user_profiles.html', user=user)



# def generate_ref_number():
#     digits = ''.join(random.choices(string.digits, k=8))  
#     letters = ''.join(random.choices(string.ascii_uppercase, k=2))  
#     return digits + letters

def generate_ref_number():
    digits = ''.join(random.choices(string.digits, k=8))  
    letters = ''.join(random.choices(string.ascii_uppercase, k=2))  
    return digits + letters

@app.route('/register/', methods=['GET', 'POST'])
def user_register():
    register = RegisterForm()
    states = db.session.query(State).all()
    register.state.choices = [(state.state_id, state.state_name) for state in State.query.all()]
    register.lga.choices = [(lga.lga_id, lga.lga_name) for lga in Lga.query.all()]
    
    if request.method == 'POST' and register.validate_on_submit():
        fname = register.fname.data
        lname = register.lname.data
        othername = register.othername.data
        dob = register.dob.data
        address = register.address.data
        state = register.state.data
        lga = register.lga.data
        phone = register.phone.data
        nin = register.nin.data
        email = register.email.data
        password = register.password.data
        confirm_password = register.confirm_password.data
        hashed_password = generate_password_hash(password)
        user_ref = generate_ref_number()

        
        new_user = User(user_fname=fname,user_lname=lname,user_othername=othername,user_dob=dob,user_address=address,user_phone=phone,user_nin=nin,user_email=email,user_password=hashed_password,user_state=state,user_lga = lga,user_ref=user_ref )

        db.session.add(new_user)
        db.session.commit()
        
        
        name = new_user.user_fname
        session['user_name'] = name
        session['useronline'] = new_user.user_id

        flash('Registration Successful!', category='success')
        return render_template('user/keep.html')
    
    return render_template('user/register.html', states=states,register=register)



# @app.route('/keep/')
# def keep():
#     return render_template('user/keep.html')




# def generate_pdf_confirmation(user):
#     html_content = render_template('user/registration_summary.html', user=user)
#     pdf = HTML(string=html_content).write_pdf()
#     pdf_filename = f"{user.user_ref}_registration_summary.pdf"
#     with open(pdf_filename, 'wb') as pdf_file:
#         pdf_file.write(pdf)

#     return pdf_filename

# @app.route('/print/confirmation/')
# def print_confirmation():
#     user_id = session.get('useronline')
#     user = User.query.get(user_id)
#     pdf_path = user.registration_pdf_path
#     return send_file(pdf_path, as_attachment=True)


# @app.route('/download/pdf/<filename>')
# def download_pdf(filename):
#     return send_file(filename, as_attachment=True)

# @app.route('/view/pdf/<filename>')
# def view_pdf(filename):
#     return send_file(filename)


# @app.route("/newsletter/", methods = ['POST','GET'])
# def newsletter():
#     email = request.form.get('email')
#     if not email:
#         flash('You need to enter your email address to subscribe', 'error')
#         return redirect('/')
#     else:
#         subscriber = NewsletterSubscriber(email=email)
#         db.session.add(subscriber)
#         db.session.commit()
        
#         flash('Thank you for subscribing for our monthly newsletter', 'success')
#         return redirect('/')


@app.route("/contact/")
def contact():
    contact = ContactForm()
    return render_template("user/contact.html", contact=contact)

@app.route('/contactsubmit/', methods=['POST', 'GET'])
def contact_submit():
    contact_form = ContactForm()
    if request.method == 'POST' and contact_form.validate_on_submit():
        fname = contact_form.fname.data
        lname = contact_form.lname.data
        email = contact_form.email.data
        phone = contact_form.phone.data
        message = contact_form.message.data

        if not fname or not lname or not email or not phone or not message:
            flash('All fields are required', 'error')
            return render_template('user/contact.html', contact=contact_form)
        else:
            new_contact = ContactUs(contact_fname=fname, contact_lname=lname, contact_email=email, contact_phone=phone, contact_message=message)
            db.session.add(new_contact)
            db.session.commit()

        flash(f'Thank you {fname} for contacting us. One of our customer care representative will contact you shortly on your Email: {email}', 'success')
        return redirect('/')
    
    return render_template('user/contact.html', contact=contact_form)




# @app.route('/about/')
# def about():
#     return render_template('user/about.html')


# @app.route('/display/image/')
# def display_image():
#     images = Image.query.all()
#     return render_template('user/display.html', images =images)

# @app.route('/mymarket/')
# def mymarket():
#     return render_template('user/dashboard/market.html')

# @app.route('/performance/') 
# def performance():
#     return render_template('user/dashboard/performance.html')




# @app.route('/faq/')
# def faq():
#     return render_template('user/faq.html')


# @app.route("/send/email/")
# def send_email():
#     msg = Message("RENT AND BUY PROPERTIES", sender = "support@iBoss.com", recipients=["talk2mulumba@gmail.com","c.uonebunne@gmail.com"])
#     msg.body = "This is a test email from our flask app"
#     msg.html = "<h1>Python Class</h1><p style='color:blue;'>This is a Python and Flask class</p>"
#     with app.open_resource('contract.pdf') as file:
#         msg.attach('contract.pdf', 'application/pdf', file.read())
#     mail.send(msg)
#     return "Email was sent successfully"






# @app.route('/state/lgas/', methods=['POST'])
# def get_lgas_by_state():
#     state_id = request.form.get("state_id")
#     state = State.query.get(state_id)  
#     if state is None:
#         return jsonify(error="State not found"), 404
#     lgas = state.lga_id
#     lga_data = [{"lga_id": lga.lga_id, "lga_name": lga.lga_name} for lga in lgas]
#     return jsonify(lga_data)




# @app.route('/changedp/', methods=['GET', 'POST'])
# def change_dp():
#     changedp = ChangdpForm()
#     user_id = session.get('useronline')
#     user = User.query.get(user_id)
#     oldpix = user.user_pics
#     if changedp.validate_on_submit():  
#         pics = changedp.pics.data  
#         if pics:  
#             filename = pics.filename 
#             if filename == "":
#                 flash('Please select a file', category='error')
#                 return redirect('/changedp/')
#             else:
#                 name, ext = os.path.splitext(filename)
#                 allowed = ['.jpg', '.png', '.jpeg']
#                 if ext.lower() in allowed:
#                     final_name = int(random.random() * 1000000)
#                     final_name = str(final_name) + ext 
#                     pics.save(os.path.join('pkg/static/profile', final_name))
#                     user = User.query.get(user_id)
#                     user.user_pics = final_name
#                     db.session.commit()
#                     try:
#                         if oldpix:  
#                             os.remove(f'pkg/static/profile/{oldpix}')
#                     except:
#                         pass
#                     flash('Profile picture added successfully', category='success')
#                     return redirect('/dashboard')
#                 else:
#                     flash('Extension not allowed', category='error')
#                     return redirect(url_for('change_dp'))
#     return render_template('user/changedp.html', changedp=changedp, user=user)



# @app.route('/cancel/')
# def cancel():
#     return redirect('/dashboard/')

# @app.route('/edit/profile/', methods=['GET', 'POST'])
# def edit_profile():
#     edit = EditForm()
#     states = db.session.query(State).all()
#     edit.state.choices = [(state.state_id, state.state_name) for state in State.query.all()]
#     edit.lga.choices = [(lga.lga_id, lga.lga_name) for lga in Lga.query.all()]
#     user_id = session.get('useronline')
#     user = User.query.get(user_id)
    
#     if request.method == 'POST':
#         if 'cancel' in request.form:
#             return redirect(url_for('dashboard'))  # Redirect to dashboard if cancel is pressed
        
#         if edit.validate_on_submit():
#             user.user_email = edit.email.data
#             user.user_phone = edit.phone.data
#             user.user_dob = edit.dob.data
#             user.user_address = edit.address.data
#             user.user_state = edit.state.data
#             user.user_lga = edit.lga.data
            
#             db.session.commit()
#             flash('Profile updated successfully!', category='success')
#             return redirect(url_for('dashboard'))
#     edit.email.data = user.user_email
#     edit.phone.data = user.user_phone
#     edit.dob.data = user.user_dob
#     edit.address.data = user.user_address
#     edit.state.data = user.user_state
#     edit.lga.data = user.user_lga
    
#     return render_template('user/dashboard/edit_profile.html', edit=edit, states=states)