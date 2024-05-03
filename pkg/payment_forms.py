from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, DateField, EmailField,DecimalField,SelectField
from wtforms.validators import DataRequired




class InitialCapitalStringField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].strip().title()
        else:
            self.data = ''



# class PaymentForm(FlaskForm):
#     fname = InitialCapitalStringField('First Name', render_kw={"placeholder": "Enter your First Name"}, validators=[DataRequired()])
#     lname = InitialCapitalStringField('Last Name', render_kw={"placeholder": "Enter your Last Name"}, validators=[DataRequired()])
#     email = EmailField('Email', render_kw={"placeholder": "Enter your email"},validators=[DataRequired()])
#     phone = StringField('Phone Number', render_kw={"placeholder": "Enter your phone number"}, validators=[DataRequired()])
#     amount = DecimalField('Payment Amount')
#     submit = SubmitField('Make payment')


class PaymentForm(FlaskForm):
    plan = SelectField('Plan',coerce=int, render_kw={"placeholder": "Select Payment for"}, validators=[DataRequired()])
    fname = InitialCapitalStringField('First Name',render_kw={"placeholder": "Enter First Name"}, validators=[DataRequired()])
    lname = InitialCapitalStringField('Last Name',render_kw={"placeholder": "Enter Last Name"}, validators=[DataRequired()])
    email = EmailField('Email',render_kw={"placeholder": "email@example.com"}, validators=[DataRequired()])
    phone = StringField('Phone Number', render_kw={"placeholder": "Enter your phone number"}, validators=[DataRequired()])
    amount = DecimalField('Payment Amount',render_kw={"placeholder": "Payment Amount"},)
    submit = SubmitField('Make payment')
