from datetime import datetime, timedelta

def daterange(func):

    def wrap_filter_by_date(query, cls, start = datetime.min, end = datetime.utcnow()):
        query = func(query, cls, start, end)
        query = query.filter(cls.timestamp > start).filter(cls.timestamp < end)
        print("Obtaining {} spanning from {} to {}".format(cls.__name__, start, end))
        return query

    return wrap_filter_by_date

def get_dict(func):
    def wrap_to_dict(*args, **kwargs):
        data, to_dict = func(*args, **kwargs)
        
        #If data returned by func doesnt has 'to_dict' method
        # it the decorator will just return data silently, accompanied by the error
        try:
            if to_dict:
                return data.to_dict()
                
        except AttributeError as err:
            return data, err

        return data

    return wrap_to_dict

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