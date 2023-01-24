from flask_restx import Namespace, Resource, fields

auth_namespace = Namespace("auth", description="namespace for authentication")

auth_model = auth_namespace.model(
    'user', {
        'id': fields.Integer(),
        'username': fields.String(required=True, description='A username'),
        'email' : fields.String(required=True, description='An email'),
        'password': fields.String(required=True, description='A password')
    }
)

@auth_namespace.route("/signup")
class Signup(Resource):
    @auth_namespace.expect()
    def post(self):
        """
         Sign up a User
        """
        pass


@auth_namespace.route('/login')
class Login(Resource):
    def post(self):
        """
        Login a User
        """
        pass
    
        
