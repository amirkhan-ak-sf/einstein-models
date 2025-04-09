from typing import Dict, Any, Optional, List
from dataclasses import dataclass

@dataclass
class CategoryScore:
    categoryName: str
    score: float

@dataclass
class ScanToxicity:
    isDetected: bool
    categories: List[CategoryScore]

@dataclass
class ContentQuality:
    scanToxicity: ScanToxicity

@dataclass
class GenerationParameters:
    finish_reason: str
    refusal: Optional[str]
    annotations: List[Any]
    index: int
    logprobs: Optional[Any]

@dataclass
class Generation:
    id: str
    generatedText: str
    contentQuality: ContentQuality
    parameters: GenerationParameters

@dataclass
class TokenDetails:
    reasoning_tokens: int
    audio_tokens: int
    accepted_prediction_tokens: int
    rejected_prediction_tokens: int

@dataclass
class PromptTokenDetails:
    cached_tokens: int
    audio_tokens: int

@dataclass
class Usage:
    completion_tokens: int
    prompt_tokens: int
    completion_tokens_details: TokenDetails
    prompt_tokens_details: PromptTokenDetails
    total_tokens: int

@dataclass
class Parameters:
    provider: str
    created: int
    usage: Usage
    model: str
    system_fingerprint: str
    object: str

@dataclass
class GenerationResponse:
    id: str
    generation: Generation
    moreGenerations: Optional[Any]
    prompt: Optional[str]
    parameters: Parameters 