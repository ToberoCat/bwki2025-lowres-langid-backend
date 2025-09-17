import os
from dataclasses import dataclass, field

import fasttext

from app.core.errors import NoExpertFoundError
from app.domain.entities.classification_result import LanguagePrediction


@dataclass(frozen=True, slots=True)
class FastTextExpertRepositoryConfig:
    model_path: str = "models"
    expert_model_patterns: tuple[str, ...] = (
        "{}/{}/langclf_quant.ftz",
        "{}/{}/langclf.bin",
    )  # (model_path, writing_system)
    labels_prefix: str = "__label__"
    max_predictions: int = 10


class FastTextExpertRepository:
    def __init__(self, config: FastTextExpertRepositoryConfig):
        self.cfg = config

        if not os.path.exists(self.cfg.model_path):
            raise RuntimeError(f"Model path does not exist: {self.cfg.model_path}")

    def _preprocess_text(self, text: str) -> str:
        return (text
                .replace("\n", " ")
                .replace("\r", " ")
                .strip()
                .lower())

    def classify(self, text: str, writing_system: str) -> list[LanguagePrediction]:
        for pattern in self.cfg.expert_model_patterns:
            expert_model_file = pattern.format(self.cfg.model_path, writing_system)
            if os.path.exists(expert_model_file):
                break
        else:
            raise NoExpertFoundError(f"No expert model found for writing system: {writing_system}")

        if not os.path.exists(expert_model_file):
            raise NoExpertFoundError(f"No expert model found for writing system: {writing_system}")

        text = self._preprocess_text(text)
        model = fasttext.load_model(expert_model_file)
        labels, probabilities = model.predict(text, k=self.cfg.max_predictions)
        predictions = [
            LanguagePrediction(language=lbl.replace(self.cfg.labels_prefix, ""), probability=prob)
            for lbl, prob in zip(labels, probabilities)
        ]
        return predictions
