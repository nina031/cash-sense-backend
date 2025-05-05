from plaid.model.link_token_create_request import LinkTokenCreateRequest
from plaid.model.products import Products
from plaid.model.country_code import CountryCode
from plaid.model.item_public_token_exchange_request import ItemPublicTokenExchangeRequest
from utils.plaid_helpers import get_plaid_client

def create_link_token(user_id):
    """
    Crée un token de liaison Plaid pour initialiser Plaid Link
    
    Args:
        user_id (str): Identifiant de l'utilisateur
        
    Returns:
        str: Token de liaison
        
    Raises:
        ValueError: Si l'ID utilisateur n'est pas fourni
    """
    if not user_id:
        raise ValueError("L'ID utilisateur est requis")
        
    client = get_plaid_client()
    
    request = LinkTokenCreateRequest(
        products=[Products('auth'), Products('transactions')],
        client_name="CashSense",
        country_codes=[CountryCode('US')],
        language='fr',
        user={'client_user_id': user_id}
    )
    
    response = client.link_token_create(request)
    print(f"Token de liaison créé pour l'utilisateur {user_id}")
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