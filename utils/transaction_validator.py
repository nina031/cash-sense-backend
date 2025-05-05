
from utils.schema_loader import TRANSACTION_SCHEMA, CATEGORIES_SCHEMA

def format_transaction(transaction):
    """
    Vérifie si la transaction respecte le schéma défini dans TRANSACTION_SCHEMA 
    et CATEGORIES_SCHEMA.
    
    Args:
        transaction: La transaction à vérifier
        
    Returns:
        dict: La transaction validée
        
    Raises:
        Exception: Si le schéma n'est pas respecté
    """    
    # Vérification que la transaction est un dictionnaire
    if not isinstance(transaction, dict):
        raise Exception("La transaction doit être un dictionnaire")
    
    # Vérification des champs requis selon TRANSACTION_SCHEMA
    for field, expected_type in TRANSACTION_SCHEMA.items():
        # Vérifier présence du champ
        if field not in transaction:
            raise Exception(f"Schéma non respecté: champ '{field}' requis par TRANSACTION_SCHEMA est manquant")
        
        # Vérifier type simple
        if expected_type == "string" and not isinstance(transaction[field], str):
            raise Exception(f"Schéma non respecté: '{field}' doit être une chaîne de caractères")
        elif expected_type == "number" and not isinstance(transaction[field], (int, float)):
            raise Exception(f"Schéma non respecté: '{field}' doit être un nombre")
        elif expected_type == "boolean" and not isinstance(transaction[field], bool):
            raise Exception(f"Schéma non respecté: '{field}' doit être un booléen")
        elif expected_type == "object" and field == "category":
            # Vérification de la structure de catégorie
            cat = transaction["category"]
            
            # Vérifier que category est un dict avec un id
            if not isinstance(cat, dict) or "id" not in cat:
                raise Exception("Schéma non respecté: 'category' doit être un dict avec un champ 'id'")
            
            # Vérifier que l'id de category existe dans CATEGORIES_SCHEMA
            if cat["id"] not in CATEGORIES_SCHEMA:
                raise Exception(f"Schéma non respecté: catégorie '{cat['id']}' inconnue dans CATEGORIES_SCHEMA")
            
            # Vérifier que subcategory est un dict avec un id
            if "subcategory" not in cat or not isinstance(cat["subcategory"], dict) or "id" not in cat["subcategory"]:
                raise Exception("Schéma non respecté: manque 'subcategory' avec 'id' dans 'category'")
            
            # Vérifier que l'id de subcategory existe dans CATEGORIES_SCHEMA
            subcat_id = cat["subcategory"]["id"]
            if subcat_id != "unknown" and (
                "subcategories" not in CATEGORIES_SCHEMA[cat["id"]] or
                subcat_id not in CATEGORIES_SCHEMA[cat["id"]]["subcategories"]
            ):
                raise Exception(f"Schéma non respecté: sous-catégorie '{subcat_id}' inconnue pour catégorie '{cat['id']}'")
    
    # Si toutes les validations passent, retourner la transaction
    return transaction