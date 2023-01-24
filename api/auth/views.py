from http import HTTPStatus

from flask import request
from flask_restx import Namespace, Resource, fields
from werkzeug.security import check_password_hash, generate_password_hash

from ..models.users import User
from ..utils import db

auth_namespace = Namespace("auth", description="namespace for authentication")

signup_model = auth_namespace.model(
    "SignUp",
    {
        "username": fields.String(required=True, description="A username"),
        "email": fields.String(required=True, description="An email"),
        "password": fields.String(required=True, description="A password"),
    },
)

user_model = auth_namespace.model(
    "User",
    {
        'id': fields.Integer(),
        "username": fields.String(required=True, description="A username"),
        "email": fields.String(required=True, description="An email"),
        "password_hash": fields.String(required=True, description="A password"),
        "is_active": fields.Boolean(description="This shows if a user is active or not"),
        "is_staff": fields.Boolean(description="This shows if the user is a staff or not"),
    },
)


@auth_namespace.route("/signup")
class Signup(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(user_model)
    def post(self):
        """
        Sign up a User
        """
        data = request.get_json()

        new_user = User(
            username=data.get("username"),
            email=data.get("email"),
            password_hash=generate_password_hash(data.get("password")),
        )

        new_user.save()

        return new_user, HTTPStatus.CREATED


@auth_namespace.route("/login")
class Login(Resource):
    def post(self):
        """
        Login a User
        """
        pass
