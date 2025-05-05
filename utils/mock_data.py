"""
Module qui génère des données de transactions fictives pour le mode test.
"""
import random
import uuid
from datetime import datetime, timedelta
import calendar
from utils.schema_loader import CATEGORIES_SCHEMA
from utils.transaction_validator import format_transaction

# Données de base pour générer des transactions
MERCHANTS = {
    'foodAndDrink': ['Restaurant Le Gourmet', 'Carrefour'],
    'shopping': ['Amazon', 'Zara'],
    'transport': ['RATP', 'Uber'],
    'travel': ['Booking.com', 'Air France'],
    'transfer': ['BNP Paribas', 'Société Générale'],
    'payment': ['EDF', 'Orange'],
    'health': ['Pharmacie Centrale', 'Dr Martin'],
    'entertainment': ['Netflix', 'Spotify'],
    'income': ['Entreprise XYZ', 'Freelance'],
    'other': ['Frais Bancaires', 'Divers']
}

# Configuration des transactions
TX_TYPES = {
    # Transactions récurrentes
    "RECURRING": [
        {"name": "Salaire", "category": "income", "subcategory": "salary", "amount": (-2000, -1800), "days": [1, 30]},
        {"name": "Loyer", "category": "payment", "subcategory": "bills", "amount": (600, 1200), "days": [1, 5]},
        {"name": "Internet", "category": "payment", "subcategory": "bills", "amount": (30, 60), "days": [5, 15]},
        {"name": "Électricité", "category": "payment", "subcategory": "bills", "amount": (40, 120), "days": [7, 17]},
        {"name": "Netflix", "category": "entertainment", "subcategory": "subscriptions", "amount": (9, 18), "days": [10, 20]}
    ],
    
    # Transactions exceptionnelles
    "SPECIAL": [
        {"name": "Restaurant Gastronomique", "category": "foodAndDrink", "subcategory": "restaurants", 
         "amount": (80, 200), "months": None, "probability": 0.2},
        {"name": "Apple Store", "category": "shopping", "subcategory": "electronics", 
         "amount": (100, 1200), "months": None, "probability": 0.15},
        {"name": "Prime", "category": "income", "subcategory": "salary", 
         "amount": (-1000, -300), "months": None, "probability": 0.1},
        {"name": "Transport Vacances", "category": "travel", "subcategory": "trainTickets", 
         "amount": (80, 300), "months": [6, 7, 8], "probability": 0.6},
        {"name": "Cadeaux Noël", "category": "shopping", "subcategory": "clothing", 
         "amount": (50, 300), "months": [12], "probability": 0.8}
    ]
}

def create_transaction(data, date):
    """Crée une transaction formatée à partir des données de base"""
    # Générer un montant aléatoire dans la plage spécifiée
    min_amount, max_amount = data.get("amount", (5, 200))
    amount = round(random.uniform(min_amount, max_amount), 2)
    
    # Créer la structure de la transaction
    tx = {
        "amount": amount,
        "date": date.strftime("%Y-%m-%d"),
        "merchant_name": data.get("name", "Inconnu"),
        "payment_channel": "online" if amount < 0 else random.choice(["in store", "online"]),
        "pending": False,
        "id": f"txn_{uuid.uuid4().hex[:12]}",
        "category": {
            "id": data.get("category", "other"),
            "subcategory": {
                "id": data.get("subcategory", "unknown")
            }
        },
        "is_test_data": True
    }
    
    # Valider le format avec notre validateur standard
    return format_transaction(tx)

