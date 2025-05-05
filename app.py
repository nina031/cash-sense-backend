from flask import Flask
from flask_cors import CORS
import os
from api.plaid_routes import plaid_blueprint
from api.demo_routes import demo_blueprint
import config  # Importer les configurations
from models import db  # Importer la base de données

app = Flask(__name__)

# Configuration de CORS
CORS(app, expose_headers=["Content-Type", "Authorization"], 
   allow_headers=["Content-Type", "Authorization"],
   supports_credentials=True)

# Initialiser le mode de l'application
app.config['APP_MODE'] = 'prod'  # Valeur par défaut: mode production

# Configurer Plaid
app.config['PLAID_CLIENT_ID'] = config.PLAID_CLIENT_ID
app.config['PLAID_SECRET'] = config.PLAID_SECRET
app.config['PLAID_ENV'] = config.PLAID_ENV

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = config.DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db.init_app(app)

# Créer les tables si elles n'existent pas
with app.app_context():
    db.create_all()

# Autres configurations
app.config['DEBUG'] = os.getenv("FLASK_ENV", "development") != "production"

# Enregistrer les blueprints
app.register_blueprint(plaid_blueprint, url_prefix='/api')
app.register_blueprint(demo_blueprint, url_prefix='/api')

@app.route('/')
def health_check():
    """Vérifie si l'API est en cours d'exécution"""
    environment = "test" if app.config['APP_MODE'] == 'demo' else "production"
    return {
        'status': 'ok', 
        'message': f'Cash Sense API is running in {environment} mode!'
    }

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=app.config['DEBUG'])