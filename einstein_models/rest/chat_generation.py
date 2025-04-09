import requests
from typing import Dict, Any, Optional, List
from ..constant.constants import CHAT_GENERATION_URL, HEADERS, EINSTEIN_HEADERS
from ..data.chat_messages import Messages
from ..data.definitions import ContentQuality, ScanToxicity, CategoryScore
from ..data.chat_response import (
    ChatGenerationResponse,
    GenerationDetails,
    Generation,
    ChatGenerationParameters,
    GenerationParameters,
    Usage,
    UsageDetails,
    PromptUsageDetails
)

def chat_generate(
    access_token: str,
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
        access_token: The access token for authentication
        model: The model ID to use for generation
        messages: The Messages object containing the chat history
        default_locale: The default locale for the chat (default: "en_US")
        input_locales: List of input locales with probabilities
        expected_locales: List of expected output locales
        tags: Optional tags for the generation
        
    Returns:
        ChatGenerationResponse object containing the structured response
    """
    if not access_token:
        raise Exception("Access token is required")
    
    if not model:
        raise Exception("Model ID is required")
    
    if not messages or not messages.messages:
        raise Exception("At least one message is required")
    
    # Prepare the request payload
    payload = {
        "messages": messages.to_dict(),
        "localization": {
            "defaultLocale": default_locale,
            "inputLocales": input_locales or [{"locale": default_locale, "probability": 0.8}],
            "expectedLocales": expected_locales or [default_locale]
        },
        "tags": tags or {}
    }
    
    # Prepare headers
    headers = HEADERS.copy()
    headers = EINSTEIN_HEADERS
    headers["Authorization"] = f"Bearer {access_token}"
    
    # Make the API request
    url = CHAT_GENERATION_URL.format(model=model)
    response = requests.post(url, json=payload, headers=headers)
    
    if response.status_code != 200:
        raise Exception(f"Chat generation failed: {response.text}")
    
    # Parse and return the response
    response_data = response.json()
    
    # Create nested objects for the response
    generations = []
    for gen in response_data["generationDetails"]["generations"]:
        # Create ContentQuality object
        content_quality = ContentQuality(
            scanToxicity=ScanToxicity(
                isDetected=gen["contentQuality"]["scanToxicity"]["isDetected"],
                categories=[
                    CategoryScore(
                        categoryName=cat["categoryName"],
                        score=cat["score"]
                    )
                    for cat in gen["contentQuality"]["scanToxicity"]["categories"]
                ]
            )
        )
        
        # Create ChatGenerationParameters object
        gen_params = ChatGenerationParameters(
            finish_reason=gen["parameters"].get("finish_reason"),
            refusal=gen["parameters"].get("refusal"),
            annotations=gen["parameters"].get("annotations", []),
            index=gen["parameters"].get("index", 0),
            logprobs=gen["parameters"].get("logprobs")
        )
        
        # Create Generation object
        generation = Generation(
            id=gen["id"],
            role=gen["role"],
            content=gen["content"],
            timestamp=gen["timestamp"],
            parameters=gen_params,
            contentQuality=content_quality
        )
        generations.append(generation)
    
    # Create UsageDetails objects
    comp_details = UsageDetails(
        reasoning_tokens=response_data["generationDetails"]["parameters"]["usage"]["completion_tokens_details"].get("reasoning_tokens", 0),
        audio_tokens=response_data["generationDetails"]["parameters"]["usage"]["completion_tokens_details"].get("audio_tokens", 0),
        accepted_prediction_tokens=response_data["generationDetails"]["parameters"]["usage"]["completion_tokens_details"].get("accepted_prediction_tokens", 0),
        rejected_prediction_tokens=response_data["generationDetails"]["parameters"]["usage"]["completion_tokens_details"].get("rejected_prediction_tokens", 0)
    )
    
    prompt_details = PromptUsageDetails(
        cached_tokens=response_data["generationDetails"]["parameters"]["usage"]["prompt_tokens_details"].get("cached_tokens", 0),
        audio_tokens=response_data["generationDetails"]["parameters"]["usage"]["prompt_tokens_details"].get("audio_tokens", 0)
    )
    
    # Create Usage object
    usage = Usage(
        completion_tokens=response_data["generationDetails"]["parameters"]["usage"]["completion_tokens"],
        prompt_tokens=response_data["generationDetails"]["parameters"]["usage"]["prompt_tokens"],
        completion_tokens_details=comp_details,
        prompt_tokens_details=prompt_details,
        total_tokens=response_data["generationDetails"]["parameters"]["usage"]["total_tokens"]
    )
    
    # Create GenerationParameters object
    params = GenerationParameters(
        provider=response_data["generationDetails"]["parameters"]["provider"],
        created=response_data["generationDetails"]["parameters"]["created"],
        usage=usage,
        model=response_data["generationDetails"]["parameters"]["model"],
        system_fingerprint=response_data["generationDetails"]["parameters"]["system_fingerprint"],
        object=response_data["generationDetails"]["parameters"]["object"]
    )
    
    # Create GenerationDetails object
    gen_details = GenerationDetails(
        generations=generations,
        parameters=params
    )
    
    # Create and return the final response object
    return ChatGenerationResponse(
        id=response_data["id"],
        generationDetails=gen_details
    ) 