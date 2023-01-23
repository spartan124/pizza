from flask import Flask
from flask_restx import Api
from .orders.views import order_namespace as ons
from .auth.views import auth_namespace as ans
def create_app():
    app = Flask(__name__)

    api = Api(app)

    api.add_namespace(ons, path="")
    api.add_namespace(ans, path="/auth")

    return app
