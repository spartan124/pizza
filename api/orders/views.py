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
order_status_model = order_namespace.model(
    'Order_status',{
        "order_status": fields.String(
            description="Status of Order",
            required=True,
            enum=["PENDING", "IN_TRANSIT", "DELIVERED"],
        ),
        
    }
)


@order_namespace.route("/orders")
class OrderGetCreate(Resource):

    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(description='Get all orders')
    @jwt_required()
    def get(self):
        """
        Get all orders
        """
        orders = Order.query.all()
        return orders, HTTPStatus.OK

    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(description='Place an Order')
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
    @order_namespace.doc(
        description='Retrieving an order by its ID',
        params= {
            'order_id':'An ID for the Order'
        }
        )
    def get(self, order_id):
        """
        Retrieving an order by ID
        """
        order = Order.get_by_id(order_id)
        return order, HTTPStatus.OK

    @order_namespace.expect(order_model)
    @order_namespace.marshal_with(order_model)
    @order_namespace.doc(
        description='Updating an Order by ID',
        params= {
            'order_id':'An ID for the Order'
        }
        )
    @jwt_required()
    def put(self, order_id):
        """
        Update an Order by ID
        """
        order_to_update = Order.get_by_id(order_id)
        
        data = order_namespace.payload
        
        order_to_update.quantity = data['quantity']
        order_to_update.flavour = data['flavour']
        order_to_update.size = data['size']
        order_to_update.order_status = data['order_status']
        
        order_to_update.update()
        
        return order_to_update,  HTTPStatus.OK
        
    @order_namespace.doc(
        description='Deleting an Order by its ID',
        params= {
            'order_id':'An ID for the Order'
        }
        )    
    @jwt_required()
    def delete(self, order_id):
        """
        Delete an Order by ID
        """
        order_to_delete = Order.get_by_id(order_id)
        
        order_to_delete.delete()
        
        return f"Order with order id {order_to_delete.id} Successfully deleted", HTTPStatus.OK
    


@order_namespace.route("/user/<int:user_id>/order/<int:order_id>")
class GetSpecificOrderByUser(Resource):
    @order_namespace.marshal_list_with(order_model)
    @order_namespace.doc(
        description='Get a user-specific order by its ID',
        params= {
            'order_id':'An ID for the Order',
            'user_id': 'An ID for the User'
        }
        )
    @jwt_required()
    def get(self, user_id, order_id):
        """
        Get an order from a specific User
        """
        user = User.get_by_id(user_id)
        order = Order.query.filter_by(id=order_id).filter_by(user=user).first()
        return order, HTTPStatus.OK


@order_namespace.route("/user/<int:user_id>/orders")
class GetUserOrder(Resource):
    @order_namespace.marshal_list_with(order_model)
    @order_namespace.doc(
        description='Get all Orders by a specific User',
        params= {
            'user_id': 'An ID for a specific User'
        }
        )
    @jwt_required()
    def get(self, user_id):
        """
        Get all Orders by user
        """
        user = User.get_by_id(user_id)
        orders = user.orders
        return orders, HTTPStatus.OK
    
    
@order_namespace.route("/order/status/<int:order_id>")
class UpdateOrdersStatus(Resource):
    
    @order_namespace.expect(order_status_model)
    @order_namespace.marshal_with(order_status_model)
    @order_namespace.doc(
        description='Updating the status of an Order',
        params= {
            'order_id': 'An ID for a specific Order'
        }
        )
    @jwt_required()
    def patch(self, order_id):
        """
        Update an Order's status
        """
        data = order_namespace.payload
        
        status_to_update = Order.get_by_id(order_id)
        
        status_to_update.order_status = data['order_status']
        
        status_to_update.update()
        
        return status_to_update, HTTPStatus.OK
