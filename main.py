"""
FastAPI backend for language identification using FastText model.
This server provides an API endpoint for detecting languages in text.
"""

import os
import logging
from typing import List, Dict, Any
from pathlib import Path

import fasttext
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Language Identification API",
    description="A FastAPI backend for language identification using FastText model",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Pydantic models for request/response
class TextInput(BaseModel):
    text: str = Field(..., description="Text to analyze for language identification", min_length=1, max_length=10000)

class LanguagePrediction(BaseModel):
    language: str = Field(..., description="Predicted language code (ISO 639-1)")
    confidence: float = Field(..., description="Confidence score between 0 and 1")

class PredictionResponse(BaseModel):
    predictions: List[LanguagePrediction] = Field(..., description="List of language predictions sorted by confidence")
    text_length: int = Field(..., description="Length of input text")

# Global model variable
model = None
MODEL_URL = "https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin"
MODEL_PATH = "models/lid.176.bin"

def download_model():
    """Download the FastText language identification model if not present."""
    model_dir = Path("models")
    model_dir.mkdir(exist_ok=True)
    
    if not Path(MODEL_PATH).exists():
        logger.info(f"Downloading FastText model from {MODEL_URL}")
        try:
            response = requests.get(MODEL_URL, stream=True)
            response.raise_for_status()
            
            with open(MODEL_PATH, 'wb') as f:
                for chunk in response.iter_content(chunk_size=8192):
                    if chunk:
                        f.write(chunk)
            logger.info(f"Model downloaded successfully to {MODEL_PATH}")
        except Exception as e:
            logger.error(f"Failed to download model: {e}")
            raise HTTPException(status_code=500, detail=f"Failed to download model: {e}")
    else:
        logger.info(f"Model already exists at {MODEL_PATH}")

def load_model():
    """Load the FastText model."""
    global model
    try:
        if not Path(MODEL_PATH).exists():
            download_model()
        
        logger.info(f"Loading FastText model from {MODEL_PATH}")
        model = fasttext.load_model(MODEL_PATH)
        logger.info("Model loaded successfully")
    except Exception as e:
        logger.error(f"Failed to load model: {e}")
        raise HTTPException(status_code=500, detail=f"Failed to load model: {e}")

@app.on_event("startup")
async def startup_event():
    """Initialize the model on startup."""
    load_model()

@app.get("/")
async def root():
    """Root endpoint with basic information."""
    return {
        "message": "Language Identification API",
        "version": "1.0.0",
        "description": "FastAPI backend for language identification using FastText model",
        "endpoints": {
            "predict": "/predict",
            "health": "/health",
            "docs": "/docs"
        }
    }

@app.get("/health")
async def health_check():
    """Health check endpoint."""
    global model
    return {
        "status": "healthy" if model is not None else "unhealthy",
        "model_loaded": model is not None
    }

@app.post("/predict", response_model=PredictionResponse)
async def predict_language(input_data: TextInput):
    """
    Predict the language of the given text.
    
    Args:
        input_data: TextInput containing the text to analyze
        
    Returns:
        PredictionResponse with language predictions
    """
    global model
    
    if model is None:
        raise HTTPException(status_code=500, detail="Model not loaded")
    
    try:
        # Clean the text (remove newlines and extra spaces)
        text = input_data.text.replace('\n', ' ').strip()
        
        # Predict language using FastText
        predictions, scores = model.predict(text, k=5)  # Get top 5 predictions
        
        # Process predictions
        language_predictions = []
        for pred, score in zip(predictions, scores):
            # FastText returns labels like '__label__en', so we need to extract the language code
            language_code = pred.replace('__label__', '')
            language_predictions.append(
                LanguagePrediction(
                    language=language_code,
                    confidence=float(score)
                )
            )
        
        return PredictionResponse(
            predictions=language_predictions,
            text_length=len(input_data.text)
        )
        
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        raise HTTPException(status_code=500, detail=f"Prediction failed: {e}")

@app.get("/supported-languages")
async def get_supported_languages():
    """Get list of supported languages by the model."""
    # This is a subset of languages supported by the FastText lid.176 model
    # The actual model supports 176 languages
    supported_languages = [
        "af", "als", "am", "an", "ar", "arz", "as", "ast", "av", "az", "azb", "ba", "bar", "bcl",
        "be", "bg", "bh", "bn", "bo", "bpy", "br", "bs", "bxr", "ca", "cbk", "ce", "ceb", "ckb",
        "co", "cs", "cv", "cy", "da", "de", "diq", "dsb", "dty", "dv", "el", "eml", "en", "eo",
        "es", "et", "eu", "fa", "fi", "fr", "frr", "fy", "ga", "gd", "gl", "gn", "gom", "gu",
        "gv", "he", "hi", "hif", "hr", "hsb", "ht", "hu", "hy", "ia", "id", "ie", "ilo", "io",
        "is", "it", "ja", "jbo", "jv", "ka", "kk", "km", "kn", "ko", "krc", "ku", "kv", "kw",
        "ky", "la", "lb", "lez", "li", "lmo", "lo", "lrc", "lt", "lv", "mai", "mg", "mhr", "min",
        "mk", "ml", "mn", "mr", "mrj", "ms", "mt", "mwl", "my", "myv", "mzn", "nah", "nap", "nds",
        "ne", "new", "nl", "nn", "no", "oc", "or", "os", "pa", "pam", "pfl", "pl", "pms", "pnb",
        "ps", "pt", "qu", "rm", "ro", "ru", "rue", "sa", "sah", "sc", "scn", "sco", "sd", "sh",
        "si", "sk", "sl", "so", "sq", "sr", "su", "sv", "sw", "ta", "te", "tg", "th", "tk", "tl",
        "tr", "tt", "tyv", "ug", "uk", "ur", "uz", "vec", "vep", "vi", "vls", "vo", "wa", "war",
        "wuu", "xal", "xmf", "yi", "yo", "yue", "zh"
    ]
    
    return {
        "total_languages": len(supported_languages),
        "languages": supported_languages,
        "note": "This is the FastText lid.176 model supporting 176 languages"
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)