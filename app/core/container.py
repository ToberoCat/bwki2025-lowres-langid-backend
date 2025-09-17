from functools import lru_cache
from typing import Annotated

from fastapi import Depends

from app.repositories.fasttext_expert_repository import FastTextExpertRepositoryConfig, FastTextExpertRepository
from app.repositories.writing_system_repository import WritingSystemDetector, WritingSystemDetectorConfig
from app.services.language_identification_service import LanguageIdentificationService


class Container:
    @staticmethod
    @lru_cache()
    def get_writing_system_detector_config() -> WritingSystemDetectorConfig:
        return WritingSystemDetectorConfig()

    @staticmethod
    @lru_cache()
    def get_fasttext_expert_repository_config():
        return FastTextExpertRepositoryConfig()

    @staticmethod
    @lru_cache()
    def get_writing_system_detector(
            config: Annotated[WritingSystemDetectorConfig, Depends(get_writing_system_detector_config)]
    ) -> WritingSystemDetector:
        return WritingSystemDetector(config)

    @staticmethod
    @lru_cache()
    def get_fasttext_expert_repository(
            config: Annotated[FastTextExpertRepositoryConfig, Depends(get_fasttext_expert_repository_config)]
    ) -> FastTextExpertRepository:
        return FastTextExpertRepository(config)

    @staticmethod
    def get_language_identification_service(
            writing_system_detector: Annotated[WritingSystemDetector, Depends(get_writing_system_detector)],
            fasttext_expert_repository: Annotated[FastTextExpertRepository, Depends(get_fasttext_expert_repository)]
    ) -> LanguageIdentificationService:
        return LanguageIdentificationService(writing_system_detector, fasttext_expert_repository)


WritingSystemDetectorDep = Annotated[WritingSystemDetector, Depends(Container.get_writing_system_detector)]
FastTextExpertRepositoryDep = Annotated[
    FastTextExpertRepository, Depends(Container.get_fasttext_expert_repository)]
LanguageIdentificationServiceDep = Annotated[
    LanguageIdentificationService, Depends(Container.get_language_identification_service)]
