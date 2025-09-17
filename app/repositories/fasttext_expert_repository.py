import os
from dataclasses import dataclass

import fasttext

from app.core.errors import NoExpertFoundError
from app.domain.entities.classification_result import LanguagePrediction


@dataclass(frozen=True)
class FastTextExpertRepositoryConfig:
    model_path: str = "models/fasttext_experts"
    expert_model_path: str = "{}/{}/langclf.bin"  # model_path, writing_system
    labels_prefix: str = "__label__"
    max_predictions: int = 10


class FastTextExpertRepository:
    def __init__(self, config: FastTextExpertRepositoryConfig):
        self.cfg = config

        if not os.path.exists(self.cfg.model_path):
            raise RuntimeError(f"Model path does not exist: {self.cfg.model_path}")

    def classify(self, text: str, writing_system: str) -> list[LanguagePrediction]:
        expert_model_file = self.cfg.expert_model_path.format(self.cfg.model_path, writing_system)
        if os.path.exists(expert_model_file):
            raise NoExpertFoundError("FastText model loading and prediction not implemented.")

        model = fasttext.load_model(expert_model_file)
        labels, probabilities = model.predict(text, k=self.cfg.max_predictions)
        predictions = [
            LanguagePrediction(language=lbl.replace(self.cfg.labels_prefix, ""), probability=prob)
            for lbl, prob in zip(labels, probabilities)
        ]
        return predictions
