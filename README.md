# Cash Sense Backend

API backend pour l'application de gestion budgétaire Cash Sense. Cette application utilise Flask et intègre plusieurs fonctionnalités avancées :

- Intégration avec l'API Plaid pour récupérer diverses données bancaires
- Modèles de machine learning pour l'analyse et la catégorisation des transactions
- Prévisions financières et analyses de tendances
- Recommandations personnalisées basées sur les habitudes de dépenses

## Fonctionnalités principales

### Intégration Plaid

- Connexion aux comptes bancaires via Plaid Link
- Récupération des transactions bancaires en temps réel
- Accès aux soldes et détails des comptes
- Support pour les virements et paiements (prévu)
- Récupération des informations sur les investissements (prévu)

### Machine Learning & Analyse de données

- Catégorisation automatique des transactions avec ML
- Détection des dépenses inhabituelles
- Prévisions de flux de trésorerie
- Identification des opportunités d'épargne
- Analyse des habitudes de dépenses

### Autres fonctionnalités

- Gestion des objectifs budgétaires
- Rapports financiers personnalisés
- Notifications et alertes personnalisées
- Exportation de données au format CSV/Excel

## Prérequis

- Python 3.8 ou supérieur
- Un compte Plaid avec des clés d'API (sandbox/développement/production)
- Bibliothèques de data science (pandas, scikit-learn, etc.)

## Installation

1. Clonez le dépôt

```bash
git clone https://github.com/votre-utilisateur/cash-sense-backend.git
cd cash-sense-backend
```

2. Créez un environnement virtuel et activez-le

```bash
python -m venv venv
source venv/bin/activate  # Sur Windows: venv\Scripts\activate
```

3. Installez les dépendances

```bash
pip install -r requirements.txt
```

4. Créez un fichier `.env` à la racine du projet

```
# Mode d'environnement (sand, dev, prod)
PLAID_ENV_MODE=sand

# ID Client
PLAID_CLIENT_ID=your_client_id

# Sandbox
PLAID_SECRET_sand=your_sandbox_secret
PLAID_ENV_sand=https://sandbox.plaid.com

# Développement
PLAID_SECRET_dev=your_dev_secret
PLAID_ENV_dev=https://development.plaid.com

# Production
PLAID_SECRET_prod=your_prod_secret
PLAID_ENV_prod=https://production.plaid.com

# Configuration de la base de données
DB_URI=sqlite:///cashsense.db  # ou votre URL de BDD
```

## Structure du projet

```
cash-sense-backend/
│
├── app.py                 # Point d'entrée principal de l'application
├── config.py              # Configuration centralisée
├── .env                   # Variables d'environnement (non commité)
├── requirements.txt       # Dépendances du projet
│
├── api/                   # Routes API
│   ├── __init__.py
│   ├── plaid_routes.py    # Routes liées à Plaid
│   ├── ml_routes.py       # Routes liées au machine learning
│   ├── budgets_routes.py  # Routes liées aux budgets
│   └── reports_routes.py  # Routes liées aux rapports
│
├── services/              # Logique métier
│   ├── __init__.py
│   ├── plaid_service.py   # Service pour interagir avec l'API Plaid
│   ├── ml_service.py      # Service pour les prédictions ML
│   └── analysis_service.py # Service pour l'analyse des données
│
├── models/                # Modèles de données et ML
│   ├── __init__.py
│   ├── db_models.py       # Modèles de base de données
│   ├── transaction_classifier.py # Modèle de classification des transactions
│   └── spending_predictor.py    # Modèle de prédiction des dépenses
│
├── utils/                 # Fonctions utilitaires
│   ├── __init__.py
│   ├── plaid_helpers.py   # Helpers pour Plaid
│   └── data_processing.py # Traitement des données
│
├── data/                  # Dossier pour les données et modèles entraînés
│   ├── models/            # Modèles ML entraînés
│   └── training/          # Données d'entraînement
│
├── notebooks/             # Notebooks Jupyter pour l'analyse et le développement ML
│   ├── retreive_data_plaid.ipynb
│   ├── transaction_categorization.ipynb
│   └── spending_prediction.ipynb
│
└── migrations/            # Migrations de base de données (si utilisé)
```

## Exécution

```bash
python app.py
```

L'API sera disponible à `http://localhost:5000`.

## Endpoints API

### Système

