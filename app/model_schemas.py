from marshmallow import Schema, fields, validates, ValidationError
from marshmallow.validate import Range
from app.models import User

class RoutineSchema(Schema):
    user_id = fields.Int(required=True)
    period = fields.Int(required=True, validate=Range(min=1))

    @validates('user_id')
    def valid_user_id(self, id):
        if not User.query.get(id):
            raise ValidationError("Not a valid User")