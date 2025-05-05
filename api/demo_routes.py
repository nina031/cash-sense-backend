# api/demo_routes.py
from flask import Blueprint, request, jsonify
from services.mode_service import toggle_demo_mode, is_demo_mode
from services.transaction_service import reset_demo_transactions

demo_blueprint = Blueprint('demo', __name__)

@demo_blueprint.route('/toggle_demo_mode', methods=['POST'])
def toggle_demo_mode_api():
    """
    Active ou désactive le mode démo
    """
    try:
        data = request.json
        enable_demo = data.get('enable_demo', True)
        
        # Basculer le mode
        new_mode = toggle_demo_mode(enable_demo)
        
        return jsonify({
            "success": True,
            "mode": new_mode,
            "is_demo_mode": is_demo_mode()
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500

@demo_blueprint.route('/reset_test_transactions', methods=['POST'])
def reset_test_transactions_api():
    """
    Réinitialise les transactions de test
    """
    try:
        data = request.json
        user_id = data.get('user_id', 'default_user')
        days = data.get('days', 30)
        
        # Réinitialiser les transactions de test
        transactions = reset_demo_transactions(user_id, days)
        
        return jsonify({
            "success": True,
            "transactions": transactions,
            "count": len(transactions)
        })
    except Exception as e:
        return jsonify({"error": str(e)}), 500