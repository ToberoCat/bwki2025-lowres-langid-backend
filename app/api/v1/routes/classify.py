from fastapi import APIRouter

from app.api.v1.schemas.classification_response import ClassificationResponse, LanguagePredictionResponse
from app.api.v1.schemas.classify_request import ClassifyRequest
from app.core.container import LanguageIdentificationServiceDep
from langcodes import Language

router = APIRouter(tags=["classify"])

def alpha3_to_name(code: str, locale: str = "en") -> str:
    lang = Language.make(language=code.strip().lower())
    display = lang.display_name(locale)
    if "unknown" in display.lower():
        return code
    return display

@router.post("/classify")
def classify_text(
        req: ClassifyRequest,
        svc: LanguageIdentificationServiceDep
) -> ClassificationResponse:
    result = svc.classify(req.text)
    return ClassificationResponse(
        predictions=[
            LanguagePredictionResponse(
                language_id=pred.language,
                language_name=alpha3_to_name(pred.language, req.locale),
                probability=pred.probability
            ) for pred in result.predictions
        ],
        writing_system=result.writing_system if result else "Unknown"
    )