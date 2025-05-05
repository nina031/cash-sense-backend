"""
Utilitaire pour charger les schémas JSON
"""
import json
import os
import logging

# Configurer le logger
logger = logging.getLogger(__name__)

def get_schema_path(filename):
    """
    Obtient le chemin vers un fichier de schéma
    
    Args:
        filename (str): Nom du fichier de schéma
        
    Returns:
        str: Chemin complet vers le fichier
    """
    # Chemin relatif depuis la racine du projet
    root_path = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    schema_path = os.path.join(root_path, 'schemas', filename)
    
    return schema_path

def load_schema(filename):
    """
    Charge un schéma JSON depuis le dossier schemas
    
    Args:
        filename (str): Nom du fichier à charger
        
    Returns:
        dict: Contenu du schéma JSON
    """
    schema_path = get_schema_path(filename)
    
    try:
        with open(schema_path, 'r', encoding='utf-8') as f:
            return json.load(f)
    except FileNotFoundError:
        logger.error(f"Schéma '{filename}' introuvable à {schema_path}")
        return {}
    except json.JSONDecodeError:
        logger.error(f"Format JSON invalide dans le schéma '{filename}'")
        return {}

# Charger les schémas
TRANSACTION_SCHEMA = load_schema('transaction.json')
CATEGORIES_SCHEMA = load_schema('categories.json')