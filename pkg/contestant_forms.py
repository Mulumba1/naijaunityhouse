from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField, TextAreaField, DateField,SelectField, EmailField,validators
from wtforms.validators import DataRequired, Email, URL, Length, EqualTo,Length, Regexp
from flask_wtf.file import FileField, FileAllowed, FileRequired

from markupsafe import Markup
from pkg.models import State,Lga



class InitialCapitalStringField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].strip().title()
        else:
            self.data = ''


class InitialCapitalTextAreaField(TextAreaField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].strip().title()
        else:
            self.data = ''



class ContestantForm(FlaskForm):
    fname = InitialCapitalStringField('First Name', render_kw={"placeholder": "Enter your first name"}, validators=[DataRequired()])
    lname = InitialCapitalStringField('Last Name', render_kw={"placeholder": "Enter your last name"}, validators=[DataRequired()])
    othername = InitialCapitalStringField('Other Name', render_kw={"placeholder": "Enter your other names"})
    dob = DateField('Date of Birth',render_kw={"placeholder":"Enter your date of birth"}, validators=[DataRequired()])
    email = EmailField('Email', render_kw={"placeholder": "Enter your email"},validators=[DataRequired()])
    phone = StringField('Phone Number', render_kw={"placeholder": "Enter your phone number"}, validators=[DataRequired(message='Phone number is required'),Length(min=11, max=11, message='Phone number must be exactly 11 characters')])
    address =InitialCapitalTextAreaField('Residential Address', render_kw={"placeholder": "Enter your residential address"})
    state = SelectField('State', coerce=int,render_kw={"placeholder": "Select your state of residence"})
    lga = SelectField('L G A', coerce=int,render_kw={"placeholder": "Select your LGA of residence"})
    bio = TextAreaField('Biography', render_kw={"placeholder": "Briefly introduce yourself", "rows": "7",})
    pics = FileField('Choose File') 
    password = PasswordField('Password',render_kw={"placeholder": "Enter password"}, validators=[DataRequired(message='Password is required'),Length(min=8, message='Password must be at least 8 characters long'),
    Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$',
    message='Password must include at least one lowercase letter, one uppercase letter, one number, and one special character')])
    confirm_password = PasswordField('Confirm Password', render_kw={"placeholder": "Confirm your password"})
    check_field = BooleanField(Markup('I Accept the Terms & Conditions <a href="/" id="terms">Terms & Conditions</a>'), validators=[DataRequired()])
    submit = SubmitField('Register')