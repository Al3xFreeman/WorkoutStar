import json
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.model_schemas import SessionSchema
from app.models import Exercise, Session
from flask import jsonify, request, url_for

sessionSchema = SessionSchema()

@bp.route('/sessions/<int:id>', methods=['GET'])
#@token_auth.login_required
def get_session(id):
    return jsonify(Session.query.get_or_404(id).to_dict())

@bp.route('/sessions', methods=['GET'])
@token_auth.login_required
def get_sessions():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    data = Session.to_collection_dict(Session.query, page, per_page, 'api.get_sessions')

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
    response['Location'] = url_for('api.get_session', id = session.id)

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
    pass

@bp.route('/sessions/<int:id>/exercises', methods=['GET'])
@token_auth.login_required
def get_session_exercises(id):
    pass

@bp.route('/sessions/<int:id>', methods=['POST', 'PUT'])
@token_auth.login_required
def add_session_exercise(id):
    pass

@bp.route('/sessions/<int:session_id>/<int:exercise_id>', methods=['DELETE', 'PUT'])
@token_auth.login_required
def remove_session_exercise(session_id, exercise_id):
    pass
