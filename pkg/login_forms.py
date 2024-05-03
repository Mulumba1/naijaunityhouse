from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField
from wtforms.validators import DataRequired,length,Email,EqualTo




class  LoginForm(FlaskForm):
    ref = StringField('ref', render_kw={"placeholder": "Enter your Reference Number"}, validators=[DataRequired()])
    password = PasswordField('Password', render_kw={"placeholder": "Enter your password"})
    submit = SubmitField('Login')