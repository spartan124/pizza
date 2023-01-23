from flask_restx import Namespace, Resource

order_namespace = Namespace("orders", description="namespace for orders")


@order_namespace.route("/orders")
class OrderGetCreate(Resource):
    def get(self):
        """
        Get all orders
        """
        pass

    def post(self):
        """
        Place an order
        """
        pass

@order_namespace.route('/order/<int:order_id>')
class GetUpdateDelete(Resource):

    def get(self, order_id):
        """
            Retrieving an order by ID
        """
        pass

    def put(self, order_id):
        """
           Update an Order by ID
        """
        pass

    def delete(self, order_id):
        """
           Delete an Order by ID
        """
        pass

@order_namespace.route('/user/<int:user_id>/order/<int:order_id>')
class GetSpecificOrderByUser(Resource):
    def get(self, user_id, order_id):
        """
           Get an order from a specific User
        """
        pass

@order_namespace.route('/user/<int:user_id>/orders')
class GetUserOrder(Resource):
    def get(self):
        
        """
           Get all Orders by user
        """
        pass

@order_namespace.route('/order/status/<int:order_id>')
class UpdateOrdersStatus(Resource):
    def patch(self, order_id):
        """
           Update an Order's status
        """
        pass
    
