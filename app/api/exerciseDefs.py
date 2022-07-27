from click import BadArgumentUsage
from flask import jsonify, request, url_for
from app.model_schemas import ExerciseDefSchema
from app.models import Exercise, ExerciseDef
from app.api import bp
from app import db
from app.api.errors import bad_request

exerciseDefSchema = ExerciseDefSchema()

@bp.route('/exerciseDefs/<int:id>', methods=['GET'])
def get_exerciseDef(id):
    return jsonify(ExerciseDef.query.get_or_404(id).to_dict())


@bp.route('/exerciseDefs', methods=['GET'])
def get_exerciseDefs():
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    data = ExerciseDef.to_collection_dict(ExerciseDef.query, page, per_page, 'api.get_exerciseDefs')

    return jsonify(data)

@bp.route('/exerciseDefs', methods=['POST'])
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
    response['Location'] = url_for('api.get_exerciseDef', id = ex_def.id)

    return response

@bp.route('/exerciseDefs/<int:id>', methods=['PUT'])
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
def delete_exerciseDef(id):
    pass


@bp.route('exerciseDefs/<int:id>/exercises', methods=['GET'])
def get_exerciseDef_exercises(id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    ex_def = ExerciseDef.query.get_or_404(id)
    data = ExerciseDef.to_collection_dict(ex_def.exercises, page, per_page, 'api.get_exercises')

    return data