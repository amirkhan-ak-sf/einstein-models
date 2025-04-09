import json
from typing import List, Dict, Any
import requests
from einstein_models.constant.constants import EINSTEIN_HEADERS, HEADERS
from einstein_models.models.embedding_models import EmbeddingModel
from einstein_models.data.embedding_objects import EmbeddingResponse, Embedding, EmbeddingParameters, EmbeddingUsage

class EmbeddingGenerator:
    def __init__(self, access_token: str, base_url: str = "https://api.salesforce.com/einstein/platform/v1"):
        self.access_token = access_token
        self.base_url = base_url

    def generate_embedding(self, model: EmbeddingModel, input_texts: List[str]) -> EmbeddingResponse:
        """
        Generate embeddings for the given input texts using the specified model.
        
        Args:
            model: The embedding model to use
            input_texts: List of text strings to generate embeddings for
            
        Returns:
            EmbeddingResponse object containing the embeddings and metadata
        """
        url = f"{self.base_url}/models/{model.value}/embeddings"
        
        headers = {
            "Authorization": f"Bearer {self.access_token}",
            "Content-Type": "application/json",
            **HEADERS,
            **EINSTEIN_HEADERS
        }
        
        payload = {
            "input": input_texts
        }
        
        response = requests.post(url, headers=headers, json=payload)
        response.raise_for_status()
        
        response_data = response.json()
        
        # Convert response to EmbeddingResponse object
        embeddings = [
            Embedding(
                embedding=item["embedding"],
                index=item["index"]
            ) for item in response_data["embeddings"]
        ]
        
        parameters = EmbeddingParameters(
            usage=EmbeddingUsage(
                prompt_tokens=response_data["parameters"]["usage"]["prompt_tokens"],
                total_tokens=response_data["parameters"]["usage"]["total_tokens"]
            ),
            model=response_data["parameters"]["model"],
            object=response_data["parameters"]["object"]
        )
        
        return EmbeddingResponse(
            embeddings=embeddings,
            parameters=parameters
        ) 