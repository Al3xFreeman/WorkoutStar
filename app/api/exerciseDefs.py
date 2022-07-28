from click import BadArgumentUsage
from flask import jsonify, request, url_for
from app.model_schemas import ExerciseDefSchema
from app.models import Exercise, ExerciseDef
from app.api import bp
from app import db
from app.api.errors import bad_request
from app.api.auth import token_auth
from datetime import datetime

exerciseDefSchema = ExerciseDefSchema()

@bp.route('/exerciseDefs/<int:id>', methods=['GET'])
@token_auth.login_required
def get_exerciseDef(id):
    return jsonify(ExerciseDef.query.get_or_404(id).to_dict())


@bp.route('/exerciseDefs', methods=['GET'])
@token_auth.login_required
def get_exerciseDefs():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    data = ExerciseDef.to_collection_dict(ExerciseDef.query, page, per_page, 'api.get_exerciseDefs')

    return jsonify(data)

@bp.route('/exerciseDefs', methods=['POST'])
@token_auth.login_required
def create_exerciseDef():

    data = request.get_json() or {}
    errors = exerciseDefSchema.validate(data)
    if errors:
        return bad_request(errors)

    ex_def = ExerciseDef()
    ex_def.from_dict(data)

    db.session.add(ex_def)
    db.session.commit()

    response = jsonify(ex_def.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_exerciseDef', id = ex_def.id)

    return response

@bp.route('/exerciseDefs/<int:id>', methods=['PUT'])
@token_auth.login_required
def update_exerciseDef(id):

    data = request.get_json() or {}
    errors = exerciseDefSchema.validate(data)
    if errors:
        return bad_request(errors)

    ex_def = ExerciseDef.get_or_404(id)
    ex_def.from_dict(data)

    db.session.commit()

    return jsonify(ex_def.to_dict())



@bp.route('/exerciseDefs/<int:id>', methods=['DELETE'])
@token_auth.login_required
def delete_exerciseDef(id):
    ex_def = ExerciseDef.query.get_or_404(id)

    ex_def.deleted = True
    ex_def.deleted_date = datetime.utcnow()

    db.session.commit()

    return jsonify(ex_def.to_dict())


@bp.route('/exerciseDefs/<int:id>/exercises', methods=['GET'])
@token_auth.login_required
def get_exerciseDef_exercises(id):
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    ex_def = ExerciseDef.query.get_or_404(id)
    data = ExerciseDef.to_collection_dict(ex_def.exercises, page, per_page, 'api.get_exercises')

    return data