from dataclasses import dataclass
from typing import Optional


@dataclass
class LanguagePredictionResponse:
    language_id: str
    language_name: Optional[str]
    probability: float


@dataclass
class ClassificationResponse:
    predictions: list[LanguagePredictionResponse]
    writing_system: str
