from flask import Flask
from flask_jwt_extended import JWTManager
from flask_migrate import Migrate
from flask_restx import Api
from werkzeug.exceptions import NotFound, MethodNotAllowed
from .auth.views import auth_namespace as ans
from .config.config import config_dict
from .models.orders import Order
from .models.users import User
from .orders.views import order_namespace as ons
from .utils import db
from flask_jwt_extended.exceptions import JWTExtendedException
import pathlib

def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)
    app.config.from_pyfile(pathlib.Path(__file__).parent / "config/config.py")

    
    db.init_app(app)
    
    api = Api(app)

    jwt = JWTManager()
    
    @api.errorhandler(JWTExtendedException)
    def handle_jwt_exceptions(error):
        return {'message': str(error)}, getattr(error, 'code', 401)
    
    jwt.init_app(app)

    migrate = Migrate(app, db)
    
    

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
