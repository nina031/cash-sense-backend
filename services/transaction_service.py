"""
Service de gestion des transactions (manuelles et de test)
"""
from datetime import datetime, timedelta
from services.mode_service import is_demo_mode
from utils.mock_data import get_mock_transactions
from utils.transaction_validator import format_transaction
from utils.category_utils import extract_category_data
from db_models import db, Transaction
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
        userId=user_id, 
        isTestData=True
    ).count()
    
    if transactions_count == 0:
        # Générer des transactions de test
        mock_transactions = get_mock_transactions(days=days)
        
        # Stocker les transactions dans la base de données
        for tx_data in mock_transactions:
            category_id, subcategory_id = extract_category_data(tx_data)
            
            # Créer une nouvelle transaction
            transaction = Transaction(
                id=tx_data.get("id", f"tx_{uuid.uuid4().hex}"),
                userId=user_id,
                amount=tx_data.get("amount", 0),
                date=tx_data.get("date", datetime.now().strftime("%Y-%m-%d")),
                merchantName=tx_data.get("merchant_name", "Unknown"),
                paymentChannel=tx_data.get("payment_channel", ""),
                pending=tx_data.get("pending", False),
                category=category_id,
                subcategory=subcategory_id,
                isTestData=True,
                isManual=False
            )
            db.session.add(transaction)
        
        db.session.commit()
        print(f"Généré et stocké {len(mock_transactions)} transactions de test pour l'utilisateur {user_id}")
    
    # Récupérer toutes les transactions de test pour cet utilisateur
    transactions = Transaction.query.filter_by(
        userId=user_id, 
        isTestData=True
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
        Transaction.userId == user_id,
        Transaction.date >= min_date
    )
    
    # Appliquer les filtres supplémentaires si spécifiés
    if is_test_data is not None:
        query = query.filter(Transaction.isTestData == is_test_data)
    
    if is_manual is not None:
        query = query.filter(Transaction.isManual == is_manual)
    
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
    
    # Créer un ID si non fourni
    if "id" not in transaction_data:
        transaction_data["id"] = f"tx_{uuid.uuid4().hex}"

    # Valider et formater la transaction
    formatted_tx = format_transaction(transaction_data)
    
    category_id, subcategory_id = extract_category_data(formatted_tx)
    
    # Créer une nouvelle transaction
    transaction = Transaction(
        id=formatted_tx.get("id"),
        userId=user_id,
        amount=formatted_tx.get("amount", 0),
        date=formatted_tx.get("date"),
        merchantName=formatted_tx.get("merchant_name"),
        paymentChannel=formatted_tx.get("payment_channel"),
        pending=formatted_tx.get("pending", False),
        category=category_id,
        subcategory=subcategory_id,
        isTestData=is_test,
        isManual=is_manual
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
        userId=user_id, 
        isTestData=True,
        isManual=False
    ).delete()
    
    # Générer de nouvelles transactions de test
    mock_transactions = get_mock_transactions(days=days)
    
    # Stocker les nouvelles transactions
    for tx_data in mock_transactions:
        # Extraire les données de catégorie
        category_id = "other"
        subcategory_id = "unknown"
        category_id, subcategory_id = extract_category_data(tx_data)
        
        transaction = Transaction(
            id=tx_data.get("id", f"tx_{uuid.uuid4().hex}"),
            userId=user_id,
            amount=tx_data.get("amount", 0),
            date=tx_data.get("date", datetime.now().strftime("%Y-%m-%d")),
            merchantName=tx_data.get("merchant_name", "Unknown"),
            paymentChannel=tx_data.get("payment_channel", ""),
            pending=tx_data.get("pending", False),
            category=category_id,
            subcategory=subcategory_id,
            isTestData=True,
            isManual=False
            # Supprimer cette ligne
            # rawData=json.dumps(tx_data)
        )
        db.session.add(transaction)
    
    db.session.commit()
    
    # Récupérer toutes les transactions de test (y compris les manuelles)
    return get_stored_transactions(user_id, days, is_test_data=True)