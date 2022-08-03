from app.models import User
import decorators

@decorators.get_dict
def get_user(id, to_dict = False):
    u = User.query.get_or_404(id)
    return u, to_dict


def get_user_collection(to_dict = False):
    u = User.query
