from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField,EmailField, TextAreaField
from wtforms.validators import DataRequired,Email


class ContactForm(FlaskForm):
    fname = StringField('First name', validators=[DataRequired()])
    lname = StringField('Last name', validators=[DataRequired()])
    email = EmailField('Email', validators=[DataRequired(), Email()])
    phone = StringField('Phone Number', validators=[DataRequired()])
    message = TextAreaField('Message', validators=[DataRequired()])
    submit = SubmitField('Submit')