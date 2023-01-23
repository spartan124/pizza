from flask_restx import Namespace, Resource

order_namespace = Namespace("order", description="namespace for orders")

@order_namespace.route("/")
class HelloOrder(Resource):
    def get(self):
        return {"message": "Hello Order, nice to meet you"}
