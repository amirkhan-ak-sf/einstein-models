import requests
from typing import Dict, Any, Optional
from ..data.definitions import (
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
from ..constant.constants import (
    MODEL_GENERATIONS_URL,
    DEFAULT_LOCALE,
    HEADERS,
    LOCALIZATION_TEMPLATE,
    PAYLOAD_TEMPLATE
)

def _parse_response(response_data: Dict[str, Any]) -> GenerationResponse:
    """Parse the raw JSON response into structured objects."""
    # Parse content quality
    scan_toxicity = ScanToxicity(
        isDetected=response_data.get("generation", {}).get("contentQuality", {}).get("scanToxicity", {}).get("isDetected", False),
        categories=[
            CategoryScore(
                categoryName=cat.get("categoryName", ""),
                score=cat.get("score", 0.0)
            )
            for cat in response_data.get("generation", {}).get("contentQuality", {}).get("scanToxicity", {}).get("categories", [])
        ]
    )
    
    content_quality = ContentQuality(scanToxicity=scan_toxicity)
    
    # Parse generation parameters
    gen_params = GenerationParameters(
        finish_reason=response_data.get("generation", {}).get("parameters", {}).get("finish_reason", ""),
        refusal=response_data.get("generation", {}).get("parameters", {}).get("refusal"),
        annotations=response_data.get("generation", {}).get("parameters", {}).get("annotations", []),
        index=response_data.get("generation", {}).get("parameters", {}).get("index", 0),
        logprobs=response_data.get("generation", {}).get("parameters", {}).get("logprobs")
    )
    
    # Parse generation
    generation = Generation(
        id=response_data.get("generation", {}).get("id", ""),
        generatedText=response_data.get("generation", {}).get("generatedText", ""),
        contentQuality=content_quality,
        parameters=gen_params
    )
    
    # Parse usage details
    completion_details = TokenDetails(
        reasoning_tokens=response_data.get("parameters", {}).get("usage", {}).get("completion_tokens_details", {}).get("reasoning_tokens", 0),
        audio_tokens=response_data.get("parameters", {}).get("usage", {}).get("completion_tokens_details", {}).get("audio_tokens", 0),
        accepted_prediction_tokens=response_data.get("parameters", {}).get("usage", {}).get("completion_tokens_details", {}).get("accepted_prediction_tokens", 0),
        rejected_prediction_tokens=response_data.get("parameters", {}).get("usage", {}).get("completion_tokens_details", {}).get("rejected_prediction_tokens", 0)
    )
    
    prompt_details = PromptTokenDetails(
        cached_tokens=response_data.get("parameters", {}).get("usage", {}).get("prompt_tokens_details", {}).get("cached_tokens", 0),
        audio_tokens=response_data.get("parameters", {}).get("usage", {}).get("prompt_tokens_details", {}).get("audio_tokens", 0)
    )
    
    usage = Usage(
        completion_tokens=response_data.get("parameters", {}).get("usage", {}).get("completion_tokens", 0),
        prompt_tokens=response_data.get("parameters", {}).get("usage", {}).get("prompt_tokens", 0),
        completion_tokens_details=completion_details,
        prompt_tokens_details=prompt_details,
        total_tokens=response_data.get("parameters", {}).get("usage", {}).get("total_tokens", 0)
    )
    
    # Parse parameters
    parameters = Parameters(
        provider=response_data.get("parameters", {}).get("provider", ""),
        created=response_data.get("parameters", {}).get("created", 0),
        usage=usage,
        model=response_data.get("parameters", {}).get("model", ""),
        system_fingerprint=response_data.get("parameters", {}).get("system_fingerprint", ""),
        object=response_data.get("parameters", {}).get("object", "")
    )
    
    # Create final response object
    return GenerationResponse(
        id=response_data.get("id", ""),
        generation=generation,
        moreGenerations=response_data.get("moreGenerations"),
        prompt=response_data.get("prompt"),
        parameters=parameters
    )

def generate(access_token: str,
            model: str, 
            prompt: str, 
            probability: float = None, 
            locale: str = None,
            **kwargs) -> GenerationResponse:
    """
    Generate content using Salesforce Einstein Models.
    
    Args:
        access_token: The OAuth access token
        model: The model name to use for generation
        prompt: The input prompt to generate from
        probability: Optional probability parameter (default is used if not provided)
        locale: Optional locale parameter (e.g., 'en_US', default is used if not provided)
        **kwargs: Additional parameters to pass to the API
        
    Returns:
        GenerationResponse object containing the structured response
    """
    if not access_token:
        raise Exception("Access token is required")
    
    url = MODEL_GENERATIONS_URL.format(model=model)
    
    headers = HEADERS.copy()
    headers["Authorization"] = f"Bearer {access_token}"
    
    # Default locale if not provided
    locale = locale or DEFAULT_LOCALE
    
    # Create payload from template
    payload = PAYLOAD_TEMPLATE.copy()
    payload["prompt"] = prompt
    
    # Update localization
    payload["localization"] = LOCALIZATION_TEMPLATE.copy()
    payload["localization"]["defaultLocale"] = locale
    payload["localization"]["expectedLocales"] = [locale]
    
    # Add probability if provided
    if probability is not None:
        payload["localization"]["inputLocales"] = [
            {"probability": probability, "locale": locale}
        ]
    
    # Add any additional parameters
    for key, value in kwargs.items():
        if key not in payload:
            payload[key] = value
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        response_data = response.json()
        return _parse_response(response_data)
    except requests.exceptions.RequestException as e:
        raise Exception(f"Generation request failed: {str(e)}") 