from flask import Flask
from flask_cors import CORS
import os
from api.plaid_routes import plaid_blueprint

app = Flask(__name__)

# Configuration de CORS
CORS(app, expose_headers=["Content-Type", "Authorization"], 
   allow_headers=["Content-Type", "Authorization"],
   supports_credentials=True)

# Initialiser le mode de l'application
app.config['APP_MODE'] = 'prod'  # Valeur par défaut: mode production

# Autres configurations
app.config['DEBUG'] = os.getenv("FLASK_ENV", "development") != "production"

# Enregistrer les blueprints
app.register_blueprint(plaid_blueprint, url_prefix='/api')

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