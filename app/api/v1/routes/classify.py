from fastapi import APIRouter

from app.api.v1.schemas.classify_request import ClassifyRequest
from app.core.container import LanguageIdentificationServiceDep

router = APIRouter(tags=["classify"])


@router.post("/classify")
def classify_text(
        req: ClassifyRequest,
        svc: LanguageIdentificationServiceDep
):
    result = svc.classify(req.text)
    return result