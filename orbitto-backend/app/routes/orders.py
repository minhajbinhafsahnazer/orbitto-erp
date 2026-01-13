from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Order, OrderItem, Product

orders_bp = Blueprint('orders', __name__, url_prefix='/orders')

@orders_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_orders():
    """Get all orders"""
    orders = Order.query.all()
    return {'orders': [order.to_dict() for order in orders]}, 200

@orders_bp.route('/<int:order_id>', methods=['GET'])
@jwt_required()
def get_order(order_id):
    """Get order by ID"""
    order = Order.query.get(order_id)
    
    if not order:
        return {'error': 'Order not found'}, 404
    
    return {'order': order.to_dict()}, 200

@orders_bp.route('/', methods=['POST'])
@jwt_required()
def create_order():
    """Create new order"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['order_number', 'customer_id', 'items']):
        return {'error': 'Missing required fields'}, 400
    
    if Order.query.filter_by(order_number=data['order_number']).first():
        return {'error': 'Order number already exists'}, 409
    
    total_amount = 0
    order_items = []
    
    for item in data['items']:
        product = Product.query.get(item['product_id'])
        if not product:
            return {'error': f"Product {item['product_id']} not found"}, 404
        
        unit_price = item.get('unit_price', product.price)
        total = unit_price * item['quantity']
        total_amount += total
        
        order_items.append({
            'product_id': item['product_id'],
            'quantity': item['quantity'],
            'unit_price': unit_price,
            'total': total
        })
    
    order = Order(
        order_number=data['order_number'],
        customer_id=data['customer_id'],
        total_amount=total_amount,
        status=data.get('status', 'pending'),
        notes=data.get('notes', '')
    )
    
    for item_data in order_items:
        order_item = OrderItem(**item_data)
        order.items.append(order_item)
    
    try:
        db.session.add(order)
        db.session.commit()
        return {'message': 'Order created successfully', 'order': order.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@orders_bp.route('/<int:order_id>', methods=['PUT'])
@jwt_required()
def update_order(order_id):
    """Update order"""
    order = Order.query.get(order_id)
    
    if not order:
        return {'error': 'Order not found'}, 404
    
    data = request.get_json()
    
    valid_statuses = ['pending', 'confirmed', 'shipped', 'delivered', 'cancelled']
    
    if 'status' in data:
        if data['status'] not in valid_statuses:
            return {'error': f'Invalid status. Must be one of {valid_statuses}'}, 400
        order.status = data['status']
    
    if 'delivery_date' in data:
        order.delivery_date = data['delivery_date']
    
    if 'notes' in data:
        order.notes = data['notes']
    
    try:
        db.session.commit()
        return {'message': 'Order updated successfully', 'order': order.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500
