import plaid
from plaid.api import plaid_api
from plaid.configuration import Configuration
from flask import current_app

def get_plaid_client():
    """
    Configure et retourne un client Plaid
    """
    configuration = Configuration(
        host=current_app.config.get('PLAID_ENV'),
        api_key={
            'clientId': current_app.config.get('PLAID_CLIENT_ID'),
            'secret': current_app.config.get('PLAID_SECRET'),
        }
    )
    api_client = plaid.ApiClient(configuration)
    return plaid_api.PlaidApi(api_client)