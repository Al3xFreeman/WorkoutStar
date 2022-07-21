from xmlrpc.client import DateTime
from flask import request
from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, DateTimeField
from wtforms.validators import DataRequired, ValidationError, Length
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
    date = DateTimeField('Date Performed', validators=[])
    due_time = DateTimeField('Due Date')
    submit = SubmitField('Submit')

class RoutineForm(FlaskForm):
    submit = SubmitField('Submit')