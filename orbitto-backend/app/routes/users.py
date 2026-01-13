from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app import db
from app.models import User
from app.middleware.auth import token_required

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('/', methods=['GET'])
@jwt_required()
def get_all_users():
    """Get all users"""
    users = User.query.filter_by(is_active=True).all()
    return {'users': [user.to_dict() for user in users]}, 200

@users_bp.route('/<int:user_id>', methods=['GET'])
@jwt_required()
def get_user(user_id):
    """Get user by ID"""
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'User not found'}, 404
    
    return {'user': user.to_dict()}, 200

@users_bp.route('/<int:user_id>', methods=['PUT'])
@jwt_required()
def update_user(user_id):
    """Update user"""
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'User not found'}, 404
    
    data = request.get_json()
    
    if 'first_name' in data:
        user.first_name = data['first_name']
    if 'last_name' in data:
        user.last_name = data['last_name']
    if 'email' in data:
        if User.query.filter_by(email=data['email']).first():
            return {'error': 'Email already exists'}, 409
        user.email = data['email']
    
    try:
        db.session.commit()
        return {'message': 'User updated successfully', 'user': user.to_dict()}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@users_bp.route('/<int:user_id>', methods=['DELETE'])
@jwt_required()
def delete_user(user_id):
    """Delete (deactivate) user"""
    user = User.query.get(user_id)
    
    if not user:
        return {'error': 'User not found'}, 404
    
    user.is_active = False
    
    try:
        db.session.commit()
        return {'message': 'User deleted successfully'}, 200
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500
