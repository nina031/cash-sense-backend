Cash Sense Backend
API backend pour l'application de gestion budgétaire Cash Sense. Cette application utilise Flask et fournit une solution simple pour suivre vos dépenses :

Mode démo avec des données fictives pour tester l'application
Mode production avec saisie manuelle des transactions
Catégorisation des transactions
Analyses visuelles des dépenses

Fonctionnalités principales
Gestion des transactions

Saisie manuelle des transactions
Mode démo avec données fictives générées automatiquement
Récupération des transactions par période
Catégorisation des transactions

Analyse de données

Visualisation des dépenses par catégorie
Répartition des revenus et dépenses
Tendances des dépenses sur le temps

Autres fonctionnalités

Gestion des objectifs budgétaires (prévu)
Rapports financiers personnalisés (prévu)
Notifications et alertes personnalisées (prévu)
Exportation de données au format CSV/Excel (prévu)

Prérequis

Python 3.8 ou supérieur
Base de données (SQLite en développement, PostgreSQL en production)

Installation

Clonez le dépôt

bashgit clone https://github.com/votre-utilisateur/cash-sense-backend.git
cd cash-sense-backend

Créez un environnement virtuel et activez-le

bashpython -m venv venv
source venv/bin/activate # Sur Windows: venv\Scripts\activate

Installez les dépendances

bashpip install -r requirements.txt

Créez un fichier .env à la racine du projet

Structure du projet
cash-sense-backend/
│
├── app.py # Point d'entrée principal de l'application
├── config.py # Configuration centralisée
├── .env # Variables d'environnement (non commité)
├── requirements.txt # Dépendances du projet
│
├── api/ # Routes API
│ ├── **init**.py
│ ├── transaction_routes.py # Routes liées aux transactions
│ ├── demo_routes.py # Routes liées au mode démo
│ └── reports_routes.py # Routes liées aux rapports
│
├── services/ # Logique métier
│ ├── **init**.py
│ ├── transaction_service.py # Service pour gérer les transactions
│ ├── mode_service.py # Service pour gérer les modes de l'application
│ └── analysis_service.py # Service pour l'analyse des données
│
├── models/ # Modèles de données
│ ├── **init**.py
│ └── db_models.py # Modèles de base de données
│
├── utils/ # Fonctions utilitaires
│ ├── **init**.py
│ ├── transaction_validator.py # Validation des transactions
│ ├── mock_data.py # Génération de données fictives
│ └── schema_loader.py # Chargement des schémas JSON
│
├── schemas/ # Schémas JSON pour la validation
│ ├── transaction.json # Schéma de transaction
│ └── categories.json # Schéma des catégories
│
└── migrations/ # Migrations de base de données (si utilisé)
Exécution
bashpython app.py
L'API sera disponible à http://localhost:5000.
Endpoints API
Système

GET / : Vérifie si l'API est en cours d'exécution

Transactions

POST /api/get_transactions : Récupère les transactions de l'utilisateur
POST /api/add_transaction : Ajoute une transaction manuelle

Mode démo

POST /api/toggle_demo_mode : Active ou désactive le mode démo
POST /api/reset_test_transactions : Réinitialise les transactions de test

Exemples d'utilisation avec curl
Activer le mode démo
bashcurl -X POST http://localhost:5000/api/toggle_demo_mode \
 -H "Content-Type: application/json" \
 -d '{"enable_demo": true, "user_id": "demo_user"}'
Récupérer les transactions
bashcurl -X POST http://localhost:5000/api/get_transactions \
 -H "Content-Type: application/json" \
 -d '{"user_id": "votre_user_id", "days": 30}'
Ajouter une transaction manuelle
bashcurl -X POST http://localhost:5000/api/add_transaction \
 -H "Content-Type: application/json" \
 -d '{
"user_id": "votre_user_id",
"transaction": {
"date": "2025-05-01",
"merchant_name": "Carrefour",
"amount": 52.30,
"category": {
"id": "foodAndDrink",
"subcategory": {
"id": "groceries"
}
},
"payment_channel": "in store"
}
}'
Modes d'application
L'application peut fonctionner dans deux modes :

Mode production : Les utilisateurs doivent saisir manuellement leurs transactions
Mode démo : Des données fictives sont générées pour tester les fonctionnalités

Pour changer de mode, utilisez l'endpoint /api/toggle_demo_mode.
Sécurité

Ne jamais commiter le fichier .env contenant vos informations sensibles
En production, implémentez un système d'authentification robuste
Chiffrez les données sensibles dans la base de données
Utilisez HTTPS en production

Déploiement
Sur un serveur
bash# Installer gunicorn
pip install gunicorn

# Lancer avec gunicorn

gunicorn -w 4 -b 0.0.0.0:5000 app:app -c gunicorn_config.py
Avec Render
Le projet inclut un fichier render.yaml pour un déploiement facile sur Render.com.
Prochaines fonctionnalités (v2)

Intégration avec des APIs bancaires pour la synchronisation automatique
Catégorisation automatique des transactions
Prévisions de dépenses
Suggestions d'économies

Contribution

Forkez le projet
Créez votre branche de fonctionnalité (git checkout -b feature/nouvelle-fonctionnalite)
Committez vos changements (git commit -m 'Ajout d'une nouvelle fonctionnalité')
Poussez vers la branche (git push origin feature/nouvelle-fonctionnalite)
Ouvrez une Pull Request

Licence
Ce projet est sous licence MIT.
