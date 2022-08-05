from datetime import datetime
from app.models import User
from app import db
import decorators


from app.model_schemas import UserCreationSchema, UserUpdateSchema

userCreationSchema = UserCreationSchema()
userUpdateSchema = UserUpdateSchema()

@decorators.stats
@decorators.to_dict
@decorators.show_deleted
def get_user(id, *args, **kwargs):
    u = User.query.get_or_404(id)
    return u

@decorators.stats
@decorators.to_collection_dict
@decorators.show_deleted_query
def get_user_collection(api, *args, **kwargs):
    u = User.query
    return u

@decorators.stats
@decorators.to_dict
def create_user(data, *args, **kwargs):
    errors = userCreationSchema.validate(data)
    if errors:
        raise Exception(errors)

    u = User()
    u.from_dict(data, new_user=True)
    db.session.add(u)
    db.session.commit()

    return u

@decorators.stats
@decorators.to_dict
def update_user(id, data, *args, **kwargs):
    errors = userUpdateSchema.validate(data)
    if errors:
        raise Exception(errors)

    u = get_user(id, to_dict=False, *args, **kwargs)
    u.from_dict(data, new_user=False)

    db.session.commit()

    return u

@decorators.stats
@decorators.to_dict
def delete_user(id, *args, **kwargs):
    u = get_user(id, to_dict=False, *args, **kwargs)
    u.deleted = True
    u.deleted_date = datetime.utcnow()
    db.session.commit()

    return u

@decorators.stats
@decorators.to_dict
def recover_user(id, *args, **kwargs):
    u = get_user(id, to_dict=False, show_deleted=True, *args, **kwargs)
    u.deleted = False
    u.deleted_date = None
    db.session.commit()

    return u
