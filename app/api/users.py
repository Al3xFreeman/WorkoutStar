from datetime import datetime, timedelta
import json
from app import db
from app.api import bp, helpers
from app.api.errors import bad_request
from app.api.auth import token_auth
from flask import jsonify
from app.model_schemas import UserCreationSchema, UserUpdateSchema
from app.models import ExerciseDef, User, Routine, Session, Exercise, Set
from flask import request, url_for
from sqlalchemy import distinct

userCreationSchema = UserCreationSchema()
userUpdateSchema = UserUpdateSchema()

@bp.route('/users/<int:id>', methods=['GET'])
@token_auth.login_required
def get_user(id):
    return jsonify(User.query.get_or_404(id).to_dict())

@bp.route('/users', methods=['GET'])
@token_auth.login_required
def get_users():
    page, per_page = helpers.get_pagination()
    start, end = helpers.get_date_range()

    query = helpers.helper_date(User.query, User, start, end)

    data = Session.to_collection_dict(query, page, per_page, 'api.get_users')
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
@token_auth.login_required
def update_user(id):
    if token_auth.current_user().id != id:
        return bad_request("User you tried to modify isn't the one logged in!")

    data = request.get_json() or {}
    errors = userUpdateSchema.validate(data)
    if errors:
        return bad_request(errors)


    user = User.query.get_or_404(id)
    
    user.from_dict(data, new_user=False)

    db.session.commit()
    return jsonify(user.to_dict())


@bp.route('/users/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_user(id):
    u = User.query.get_or_404(id)

    if(u.deleted):
        return bad_request("User doesn't exists")

    u.deleted = True
    u.deleted_date = datetime.utcnow()

    db.session.commit()

    return jsonify(u.to_dict())

    
@bp.route('/users/<int:id>/routines', methods=['GET'])
@token_auth.login_required
def get_user_routines(id):

    page, per_page = helpers.get_pagination()
    start, end = helpers.get_date_range()

    u = User.query.get_or_404(id)

    query = helpers.helper_date(u.routines, Routine, start, end)

    data = Session.to_collection_dict(query, page, per_page, 'api.get_routines')
    return jsonify(data)

@bp.route('/users/<int:id>/sessions', methods=['GET'])
@token_auth.login_required
def get_user_sessions(id):
    page, per_page = helpers.get_pagination()
    start, end = helpers.get_date_range()

    u = User.query.get_or_404(id)

    query = helpers.helper_date(u.sessions, Session, start, end)

    data = Session.to_collection_dict(query, page, per_page, 'api.get_sessions')

    return jsonify(data)

@bp.route('/users/<int:id>/exercises', methods=['GET'])
def get_user_exercises(id):
    page, per_page = helpers.get_pagination()
    start, end = helpers.get_date_range()

    ex_list = db.session.query(Exercise).filter(Exercise.session_id == Session.id).filter(Session.user_id == id).filter(Exercise.exercise_def_id == ExerciseDef.id)
    query = helpers.helper_date(ex_list, Exercise, start, end)
    data = Exercise.to_collection_dict(query, page, per_page, 'api.get_exercises')
    print(len(ex_list.all()))
    #data['data'] = 

    return jsonify(data)

@bp.route('/users/<int:id>/exercise_data', methods=['GET'])
def get_user_exercise_data(id):

    exercise = request.args.get("exercise")
    start, end = helpers.get_date_range()

    q = db.session.query(ExerciseDef.name, db.func.count(distinct(Exercise.id)), db.func.sum(Set.weight), db.func.sum(Set.reps)).filter(Exercise.session_id == Session.id).filter(Session.user_id == id).filter(Exercise.exercise_def_id == ExerciseDef.id).filter(Set.exercise_id == Exercise.id)
    query = helpers.helper_date(q, Exercise, start, end)

    if not (data := helpers.exerciseDef_query(query, exercise)):
        return bad_request("Provided exercise doesn't exist")

    data_dict = {}
    for elem in data:
        tmp = {}
        tmp['Number of exercises:'] = elem[1]
        tmp['Total weight'] = elem[2]
        tmp['Total reps'] = elem[3]
        data_dict[elem[0]] = tmp
    return data_dict