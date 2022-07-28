from datetime import datetime
from os import abort
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from flask import jsonify
from app.model_schemas import UserCreationSchema
from app.models import User, Routine, Session
from flask import request, url_for

userCreationSchema = UserCreationSchema()

@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users', methods=['GET'])
#@token_auth.login_required
def get_users():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    data = User.to_collection_dict(User.query, page, per_page, 'api.get_users')

    return jsonify(data)

@bp.route('/users', methods=['POST'])
def create_user():

    data = request.get_json() or {}
    errors = userCreationSchema.validate(data)
    if errors:
        return bad_request(errors)

    user = User()
    user.from_dict(data, new_user=True)
    db.session.add(user)
    db.session.commit()


    response = jsonify(user.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_user', id=user.id)

    return response

@bp.route('/users/<int:id>', methods=['PUT'])
#@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        abort(403)

    data = request.get_json() or {}
    errors = userCreationSchema.validate(data)
    if errors:
        return bad_request(errors)


    user = User.query.get_or_404(id)
    
    user.from_dict(data, new_user=False)

    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/users/<int:id>', methods=['DELETE'])
def delete_user(id):
    u = User.query.get_or_404(id)

    u.deleted = True
    u.deleted_date = datetime.utcnow()

    db.session.commit()

    return jsonify(u.to_dict())

    
@bp.route('/users/<int:id>/routines', methods=['GET'])
def get_user_routines(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    u = User.query.get_or_404(id)

    data = Routine.to_collection_dict(u.routines, page, per_page, 'api.get_routines')

    return jsonify(data)

@bp.route('/users/<int:id>/sessions', methods=['GET'])
def get_user_sessions(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    u = User.query.get_or_404(id)

    data = Session.to_collection_dict(u.sessions, page, per_page, 'api.get_sessions')

    return jsonify(data)