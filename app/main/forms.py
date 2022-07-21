from xmlrpc.client import DateTime
from flask import request
from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, DateTimeField, DateField
from wtforms.validators import DataRequired, ValidationError, Length, Optional
from app.models import User



class EditProfileForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    about_me = TextAreaField('About Me', validators=[Length(min=0, max=140)])
    submit = SubmitField('Submit')

    def __init__(self, original_username, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.original_username = original_username

    def validate_username(self, username):
        if username.data != self.original_username:
            user = User.query.filter_by(username=self.username.data).first()
            if user is not None:
                raise ValidationError('Please use a different username.')


class EmptyForm(FlaskForm):
    submit = SubmitField('Submit')

class PostForm(FlaskForm):
    post = TextAreaField('Say something', validators=[DataRequired(), Length(min=1, max=140)])
    submit = SubmitField('Submit')


class ExerciseForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired(), Length(min=3, max=128)])
    submit = SubmitField('Submit')

class SetForm(FlaskForm):
    weight = IntegerField('weight', validators=[])
    reps = IntegerField('repetitions', validators=[])
    submit = SubmitField('Submit')

class SesionForm(FlaskForm):
    date = DateField('Date Performed (Default: now)', validators=[Optional()])
    due_time = DateField('Due Date (Optional)', validators=[Optional()])
    submit = SubmitField('Submit')

class RoutineForm(FlaskForm):
    submit = SubmitField('Submit')