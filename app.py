from flask import Flask
from flask_cors import CORS
import os
from api.transaction_routes import transaction_blueprint
from api.demo_routes import demo_blueprint
from models import db  # Importer la base de données

app = Flask(__name__)

# Configuration de CORS
CORS(app, expose_headers=["Content-Type", "Authorization"], 
   allow_headers=["Content-Type", "Authorization"],
   supports_credentials=True)

# Initialiser le mode de l'application
app.config['APP_MODE'] = 'prod'  # Valeur par défaut: mode production

# Configuration de la base de données
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL', 'sqlite:///cashsense.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialisation de la base de données
db.init_app(app)

# Créer les tables si elles n'existent pas
with app.app_context():
    db.create_all()

# Autres configurations
app.config['DEBUG'] = os.getenv("FLASK_ENV", "development") != "production"

# Enregistrer les blueprints
app.register_blueprint(transaction_blueprint, url_prefix='/api')
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