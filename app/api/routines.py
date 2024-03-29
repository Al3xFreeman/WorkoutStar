from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import Routine, User, Workout
from flask import jsonify, request, url_for
from app.model_schemas import RoutineSchema
from datetime import datetime
from app.api.workouts import get_workout_exercises_data
import app.api.helpers as helpers

routineSchema = RoutineSchema()


@bp.route('/routines/<int:id>', methods=['GET'])
@token_auth.login_required
def get_routine(id):
    return jsonify(Routine.query.get_or_404(id).to_dict())


@bp.route('/routines', methods=['GET'])
@token_auth.login_required
def get_routines():
    page, per_page = helpers.get_pagination()
    start, end = helpers.get_date_range()
    query = helpers.helper_date(Routine.query , Routine, start, end)
    
    data = Routine.to_collection_dict(query, page, per_page, 'api.get_routines')

    return jsonify(data)

@bp.route('/routines', methods=['POST'])
@token_auth.login_required
def create_routine():
    
    data = request.get_json() or {}
    errors = routineSchema.validate(data)
    if errors:
        return bad_request(errors)

    routine = Routine()
    routine.from_dict(data)

    db.session.add(routine)
    db.session.commit()

    response = jsonify(routine.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_routine', id = routine.id)

    return response

@bp.route('/routines/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_routine(id):
    
    # TODO: Make policy for who can modify what resource

    #if token_auth.current_user().id != r.user_id:
    #    abort(403)
    
    data = request.get_json() or {}
    errors = routineSchema.validate(data)
    if errors:
        return bad_request(errors)

    r = Routine.query.get_or_404(id)
    r.from_dict(data)

    db.session.commit()
    
    return jsonify(r.to_dict())

@bp.route('/routines/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_routine(id):
    r = Routine.query.get_or_404(id)

    r.deleted = True
    r.deleted_date = datetime.utcnow()

    db.session.commit()

    return jsonify(r.to_dict())
    
"""
@bp.route('/routines/<int:id>/sessions', methods=['GET'])
@token_auth.login_required
def get_routine_sessions(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    r = Routine.query.get_or_404(id)

    data = Session.to_collection_dict(r.sessions, page, per_page, 'api.get_sessions')

    return jsonify(data)
"""
@bp.route('/routines/<int:routine_id>', methods=['POST', 'PUT'])
@token_auth.login_required
def add_routine_session(id):
    pass

@bp.route('/routines/<int:routine_id>/<int:session_id>', methods=['PUT', 'DELETE'])
@token_auth.login_required
def remove_routine_session(routine_id, session_id):
    pass

@bp.route('/routines/<int:id>/workouts', methods=['GET'])
@token_auth.login_required
def get_routine_workouts(id):
    page, per_page = helpers.get_pagination()
    start, end = helpers.get_date_range()

    r = Routine.query.get_or_404(id)

    query = helpers.helper_date(r.workouts , Workout, start, end)
    
    data = Routine.to_collection_dict(query, page, per_page, 'api.get_routine_workouts', id=id)

    return jsonify(data)


@bp.route('/routines/<int:id>/extended', methods=['GET'])
def get_routine_info_extended(id):
    routine = Routine.query.get_or_404(id)

    data = {}

    r_works = routine.workouts.all()
    for workout in r_works:
        w_data = get_workout_exercises_data(workout.id)
        for key, value in w_data.items():
            if key not in data:
                data[key] = value
            else:
                for key_1, value_1 in value.items():
                    data[key][key_1] += value_1

    #data['workouts'] = 
    return data