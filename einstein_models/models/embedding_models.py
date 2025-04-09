from enum import Enum
from typing import Dict, List, Tuple, Type

class EmbeddingModel(Enum):
    OPENAI_ADA_002 = "sfdc_ai__DefaultOpenAITextEmbeddingAda_002"
    AZURE_OPENAI_ADA_002 = "sfdc_ai__DefaultAzureOpenAITextEmbeddingAda_002"

    @classmethod
    def get_model_name(cls, model: 'EmbeddingModel') -> str:
        return model.value 


# List of available models with their names, IDs, and descriptions
MODELS: List[Tuple[str, str, str]] = [
    ("OPENAI_ADA_002", EmbeddingModel.OPENAI_ADA_002.value, ""),
    ("AZURE_OPENAI_ADA_002", EmbeddingModel.AZURE_OPENAI_ADA_002.value, ""),
]

def get_embed_models() -> List[Dict[str, str]]:
    """
    Get a list of available embedding models with their details.
    
    Returns:
        List of dictionaries containing model name, ID, and description
    """
    return [
        {
            "name": name,
            "id": model_id,
            "description": description
        }
        for name, model_id, description in MODELS
    ]

def get_model_ids() -> List[str]:
    """
    Get a list of available model IDs.
    
    Returns:
        List of model IDs
    """
    return [model_id for _, model_id, _ in MODELS]

def is_valid_embed_model(model_id: str) -> bool:
    """
    Check if a model ID is valid.
    
    Args:
        model_id: The model ID to check
        
    Returns:
        True if the model ID is valid, False otherwise
    """
    return model_id in get_model_ids()

def get_embed_models() -> Type[EmbeddingModel]:
    """
    Get the Model enum class.
    
    Returns:
        The Model enum class
    """
    return EmbeddingModel 