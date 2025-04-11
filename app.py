from flask import Flask
from flask_cors import CORS
import os
from api.plaid_routes import plaid_blueprint
from config import DEBUG  # Importer la config

app = Flask(__name__)
# Configuration de CORS
CORS(app, expose_headers=["Content-Type", "Authorization"], 
     allow_headers=["Content-Type", "Authorization"],
     supports_credentials=True,
     allow_private_network=False)  

# Enregistrer les blueprints
app.register_blueprint(plaid_blueprint, url_prefix='/api')

@app.route('/')
def health_check():
    return {'status': 'ok', 'message': 'Cash Sense API is running!'}

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=DEBUG)  # Utiliser DEBUG de la config