"""
Module pour valider et formater les transactions selon un schéma commun
"""
import uuid
from datetime import datetime
from utils.schema_loader import TRANSACTION_SCHEMA, CATEGORIES_SCHEMA

def format_transaction(transaction):
    """
    Formate une transaction pour assurer un format cohérent
    Conserve les données existantes si elles sont déjà au bon format
    """
    # Si c'est déjà un dictionnaire avec le format de catégorie correct
    if (isinstance(transaction, dict) and 
        "category" in transaction and 
        isinstance(transaction["category"], dict) and
        "subcategory" in transaction["category"] and
        isinstance(transaction["category"]["subcategory"], dict)):
        return transaction
    
    # Déterminer si c'est un dict ou un objet
    is_dict = isinstance(transaction, dict)
    
    # Extraire les valeurs (soit d'un dict, soit d'un objet)
    def get_value(key, default=None):
        if is_dict:
            return transaction.get(key, default)
        return getattr(transaction, key, default)
    
    # Traiter la catégorie
    category_id = "other"
    subcategory_id = "unknown"
    
    category_value = get_value('category')
    if category_value:
        if isinstance(category_value, dict):
            # Si la catégorie est déjà un dict mais pas complètement formatée
            category_id = category_value.get('id', 'other')
            if 'subcategory' in category_value and isinstance(category_value['subcategory'], dict):
                subcategory_id = category_value['subcategory'].get('id', 'unknown')
        elif isinstance(category_value, str):
            if category_value != "Non catégorisé":
                categories = category_value.split(', ')
                if categories:
                    category_id = categories[0].lower().replace(' ', '') if categories[0] else "other"
                    if len(categories) > 1:
                        subcategory_id = categories[1].lower().replace(' ', '')
        elif isinstance(category_value, list):
            if category_value:
                category_id = category_value[0].lower().replace(' ', '') if category_value[0] else "other"
                if len(category_value) > 1:
                    subcategory_id = category_value[1].lower().replace(' ', '')
    
    # Construire le résultat
    result = {
        "id": get_value('id', f"txn_{uuid.uuid4().hex[:12]}"),
        "date": get_value('date', datetime.now().strftime('%Y-%m-%d')),
        "merchant_name": get_value('merchant_name') or get_value('name', "Unknown Merchant"),
        "amount": get_value('amount', 0.0),
        "category": {
            "id": category_id,
            "subcategory": {
                "id": subcategory_id
            }
        },
        "payment_channel": get_value('payment_channel', 'other'),
        "pending": get_value('pending', False),
        "is_test_data": get_value('is_test_data', False)
    }
    
    return result