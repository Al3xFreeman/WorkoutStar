from os import abort
from app import db
from app.api import bp
from app.api.errors import bad_request
from app.api.auth import token_auth
from flask import jsonify
from app.models import Workout, Session
from flask import request, url_for

@bp.route('/workouts/<int:id>', methods=['GET'])
#@token_auth.login_required
def get_workout(id):
    return jsonify(Workout.query.get_or_404(id).to_dict())

@bp.route('/workouts/<int:id>/sessions')
def get_workout_sessions(id):
    page = request.args.get('page', 1, type=int)
    per_page = request.args.get('per_page', 10, type=int)

    workout = Workout.query.get_or_404(id)
    data = Workout.to_collection_dict(workout.sessions, page, per_page, 'api.get_sessions')

    return jsonify(data)