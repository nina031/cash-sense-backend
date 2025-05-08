# db_models.py
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()


class User(db.Model):
    """
    Modèle pour les utilisateurs
    """
    __tablename__ = 'User'
    
    id = db.Column(db.String(36), primary_key=True)
    name = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(255), unique=True, nullable=True)
    emailVerified = db.Column(db.DateTime, nullable=True)
    password = db.Column(db.String(255), nullable=True)
    image = db.Column(db.String(255), nullable=True)
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

class Transaction(db.Model):
    """
    Modèle pour stocker les transactions de test ou manuelles
    """
    __tablename__ = 'Transaction'
    
    id = db.Column(db.String(36), primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    merchantName = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    paymentChannel = db.Column(db.String(50))
    pending = db.Column(db.Boolean, default=False)
    
    userId = db.Column(db.String(36), db.ForeignKey('User.id'), nullable=False)
    category = db.Column(db.String(100))
    subcategory = db.Column(db.String(100))
    
    isTestData = db.Column(db.Boolean, default=False)
    isManual = db.Column(db.Boolean, default=False)
    
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    def to_dict(self):
        """Convertit le modèle en dictionnaire pour l'API"""
        return {
            "id": self.id,
            "date": self.date,
            "amount": self.amount,
            "merchant_name": self.merchantName,
            "payment_channel": self.paymentChannel or ("online" if self.amount < 0 else "in store"),
            "pending": self.pending,
            "category": {
                "id": self.category,
                "subcategory": {
                    "id": self.subcategory
                }
            },
            "is_test_data": self.isTestData,
            "is_manual": self.isManual
        }