from flask_restx import Namespace, Resource

auth_namespace = Namespace("auth", description="namespace for authentication")

@auth_namespace.route("/signup")
class Signup(Resource):
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
    
        
