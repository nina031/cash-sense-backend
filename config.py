"""
Configuration centralisée de l'application
"""
import os
from dotenv import load_dotenv

# Charger les variables d'environnement (pour les clés API, etc.)
load_dotenv()

# Configuration Plaid (uniquement utilisée en mode prod)
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv("PLAID_SECRET")
PLAID_ENV = os.getenv("PLAID_ENV", "development")