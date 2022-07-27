from dataclasses import Field
from email.policy import strict
from operator import length_hint
from typing_extensions import Required
from wsgiref import validate
from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Range, Length
from pkg_resources import require
from app.models import User, Routine, Session, ExerciseDef, Exercise


class UserCreationSchema(Schema):
    username = fields.Str(required=True, validate=Length(3, 64, error='The username length must be between {min} and {max} characters long'))
    email = fields.Email(required=True, validate=Length(3, 128, error='The email length must be between {min} and {max} characters long'))
    password = fields.String(required=True)
    

    #Custom validation for passwrod, so we can perform regex to check for it's security
    @validates('password')
    def check_password(self, password):
        pass


class RoutineSchema(Schema):
    user_id = fields.Int(required=True)
    period = fields.Int(required=True, validate=Range(min=1, error="The minimum length of a routine is {min} day"))

    @validates('user_id')
    def valid_user_id(self, id):
        if not User.query.get(id):
            raise ValidationError("Not a valid User")



class WorkoutSchema(Schema):
    day = fields.Int(required=False)
    name = fields.Str(required=False, validate=Length(3, 128))
    routine_id = fields.Int(required=True)

    @validates('routine_id')
    def valid_routine_id(self, id):
        if not Routine.query.get(id):
            raise ValidationError("Routine id is not valid")

class SessionSchema(Schema):
    date = fields.DateTime(required=False)
    workout_id = fields.Int(required=False)
    user_id = fields.Int(required=True)
    
    @validates('user_id')
    def valid_user_id(self, id):
        if not User.query.get(id):
            raise ValidationError("Not a valid User")

class ExerciseDefSchema(Schema):
    name = fields.Str(required=True, validate=Length(3, 128))
    description = fields.Str(required=False, validate=(3, 128))


class ExerciseSchema(Schema):
    session_id = fields.Int(required=True)
    name = fields.Str(required=False, validate=Length(3, 128))
    done = fields.Bool(required=False)
    duration = fields.Int(required=False)
    timestamp = fields.DateTime(required=False)
    exercise_def_id = fields.Int(required=True)

    @validates('session_id')
    def valid_session_id(self, id):
        if not Session.query.get(id):
            raise ValidationError("Not a valid Session id")

    @validates('exercise_def_id')
    def valid_session_id(self, id):
        if not ExerciseDef.query.get(id):
            raise ValidationError("Not a valid ExerciseDef id")

class SetSchema(Schema):
    exercise_id = fields.Int(required=True)
    weight = fields.Int(required=False, validate=Range(min=0))
    reps = fields.Int(required=False, validate=Range(min=0))

    @validates('exercise_id')
    def valid_exercise_id(self, id):
        if not Exercise.query.get(id):
            raise ValidationError("Not a valid Exercise id")