- **GET /** : Vérifie si l'API est en cours d'exécution

### Plaid API

- **POST /api/create_link_token** : Crée un token de liaison pour initialiser Plaid Link
- **POST /api/exchange_token** : Échange un token public contre un token d'accès
- **POST /api/get_transactions** : Récupère les transactions bancaires
- **POST /api/get_accounts** : Récupère les informations des comptes
- **POST /api/get_balances** : Récupère les soldes actuels des comptes
- **POST /api/get_investments** : Récupère les données d'investissement (prévu)

### Machine Learning

- **POST /api/categorize_transaction** : Catégorise une transaction avec le modèle ML
- **POST /api/predict_expenses** : Prédit les dépenses futures
- **POST /api/detect_anomalies** : Détecte les transactions inhabituelles
- **GET /api/retrain_models** : Déclenche un réentraînement des modèles

### Budgets & Rapports

- **GET /api/budget_summary** : Récupère le résumé du budget
- **POST /api/set_budget_goal** : Définit un objectif budgétaire
- **GET /api/spending_report** : Génère un rapport de dépenses
- **GET /api/savings_opportunities** : Identifie les opportunités d'épargne

### Endpoints de développement/test

- **POST /api/create_sandbox_token** : Crée un token public sandbox pour les tests

## Exemples d'utilisation avec curl

### Créer un token de liaison

```bash
curl -X POST http://localhost:5000/api/create_link_token \
  -H "Content-Type: application/json"
```

### Créer un token public sandbox (pour les tests)

```bash
curl -X POST http://localhost:5000/api/create_sandbox_token \
  -H "Content-Type: application/json" \
  -d '{"institution_id": "ins_1"}'
```

### Échanger un token public contre un token d'accès

```bash
curl -X POST http://localhost:5000/api/exchange_token \
  -H "Content-Type: application/json" \
  -d '{"public_token": "votre_public_token"}'
```

### Récupérer les transactions

```bash
curl -X POST http://localhost:5000/api/get_transactions \
  -H "Content-Type: application/json" \
  -d '{"access_token": "votre_access_token"}'
```

### Catégoriser une transaction avec ML

```bash
curl -X POST http://localhost:5000/api/categorize_transaction \
  -H "Content-Type: application/json" \
  -d '{"description": "CARREFOUR", "amount": 52.30}'
```

## Changement d'environnement

Pour changer d'environnement (sandbox, développement, production), modifiez la variable `PLAID_ENV_MODE` dans le fichier `.env` ou passez-la en variable d'environnement au lancement :

```bash
PLAID_ENV_MODE=prod python app.py
```

## Modèles de Machine Learning

### Catégorisation des transactions

- Utilise un modèle de classification supervisée (RandomForest, XGBoost)
- Entraîné sur l'historique des transactions catégorisées
- Prend en compte la description, le montant et d'autres métadonnées

### Prédiction des dépenses

- Modèle de série temporelle pour prédire les dépenses futures
- Analyse les tendances saisonnières et les cycles récurrents
- Génère des prévisions de dépenses par catégorie

### Recommandations d'épargne

- Analyse les habitudes de dépenses et identifie les opportunités d'optimisation
- Suggère des ajustements budgétaires basés sur l'historique

## Sécurité

- Ne jamais commiter le fichier `.env` contenant vos clés d'API
- En production, stockez les tokens d'accès de manière sécurisée
- Implémentez un système d'authentification pour sécuriser votre API
- Chiffrez les données sensibles dans la base de données
- Utilisez HTTPS en production

## Déploiement

### Sur un serveur

```bash
# Installer gunicorn
pip install gunicorn

# Lancer avec gunicorn
gunicorn -w 4 -b 0.0.0.0:5000 app:app
```

### Avec Docker

Un Dockerfile est inclus pour faciliter le déploiement.

```bash
# Construire l'image
docker build -t cash-sense-backend .

# Exécuter le conteneur
docker run -p 5000:5000 -d cash-sense-backend
```

## Contribution

1. Forkez le projet
2. Créez votre branche de fonctionnalité (`git checkout -b feature/nouvelle-fonctionnalite`)
3. Committez vos changements (`git commit -m 'Ajout d'une nouvelle fonctionnalité'`)
4. Poussez vers la branche (`git push origin feature/nouvelle-fonctionnalite`)
5. Ouvrez une Pull Request

## Licence

Ce projet est sous licence MIT.
