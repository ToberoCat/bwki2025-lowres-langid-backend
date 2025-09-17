from app.domain.entities.classification_result import ClassificationResult
from app.repositories.fasttext_expert_repository import FastTextExpertRepository
from app.repositories.writing_system_repository import WritingSystemDetector


class LanguageIdentificationService:
    def __init__(self,
                 writing_system_repository: WritingSystemDetector,
                 fasttext_expert_repository: FastTextExpertRepository
                 ):
        self.writing_system_repository = writing_system_repository
        self.fasttext_expert_repository = fasttext_expert_repository

    def classify(self, text: str) -> ClassificationResult:
        writing_system = self.writing_system_repository.detect(text)

        predictions = self.fasttext_expert_repository.classify(text, writing_system)
        return ClassificationResult(
            predictions=predictions,
            writing_system=writing_system
        )