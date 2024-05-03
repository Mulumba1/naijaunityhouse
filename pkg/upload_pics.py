from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField, StringField


class UploadForm(FlaskForm):
    pics = FileField('Upload Picture')
    submit = SubmitField('Upload')
    cancel = SubmitField('Cancel')