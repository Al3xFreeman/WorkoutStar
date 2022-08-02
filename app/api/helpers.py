from datetime import datetime
import decorators
from flask import request
from app.models import ExerciseDef
from app.api.errors import bad_request


#@decorators.daterange
def helper_date(query, cls, start = datetime.min, end = datetime.utcnow()):
    if not hasattr(cls, 'created_at'):
        return query

    query = query.filter(cls.created_at > start).filter(cls.created_at < end)
    print("Obtaining {} spanning from {} to {}".format(cls.__name__, start, end))
    return query


def get_pagination(page = 1, per_page = 10):
    _page = request.args.get('page', page, type=int)
    _per_page = min(request.args.get('per_page', per_page, type=int), 100)

    return _page, _per_page


def get_date_range(start = datetime.min, end = datetime.utcnow()):
    _start = request.args.get('from', start, type=datetime)
    _end = request.args.get('to', end, type=datetime)

    return _start, _end

def exerciseDef_query(query, exercise):
    if exercise:
        if not ExerciseDef.query.filter_by(name=exercise).first():
            return False
        data = query.filter(ExerciseDef.name == exercise).all()
    else:    
        data = query.group_by(ExerciseDef.id).all()

    return data