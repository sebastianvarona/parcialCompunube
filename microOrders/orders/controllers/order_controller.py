from flask import Blueprint, request, jsonify, session
from orders.models.order_model import Order, OrderItem
from db.db import db
import requests
import os
import consul

order_controller = Blueprint('order_controller', __name__)

# Consul configuration
CONSUL_HOST = os.environ.get('CONSUL_HOST', 'consul')
CONSUL_PORT = int(os.environ.get('CONSUL_PORT', 8500))

def get_service_url(service_name):
    """Discover service URL from Consul"""
    try:
        c = consul.Consul(host=CONSUL_HOST, port=CONSUL_PORT)
        services = c.agent.services()
        for service_id, service in services.items():
            if service['Service'] == service_name:
                # Use Address if available, otherwise use service name (for Docker networking)
                address = service.get('Address') or service['Service']
                return f"http://{address}:{service['Port']}"
        print(f"Service {service_name} not found in Consul")
        return None
    except Exception as e:
        print(f"Consul error: {e}")
        return None

def get_products_service_url():
    """Get microProducts service URL"""
    return get_service_url('microProducts')

@order_controller.route('/api/orders', methods=['GET'])
def get_orders():
    orders = Order.query.all()
    result = [order.to_dict() for order in orders]
    return jsonify(result)

@order_controller.route('/api/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    order = Order.query.get_or_404(order_id)
    return jsonify(order.to_dict())

@order_controller.route('/api/orders', methods=['POST'])
def create_order():
    data = request.json

    # Get user info from session
    user_name = session.get('username', 'anonymous')
    user_email = session.get('email', '')

    if not user_name or user_name == 'anonymous':
        # If no session, use provided user info or defaults
        user_name = data.get('user_name', 'anonymous')
        user_email = data.get('user_email', '')

    # Get products from request
    products = data.get('products', [])

    if not products:
        return jsonify({'message': 'No products provided'}), 400

    # Get microProducts service URL
    products_url = get_products_service_url()
    if not products_url:
        return jsonify({'message': 'Products service not available'}), 500

    # Verify availability and calculate total
    order_items = []
    total = 0
    items_to_update = []

    for item in products:
        product_id = item.get('id')
        quantity = item.get('quantity', 1)

        # Get product from microProducts service
        try:
            response = requests.get(f"{products_url}/api/products/{product_id}")
            if response.status_code == 404:
                return jsonify({'message': f'Product {product_id} not found'}), 404
            if response.status_code != 200:
                return jsonify({'message': 'Error fetching product'}), 500

            product = response.json()

            # Check availability
            if product['quantity'] < quantity:
                return jsonify({
                    'message': f'Insufficient inventory for product {product["name"]}',
                    'available': product['quantity'],
                    'requested': quantity
                }), 409

            # Calculate item total
            item_total = product['price'] * quantity
            total += item_total

            order_items.append({
                'product_id': product_id,
                'product_name': product['name'],
                'quantity': quantity,
                'price': product['price']
            })

            items_to_update.append({
                'product_id': product_id,
                'quantity': quantity
            })

        except requests.exceptions.RequestException as e:
            return jsonify({'message': f'Error connecting to products service: {str(e)}'}), 500

    # Update inventory in microProducts
    for item in items_to_update:
        try:
            response = requests.post(
                f"{products_url}/api/products/{item['product_id']}/decrease",
                json={'quantity': item['quantity']}
            )
            if response.status_code == 409:
                # Rollback if inventory update fails
                return jsonify({'message': 'Failed to update inventory'}), 500
        except requests.exceptions.RequestException as e:
            return jsonify({'message': f'Error updating inventory: {str(e)}'}), 500

    # Create order
    new_order = Order(
        user_name=user_name,
        user_email=user_email,
        total=total
    )
    db.session.add(new_order)
    db.session.flush()  # Get the order ID

    # Create order items
    for item in order_items:
        order_item = OrderItem(
            order_id=new_order.id,
            product_id=item['product_id'],
            product_name=item['product_name'],
            quantity=item['quantity'],
            price=item['price']
        )
        db.session.add(order_item)

    db.session.commit()

    return jsonify({
        'message': 'Order created successfully',
        'order': new_order.to_dict()
    }), 201
