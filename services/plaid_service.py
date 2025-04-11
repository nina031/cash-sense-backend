from datetime import datetime, timedelta
from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from plaid.model.transactions_get_request import TransactionsGetRequest
from utils.plaid_helpers import get_plaid_client, format_transaction

def create_link_token():
    """
    Crée un token de liaison Plaid pour initialiser Plaid Link
    """
    client = get_plaid_client()
    
    request = LinkTokenCreateRequest(
        products=[Products('auth'), Products('transactions')],
        client_name="CashSense",
        country_codes=[CountryCode('US')],
        language='fr',
        user={'client_user_id': 'user_12345'}  # En production, utilisez un ID utilisateur réel
    )
    
    response = client.link_token_create(request)
    return response['link_token']

def exchange_public_token(public_token):
    """
    Échange un token public contre un token d'accès permanent
    """
    client = get_plaid_client()
    
    exchange_request = ItemPublicTokenExchangeRequest(
        public_token=public_token
    )
    exchange_response = client.item_public_token_exchange(exchange_request)
    
    # Dans une application réelle, stockez cet access_token en sécurité
    access_token = exchange_response.access_token
    item_id = exchange_response.item_id
    
    return {
        "access_token": access_token,
        "item_id": item_id
    }

def get_user_transactions(access_token, days=30):
    """
    Récupère les transactions des X derniers jours
    """
    client = get_plaid_client()
    
    # Calculer les dates de début et de fin
    end_date = datetime.now().date()
    start_date = end_date - timedelta(days=days)
    
    # Récupérer les transactions
    request = TransactionsGetRequest(
        access_token=access_token,
        start_date=start_date,
        end_date=end_date
    )
    
    response = client.transactions_get(request)
    transactions = response['transactions']
    
    # Formater les transactions pour le frontend
    return [format_transaction(transaction) for transaction in transactions]