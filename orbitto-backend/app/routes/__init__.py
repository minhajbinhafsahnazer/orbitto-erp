from flask import Blueprint

api_bp = Blueprint('api', __name__)

# Import route blueprints
from .auth import auth_bp
from .users import users_bp
from .products import products_bp
from .orders import orders_bp
from .customers import customers_bp
from .inventory import inventory_bp

# Register blueprints
api_bp.register_blueprint(auth_bp)
api_bp.register_blueprint(users_bp)
api_bp.register_blueprint(products_bp)
api_bp.register_blueprint(orders_bp)
api_bp.register_blueprint(customers_bp)
api_bp.register_blueprint(inventory_bp)
