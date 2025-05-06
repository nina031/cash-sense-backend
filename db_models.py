# models.py (version modifiée)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import json

db = SQLAlchemy()

class Transaction(db.Model):
    """
    Modèle pour stocker les transactions de test ou manuelles

    """
    __tablename__ = 'transactions'
    
    # Champs de base définis par TRANSACTION_SCHEMA
    id = db.Column(db.String(36), primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    merchant_name = db.Column(db.String(100))
    amount = db.Column(db.Float, nullable=False)
    payment_channel = db.Column(db.String(50))
    pending = db.Column(db.Boolean, default=False)
    
    # Champs additionnels pour notre application
    user_id = db.Column(db.String(36), nullable=False, index=True)
    category = db.Column(db.String(100))
    subcategory = db.Column(db.String(100))
    
    # Distinguer les types de transactions
    is_test_data = db.Column(db.Boolean, default=False)  # True = mode démo
    is_manual = db.Column(db.Boolean, default=False)     # True = créée manuellement
    
    # Stockage JSON complet pour préserver toutes les données
    raw_data = db.Column(db.Text, nullable=True)
    
    # Métadonnées
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    
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