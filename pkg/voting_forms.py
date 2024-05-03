from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired




class  VotingForm(FlaskForm):
    ref = StringField('ref', render_kw={"placeholder": "Candidate Code Eg: 2024000AG"}, validators=[DataRequired()])
    submit = SubmitField('submit to vote')