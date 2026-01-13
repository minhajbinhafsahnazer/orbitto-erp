from flask import Blueprint, request, jsonify
from flask_jwt_extended import create_access_token
from app import db
from app.models import User

auth_bp = Blueprint('auth', __name__, url_prefix='/auth')

@auth_bp.route('/register', methods=['POST'])
def register():
    """Register a new user"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'password', 'first_name', 'last_name']):
        return {'error': 'Missing required fields'}, 400
    
    if User.query.filter_by(email=data['email']).first():
        return {'error': 'User already exists'}, 409
    
    user = User(
        email=data['email'],
        first_name=data['first_name'],
        last_name=data['last_name'],
        role=data.get('role', 'user')
    )
    user.set_password(data['password'])
    
    try:
        db.session.add(user)
        db.session.commit()
        
        access_token = create_access_token(identity={
            'id': user.id,
            'email': user.email,
            'role': user.role
        })
        
        return {
            'message': 'User registered successfully',
            'token': access_token,
            'user': user.to_dict()
        }, 201
    except Exception as e:
        db.session.rollback()
        return {'error': str(e)}, 500

@auth_bp.route('/login', methods=['POST'])
def login():
    """User login"""
    data = request.get_json()
    
    if not data or not all(k in data for k in ['email', 'password']):
        return {'error': 'Missing email or password'}, 400
    
    user = User.query.filter_by(email=data['email']).first()
    
    if not user or not user.check_password(data['password']):
        return {'error': 'Invalid credentials'}, 401
    
    if not user.is_active:
        return {'error': 'User account is inactive'}, 403
    
    access_token = create_access_token(identity={
        'id': user.id,
        'email': user.email,
        'role': user.role
    })
    
    return {
        'message': 'Login successful',
        'token': access_token,
        'user': user.to_dict()
    }, 200
