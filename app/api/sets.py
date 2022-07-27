from flask import jsonify, request, url_for
from app.api import bp
from app.api.errors import bad_request
from app import db
from app.models import Set
from app.model_schemas import SetSchema

setSchema = SetSchema()


@bp.route('/sets/<int:id>', methods=['GET'])
def get_set(id):
    return jsonify(Set.query.get_or_404(id).to_dict())


@bp.route('/sets', methods=['GET'])
def get_sets():
    page = request.args.get('page', 1, type=int)
    per_page = min(request.args.get('per_page', 10, type=int), 100)

    data = Set.to_collection_dict(Set.query, page, per_page, 'api.get_sets')

    return jsonify(data)


@bp.route('/sets', methods=['POST'])
def create_set():

    data = request.get_json() or {}
    errors = setSchema.validate(data)
    if errors:
        return bad_request(errors)

    set = Set()
    set.from_dict(data)

    db.session.add(set)
    db.session.commit()

    response = jsonify(set.to_dict())
    response.status_code = 201
    response.headers['Location'] = url_for('api.get_set', id = set.id)

    return response


@bp.route('/sets/<int:id>', methods=['PUT'])
def update_set(id):
    
    data = request.get_json() or {}
    errors = setSchema.validate(data)
    if errors:
        return bad_request(errors)

    set = Set.query.get_or_404(id)
    set.from_dict(data)

    db.session.commit()

    return jsonify(set.to_dict())

@bp.route('sets/<int:id>', methods=['DELETE'])
def delete_set(id):
    pass