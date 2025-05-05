from flask import Blueprint, request, jsonify
from plaid.model.products import Products
from services.plaid_service import create_link_token, exchange_public_token
from services.transaction_service import get_transactions
from utils.plaid_helpers import get_plaid_client


plaid_blueprint = Blueprint('plaid', __name__)

@plaid_blueprint.route('/create_link_token', methods=['POST'])
def link_token_api():
    try:
        link_token = create_link_token()
        return jsonify({"link_token": link_token})
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@plaid_blueprint.route('/exchange_token', methods=['POST'])
def exchange_token_api():
    try:
        public_token = request.json.get('public_token')
        if not public_token:
            return jsonify({"error": "Public token is required"}), 400
            
        result = exchange_public_token(public_token)
        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@plaid_blueprint.route('/get_transactions', methods=['POST'])
def transactions_api():
    try:
        access_token = request.json.get('access_token')
        if not access_token:
            return jsonify({"error": "Access token is required"}), 400
            
        # Récupérer le paramètre days s'il est fourni
        days = request.json.get('days', 30)  # Valeur par défaut: 30
        user_id = request.json.get('user_id', 'default_user')  # ID utilisateur par défaut
        transactions = get_transactions(user_id, days, access_token)
        return jsonify({"transactions": transactions})
    except Exception as e:
        return jsonify({"error": str(e)}), 500