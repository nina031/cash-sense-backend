# api/transaction_routes.py
from flask import Blueprint, request, jsonify
from services.transaction_service import get_transactions
import logging

# Configuration du logger
logger = logging.getLogger(__name__)

transaction_blueprint = Blueprint('transaction', __name__)

@transaction_blueprint.route('/get_transactions', methods=['POST'])
def get_transactions_api():
    """
    Récupère les transactions pour un utilisateur, quelle que soit la source
    (Plaid, mode démo, ou transactions manuelles)
    """
    try:
        # Récupérer et valider les paramètres requis
        access_token = request.json.get('access_token')
        user_id = request.json.get('user_id')
        
        if not access_token:
            return jsonify({"error": "Access token is required"}), 400
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
            
        # Récupérer le paramètre days s'il est fourni
        days = request.json.get('days', 30)  # Valeur par défaut: 30
        
        transactions = get_transactions(user_id, days, access_token)
        return jsonify({"transactions": transactions})
    except ValueError as e:
        # Erreur de validation (comme un ID utilisateur manquant)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Erreur lors de la récupération des transactions: {str(e)}")
        return jsonify({"error": str(e)}), 500