from flask_wtf import FlaskForm
from wtforms import PasswordField, SubmitField,StringField
from wtforms.validators import DataRequired, Email, Length, EqualTo,Length, Regexp


class ResetForm(FlaskForm):
    ref = StringField('ref', render_kw={"placeholder": "Enter your Reference Number"}, validators=[DataRequired()])
    new_password = PasswordField('New Password',render_kw={"placeholder": "Enter New Password"}, validators=[DataRequired(),
    Length(min=8, message='Password must be at least 8 characters long'),Regexp(r'^(?=.*[a-z])(?=.*[A-Z])(?=.*\d)(?=.*[@$!%*?&])[A-Za-z\d@$!%*?&]+$', message='Password must include at least one lowercase letter, one uppercase letter, one number, and one special character')])
    confirm_password = PasswordField('Confirm Password',render_kw={"placeholder": "Confirm New Password"}, validators=[DataRequired(), EqualTo('new_password', message='Password do not match')])
    submit = SubmitField('Reset Password')