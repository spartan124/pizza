import unittest

from flask_jwt_extended import create_access_token

from .. import create_app
from ..config.config import config_dict
from ..models.orders import Order
from ..utils import db


class OrderTestCase(unittest.TestCase):
    def setUp(self):
        
        self.app = create_app(config=config_dict['test'])

        self.appctx = self.app.app_context()

        self.appctx.push()

        self.client = self.app.test_client()

        db.create_all()
        
    def tearDown(self):
        db.drop_all()
        
        self.appctx.pop()

        self.app = None

        self.client = None
        
    def test_get_all_orders(self):
        token = create_access_token(identity='testuser')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        response = self.client.get('/orders/orders', headers=headers)
        assert response.status_code == 200
        assert response.json == []
        
    def test_create_an_order(self):
        token = create_access_token(identity='testuser')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        data = {
            'size': 'EXTRA_LARGE',
            'flavour': 'chicken bbq pizza',
            'quantity': 1,
        }
        
        response = self.client.post('/orders/orders', headers=headers, json=data)
        
        # orders = Order.query.filter_by(size='EXTRA_LARGE').first()
        orders = Order.query.all()
        order_id = orders[0].id
        assert response.status_code == 201
        # assert orders.flavour == 'chicken bbq pizza'
        assert len(orders) == 1
        assert order_id == 1
        assert response.json['size'] == 'Sizes.EXTRA_LARGE'
        
    def test_get_single_order(self):
        token = create_access_token(identity='testuser')
        headers = {
            'Authorization': f'Bearer {token}'
        }
        
        response = self.client.get('/orders/order/1', headers=headers)
        orders = Order.query.all()
        assert len(orders) == 0
        assert response.status_code == 404 