from datetime import datetime, timedelta
from email.policy import default
from hashlib import md5
from time import time
from flask import current_app, url_for
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
from app import db, login

import base64
import os

class MetadataMixin(object):
    deleted = db.Column(db.Boolean, default=False)
    deleted_date = db.Column(db.DateTime)
    created_at = db.Column(db.DateTime)
    updated_at = db.Column(db.DateTime)

class PaginatedAPIMixin(object):

    @staticmethod
    def to_collection_dict(query, page, per_page, endpoint, **kwargs):
        resources = query.paginate(page, per_page, False)
        data = {
            'items': [item.to_dict() for item in resources.items],
            '_meta': {
                'page': page,
                'per_page': per_page,
                'total_pages': resources.pages,
                'total_items': resources.total
            },
            '_links': {
                'self': url_for(endpoint, page=page, per_page=per_page, **kwargs),
                'next': url_for(endpoint, page=page + 1, per_page=per_page, **kwargs) if resources.has_next else None,
                'prev': url_for(endpoint, page=page - 1, per_page=per_page, **kwargs) if resources.has_prev else None
            }
        }

        return data



class User(MetadataMixin, PaginatedAPIMixin, UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(64), index = True, unique = True)
    email = db.Column(db.String(128), index = True, unique = True)
    password_hash = db.Column(db.String(128))
    sessions = db.relationship('Session', backref='user', lazy='dynamic')
    routines = db.relationship('Routine', backref='user', lazy='dynamic')
    #routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'))
    about_me = db.Column(db.String(140))
    last_seen = db.Column(db.DateTime, default=datetime.utcnow)


    token = db.Column(db.String(32), index = True, unique = True)
    token_expiration = db.Column(db.DateTime)

    def get_token(self, expires_in=3600):
        now = datetime.utcnow()
        if self.token and self.token_expiration > now + timedelta(seconds=60):
            return self.token
        
        self.token = base64.b64encode(os.urandom(24)).decode("utf-8")
        self.token_expiration = now + timedelta(seconds=expires_in)

        db.session.add(self)

        return self.token

    def revoke_token(self):
        self.token_expiration = datetime.utcnow() - timedelta(seconds=1)

    @staticmethod
    def check_token(token):
        user = User.query.filter_by(token=token).first()
        if user is None or user.token_expiration < datetime.utcnow():
            return None
        return user


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


    def to_dict(self, include_email=False, avatar_size=128):
        data = {
            'id': self.id,
            'username': self.username,
            'rutine_count': self.routines.count(),
            'session_count': self.sessions.count(),
            'deleted': self.deleted,
            '_links': {
                'self': url_for('api.get_user', id=self.id),
                'user_routines': url_for('api.get_user_routines', id=self.id),
                'user_sessions': url_for('api.get_user_sessions', id=self.id),
                'avatar': self.avatar(avatar_size)
            }   
        }

        if include_email:
            data['email'] = self.email

        return data

    def from_dict(self, data, new_user=False):
        for field in ['username', 'email']:
            if field in data:
                setattr(self, field, data[field])
        
        if new_user and 'password' in data:
            self.set_password(data['password'])




@login.user_loader
def load_user(id):
    return User.query.get(int(id))



