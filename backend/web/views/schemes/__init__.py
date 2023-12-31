from marshmallow import Schema, fields


class OkResponseSchema(Schema):
    status = fields.Str()
    data = fields.Dict()


class LoginSchema(Schema):
    login = fields.Str(required=True)
    password = fields.Str(required=True)
