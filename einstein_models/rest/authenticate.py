import requests
from typing import Dict, Any
from ..constant.constants import (
    OAUTH_TOKEN_URL,
    GRANT_TYPE,
    CONTENT_TYPE_FORM
)

def authenticate(salesforceDomain: str, clientId: str, clientSecret: str) -> Dict[str, Any]:
    """
    Authenticate against the Salesforce OAuth2 endpoint.
    
    Args:
        salesforceDomain: The Salesforce domain (e.g., 'myorg.my.salesforce.com')
        clientId: The OAuth client ID (consumer key)
        clientSecret: The OAuth client secret (consumer secret)
        
    Returns:
        Dict containing the authentication response with access_token and token_type
    """
    url = OAUTH_TOKEN_URL.format(salesforceDomain=salesforceDomain)
    
    payload = {
        "grant_type": GRANT_TYPE,
        "client_id": clientId,
        "client_secret": clientSecret
    }
    
    headers = {
        "Content-Type": CONTENT_TYPE_FORM
    }
    
    try:
        response = requests.post(url, data=payload, headers=headers)
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        raise Exception(f"Authentication failed: {str(e)}") 