"""

db.session.query(ExerciseDef.name, db.func.count(distinct(Exercise.id)), db.func.sum(Set.weight), db.func.sum(Set.reps)).join(Exercise, ExerciseDef.id == Exercise.exercise_def_id).join(Session, Session.id == Exercise.session_id).join(User, User.id ==Session.user_id).outerjoin(Set, Set.exercise_id == Exercise.id).group_by(ExerciseDef.id).filter(User.id==1, Exercise.done==True).all()

"""

from flask import jsonify, request, url_for
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from app.model_schemas import ExerciseSchema
from app.models import Exercise
from app import db
from datetime import datetime


exerciseSchema = ExerciseSchema()

@bp.route('/exercises/<int:id>', methods=['GET'])
@token_auth.login_required
def get_exercise(id):
    return jsonify(Exercise.query.get_or_404(id).to_dict())


@bp.route('/exercises', methods=['GET'])
@token_auth.login_required
def get_exercises():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    data = Exercise.to_collection_dict(Exercise.query, page, per_page, 'api.get_exercises')

    return jsonify(data)


@bp.route('/exercises', methods=['POST'])
@token_auth.login_required
def create_exercise():

    data = request.get_json() or {}
    errors = exerciseSchema.validate(data)
    if errors:
        return bad_request(errors)

    exercise = Exercise()
    exercise.from_dict(data)

    db.session.add(exercise)
    db.session.commit()

    response = jsonify(exercise.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_exercise', id = exercise.id)

    return response


@bp.route('/exercise/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_exercise(id):
    data = request.get_json() or {}
    errors = exerciseSchema.validate(data)
    if errors:
        return bad_request(errors)

    exercise = Exercise.query.get_or_404(id)
    exercise.from_dict(data)

    db.session.commit()

    return jsonify(exercise.to_dict())


@bp.route('/exercises/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_exercise(id):
    ex = Exercise.query.get_or_404(id)

    ex.deleted = True
    ex.deleted_date = datetime.utcnow()

    db.session.commit()

    return jsonify(ex.to_dict())

@bp.route('/exercises/<int:id>/sets', methods=['GET'])
@token_auth.login_required
def get_exercise_sets(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    ex = Exercise.query.get_or_404(id)
    data = Exercise.to_collection_dict(ex.sets, page, per_page, 'api.get_sets')

    return data