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
    __tablename__ = 'Transaction'  # Nom de table tel que défini par Prisma (avec majuscule)
    
    id = db.Column(db.String(36), primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    merchantName = db.Column(db.String(100))  # Adaptez les noms de champs à ceux de Prisma
    amount = db.Column(db.Float, nullable=False)
    paymentChannel = db.Column(db.String(50))
    pending = db.Column(db.Boolean, default=False)
    
    userId = db.Column(db.String(36), db.ForeignKey('User.id'), nullable=False)  # Avec majuscule pour User
    category = db.Column(db.String(100))
    subcategory = db.Column(db.String(100))
    
    isTestData = db.Column(db.Boolean, default=False)
    isManual = db.Column(db.Boolean, default=False)
    
    rawData = db.Column(db.Text, nullable=True)
    
    createdAt = db.Column(db.DateTime, default=datetime.utcnow)
    updatedAt = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    
    def to_dict(self):
        """Convertit le modèle en dictionnaire pour l'API"""
        if self.raw_data:
            # Si nous avons des données brutes stockées, les utiliser
            return json.loads(self.raw_data)
        
        # Sinon, construire un dictionnaire à partir des champs individuels
        return {
            "id": self.id,
            "date": self.date,
            "amount": self.amount,
            "merchant_name": self.merchant_name,
            "payment_channel": self.payment_channel or ("online" if self.amount < 0 else "in store"),
            "pending": self.pending,
            "category": {
                "id": self.category,
                "subcategory": {
                    "id": self.subcategory
                }
            },
            "is_test_data": self.is_test_data,
            "is_manual": self.is_manual
        }
    
