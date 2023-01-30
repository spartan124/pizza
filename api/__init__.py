from flask import Flask, jsonify
from flask_restx import Api
from .orders.views import order_namespace as ons
from .auth.views import auth_namespace as ans
from .config.config import config_dict
from .utils import db
from .models.orders import Order
from .models.users import User
from flask_migrate import Migrate
from flask_jwt_extended import JWTManager

def create_app(config=config_dict['dev']):
    app = Flask(__name__)

    app.config.from_object(config)
    
    db.init_app(app)

    jwt = JWTManager(app)

    

    migrate = Migrate(app, db)
    
    api = Api(app)

    api.add_namespace(ons)
    api.add_namespace(ans, path="/auth")

    @app.shell_context_processor
    def make_shell_context():
        return {
            'db': db,
            'User': User,
            'Order': Order

        }

    return app
