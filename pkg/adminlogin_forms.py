from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField,EmailField
from wtforms.validators import DataRequired,length,Email,EqualTo



class InitialCapitalStringField(StringField):
    def process_formdata(self, valuelist):
        if valuelist:
            self.data = valuelist[0].strip().title()
        else:
            self.data = ''


class AdminloginForm(FlaskForm):
    username = InitialCapitalStringField('Username', render_kw={"placeholder": "Enter your username"}, validators=[DataRequired()])
    password = PasswordField('Password', render_kw={"placeholder": "Enter your password"})
    submit = SubmitField('Login')