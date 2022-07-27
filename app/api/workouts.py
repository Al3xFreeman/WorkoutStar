from os import abort
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from flask import jsonify
from app.models import Workout
from flask import request, url_for

@bp.route('/workouts/<int:id>', methods=['GET'])
@token_auth.login_required
def get_workout(id):
    return jsonify(Workout.query.get_or_404(id).to_dict())
