from flask import jsonify, render_template, request
from app.repositories.order_repository import OrderRepository
from app.repositories.product_repository import ProductRepository
from app.services.order_service import OrderService
from app.strategies.delivery import FixedDeliveryFeeStrategy


def register_routes(app):
    orders = OrderRepository(app.config['DATABASE'])
    products = ProductRepository(app.config['DATABASE'])
    service = OrderService(orders, products, FixedDeliveryFeeStrategy(5.0))

    @app.get('/')
    def index():
        return render_template('index.html')

    @app.get('/api/products')
    def list_products():
        return jsonify(products.list_available())

    @app.get('/api/orders')
    def list_orders():
        return jsonify(orders.list_all())

    @app.post('/api/orders')
    def create_order():
        try:
            return jsonify(service.create_order(request.get_json())), 201
        except (ValueError, KeyError, TypeError) as exc:
            return jsonify({'error': str(exc)}), 400

    @app.patch('/api/orders/<int:order_id>/status')
    def change_status(order_id):
        try:
            data = request.get_json() or {}
            return jsonify(service.change_status(order_id, data['status']))
        except (ValueError, KeyError) as exc:
            return jsonify({'error': str(exc)}), 400

    @app.patch('/api/orders/<int:order_id>/payment')
    def mark_paid(order_id):
        try:
            return jsonify(service.mark_paid(order_id))
        except ValueError as exc:
            return jsonify({'error': str(exc)}), 404
