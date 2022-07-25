from os import abort
from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import Routine, Session, User
from flask import jsonify, request, url_for


@bp.route('/routines/<int:id>', methods=['GET'])
@token_auth.login_required
def get_routine(id):
    return jsonify(Routine.query.get_or_404(id).to_dict())


@bp.route('/routines', methods=['GET'])
@token_auth.login_required
def get_routines():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    data = Routine.to_collection_dict(Routine.query, page, per_page, 'api.get_routines')

    return jsonify(data)

@bp.route('/routines', methods=['POST'])
@token_auth.login_required
def create_routine():
    data = request.get_json() or {}
    if 'user_id' not in data or 'period' not in data:
        return bad_request('Must specify a valid user id and a period for the routine')
    u = User.query.get(data['user_id'])
    if u == None:
        return bad_request('Please use a valid user_id')
    
    routine = Routine(user=u, period=data['period'])
    routine.from_dict(data)

    db.session.add(routine)
    db.session.commit()

@bp.route('/routines/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_routine(id):
    r = Routine.query.get_or_404(id)
    #if token_auth.current_user().id != r.user_id:
    #    abort(403)
    
    data = request.get_json() or {}    
    
    if 'user_id' in data:
        u = User.query.get_or_404(data['user_id'])
        r.user_id = data['user_id']
    if 'period' in data and int(data['period']):
        r.period = data['period']

    db.session.commit()
    return jsonify(r.to_dict())

@bp.route('/routines/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_routine(id):
    pass

@bp.route('/routines/<int:id>/user', methods=['GET'])
@token_auth.login_required
def get_routine_user(id):
    pass

@bp.route('/routines/<int:id>/sessions', methods=['GET'])
@token_auth.login_required
def get_sessions(id):
    pass

@bp.route('/routines/<int:routine_id>', methods=['POST', 'PUT'])
@token_auth.login_required
def add_session(id):
    pass

@bp.route('/routines/<int:routine_id>/<int:session_id>', methods=['PUT', 'DELETE'])
@token_auth.login_required
def remove_session(routine_id, session_id):
    pass

@bp.route('/routines/<int:id>/workouts', methods=['GET'])
def get_routine_workouts(id):
    pass