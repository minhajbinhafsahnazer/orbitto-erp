from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Product

products_bp = Blueprint('products', __name__, url_prefix='/products')

@products_bp.route('/', methods=['GET'])
def get_all_products():
    """Get all products"""
    products = Product.query.filter_by(is_active=True).all()
    return {'products': [product.to_dict() for product in products]}, 200

@products_bp.route('/<int:product_id>', methods=['GET'])
def get_product(product_id):
    """Get product by ID"""
    product = Product.query.get(product_id)
    
    if not product:
        return {'error': 'Product not found'}, 404
    
    return {'product': product.to_dict()}, 200

@products_bp.route('/', methods=['POST'])
@jwt_required()
def create_product():
    """Create new product"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['name', 'sku', 'price', 'category']):
        return {'error': 'Missing required fields'}, 400
    
    if Product.query.filter_by(sku=data['sku']).first():
        return {'error': 'Product with this SKU already exists'}, 409
    
    product = Product(
        name=data['name'],
        description=data.get('description', ''),
        sku=data['sku'].upper(),
        price=data['price'],
        category=data['category'],
        supplier=data.get('supplier', ''),
        quantity=data.get('quantity', 0),
        reorder_level=data.get('reorder_level', 10)
    )
    
    try:
        db.session.add(product)
        db.session.commit()
        return {'message': 'Product created successfully', 'product': product.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@products_bp.route('/<int:product_id>', methods=['PUT'])
@jwt_required()
def update_product(product_id):
    """Update product"""
    product = Product.query.get(product_id)
    
    if not product:
        return {'error': 'Product not found'}, 404
    
    data = request.get_json()
    
    if 'name' in data:
        product.name = data['name']
    if 'description' in data:
        product.description = data['description']
    if 'price' in data:
        product.price = data['price']
    if 'category' in data:
        product.category = data['category']
    if 'quantity' in data:
        product.quantity = data['quantity']
    if 'reorder_level' in data:
        product.reorder_level = data['reorder_level']
    if 'supplier' in data:
        product.supplier = data['supplier']
    
    try:
        db.session.commit()
        return {'message': 'Product updated successfully', 'product': product.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@products_bp.route('/<int:product_id>', methods=['DELETE'])
@jwt_required()
def delete_product(product_id):
    """Delete (deactivate) product"""
    product = Product.query.get(product_id)
    
    if not product:
        return {'error': 'Product not found'}, 404
    
    product.is_active = False
    
    try:
        db.session.commit()
        return {'message': 'Product deleted successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500