def generate_monthly_transactions(year, month, start_date=None, end_date=None, min_count=10):
    """Génère les transactions pour un mois spécifique, en garantissant les récurrentes"""
    # Calculer les dates du mois
    month_start = datetime(year, month, 1).date()
    last_day = calendar.monthrange(year, month)[1]
    month_end = datetime(year, month, last_day).date()
    
    # Appliquer les filtres de date si nécessaire
    if (start_date and start_date > month_end) or (end_date and end_date < month_start):
        return []
        
    actual_start = max(month_start, start_date) if start_date else month_start
    actual_end = min(month_end, end_date) if end_date else month_end
    
    if actual_start > actual_end:
        return []
    
    transactions = []
    
    # 1. Ajouter les transactions récurrentes - TOUJOURS dans les 5 premiers jours du mois
    for index, tx_config in enumerate(TX_TYPES["RECURRING"]):
        # Attribuer un jour fixe entre 1 et 5 (en fonction de l'index de la transaction)
        fixed_day = (index % 5) + 1  # Jour entre 1 et 5
        
        # Vérifier que le jour est valide pour ce mois (pour gérer les mois courts)
        if fixed_day <= last_day:
            # Créer la date pour cette transaction
            tx_date = datetime(year, month, fixed_day).date()
            
            # Créer la transaction (sans tenir compte de la période filtrée)
            # Cela garantit que chaque mois aura toujours ses transactions récurrentes
            tx_config_copy = tx_config.copy()
            tx_config_copy["days"] = [fixed_day]  # Jour fixe pour documentation
            transactions.append(create_transaction(tx_config_copy, tx_date))
    
    # 2. Ajouter les transactions spéciales pour ce mois
    for tx_config in TX_TYPES["SPECIAL"]:
        # Vérifier si la transaction s'applique ce mois-ci
        if tx_config["months"] and month not in tx_config["months"]:
            continue
            
        # Vérifier la probabilité
        if random.random() > tx_config["probability"]:
            continue
            
        # Choisir une date aléatoire dans la période filtrée du mois
        days_in_range = (actual_end - actual_start).days + 1
        random_day = random.randint(0, days_in_range - 1)
        tx_date = actual_start + timedelta(days=random_day)
        
        # Ajouter la transaction
        transactions.append(create_transaction(tx_config, tx_date))
    
    # 3. Compléter avec des transactions aléatoires pour atteindre le minimum
    while len(transactions) < min_count:
        # Choisir une date aléatoire dans la période filtrée
        days_in_range = (actual_end - actual_start).days + 1
        random_day = random.randint(0, days_in_range - 1)
        tx_date = actual_start + timedelta(days=random_day)
        
        # Choisir une catégorie aléatoire
        cat_id = random.choice(list(CATEGORIES_SCHEMA.keys()))
        subcat_id = random.choice(list(CATEGORIES_SCHEMA[cat_id]["subcategories"].keys()))
        
        # Déterminer si c'est un revenu
        is_income = cat_id == "income"
        
        # Générer la transaction
        tx_data = {
            "category": cat_id,
            "subcategory": subcat_id,
            "name": random.choice(MERCHANTS.get(cat_id, ["Inconnu"])),
            "amount": (-200, -50) if is_income else (5, 200)
        }
        
        # Ajouter la transaction
        transactions.append(create_transaction(tx_data, tx_date))
    
    # Tri par date (du plus récent au plus ancien)
    return sorted(transactions, key=lambda x: x["date"], reverse=True)

def get_mock_transactions(days=30, count=None):
    """Génère des transactions de test sur une période donnée"""
    # Calculer la période
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Générer les transactions pour chaque mois
    all_transactions = []
    current = start_date.replace(day=1)
    
    while current <= end_date:
        year, month = current.year, current.month
        monthly_txs = generate_monthly_transactions(year, month, start_date, end_date, 15)
        all_transactions.extend(monthly_txs)
        
        # Passer au mois suivant
        if month == 12:
            current = current.replace(year=year+1, month=1)
        else:
            current = current.replace(month=month+1)
    
    # Ajuster le nombre si nécessaire
    if count is not None:
        if len(all_transactions) < count:
            # Ajouter des transactions supplémentaires pour atteindre le nombre demandé
            for _ in range(count - len(all_transactions)):
                # Choisir une date aléatoire dans la période
                random_date = start_date + timedelta(days=random.randint(0, days))
                
                # Choisir une catégorie aléatoire
                cat_id = random.choice(list(CATEGORIES_SCHEMA.keys()))
                subcat_id = random.choice(list(CATEGORIES_SCHEMA[cat_id]["subcategories"].keys()))
                
                # Générer la transaction
                tx_data = {
                    "category": cat_id,
                    "subcategory": subcat_id,
                    "name": random.choice(MERCHANTS.get(cat_id, ["Inconnu"])),
                    "amount": (-200, -50) if cat_id == "income" else (5, 200)
                }
                
                # Ajouter la transaction
                all_transactions.append(create_transaction(tx_data, random_date))
        elif len(all_transactions) > count:
            # Limiter au nombre demandé
            all_transactions = all_transactions[:count]
    
    # Tri final (du plus récent au plus ancien)
    return sorted(all_transactions, key=lambda x: x["date"], reverse=True)