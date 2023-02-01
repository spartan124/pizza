from http import HTTPStatus

from flask_jwt_extended import get_jwt_identity, jwt_required
from flask_restx import Namespace, Resource, fields

from ..models.orders import Order
from ..models.users import User

order_namespace = Namespace("orders", description="namespace for orders")

order_model = order_namespace.model(
    "Order",
    {
        "id": fields.Integer(
            description='Order ID'
        ),
        "flavour": fields.String(
            description='pizza flavour',
            required=True
        ),
        "quantity": fields.Integer(
            description='Number of Pizza ordered',
            required=True
        ),
        "size": fields.String(
            description="size of order",
            required=True,
            enum=["SMALL", "MEDIUM", "LARGE", "EXTRA_LARGE"],
        ),
        "order_status": fields.String(
            description="Status of Order",
            required=True,
            enum=["PENDING", "IN_TRANSIT", "DELIVERED"],
        ),
    },
)


@order_namespace.route("/orders")
class OrderGetCreate(Resource):

    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def get(self):
        """
        Get all orders
        """
        orders = Order.query.all()
        return orders, HTTPStatus.OK

    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @jwt_required()
    def post(self):
        """
        Place an order
        """
        username = get_jwt_identity()

        current_user = User.query.filter_by(username=username).first()

        data = order_namespace.payload

        new_order = Order(
            size=data['size'],
            quantity=data['quantity'],
            flavour=data['flavour']
        )

        new_order.user = current_user

        new_order.save()

        return new_order, HTTPStatus.CREATED


@order_namespace.route("/order/<int:order_id>")
class GetUpdateDelete(Resource):
    @jwt_required()
    @order_namespace.marshal_with(order_model)
    def get(self, order_id):
        """
        Retrieving an order by ID
        """
        order = Order.get_by_id(order_id)
        return order, HTTPStatus.OK

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


@order_namespace.route("/user/<int:user_id>/order/<int:order_id>")
class GetSpecificOrderByUser(Resource):
    def get(self, user_id, order_id):
        """
        Get an order from a specific User
        """
        pass


@order_namespace.route("/user/<int:user_id>/orders")
class GetUserOrder(Resource):
    def get(self):
        """
        Get all Orders by user
        """
        pass


@order_namespace.route("/order/status/<int:order_id>")
class UpdateOrdersStatus(Resource):
    def patch(self, order_id):
        """
        Update an Order's status
        """
        pass
