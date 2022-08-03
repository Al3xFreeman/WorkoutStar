from datetime import datetime, timedelta

def daterange(func):

    def wrap_filter_by_date(query, cls, start = datetime.min, end = datetime.utcnow()):
        query = func(query, cls, start, end)
        query = query.filter(cls.timestamp > start).filter(cls.timestamp < end)
        print("Obtaining {} spanning from {} to {}".format(cls.__name__, start, end))
        return query

    return wrap_filter_by_date


def show_deleted(func):
    def wrap_deleted(*args, **kwargs):
        print("ENTER SHOW DELETED")
        data = func(args, kwargs)
        if not hasattr(data, 'deleted'):
            print("EXIT SHOW DELETED")
            return data
        
        has_show_deleted = 'show_deleted' in kwargs
        if has_show_deleted:
            show_deleted = kwargs['show_deleted']

            if not show_deleted and data.deleted:
                print("EXIT SHOW DELETED")
                return "Resource not available"
            print("EXIT SHOW DELETED")
            return data            

        if data.deleted:
            print("EXIT SHOW DELETED")
            return "Resource not available"
        print("EXIT SHOW DELETED")
        return data

    return wrap_deleted

def show_deleted_query(func):
    def wrap_deleted(*args, **kwargs):
        data = func(args, kwargs)
        
        is_deleted = 'deleted' in kwargs
        if is_deleted:
            deleted = kwargs['deleted']
    return wrap_deleted


def get_dict(func):
    def wrap_to_dict(*args, **kwargs):
        print("ENTER GET DICT")
        data = func(*args, **kwargs)
        if not hasattr(data, 'to_dict'):
            print("EXIT GET DICT")
            return data

        has_to_dict = 'to_dict' in kwargs
        to_dict = kwargs['to_dict']
        #If data returned by func doesnt has 'to_dict' method
        # it the decorator will just return data silently, accompanied by the error
        try:
            if to_dict:
                print("EXIT GET DICT")
                return data.to_dict()

        except AttributeError as err:
            print("EXIT GET DICT")
            return data, err
        print("EXIT GET DICT")
        return data

    return wrap_to_dict

def get_collection_dict(func):
    def wrap_collection_dict(*args, **kwargs):
        data, to_d
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