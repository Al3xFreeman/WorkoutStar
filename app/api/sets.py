from flask import jsonify, request, url_for
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from app import db
from app.models import Set
from app.model_schemas import SetSchema
from datetime import datetime, timedelta
import app.api.helpers as helpers

setSchema = SetSchema()


@bp.route('/sets/<int:id>', methods=['GET'])
@token_auth.login_required
def get_set(id):
    return jsonify(Set.query.get_or_404(id).to_dict())


@bp.route('/sets', methods=['GET'])
@token_auth.login_required
def get_sets():
    page, per_page = helpers.get_pagination()
    start, end = helpers.get_date_range()
    query = helpers.helper_date(Set.query , Set, start, end)
    
    data = Set.to_collection_dict(query, page, per_page, 'api.get_sets')

    return jsonify(data)


@bp.route('/sets', methods=['POST'])
@token_auth.login_required
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
@token_auth.login_required
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
@token_auth.login_required
def delete_set(id):
    s = Set.query.get_or_404(id)

    s.deleted = True
    s.deleted_date = datetime.utcnow()

    db.session.commit()

    return jsonify(s.to_dict())