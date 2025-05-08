def extract_category_data(transaction_data):
    """
    Extrait les identifiants de catégorie et sous-catégorie d'une transaction
    
    Args:
        transaction_data (dict): Données de la transaction
        
    Returns:
        tuple: (category_id, subcategory_id)
    """
    # Valeurs par défaut
    category_id = "other"
    subcategory_id = "unknown"
    
    # Extraction de la catégorie
    if "category" in transaction_data and isinstance(transaction_data["category"], dict):
        category = transaction_data["category"]
        if "id" in category:
            category_id = category["id"]
        
        # Extraction de la sous-catégorie
        if "subcategory" in category and isinstance(category["subcategory"], dict):
            if "id" in category["subcategory"]:
                subcategory_id = category["subcategory"]["id"]
    
    return category_id, subcategory_id