class Routine(MetadataMixin, PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    #session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    period = db.Column(db.Integer)
    workouts = db.relationship('Workout', backref='routine', lazy='dynamic')

    def __repr__(self):
        return '<Routine Nº {}'.format(self.id) + (' assigned to user: {}>'.format(self.user.username) if self.user else '') + '>'

    def to_dict(self):
        data = {
            'id': self.id,
            'period' : self.period,
            '_links': {
                'self': url_for('api.get_routine', id=self.id),
                'workouts': url_for('api.get_routine_workouts', id=self.id),
                'user': url_for('api.get_user', id=self.user_id)
            }
        }
    
        return data

    def from_dict(self, data):
        for field in ['period', 'user_id']:
            if field in data:
                setattr(self, field, data[field])


# Definition of workouts

class Workout(MetadataMixin, PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    day = db.Column(db.Integer)
    name = db.Column(db.String(128))
    routine_id = db.Column(db.Integer, db.ForeignKey('routine.id'))
    goal_exercises = db.relationship('GoalExercise', backref='workout', lazy='dynamic')

    # Session history
    sessions = db.relationship('Session', backref='workout', lazy='dynamic')
    
    def to_dict(self):
        data = {
            'id': self.id,
            'day' : self.day,
            'name' : self.name,
            'number_of_sessions': self.sessions.count(),
            '_links': {
                'self': url_for('api.get_workout', id=self.id),
                #'goal_exercises': url_for('api.get_workout_goal_exercises', id=self.id),
                'sessions' : url_for('api.get_workout_sessions', id=self.id)
            }
        }
    
        return data

    def from_dict(self, data):
        for field in ['day', 'name']:
            if field in data:
                setattr(self, field, data[field])

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



class ExerciseDef(MetadataMixin, PaginatedAPIMixin, db.Model):
    __tablename__ = 'exercise_def'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable = False)
    description = db.Column(db.String(256))
    exercises = db.relationship('Exercise', backref='exercise_def', lazy='dynamic')

    def to_dict(self):
        data = {
            'id': self.id,
            'name' : self.name,
            'description' : self.description,
            '_links': {
                'self': url_for('api.get_exerciseDef', id=self.id),
                'exercises': url_for('api.get_exerciseDef_exercises', id=self.id)
            }
        }
    
        return data

    def from_dict(self, data):
        for field in ['name', 'description']:
            if field in data:
                setattr(self, field, data[field])


class Session(MetadataMixin, PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    date = db.Column(db.DateTime, index = True, nullable = True, default = datetime.utcnow)
    exercises = db.relationship('Exercise', backref='session', lazy='dynamic')
    workout_id = db.Column(db.Integer, db.ForeignKey('workout.id'))
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Session Nº {}, with {} exercises, assigned to user: {}'.format(self.id, self.exercises.count(), self.user.username) + '>'

    def to_dict(self):
        data = {
            'id': self.id,
            'date' : self.date,
            'number of exercises': self.exercises.count(),
            '_links': {
                'self': url_for('api.get_session', id=self.id),
                'workout': url_for('api.get_workout', id=self.workout_id) if self.workout_id else None,
                'user': url_for('api.get_user', id=self.user_id),
                'exercises': url_for('api.get_session_exercises', id=self.id)
            }
        }
    
        return data

    def from_dict(self, data):
        for field in ['date', 'user_id', 'workout_id']:
            if field in data:
                setattr(self, field, data[field])


class Exercise(MetadataMixin, PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    session_id = db.Column(db.Integer, db.ForeignKey('session.id'))
    goal_exercise_id = db.Column(db.Integer, db.ForeignKey('goal_exercise.id'))
    name = db.Column(db.String(128))
    done = db.Column(db.Boolean)
    duration = db.Column(db.Integer)
    timestamp = db.Column(db.DateTime, index = True, default = datetime.utcnow)
    sets = db.relationship('Set', backref='exercise', lazy='dynamic')

    exercise_def_id = db.Column(db.Integer, db.ForeignKey('exercise_def.id'))

    def __repr__(self):
        return '<Exercise Nº {} with name {}, DONE = '.format(self.id, self.name) + ('Yes' if self.done else 'No') + '>'

    def to_dict(self):
        data = {
            'id': self.id,
            'name' : self.name,
            'done' : self.done,
            'duration' : self.duration,
            'timestamp' : self.timestamp,
            'number_of_sets': self.sets.count(),
            'total_stats': self.sets_info(),
            '_links': {
                'self': url_for('api.get_routine', id=self.id),
                'session': url_for('api.get_session', id=self.session_id),
                'goal_exercise_id': url_for('api.get_goal_exercise', id=self.goal_exercise_id) if self.goal_exercise_id else None,
                'exerciseDef': url_for('api.get_exerciseDef', id=self.exercise_def_id),
                'sets':url_for('api.get_exercise_sets', id=self.id)
            }
        }
    
        return data

    def from_dict(self, data):
        for field in ['period', 'user_id']:
            if field in data:
                setattr(self, field, data[field])

    def sets_info(self):
        data = {}
        for set in self.sets:
            for key, value in set.set_info().items():
                if value is not None:
                    if key not in data:
                        data[key] = value
                    else:
                        data[key] += value
        
        
        print(data)
        return data



class Set(MetadataMixin, PaginatedAPIMixin, db.Model):
    id = db.Column(db.Integer, primary_key = True)
    exercise_id = db.Column(db.Integer, db.ForeignKey('exercise.id'))
    weight = db.Column(db.Integer)
    reps = db.Column(db.Integer)

    def __repr__(self):
        return '<Set Nº {}, weight lifted: {}, reps done: {}>'.format(self.id, self.weight, self.reps)

    def set_info(self):
        return {
            'weight': self.weight if self.weight else None,
            'reps': self.reps if self.reps else None
        }

    def to_dict(self):
        data = {
            'id': self.id,
            'exercise_id' : self.exercise_id,
            'weight': self.weight,
            'reps':self.reps,
            '_links': {
                'self': url_for('api.get_set', id=self.id),
                'exercise': url_for('api.get_exercise', id=self.exercise_id)
            }
        }
    
        return data

    def from_dict(self, data):
        for field in ['exercise_id', 'weight', 'reps']:
            if field in data:
                setattr(self, field, data[field])