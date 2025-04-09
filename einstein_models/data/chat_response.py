from dataclasses import dataclass
from typing import List, Optional, Dict, Any
from .definitions import ContentQuality, ScanToxicity, CategoryScore

@dataclass
class ChatGenerationParameters:
    """Parameters for a single chat generation."""
    finish_reason: Optional[str]
    refusal: Optional[str]
    annotations: List[Any]
    index: int
    logprobs: Optional[Any]

@dataclass
class Generation:
    """Single generation from the chat response."""
    id: str
    role: str
    content: str
    timestamp: int
    parameters: ChatGenerationParameters
    contentQuality: ContentQuality

@dataclass
class UsageDetails:
    """Detailed usage statistics."""
    reasoning_tokens: int
    audio_tokens: int
    accepted_prediction_tokens: int
    rejected_prediction_tokens: int

@dataclass
class PromptUsageDetails:
    """Detailed prompt usage statistics."""
    cached_tokens: int
    audio_tokens: int

@dataclass
class Usage:
    """Usage statistics for the chat generation."""
    completion_tokens: int
    prompt_tokens: int
    completion_tokens_details: UsageDetails
    prompt_tokens_details: PromptUsageDetails
    total_tokens: int

@dataclass
class GenerationParameters:
    """Parameters for the chat generation."""
    provider: str
    created: int
    usage: Usage
    model: str
    system_fingerprint: str
    object: str

@dataclass
class GenerationDetails:
    """Details of the chat generation."""
    generations: List[Generation]
    parameters: GenerationParameters

@dataclass
class ChatGenerationResponse:
    """Complete chat generation response."""
    id: str
    generationDetails: GenerationDetails 