from flask import request
from flask_restx import Namespace, Resource, fields
from ..models.users import User
from ..utils import db
from werkzeug.security import generate_password_hash, check_password_hash
from http import HTTPStatus
auth_namespace = Namespace("auth", description="namespace for authentication")

signup_model = auth_namespace.model(
    'user', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description='A username'),
        'email' : fields.String(required=True, description='An email'),
        'password': fields.String(required=True, description='A password')
    }
)

@auth_namespace.route("/signup")
class Signup(Resource):
    @auth_namespace.expect(signup_model)
    @auth_namespace.marshal_with(signup_model)
    def post(self):
        """
         Sign up a User
        """
        data = request.get_json()

        new_user = User(
            username = data.get('username'),
            email = data.get('email'),
            password = generate_password_hash(data.get('password'))
        )

        new_user.save()

        return new_user, HTTPStatus.CREATED
        


@auth_namespace.route('/login')
class Login(Resource):
    def post(self):
        """
        Login a User
        """
        pass
    
        
