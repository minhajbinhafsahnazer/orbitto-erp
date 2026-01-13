from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Inventory, Product

inventory_bp = Blueprint('inventory', __name__, url_prefix='/inventory')

@inventory_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_inventory():
    """Get all inventory items"""
    inventory = Inventory.query.all()
    return {'inventory': [item.to_dict() for item in inventory]}, 200

@inventory_bp.route('/<int:inventory_id>', methods=['GET'])
@jwt_required()
def get_inventory(inventory_id):
    """Get inventory item by ID"""
    item = Inventory.query.get(inventory_id)
    
    if not item:
        return {'error': 'Inventory item not found'}, 404
    
    return {'inventory': item.to_dict()}, 200

@inventory_bp.route('/<int:inventory_id>', methods=['PUT'])
@jwt_required()
def update_inventory(inventory_id):
    """Update inventory quantity"""
    item = Inventory.query.get(inventory_id)
    
    if not item:
        return {'error': 'Inventory item not found'}, 404
    
    data = request.get_json()
    
    if 'quantity_on_hand' in data:
        item.quantity_on_hand = data['quantity_on_hand']
    if 'quantity_reserved' in data:
        item.quantity_reserved = data['quantity_reserved']
    if 'reorder_point' in data:
        item.reorder_point = data['reorder_point']
    if 'reorder_quantity' in data:
        item.reorder_quantity = data['reorder_quantity']
    
    # Calculate available quantity
    item.quantity_available = item.quantity_on_hand - item.quantity_reserved
    
    try:
        db.session.commit()
        return {'message': 'Inventory updated successfully', 'inventory': item.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@inventory_bp.route('/low-stock', methods=['GET'])
@jwt_required()
def get_low_stock():
    """Get low stock items"""
    low_stock_items = Inventory.query.filter(
        Inventory.quantity_on_hand <= Inventory.reorder_point
    ).all()
    
    return {'items': [item.to_dict() for item in low_stock_items]}, 200
