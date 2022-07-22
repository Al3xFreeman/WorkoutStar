from xmlrpc.client import DateTime
from flask import request
from flask_wtf import FlaskForm
from sqlalchemy import Integer
from wtforms import StringField, SubmitField, TextAreaField, IntegerField, DateTimeField, DateField
from wtforms.validators import DataRequired, ValidationError, Length, Optional
from app.models import User, Session, ExerciseDef



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
    session_id = IntegerField('Session Id', validators=[DataRequired()])
    exercise_def_id = IntegerField('ExerciseDef Id', validators=[DataRequired()])
    submit = SubmitField('Submit')

    def validate_session_id(self, session_id):
        session = Session.query.filter_by(id=session_id.data).first()
        if session is None:
            raise ValidationError('Session ID is not valid.')

    def validate_exercise_def_id(self, exercise_def_id):
        exercise_def = ExerciseDef.query.filter_by(id=exercise_def_id.data).first()
        if exercise_def is None:
            raise ValidationError('ExerciseDef ID is not valid.')

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


class ExerciseDefForm(FlaskForm):
    name = StringField('Exercise Name', validators=[DataRequired(), Length(min=1, max=128)])
    description = TextAreaField('Description', validators=[Length(min=1, max=256)])
    submit = SubmitField('Submit')
