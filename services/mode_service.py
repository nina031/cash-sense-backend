"""
Module de gestion du mode de l'application (prod ou demo)
"""
from flask import current_app

def get_current_mode():
    """
    Retourne le mode actuel de l'application
    
    Returns:
        str: 'prod' ou 'demo'
    """
    return current_app.config.get('APP_MODE', 'prod')

def toggle_demo_mode(enable_demo):
    """
    Active ou désactive le mode demo
    
    Args:
        enable_demo (bool): True pour activer le mode demo, False pour le désactiver
        
    Returns:
        str: Le nouveau mode ('prod' ou 'demo')
    """
    new_mode = 'demo' if enable_demo else 'prod'
    current_app.config['APP_MODE'] = new_mode
    return new_mode

def is_demo_mode():
    """
    Vérifie si l'application est en mode demo
    
    Returns:
        bool: True si en mode demo, False sinon
    """
    return get_current_mode() == 'demo'