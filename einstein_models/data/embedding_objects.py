from dataclasses import dataclass
from typing import List, Optional

@dataclass
class EmbeddingUsage:
    prompt_tokens: int
    total_tokens: int

@dataclass
class EmbeddingParameters:
    usage: EmbeddingUsage
    model: str
    object: str

@dataclass
class Embedding:
    embedding: List[float]
    index: int

@dataclass
class EmbeddingResponse:
    embeddings: List[Embedding]
    parameters: EmbeddingParameters 