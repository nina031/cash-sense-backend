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
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
        
        # Basculer le mode
        new_mode = toggle_demo_mode(enable_demo)
        print(f"Mode démo {'activé' if enable_demo else 'désactivé'} par l'utilisateur {user_id}")
        
        return jsonify({
            "success": True,
            "mode": new_mode,
            "is_demo_mode": is_demo_mode()
        })
    except Exception as e:
        print(f"Erreur lors du basculement du mode démo: {str(e)}")
        return jsonify({"error": str(e)}), 500

@demo_blueprint.route('/reset_test_transactions', methods=['POST'])
def reset_test_transactions_api():
    """
    Réinitialise les transactions de test
    """
    try:
        data = request.json
        user_id = data.get('user_id')
        
        if not user_id:
            return jsonify({"error": "User ID is required"}), 400
            
        days = data.get('days', 30)
        
        # Réinitialiser les transactions de test
        transactions = reset_demo_transactions(user_id, days)
        print(f"Transactions de test réinitialisées pour l'utilisateur {user_id}")
        
        return jsonify({
            "success": True,
            "transactions": transactions,
            "count": len(transactions)
        })
    except Exception as e:
        print(f"Erreur lors de la réinitialisation des transactions de test: {str(e)}")
        return jsonify({"error": str(e)}), 500