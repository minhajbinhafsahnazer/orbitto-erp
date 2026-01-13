from app import db
from datetime import datetime

class Inventory(db.Model):
    __tablename__ = 'inventory'
    
    id = db.Column(db.Integer, primary_key=True)
    product_id = db.Column(db.Integer, db.ForeignKey('products.id'), nullable=False, unique=True)
    quantity_on_hand = db.Column(db.Integer, default=0)
    quantity_reserved = db.Column(db.Integer, default=0)
    quantity_available = db.Column(db.Integer, default=0)
    reorder_point = db.Column(db.Integer, default=10)
    reorder_quantity = db.Column(db.Integer, default=50)
    last_counted = db.Column(db.DateTime, default=datetime.utcnow)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    product = db.relationship('Product', backref=db.backref('inventory', uselist=False))
    
    def __repr__(self):
        return f'<Inventory {self.product_id}>'
    
    def to_dict(self):
        return {
            'id': self.id,
            'product_id': self.product_id,
            'quantity_on_hand': self.quantity_on_hand,
            'quantity_reserved': self.quantity_reserved,
            'quantity_available': self.quantity_available,
            'reorder_point': self.reorder_point,
            'reorder_quantity': self.reorder_quantity,
            'last_counted': self.last_counted.isoformat(),
            'created_at': self.created_at.isoformat(),
            'updated_at': self.updated_at.isoformat()
        }
