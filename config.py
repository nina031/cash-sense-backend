import os
from dotenv import load_dotenv

# Charger les variables d'environnement
load_dotenv()

# Définir l'environnement (sand, dev, prod)
# Peut être défini via une variable d'environnement ou en dur
ENV = os.getenv("PLAID_ENV_MODE", "sand")  # Valeur par défaut: sandbox

# Configuration Plaid basée sur l'environnement
PLAID_CLIENT_ID = os.getenv("PLAID_CLIENT_ID")
PLAID_SECRET = os.getenv(f"PLAID_SECRET_{ENV}")
PLAID_ENV = os.getenv(f"PLAID_ENV_{ENV}")

# Autres configurations
DEBUG = ENV != "prod"  # Activer le mode debug sauf en production