from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import Routine, Session
from flask import request, url_for


@bp.route('/routines/<int:id>', methods=['GET'])
@token_auth.login_required
def get_routine(id):
    pass

@bp.route('/routines', methods=['POST'])
@token_auth.login_required
def create_routine():
    pass

@bp.route('/routines/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_routine(id):
    pass

@bp.route('/routines/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_routine(id):
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

