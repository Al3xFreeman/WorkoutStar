import json
from os import abort
from urllib import response
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from flask import jsonify
from app.models import Workout, Session
from flask import request, url_for
from app.model_schemas import WorkoutSchema

workoutSchema = WorkoutSchema()

@bp.route('/workouts/<int:id>', methods=['GET'])
#@token_auth.login_required
def get_workout(id):
    return jsonify(Workout.query.get_or_404(id).to_dict())

@bp.route('/workouts/<int:id>/sessions', methods=['GET'])
#@token_auth.login_required
def get_workout_sessions(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    workout = Workout.query.get_or_404(id)
    data = Workout.to_collection_dict(workout.sessions, page, per_page, 'api.get_sessions')

    return jsonify(data)

@bp.route('/workouts', methods=['GET'])
#@token_auth.login_required
def get_workouts():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    data = Workout.to_collection_dict(Workout.query, page, per_page, 'api.get_workouts')

    return jsonify(data)

@bp.route('/workouts', methods=['POST'])
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
def update_workout(id):
    data = request.get_json() or {}
    errors = workoutSchema.validate(data)
    if errors:
        return bad_request(errors)

    w = Workout.query.get_or_404(id)
    w.from_dict(data)

    db.session.commit()


@bp.route('/workouts/<int:id>', methods=['DELETE'])
def delete_workout(id):
    pass

