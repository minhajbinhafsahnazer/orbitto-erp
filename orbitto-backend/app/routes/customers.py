from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required
from app import db
from app.models import Customer

customers_bp = Blueprint('customers', __name__, url_prefix='/customers')

@customers_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_customers():
    """Get all customers"""
    customers = Customer.query.filter_by(is_active=True).all()
    return {'customers': [customer.to_dict() for customer in customers]}, 200

@customers_bp.route('/<int:customer_id>', methods=['GET'])
@jwt_required()
def get_customer(customer_id):
    """Get customer by ID"""
    customer = Customer.query.get(customer_id)
    
    if not customer:
        return {'error': 'Customer not found'}, 404
    
    return {'customer': customer.to_dict()}, 200

@customers_bp.route('/', methods=['POST'])
@jwt_required()
def create_customer():
    """Create new customer"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['name', 'email']):
        return {'error': 'Missing required fields'}, 400
    
    if Customer.query.filter_by(email=data['email']).first():
        return {'error': 'Customer with this email already exists'}, 409
    
    customer = Customer(
        name=data['name'],
        email=data['email'],
        phone=data.get('phone', ''),
        address=data.get('address', ''),
        city=data.get('city', ''),
        state=data.get('state', ''),
        postal_code=data.get('postal_code', ''),
        country=data.get('country', '')
    )
    
    try:
        db.session.add(customer)
        db.session.commit()
        return {'message': 'Customer created successfully', 'customer': customer.to_dict()}, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@customers_bp.route('/<int:customer_id>', methods=['PUT'])
@jwt_required()
def update_customer(customer_id):
    """Update customer"""
    customer = Customer.query.get(customer_id)
    
    if not customer:
        return {'error': 'Customer not found'}, 404
    
    data = request.get_json()
    
    for field in ['name', 'email', 'phone', 'address', 'city', 'state', 'postal_code', 'country']:
        if field in data:
            setattr(customer, field, data[field])
    
    try:
        db.session.commit()
        return {'message': 'Customer updated successfully', 'customer': customer.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@customers_bp.route('/<int:customer_id>', methods=['DELETE'])
@jwt_required()
def delete_customer(customer_id):
    """Delete (deactivate) customer"""
    customer = Customer.query.get(customer_id)
    
    if not customer:
        return {'error': 'Customer not found'}, 404
    
    customer.is_active = False
    
    try:
        db.session.commit()
        return {'message': 'Customer deleted successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500
