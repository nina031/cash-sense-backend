import plaid
from plaid.api import plaid_api
from plaid.configuration import Configuration
from config import PLAID_CLIENT_ID, PLAID_SECRET, PLAID_ENV  # Importer de config.py

def get_plaid_client():
    """
    Configure et retourne un client Plaid
    """
    configuration = Configuration(
        host=PLAID_ENV,
        api_key={
            'clientId': PLAID_CLIENT_ID,
            'secret': PLAID_SECRET,
        }
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)

def format_transaction(transaction):
    """
    Formate une transaction Plaid pour le frontend
    """
    return {
        "id": transaction.transaction_id,
        "date": transaction.date,
        "name": transaction.name,
        "amount": transaction.amount,
        "category": ', '.join(transaction.category) if transaction.category else "Non catégorisé",
        "payment_channel": transaction.payment_channel,
        "pending": transaction.pending,
        "merchant_name": transaction.merchant_name
    }