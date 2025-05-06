"""
Service de gestion des transactions (manuelles et de test)
"""
from datetime import datetime, timedelta
from services.mode_service import is_demo_mode
from utils.mock_data import get_mock_transactions
from utils.transaction_validator import format_transaction
from models import db, Transaction
import json
import uuid

def get_transactions(user_id, days=30):
    """
    Récupère les transactions pour un utilisateur.
    En mode demo, utilise les données générées.
    En mode prod, utilise les transactions manuelles de la base de données.
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        days (int, optional): Nombre de jours de transactions à récupérer
        
    Returns:
        list: Liste des transactions
        
    Raises:
        ValueError: Si l'ID utilisateur n'est pas fourni
    """
    # Vérifier que user_id n'est pas vide ou None
    if not user_id:
        print("Erreur: Tentative d'accès aux transactions sans ID utilisateur")
        raise ValueError("L'ID utilisateur est requis pour accéder aux transactions")
    
    if is_demo_mode():
        # Récupérer les transactions de test
        return get_demo_transactions(user_id, days)
    else :
    # Mode prod - récupérer les transactions manuelles depuis la base de données
        return get_manual_transactions(user_id, days)

def get_demo_transactions(user_id, days=30):
    """
    Récupère ou génère des transactions de test pour un utilisateur
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        days (int): Nombre de jours de transactions à récupérer
        
    Returns:
        list: Liste des transactions de test
    """
    if not user_id:
        raise ValueError("L'ID utilisateur est requis")
    
    # Vérifier si nous avons déjà des transactions de test pour cet utilisateur
    transactions_count = Transaction.query.filter_by(
        user_id=user_id, 
        is_test_data=True
    ).count()
    
    if transactions_count == 0:
        # Générer des transactions de test
        mock_transactions = get_mock_transactions(days=days)
        
        # Stocker les transactions dans la base de données
        for tx_data in mock_transactions:
            # Créer une nouvelle transaction
            transaction = Transaction(
                id=tx_data.get("id", f"tx_{uuid.uuid4().hex}"),
                user_id=user_id,
                amount=tx_data.get("amount", 0),
                date=tx_data.get("date", datetime.now().strftime("%Y-%m-%d")),
                merchant_name=tx_data.get("merchant_name", "Unknown"),
                payment_channel=tx_data.get("payment_channel", ""),
                pending=tx_data.get("pending", False),
                category=tx_data.get("category", {}).get("id", "other"),
                subcategory=tx_data.get("category", {}).get("subcategory", {}).get("id", "unknown"),
                is_test_data=True,
                is_manual=False,
                raw_data=json.dumps(tx_data)
            )
            db.session.add(transaction)
        
        db.session.commit()
        print(f"Généré et stocké {len(mock_transactions)} transactions de test pour l'utilisateur {user_id}")
    
    # Récupérer toutes les transactions de test pour cet utilisateur
    transactions = Transaction.query.filter_by(
        user_id=user_id, 
        is_test_data=True
    ).all()
    
    # Convertir en format API
    result = [tx.to_dict() for tx in transactions]
    
    # Trier par date décroissante
    result.sort(key=lambda x: x["date"], reverse=True)
    
    return result

def get_manual_transactions(user_id, days=30):
    """
    Récupère les transactions manuelles de l'utilisateur
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        days (int): Nombre de jours de transactions à récupérer
        
    Returns:
        list: Liste des transactions manuelles
    """
    return get_stored_transactions(user_id, days, is_manual=True)

def get_stored_transactions(user_id, days=30, is_test_data=None, is_manual=None):
    """
    Récupère les transactions stockées en base de données
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        days (int): Nombre de jours de transactions à récupérer
        is_test_data (bool): Filtre sur les données de test
        is_manual (bool): Filtre sur les transactions manuelles
        
    Returns:
        list: Liste des transactions stockées
    """
    # Calculer la date minimale
    min_date = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    
    # Construire la requête
    query = Transaction.query.filter(
        Transaction.user_id == user_id,
        Transaction.date >= min_date
    )
    
    # Appliquer les filtres supplémentaires si spécifiés
    if is_test_data is not None:
        query = query.filter(Transaction.is_test_data == is_test_data)
    
    if is_manual is not None:
        query = query.filter(Transaction.is_manual == is_manual)
    
    # Exécuter la requête
    transactions = query.all()
    
    # Convertir en format API
    result = [tx.to_dict() for tx in transactions]
    
    # Trier par date décroissante
    result.sort(key=lambda x: x["date"], reverse=True)
    
    return result

def add_transaction(user_id, transaction_data, is_test=False, is_manual=True):
    """
    Ajoute une transaction (réelle ou de test) en base de données
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        transaction_data (dict): Données de la transaction
        is_test (bool): Indique si c'est une transaction de test
        is_manual (bool): Indique si c'est une transaction manuelle
        
    Returns:
        dict: La transaction ajoutée
    """
    if not user_id:
        raise ValueError("L'ID utilisateur est requis")
    
    # Valider et formater la transaction
    formatted_tx = format_transaction(transaction_data)
    
    # Créer un ID si non fourni
    if "id" not in formatted_tx:
        formatted_tx["id"] = f"tx_{uuid.uuid4().hex}"
    
    # Créer une nouvelle transaction
    transaction = Transaction(
        id=formatted_tx.get("id"),
        user_id=user_id,
        amount=formatted_tx.get("amount", 0),
        date=formatted_tx.get("date"),
        merchant_name=formatted_tx.get("merchant_name"),
        payment_channel=formatted_tx.get("payment_channel"),
        pending=formatted_tx.get("pending", False),
        category=formatted_tx.get("category", {}).get("id", "other"),
        subcategory=formatted_tx.get("category", {}).get("subcategory", {}).get("id", "unknown"),
        is_test_data=is_test,
        is_manual=is_manual,
        raw_data=json.dumps(formatted_tx)
    )
    
    # Ajouter à la base de données
    db.session.add(transaction)
    db.session.commit()
    
    return transaction.to_dict()

def reset_demo_transactions(user_id, days=30):
    """
    Réinitialise les transactions de test pour un utilisateur
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        days (int): Nombre de jours de transactions à générer
        
    Returns:
        list: Liste des transactions réinitialisées
    """
    if not user_id:
        raise ValueError("L'ID utilisateur est requis")
    
    # Supprimer toutes les transactions de test automatiques (non manuelles)
    Transaction.query.filter_by(
        user_id=user_id, 
        is_test_data=True,
        is_manual=False
    ).delete()
    
    # Générer de nouvelles transactions de test
    mock_transactions = get_mock_transactions(days=days)
    
    # Stocker les nouvelles transactions
    for tx_data in mock_transactions:
        transaction = Transaction(
            id=tx_data.get("id", f"tx_{uuid.uuid4().hex}"),
            user_id=user_id,
            amount=tx_data.get("amount", 0),
            date=tx_data.get("date", datetime.now().strftime("%Y-%m-%d")),
            merchant_name=tx_data.get("merchant_name", "Unknown"),
            payment_channel=tx_data.get("payment_channel", ""),
            pending=tx_data.get("pending", False),
            category=tx_data.get("category", {}).get("id", "other"),
            subcategory=tx_data.get("category", {}).get("subcategory", {}).get("id", "unknown"),
            is_test_data=True,
            is_manual=False,
            raw_data=json.dumps(tx_data)
        )
        db.session.add(transaction)
    
    db.session.commit()
    
    # Récupérer toutes les transactions de test (y compris les manuelles)
    return get_stored_transactions(user_id, days, is_test_data=True)