from typing import Dict, List, Tuple, Type
from enum import Enum

class Model(Enum):
    """Enum class for available models."""
    ANTHROPIC_CLAUDE_3_HAIKU = "sfdc_ai__DefaultBedrockAnthropicClaude3Haiku"
    AZURE_GPT_35_TURBO = "sfdc_ai__DefaultAzureOpenAIGPT35Turbo"
    AZURE_GPT_35_TURBO_16K = "sfdc_ai__DefaultAzureOpenAIGPT35Turbo_16k"
    OPENAI_GPT_35_TURBO = "sfdc_ai__DefaultOpenAIGPT35Turbo"
    OPENAI_GPT_35_TURBO_16K = "sfdc_ai__DefaultOpenAIGPT35Turbo_16k"
    OPENAI_GPT_4 = "sfdc_ai__DefaultOpenAIGPT4"
    OPENAI_GPT_4_32K = "sfdc_ai__DefaultOpenAIGPT4_32k"
    OPENAI_GPT_4_OMNI = "sfdc_ai__DefaultGPT4Omni"
    OPENAI_GPT_4_OMNI_MINI = "sfdc_ai__DefaultOpenAIGPT4OmniMini"
    OPENAI_GPT_4_TURBO = "sfdc_ai__DefaultOpenAIGPT4Turbo"

# List of available models with their names, IDs, and descriptions
MODELS: List[Tuple[str, str, str]] = [
    ("Anthropic Claude 3 Haiku on Amazon", Model.ANTHROPIC_CLAUDE_3_HAIKU.value, ""),
    ("Azure OpenAI GPT 3.5 Turbo", Model.AZURE_GPT_35_TURBO.value, ""),
    ("Azure OpenAI GPT 3.5 Turbo 16k", Model.AZURE_GPT_35_TURBO_16K.value, ""),
    ("OpenAI GPT 3.5 Turbo", Model.OPENAI_GPT_35_TURBO.value, ""),
    ("OpenAI GPT 3.5 Turbo 16k", Model.OPENAI_GPT_35_TURBO_16K.value, ""),
    ("OpenAI GPT 4", Model.OPENAI_GPT_4.value, ""),
    ("OpenAI GPT 4 32k", Model.OPENAI_GPT_4_32K.value, ""),
    ("OpenAI GPT 4 Omni (GPT-4o)", Model.OPENAI_GPT_4_OMNI.value, "Latest GPT-4 model"),
    ("OpenAI GPT 4 Omni Mini (GPT-4o mini)", Model.OPENAI_GPT_4_OMNI_MINI.value, ""),
    ("OpenAI GPT 4 Turbo", Model.OPENAI_GPT_4_TURBO.value, "")
]

def get_models() -> List[Dict[str, str]]:
    """
    Get a list of available models with their details.
    
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

def is_valid_model(model_id: str) -> bool:
    """
    Check if a model ID is valid.
    
    Args:
        model_id: The model ID to check
        
    Returns:
        True if the model ID is valid, False otherwise
    """
    return model_id in get_model_ids()

def get_models() -> Type[Model]:
    """
    Get the Model enum class.
    
    Returns:
        The Model enum class
    """
    return Model 