"""
Constants used throughout the Einstein Models SDK.
"""

# Base URL for the Einstein Models API
BASE_URL = "https://api.salesforce.com/einstein/platform/v1"

# Base URLs
OAUTH_TOKEN_URL = "https://{salesforceDomain}/services/oauth2/token"
MODEL_GENERATIONS_URL = f"{BASE_URL}/models/{{model}}/generations"

# Chat Generation URL
CHAT_GENERATION_URL = f"{BASE_URL}/models/{{model}}/chat-generations"

# OAuth Constants
GRANT_TYPE = "client_credentials"
CONTENT_TYPE_FORM = "application/x-www-form-urlencoded"
CONTENT_TYPE_JSON = "application/json"

# Default Values
DEFAULT_LOCALE = "en_US"

# Default headers for API requests
HEADERS = {
    "Content-Type": "application/json",
    "Accept": "application/json",
}

# Request headers for operations
EINSTEIN_HEADERS = {
    "x-client-feature-id": "ai-platform-models-connected-app",
    "x-sfdc-app-context":"EinsteinGPT",
}

# Payload Templates
LOCALIZATION_TEMPLATE = {
    "defaultLocale": DEFAULT_LOCALE,
    "expectedLocales": [DEFAULT_LOCALE],
    "inputLocales": []
}

PAYLOAD_TEMPLATE = {
    "localization": LOCALIZATION_TEMPLATE,
    "prompt": "",
    "tags": {}
} 