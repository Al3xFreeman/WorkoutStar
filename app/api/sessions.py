from app import db
from app.api import bp
from app.api.auth import token_auth
from app.api.errors import bad_request
from app.models import Exercise, Session
from flask import request, url_for


@bp.route('/session/<int:id>', methods=['GET'])
@token_auth.login_required
def get_session(id):
    pass

@bp.route('/session', methods=['POST'])
@token_auth.login_required
def create_session():
    pass

@bp.route('/session/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_session(id):
    pass

@bp.route('/session/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_session(id):
    pass

@bp.route('/session/<int:id>/exercises', methods=['GET'])
@token_auth.login_required
def get_exercises(id):
    pass

@bp.route('/session/<int:id>', methods=['POST', 'PUT'])
@token_auth.login_required
def add_exercise(id):
    pass

@bp.route('/session/<int:session_id>/<int:exercise_id', methods=['DELETE', 'PUT'])
@token_auth.login_required
def remove_exercise(session_id, exercise_id):
    pass
