from flask import request, jsonify
from flask_jwt_extended import verify_jwt_in_request, get_jwt_identity
from functools import wraps

def token_required(fn):
    """Decorator to require JWT token"""
    @wraps(fn)
    def decorated_function(*args, **kwargs):
        try:
            verify_jwt_in_request()
            current_user_id = get_jwt_identity()
            return fn(current_user_id=current_user_id, *args, **kwargs)
        except Exception as e:
            return {'error': 'Unauthorized'}, 401
    return decorated_function

def role_required(role):
    """Decorator to check user role"""
    def decorator(fn):
        @wraps(fn)
        def decorated_function(*args, **kwargs):
            try:
                verify_jwt_in_request()
                claims = get_jwt_identity()
                if claims.get('role') != role and claims.get('role') != 'admin':
                    return {'error': 'Insufficient permissions'}, 403
                return fn(*args, **kwargs)
            except Exception as e:
                return {'error': 'Unauthorized'}, 401
        return decorated_function
    return decorator
