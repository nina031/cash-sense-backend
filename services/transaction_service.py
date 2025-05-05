"""
Service de gestion des transactions (réelles et de test)
"""
from datetime import datetime, timedelta
from services.mode_service import is_demo_mode
from utils.mock_data import get_mock_transactions
from plaid.model.transactions_get_request import TransactionsGetRequest
from utils.plaid_helpers import get_plaid_client
from utils.transaction_validator import format_transaction

# Stockage temporaire des transactions de test
DEMO_TRANSACTIONS = {}

def get_transactions(user_id, days=30, access_token=None):
    """
    Récupère les transactions pour un utilisateur.
    En mode demo, utilise les données générées.
    En mode prod, utilise Plaid ou les transactions de la base de données.
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        days (int, optional): Nombre de jours de transactions à récupérer
        access_token (str, optional): Token d'accès Plaid (en mode prod)
        
    Returns:
        list: Liste des transactions
    """
    if is_demo_mode():
        # Récupérer les transactions de test
        return get_demo_transactions(user_id, days)
    
    # Mode prod
    if access_token:
        # Utiliser Plaid
        return get_plaid_transactions(access_token, days)
    
    # Si aucun token d'accès n'est fourni, on n'a pas de données à montrer
    # Dans une application réelle, on pourrait récupérer des transactions
    # manuelles depuis une base de données
    return []

def get_demo_transactions(user_id, days=30):
    """
    Récupère ou génère des transactions de test pour un utilisateur
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        days (int): Nombre de jours de transactions à récupérer
        
    Returns:
        list: Liste des transactions de test
    """
    # Vérifier si nous avons déjà des transactions pour cet utilisateur
    if user_id not in DEMO_TRANSACTIONS:
        # Générer des transactions de test
        base_transactions = get_mock_transactions(days=days)
        
        # Stocker les transactions
        DEMO_TRANSACTIONS[user_id] = {
            "base_transactions": base_transactions,
            "custom_transactions": [],
            "generated_at": datetime.now().timestamp()
        }
    
    # Combiner les transactions de base et personnalisées
    user_data = DEMO_TRANSACTIONS[user_id]
    all_transactions = user_data["base_transactions"] + user_data["custom_transactions"]
    
    # Trier par date (plus récentes d'abord)
    all_transactions.sort(key=lambda x: x["date"], reverse=True)
    
    return all_transactions

def get_plaid_transactions(access_token, days=30):
    """
    Récupère les transactions depuis Plaid
    
    Args:
        access_token (str): Token d'accès Plaid
        days (int): Nombre de jours de transactions à récupérer
        
    Returns:
        list: Liste des transactions
    """
    client = get_plaid_client()
    
    # Calculer les dates de début et de fin
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Récupérer les transactions
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date
    )
    
    response = client.transactions_get(request)
    transactions = response['transactions']
    
    # Formater les transactions pour le frontend
    # Utilisation de format_transaction pour assurer la cohérence du format
    return [format_transaction(transaction) for transaction in transactions]

def add_transaction(user_id, transaction_data):
    """
    Ajoute une transaction (réelle ou de test selon le mode)
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        transaction_data (dict): Données de la transaction
        
    Returns:
        dict: La transaction ajoutée
    """
    if is_demo_mode():
        return add_demo_transaction(user_id, transaction_data)
    
    # En mode prod, on ajouterait à la base de données
    # Ceci est un exemple simplifié
    return {"error": "Ajout de transactions manuelles non implémenté en mode prod"}

def add_demo_transaction(user_id, transaction_data):
    """
    Ajoute une transaction de test
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        transaction_data (dict): Données de la transaction
        
    Returns:
        dict: La transaction ajoutée
    """
    # Initialiser les données utilisateur si nécessaires
    if user_id not in DEMO_TRANSACTIONS:
        get_demo_transactions(user_id)  # Initialise les données
    
    # Formater la transaction pour s'assurer qu'elle est conforme au schéma
    transaction = format_transaction(transaction_data)
    
    # Marquer comme données de test
    transaction["is_test_data"] = True
    
    # Ajouter à la liste des transactions personnalisées
    DEMO_TRANSACTIONS[user_id]["custom_transactions"].append(transaction)
    return transaction

def reset_demo_transactions(user_id, days=30):
    """
    Réinitialise les transactions de test pour un utilisateur
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        days (int): Nombre de jours de transactions à récupérer
        
    Returns:
        list: Liste des transactions réinitialisées
    """
    if not is_demo_mode():
        return {"error": "Cette opération n'est disponible qu'en mode test"}
    
    # Générer de nouvelles transactions de base
    base_transactions = get_mock_transactions(days=days)
    
    # Conserver les transactions personnalisées
    custom_transactions = []
    if user_id in DEMO_TRANSACTIONS:
        custom_transactions = DEMO_TRANSACTIONS[user_id]["custom_transactions"]
    
    # Mettre à jour le stockage
    DEMO_TRANSACTIONS[user_id] = {
        "base_transactions": base_transactions,
        "custom_transactions": custom_transactions,
        "generated_at": datetime.now().timestamp()
    }
    
    # Renvoyer toutes les transactions
    all_transactions = base_transactions + custom_transactions
    all_transactions.sort(key=lambda x: x["date"], reverse=True)
    
    return all_transactions