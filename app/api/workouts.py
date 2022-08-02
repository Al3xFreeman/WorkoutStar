from app import db
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from flask import jsonify
from app.models import Workout, ExerciseDef, User, Routine, Session, Exercise, Set
from flask import request, url_for
from app.model_schemas import WorkoutSchema
from datetime import datetime, timedelta
from sqlalchemy import distinct
import app.api.helpers as helpers

workoutSchema = WorkoutSchema()

@bp.route('/workouts/<int:id>', methods=['GET'])
@token_auth.login_required
def get_workout(id):
    return jsonify(Workout.query.get_or_404(id).to_dict())

@bp.route('/workouts/<int:id>/sessions', methods=['GET'])
@token_auth.login_required
def get_workout_sessions(id):    
    page, per_page = helpers.get_pagination()
    start, end = helpers.get_date_range()

    workout = Workout.query.get_or_404(id)

    query = helpers.helper_date(workout.sessions , Session, start, end)
    
    data = Session.to_collection_dict(query, page, per_page, 'api.get_sessions')


    return jsonify(data)

@bp.route('/workouts', methods=['GET'])
@token_auth.login_required
def get_workouts():
    page, per_page = helpers.get_pagination()
    start, end = helpers.get_date_range()
    query = helpers.helper_date(Workout.query, Workout, start, end)
    
    data = Session.to_collection_dict(query, page, per_page, 'api.get_workouts')

    return jsonify(data)

@bp.route('/workouts', methods=['POST'])
@token_auth.login_required
def create_workout():
    data = request.get_json() or {}
    errors = workoutSchema.validate(data)
    if errors:
        return bad_request(errors)

    workout = Workout()
    workout.from_dict(data)

    db.session.add(workout)
    db.session.commit()

    response = jsonify(workout.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_workout', id=workout.id)

    return response

@bp.route('/workouts/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_workout(id):
    data = request.get_json() or {}
    errors = workoutSchema.validate(data)
    if errors:
        return bad_request(errors)

    w = Workout.query.get_or_404(id)
    w.from_dict(data)

    db.session.commit()


@bp.route('/workouts/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_workout(id):
    w = Workout.query.get_or_404(id)

    w.deleted = True
    w.deleted_date = datetime.utcnow()

    db.session.commit()

    return jsonify(w.to_dict())


@bp.route('/workouts/<int:id>/exercises', methods=['GET'])
def get_workout_exercises(id):
    workout = Workout.query.get_or_404(id)
    
    page, per_page = helpers.get_pagination()
    start, end = helpers.get_date_range()
    query_1 = db.session.query(Exercise).filter(Exercise.session_id == Session.id).filter(Workout.id == Session.workout_id).filter(Workout.id == id)
    query = helpers.helper_date(query_1, Exercise, start, end)
    
    data = Exercise.to_collection_dict(query, page, per_page, 'api.get_exercises')

    return jsonify(data)
    
@bp.route('/workouts/<int:id>/exercises/data', methods=['GET'])
def get_workout_exercises_data(id):
    workout = Workout.query.get_or_404(id)
    
    start, end = helpers.get_date_range()

    q = db.session.query(ExerciseDef.name, db.func.count(distinct(Exercise.id)), db.func.sum(Set.weight), db.func.sum(Set.reps)).filter(Workout.id == id).filter(Session.workout_id == Workout.id).filter(Exercise.session_id == Session.id).filter(Set.exercise_id == Exercise.id).filter(Exercise.exercise_def_id == ExerciseDef.id).group_by(ExerciseDef.id)
    data = helpers.helper_date(q, Exercise, start, end).all()

    data_dict = {}
    for elem in data:
        tmp = {}
        tmp['Number of exercises:'] = elem[1]
        tmp['Total weight'] = elem[2]
        tmp['Total reps'] = elem[3]
        data_dict[elem[0]] = tmp
    return data_dict
