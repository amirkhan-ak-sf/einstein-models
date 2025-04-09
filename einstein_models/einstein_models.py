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
    HEADERS,
    OAUTH_TOKEN_URL,
    MODEL_GENERATIONS_URL,
    CHAT_GENERATION_URL,
    GRANT_TYPE,
    CONTENT_TYPE_FORM,
    CONTENT_TYPE_JSON,
    PAYLOAD_TEMPLATE
)
from .models.models import get_models, is_valid_model
from .models.embedding_models import get_embed_models, is_valid_embed_model, EmbeddingModel
from .rest.chat_generation import chat_generate
from .data.chat_messages import Messages
from dotenv import load_dotenv
from .rest.authenticate import authenticate as authenticate_user
from .rest.generate import generate as generate_content
from .rest.generate_embedding import EmbeddingGenerator

__all__ = ['ModelsAI', 'Messages']

class Messages:
    def __init__(self):
        self.messages = []

    def add_message(self, role, content):
        self.messages.append({"role": role, "content": content})

    def get_messages(self):
        return self.messages

class ModelsAI:
    """
    Python SDK for Salesforce Einstein Models API.
    
    Provides a wrapper around the Models API for authentication and
    generating content using Salesforce Einstein Models.
    """
    
    def __init__(self):
        self._access_token = None
        self._token_type = None
        self._salesforce_domain = None
        self._base_url = BASE_URL
        load_dotenv()
    
    def authenticate(self, salesforce_domain, client_id, client_secret):
        self._salesforce_domain = salesforce_domain
        auth_data = authenticate_user(salesforce_domain, client_id, client_secret)
        self._access_token = auth_data.get("access_token")
        self._token_type = auth_data.get("token_type", "Bearer")
        return auth_data
    
    def generate(self, model, prompt, probability=None, locale=None, **kwargs):
        if not self._access_token:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        if not is_valid_model(model):
            valid_models = "\n".join(f"- {m.name} ({m.value})" for m in self.list_models())
            raise Exception(f"Invalid model ID: {model}\n\nAvailable models:\n{valid_models}")
        
        return generate_content(
            access_token=self._access_token,
            model=model,
            prompt=prompt,
            probability=probability,
            locale=locale,
            **kwargs
        )
    
    def chat_generate(self, model, messages, default_locale="en_US", input_locales=None, expected_locales=None, tags=None):
        if not self._access_token:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        return chat_generate(
            access_token=self._access_token,
            model=model,
            messages=messages,
            default_locale=default_locale,
            input_locales=input_locales,
            expected_locales=expected_locales,
            tags=tags
        )

    def generate_embedding(self, model, input_texts):
        if not self._access_token:
            raise Exception("Not authenticated. Call authenticate() first.")
        
        if not is_valid_embed_model(model):
            valid_models = "\n".join(f"- {m.name} ({m.value})" for m in self.list_embed_models())
            raise Exception(f"Invalid model ID: {model}\n\nAvailable models:\n{valid_models}")

        generator = EmbeddingGenerator(access_token=self._access_token)
        # Convert string model to enum if needed
        if isinstance(model, str):
            model = EmbeddingModel(model)
        return generator.generate_embedding(model=model, input_texts=input_texts)

    def list_models(self):
        return get_models()
    
    def list_embed_models(self):
        return get_embed_models()