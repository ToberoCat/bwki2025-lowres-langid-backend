from pydantic import BaseModel


class ClassifyRequest(BaseModel):
    text: str
    locale: str = "en"