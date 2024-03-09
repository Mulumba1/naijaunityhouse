from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, RadioField, BooleanField, TextAreaField, DateField,SelectField, EmailField
from wtforms.validators import DataRequired, Email, URL, Length, EqualTo,Length, Regexp

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



class RegisterForm(FlaskForm):
    fname = InitialCapitalStringField('First Name', validators=[DataRequired()])
    lname = InitialCapitalStringField('Last Name', validators=[DataRequired()])
    othername = InitialCapitalStringField('Other Names')
    dob = DateField('Date of Birth', validators=[DataRequired()])
    address = InitialCapitalTextAreaField('Residence Address', validators=[DataRequired()])
    phone = StringField('Phone number', validators=[DataRequired()])
    nin = StringField('National Identification Number', validators=[DataRequired(),Length(min=11, max=11)])
    state = SelectField('State', coerce=int, validators=[DataRequired()])
    lga = SelectField('L G A', coerce=int, validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email(message='Please enter a valid email address')])
    password = PasswordField('Password', validators=[DataRequired(),
    Length(min=8, message='Password must be at least 8 characters long'),Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', message='Password must include at least one lowercase letter, one uppercase letter, one number, and one special character')])
    confirm_password = PasswordField('Confirm Password', validators=[DataRequired(), EqualTo('password', message='Password do not match')])
    check_field = BooleanField(Markup('I Accept the Terms & Conditions <a href="/" id="terms">Terms & Conditions</a>'), validators=[DataRequired()])
    submit = SubmitField('Create Account')




    