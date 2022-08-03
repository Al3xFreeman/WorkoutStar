from datetime import datetime, timedelta

from app.models import PaginatedAPIMixin
import app.api.helpers as helpers

def daterange(func):

    def wrap_filter_by_date(query, cls, start = datetime.min, end = datetime.utcnow()):
        query = func(query, cls, start, end)
        query = query.filter(cls.timestamp > start).filter(cls.timestamp < end)
        print("Obtaining {} spanning from {} to {}".format(cls.__name__, start, end))
        return query

    return wrap_filter_by_date


def show_deleted(func):
    def wrap_deleted(*args, **kwargs):
        print("ENTER DELETED")
        data = func(*args, **kwargs)
        if not hasattr(data, 'deleted'):
            return data
        
        show_deleted = kwargs.get('show_deleted', False)
        if not show_deleted and data.deleted:
            print("EXIT DELETED")
            return "Resource not available"

        print("EXIT DELETED")
        return data            

    return wrap_deleted

def show_deleted_query(func):
    def wrap_deleted(*args, **kwargs):
        query = func(args, kwargs)
        print(kwargs)

        try:
            show_deleted = kwargs.get('show_deleted', 'False')
            show_deleted = show_deleted.lower() in ['true', 'True']

            if not show_deleted:
                return query.filter_by(deleted=False)

            return query
        except Exception:
            return query

    return wrap_deleted


def get_dict(func):
    def wrap_to_dict(*args, **kwargs):
        print("ENTER DICT")
        data = func(*args, **kwargs)
        if not hasattr(data, 'to_dict'):
            return data

        to_dict = kwargs.get('to_dict', True)
        #If data returned by func doesnt has 'to_dict' method
        # it the decorator will just return data silently, accompanied by the error
        try:
            if to_dict:
                print("EXIT DICT")
                return data.to_dict()

        except AttributeError as err:
            return data, err
        return data

    return wrap_to_dict

def get_collection_dict(func):
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