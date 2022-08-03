from app.models import User
import decorators

@decorators.get_dict
@decorators.show_deleted
def get_user(id, *args, **kwargs):
    u = User.query.get_or_404(id)
    return u


def get_user_collection(to_dict = False):
    u = User.query
