from flask import Blueprint, request, jsonify
from plaid.model.products import Products
from services.plaid_service import create_link_token, exchange_public_token
from services.transaction_service import get_transactions
from utils.plaid_helpers import get_plaid_client


plaid_blueprint = Blueprint('plaid', __name__)

@plaid_blueprint.route('/create_link_token', methods=['POST'])
def link_token_api():
    try:
        # Récupérer l'ID utilisateur depuis la requête
        user_id = request.json.get('user_id')
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
            
        link_token = create_link_token(user_id)
        return jsonify({"link_token": link_token})
    except ValueError as e:
        return jsonify({"error": str(e)}), 400
    except Exception as e:
        print(f"Erreur lors de la création du token de liaison: {str(e)}")
        return jsonify({"error": str(e)}), 500

@plaid_blueprint.route('/exchange_token', methods=['POST'])
def exchange_token_api():
    try:
        # Récupérer les paramètres de la requête
        public_token = request.json.get('public_token')
        user_id = request.json.get('user_id')
        
        if not public_token:
            return jsonify({"error": "Public token is required"}), 400
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
            
        result = exchange_public_token(public_token)
        return jsonify(result)
    except Exception as e:
        print(f"Erreur lors de l'échange du token: {str(e)}")
        return jsonify({"error": str(e)}), 500