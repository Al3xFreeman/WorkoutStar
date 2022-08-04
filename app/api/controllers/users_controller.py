from app.models import User
from app import db
import decorators


from app.model_schemas import UserCreationSchema, UserUpdateSchema

userCreationSchema = UserCreationSchema()
userUpdateSchema = UserUpdateSchema()

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

@decorators.get_dict
def create_user(data, *args, **kwargs):
    errors = userCreationSchema.validate(data)
    if errors:
        return False
    u = User()
    u.from_dict(data, new_user=True)
    db.session.add(u)
    db.session.commit()

    return u