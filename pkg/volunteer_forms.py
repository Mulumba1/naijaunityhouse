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



class VolunteerForm(FlaskForm):
    name = InitialCapitalStringField('Full Name', render_kw={"placeholder": "Enter your Full Name"}, validators=[DataRequired()])
    email = EmailField('Email', render_kw={"placeholder": "Enter your email"},validators=[DataRequired()])
    phone = StringField('Phone Number', render_kw={"placeholder": "Enter your phone number"}, validators=[DataRequired()])
    address =InitialCapitalTextAreaField('Residential Address', render_kw={"placeholder": "Enter your residential address"})
    state = SelectField('State', coerce=int,render_kw={"placeholder": "Select your state of residence"})
    lga = SelectField('L G A', coerce=int,render_kw={"placeholder": "Select your LGA of residence"})
    submit = SubmitField('Register')