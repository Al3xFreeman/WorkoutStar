from datetime import datetime
from hashlib import md5
from time import time
from flask import current_app
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(128), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    sessions = db.relationship('Session', backref='user', lazy='dynamic')
    routines = db.relationship('Routine', backref='user', lazy='dynamic')
    #routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)

    #__table_args__ = (
    #    db.ForeignKeyConstraint(
    #        []
    #    )
    #)

    def __repr__(self):
        return '<User {}>'.format(self.username)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

    def avatar(self, size):
        digest = md5(self.email.lower().encode('utf-8')).hexdigest()
        return 'https://www.gravatar.com/avatar/{}?d=identicon&s={}'.format(digest, size)


    def get_reset_password_token(self, expires_in=600):
        return jwt.encode(
            {
                'reset_password': self.id,
                'exp': time() + expires_in,
            },
            current_app.config['SECRET_KEY'],
            algorithm='HS256'
        )

    @staticmethod
    def verify_reset_password_token(token):
        try:
            id = jwt.decode(token, current_app.config['SECRET_KEY'],
                            algorithms=['HS256'])['reset_password']
        except:
            return
        return User.query.get(id)



@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class Routine(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    period = db.Column(db.Integer)
    workouts = db.relationship('Workout', backref='routine', lazy='dynamic')

    def __repr__(self):
        return '<Routine Nº {}'.format(self.id) + (' assigned to user: {}>'.format(self.user.username) if self.user else '') + '>'

# Definition of workouts

class Workout(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    day = db.Column(db.Integer)
    name = db.Column(db.String(128))
    routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'))
    goal_exercises = db.relationship('GoalExercise', backref='workout', lazy='dynamic')

    # Session history
    sessions = db.relationship('Session', backref='workout', lazy='dynamic')
    

class GoalExercise(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise_def.id'))
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))

    sets_max = db.Column(db.Integer)
    sets_min = db.Column(db.Integer)
    reps_max = db.Column(db.Integer)
    reps_min = db.Column(db.Integer)
    weights_max = db.Column(db.Integer)
    weights_min = db.Column(db.Integer)
    duration_max = db.Column(db.Integer)
    duration_min = db.Column(db.Integer)

    exercise_history = db.relationship('Exercise', backref='goal_exercise', lazy='dynamic')



class ExerciseDef(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128))
    goal_exercies_id

# Active Session 

class Session(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, index = True, nullable = True, default = datetime.utcnow)
    exercises = db.relationship('Exercise', backref='session', lazy='dynamic')
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Session Nº {}, with {} exercises, assigned to user: {}'.format(self.id, self.exercises.count(), self.user.username) + (', is part of routine Nº {}'.format(self.routine.id) if self.routine else '') + '>'



class Exercise(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    goal_exercise_id = db.Column(db.Integer, db.ForeingKey('goal_exercise.id'))
    name = db.Column(db.String(128))
    done = db.Column(db.Boolean)
    duration = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    sets = db.relationship('Set', backref='exercise', lazy='dynamic')


    def __repr__(self):
        return '<Exercise Nº {} with name {}, DONE = '.format(self.id, self.name) + ('Yes' if self.done else 'No') + '>'

class Set(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    weight = db.Column(db.Integer)
    reps = db.Column(db.Integer)

    def __repr__(self):
        return '<Set Nº {}, weight lifted: {}, reps done: {}>'.format(self.id, self.weight, self.reps)