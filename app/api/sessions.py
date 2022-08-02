import json
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.model_schemas import SessionSchema
from app.models import Exercise, Session, ExerciseDef, Set
from flask import jsonify, request, url_for
from datetime import datetime, timedelta
from sqlalchemy import distinct
import app.api.helpers as helpers
sessionSchema = SessionSchema()

@bp.route('/sessions/<int:id>', methods=['GET'])
@token_auth.login_required
def get_session(id):
    return jsonify(Session.query.get_or_404(id).to_dict())

@bp.route('/sessions', methods=['GET'])
@token_auth.login_required
def get_sessions():
    page, per_page = helpers.get_pagination()
    start, end = helpers.get_date_range()
    query = helpers.helper_date(Session.query , Session, start, end)
    
    data = Session.to_collection_dict(query, page, per_page, 'api.get_sessions')

    return jsonify(data)

@bp.route('/sessions', methods=['POST'])
@token_auth.login_required
def create_session():
    data = request.get_json() or {}
    errors = sessionSchema.validate(data)
    if errors:
        return bad_request(errors)

    session = Session()
    session.from_dict(data)

    db.session.add(session)
    db.session.commit()

    response = jsonify(session.to_dict())
    response.status_code(201)
    response.headers['Location'] = url_for('api.get_session', id = session.id)

    return response

@bp.route('/sessions/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_session(id):
    data = request.get_json() or {}
    errors = sessionSchema.validate(data)
    if errors:
        return bad_request(errors)
    
    s = Session.query.get_or_404(id)
    s.from_dict(data)

    db.session.commit()

    return jsonify(s.to_dict())

@bp.route('/sessions/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_session(id):
    s = Session.query.get_or_404(id)

    s.deleted = True
    s.deleted_date = datetime.utcnow()

    db.session.commit()

    return jsonify(s.to_dict())
@bp.route('/sessions/<int:id>/exercises', methods=['GET'])
@token_auth.login_required
def get_session_exercises(id):
    session = Session.query.get_or_404(id)
    page, per_page = helpers.get_pagination()
    start, end = helpers.get_date_range()

    query = helpers.helper_date(session.exercises , Exercise, start, end)
    
    data = Exercise.to_collection_dict(query, page, per_page, 'api.get_exercises')

    return jsonify(data)

@bp.route('/sessions/<int:id>/exercises/data', methods=['GET'])
@token_auth.login_required
def get_session_exercises_data(id):
    session = Session.query.get_or_404(id)
    start, end = helpers.get_date_range()

    q = db.session.query(ExerciseDef.name, db.func.count(distinct(Exercise.id)), db.func.sum(Set.weight), db.func.sum(Set.reps)).filter(Exercise.session_id == id).filter(Exercise.exercise_def_id == ExerciseDef.id).filter(Set.exercise_id == Exercise.id).group_by(ExerciseDef.id)
    data = helpers.helper_date(q, Exercise, start, end).all()

    data_dict = {}
    for elem in data:
        tmp = {}
        tmp['Number of exercises:'] = elem[1]
        tmp['Total weight'] = elem[2]
        tmp['Total reps'] = elem[3]
        data_dict[elem[0]] = tmp
    return data_dict


@bp.route('/sessions/<int:id>', methods=['POST', 'PUT'])
@token_auth.login_required
def add_session_exercise(id):
    pass

@bp.route('/sessions/<int:session_id>/<int:exercise_id>', methods=['DELETE', 'PUT'])
@token_auth.login_required
def remove_session_exercise(session_id, exercise_id):
    pass
