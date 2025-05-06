# utils/auth_utils.py
from db_models import db, User
from functools import wraps
from flask import request, jsonify

def verify_user_exists(user_id):
    """
    Vérifie qu'un utilisateur existe dans la base de données
    
    Args:
        user_id (str): Identifiant de l'utilisateur à vérifier
        
    Returns:
        bool: True si l'utilisateur existe, False sinon
    """
    if not user_id:
        return False
        
    # Vérifier si l'utilisateur existe
    user = User.query.filter_by(id=user_id).first()
    return user is not None

def require_valid_user(view_function):
    """
    Décorateur pour vérifier que l'utilisateur existe dans la base de données
    """
    @wraps(view_function)
    def wrapper(*args, **kwargs):
        try:
            # Extraire l'ID utilisateur de la requête JSON
            user_id = request.json.get('user_id')
            
            if not user_id:
                return jsonify({"error": "User ID is required"}), 400
                
            # Vérifier si l'utilisateur existe
            if not verify_user_exists(user_id):
                return jsonify({"error": "User not found"}), 404
                
            # Si l'utilisateur existe, continuer le traitement
            return view_function(*args, **kwargs)
        except Exception as e:
            return jsonify({"error": str(e)}), 500
            
    return wrapper