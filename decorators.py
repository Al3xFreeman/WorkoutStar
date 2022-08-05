from datetime import datetime, timedelta

from app.models import PaginatedAPIMixin
import app.api.helpers as helpers
import functools

def daterange(func):

    def wrap_filter_by_date(query, cls, start = datetime.min, end = datetime.utcnow()):
        query = func(query, cls, start, end)
        query = query.filter(cls.timestamp > start).filter(cls.timestamp < end)
        print("Obtaining {} spanning from {} to {}".format(cls.__name__, start, end))
        return query

    return wrap_filter_by_date


def show_deleted(func):
    @functools.wraps(func)
    def wrap_deleted(*args, **kwargs):
        data = func(*args, **kwargs)
        if not hasattr(data, 'deleted'):
            return data
        
        show_deleted = kwargs.get('show_deleted', False)
        if not show_deleted and data.deleted:
            raise Exception("Resource not available")

        return data            

    return wrap_deleted

def show_deleted_query(func):
    @functools.wraps(func)
    def wrap_deleted(*args, **kwargs):
        query = func(args, kwargs)

        try:
            show_deleted = kwargs.get('show_deleted', 'False')
            show_deleted = show_deleted.lower() in ['true', 'True']

            if not show_deleted:
                return query.filter_by(deleted=False)

            return query
        except Exception:
            return query

    return wrap_deleted


def to_dict(func):
    @functools.wraps(func)
    def wrap_to_dict(*args, **kwargs):
        data = func(*args, **kwargs)
        if not hasattr(data, 'to_dict'):
            return data

        to_dict = kwargs.get('to_dict', True)
        #If data returned by func doesnt has 'to_dict' method
        # it the decorator will just return data silently, accompanied by the error
        try:
            if to_dict:
                return data.to_dict()

        except AttributeError as err:
            return data, err
        return data

    return wrap_to_dict

def to_collection_dict(func):
    @functools.wraps(func)
    def wrap_collection_dict(api, *args, **kwargs):
        query = func(*args, **kwargs)
        to_dict = kwargs.get('to_dict', 'True')
        to_dict = to_dict.lower() in ['true', 'True', 'ahá']

        page, per_page = helpers.get_pagination()
        try:
            if to_dict:
                return PaginatedAPIMixin.to_collection_dict(query, page, per_page, api)
        except Exception:
            return query.all()

        return query.all()
    return wrap_collection_dict

#TODO Improve origin of calls and log the time it took (maybe Monads?)
tmp_dict_stats = {}
def stats(func):
    @functools.wraps(func)
    def wrap_stats(*args, **kwargs):
        if func.__name__ not in tmp_dict_stats.keys():
            tmp_dict_stats[func.__name__] = 1
        else:
            tmp_dict_stats[func.__name__] += 1
        
        print("Function stats: ", tmp_dict_stats)     
        print(kwargs.get('origin', 'Unknown'))

        return func(*args, **kwargs)
    return wrap_stats

"""
def pagination(func):
    def wrap_pagination(*args, **kwargs):

    return wrap_pagination
"""
def add(add):
    def decorator_addN(func):
        def wrap_addN(num = 0):
            return func(num) + add
        
        return wrap_addN
    return decorator_addN


def add1(func):
    def wrap_add1(num = 0):
        return func(num) + 1
    return wrap_add1