# api/transaction_routes.py
from flask import Blueprint, request, jsonify
from services.transaction_service import get_transactions, add_transaction
from utils.auth_utils import require_valid_user
import logging

# Configuration du logger
logger = logging.getLogger(__name__)

transaction_blueprint = Blueprint('transaction', __name__)

@transaction_blueprint.route('/get_transactions', methods=['POST'])
@require_valid_user
def get_transactions_api():
    """
    Récupère les transactions pour un utilisateur
    (mode démo ou transactions manuelles)
    """
    try:
        # Récupérer et valider les paramètres requis
        user_id = request.json.get('user_id')
        
        # Récupérer le paramètre days s'il est fourni
        days = request.json.get('days', 30)  # Valeur par défaut: 30
        
        transactions = get_transactions(user_id, days)
        return jsonify({"transactions": transactions})
    except ValueError as e:
        # Erreur de validation (comme un ID utilisateur manquant)
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Erreur lors de la récupération des transactions: {str(e)}")
        return jsonify({"error": str(e)}), 500

@transaction_blueprint.route('/add_transaction', methods=['POST'])
@require_valid_user
def add_transaction_api():
    """
    Ajoute une transaction manuelle pour un utilisateur
    """
    try:
        # Récupérer les paramètres
        user_id = request.json.get('user_id')
        transaction_data = request.json.get('transaction')
        
        if not transaction_data:
            return jsonify({"error": "Transaction data is required"}), 400
        
        # Ajouter la transaction
        transaction = add_transaction(user_id, transaction_data, is_manual=True)
        
        return jsonify({
            "success": True,
            "transaction": transaction
        })
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Erreur lors de l'ajout de la transaction: {str(e)}")
        return jsonify({"error": str(e)}), 500