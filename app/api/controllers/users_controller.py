from app.models import User
import decorators

@decorators.get_dict
@decorators.show_deleted
def get_user(id, *args, **kwargs):
    print(kwargs)
    u = User.query.get_or_404(id)
    return u

@decorators.get_collection_dict
@decorators.show_deleted_query
def get_user_collection(api, *args, **kwargs):
    u = User.query
    return u
