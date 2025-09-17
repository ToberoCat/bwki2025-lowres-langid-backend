from dataclasses import dataclass


@dataclass
class LanguagePrediction:
    language: str
    probability: float


@dataclass
class ClassificationResult:
    predictions: list[LanguagePrediction]
    writing_system: str
