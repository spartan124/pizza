import pathlib

from flask import Flask
from flask_jwt_extended import JWTManager
from flask_jwt_extended.exceptions import JWTExtendedException
from flask_migrate import Migrate
from flask_restx import Api
from werkzeug.exceptions import MethodNotAllowed, NotFound

from .auth.views import auth_namespace as ans
from .config.config import config_dict
from .models.orders import Order
from .models.users import User
from .orders.views import order_namespace as ons
from .utils import db


def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)
    app.config.from_pyfile(pathlib.Path(__file__).parent / "config/config.py")

    
    db.init_app(app)
    jwt = JWTManager()
    jwt.init_app(app)

    migrate = Migrate(app, db)
    authorizations= {
        "Bearer Auth": {
            'type': 'apiKey',
            'in':'header',
            'name':'Authorization',
            'description': 'Add a JWT token to the header with ** Bearer &lt;JWT&gt; token to authorize **'
        }
    }

    api = Api(app,
              title='Pizza Delivery API',
              description='A simple pizza delivery REST API service',
              authorizations=authorizations,
              security='Bearer Auth'
              )
    
  
    
    @api.errorhandler(JWTExtendedException)
    def handle_jwt_exceptions(error):
        return {'message': str(error)}, getattr(error, 'code', 401)
    
    
    
    

    api.add_namespace(ons)
    api.add_namespace(ans, path="/auth")

    @api.errorhandler(NotFound)
    def not_found(error):
        return {'error': 'Not Found'}, 404
    
    @api.errorhandler(MethodNotAllowed)
    def method_not_allowed(error):
        return {'error': 'Method Not Allowed'}
    
    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Order': Order

        }

    return app
