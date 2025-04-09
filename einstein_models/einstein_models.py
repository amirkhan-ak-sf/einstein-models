import requests
from typing import Dict, Any, Optional, List, Union
from .data.definitions import (
    CategoryScore,
    ScanToxicity,
    ContentQuality,
    GenerationParameters,
    Generation,
    TokenDetails,
    PromptTokenDetails,
    Usage,
    Parameters,
    GenerationResponse
)
from .data.chat_response import ChatGenerationResponse
from .constant.constants import (
    BASE_URL,
    HEADERS
)
from .rest.generate import generate as generate_content
from .rest.authenticate import authenticate as authenticate_user
from .models.models import get_models, is_valid_model
from .rest.chat_generation import chat_generate
from .data.chat_messages import Messages

class ModelsAI:
    """
    Python SDK for Salesforce Einstein Models API.
    
    Provides a wrapper around the Models API for authentication and
    generating content using Salesforce Einstein Models.
    """
    
    def __init__(self):
        self.accessToken = None
        self.tokenType = None
        self.salesforceDomain = None
        self.baseUrl = BASE_URL
    
    def authenticate(self, salesforceDomain: str, clientId: str, clientSecret: str) -> Dict[str, Any]:
        """
        Authenticate against the Salesforce OAuth2 endpoint.
        
        Args:
            salesforceDomain: The Salesforce domain (e.g., 'myorg.my.salesforce.com')
            clientId: The OAuth client ID (consumer key)
            clientSecret: The OAuth client secret (consumer secret)
            
        Returns:
            Dict containing the authentication response
        """
        self.salesforceDomain = salesforceDomain
        
        auth_data = authenticate_user(salesforceDomain, clientId, clientSecret)
        self.accessToken = auth_data.get("access_token")
        self.tokenType = auth_data.get("token_type", "Bearer")
        
        return auth_data
    
    def list_models(self) -> List[Dict[str, str]]:
        """
        Get a list of available models with their details.
        
        Returns:
            List of dictionaries containing model name, ID, and description
        """
        return get_models()
    
    def generate(self, 
                model: str, 
                prompt: str, 
                probability: float = None, 
                locale: str = None,
                **kwargs) -> GenerationResponse:
        """
        Generate content using Salesforce Einstein Models.
        
        Args:
            model: The model name to use for generation
            prompt: The input prompt to generate from
            probability: Optional probability parameter (default is used if not provided)
            locale: Optional locale parameter (e.g., 'en_US', default is used if not provided)
            **kwargs: Additional parameters to pass to the API
            
        Returns:
            GenerationResponse object containing the structured response
            
        Raises:
            Exception: If the model ID is not valid or if not authenticated
        """
        if not self.accessToken:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        if not is_valid_model(model):
            valid_models = "\n".join(f"- {m['name']} ({m['id']})" for m in self.list_models())
            raise Exception(f"Invalid model ID: {model}\n\nAvailable models:\n{valid_models}")
        
        return generate_content(
            access_token=self.accessToken,
            model=model,
            prompt=prompt,
            probability=probability,
            locale=locale,
            **kwargs
        )
    
    def _get_headers(self) -> Dict[str, str]:
        """
        Get the headers for API requests.
        
        Returns:
            Dict containing the request headers
        """
        if not self.accessToken:
            raise Exception("Not authenticated. Call authenticate() first.")
            
        headers = HEADERS.copy()
        headers["Authorization"] = f"Bearer {self.accessToken}"
        return headers
    
    def chat_generate(
        self,
        model: str,
        messages: Messages,
        default_locale: str = "en_US",
        input_locales: Optional[List[Dict[str, Any]]] = None,
        expected_locales: Optional[List[str]] = None,
        tags: Optional[Dict[str, Any]] = None
    ) -> ChatGenerationResponse:
        """
        Generate chat responses using Salesforce Einstein Models.
        
        Args:
            model: The model ID to use for generation
            messages: The Messages object containing the chat history
            default_locale: The default locale for the chat (default: "en_US")
            input_locales: List of input locales with probabilities
            expected_locales: List of expected output locales
            tags: Optional tags for the generation
            
        Returns:
            ChatGenerationResponse object containing the structured response
            
        Raises:
            Exception: If not authenticated or if the request fails
        """
        if not self.accessToken:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        return chat_generate(
            access_token=self.accessToken,
            model=model,
            messages=messages,
            default_locale=default_locale,
            input_locales=input_locales,
            expected_locales=expected_locales,
            tags=tags
        )