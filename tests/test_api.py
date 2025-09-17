"""
Test cases for the Language Identification API.
"""

import pytest
from fastapi.testclient import TestClient
from unittest.mock import patch, MagicMock
import sys
import os

# Add the parent directory to the path so we can import main
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from main import app

client = TestClient(app)

class TestAPI:
    """Test cases for the API endpoints."""

    def test_root_endpoint(self):
        """Test the root endpoint."""
        response = client.get("/")
        assert response.status_code == 200
        data = response.json()
        assert "message" in data
        assert "version" in data
        assert data["version"] == "1.0.0"

    def test_health_endpoint_without_model(self):
        """Test health endpoint when model is not loaded."""
        with patch('main.model', None):
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "unhealthy"
            assert data["model_loaded"] is False

    def test_health_endpoint_with_model(self):
        """Test health endpoint when model is loaded."""
        mock_model = MagicMock()
        with patch('main.model', mock_model):
            response = client.get("/health")
            assert response.status_code == 200
            data = response.json()
            assert data["status"] == "healthy"
            assert data["model_loaded"] is True

    def test_supported_languages_endpoint(self):
        """Test the supported languages endpoint."""
        response = client.get("/supported-languages")
        assert response.status_code == 200
        data = response.json()
        assert "total_languages" in data
        assert "languages" in data
        assert isinstance(data["languages"], list)
        assert len(data["languages"]) > 0

    @patch('main.model')
    def test_predict_endpoint_success(self, mock_model):
        """Test successful prediction."""
        # Mock the model prediction
        mock_model.predict.return_value = (['__label__en', '__label__de'], [0.95, 0.05])
        
        response = client.post(
            "/predict",
            json={"text": "Hello, this is an English text."}
        )
        
        assert response.status_code == 200
        data = response.json()
        assert "predictions" in data
        assert "text_length" in data
        assert len(data["predictions"]) == 2
        assert data["predictions"][0]["language"] == "en"
        assert data["predictions"][0]["confidence"] == 0.95

    def test_predict_endpoint_no_model(self):
        """Test prediction when model is not loaded."""
        with patch('main.model', None):
            response = client.post(
                "/predict",
                json={"text": "Test text"}
            )
            assert response.status_code == 500

    def test_predict_endpoint_empty_text(self):
        """Test prediction with empty text."""
        response = client.post(
            "/predict",
            json={"text": ""}
        )
        assert response.status_code == 422  # Validation error

    def test_predict_endpoint_long_text(self):
        """Test prediction with very long text."""
        long_text = "a" * 10001  # Exceeds max_length
        response = client.post(
            "/predict",
            json={"text": long_text}
        )
        assert response.status_code == 422  # Validation error

    @patch('main.model')
    def test_predict_endpoint_model_error(self, mock_model):
        """Test prediction when model throws an error."""
        mock_model.predict.side_effect = Exception("Model error")
        
        response = client.post(
            "/predict",
            json={"text": "Test text"}
        )
        assert response.status_code == 500

    def test_docs_endpoint(self):
        """Test that the documentation endpoint is accessible."""
        response = client.get("/docs")
        assert response.status_code == 200

    def test_redoc_endpoint(self):
        """Test that the ReDoc endpoint is accessible."""
        response = client.get("/redoc")
        assert response.status_code == 200


class TestDataModels:
    """Test the Pydantic data models."""

    def test_text_input_valid(self):
        """Test valid TextInput creation."""
        from main import TextInput
        
        text_input = TextInput(text="Hello world")
        assert text_input.text == "Hello world"

    def test_text_input_invalid_empty(self):
        """Test TextInput with empty text."""
        from main import TextInput
        from pydantic import ValidationError
        
        with pytest.raises(ValidationError):
            TextInput(text="")

    def test_language_prediction_valid(self):
        """Test valid LanguagePrediction creation."""
        from main import LanguagePrediction
        
        prediction = LanguagePrediction(language="en", confidence=0.95)
        assert prediction.language == "en"
        assert prediction.confidence == 0.95

    def test_prediction_response_valid(self):
        """Test valid PredictionResponse creation."""
        from main import PredictionResponse, LanguagePrediction
        
        predictions = [
            LanguagePrediction(language="en", confidence=0.95),
            LanguagePrediction(language="de", confidence=0.05)
        ]
        response = PredictionResponse(predictions=predictions, text_length=20)
        assert len(response.predictions) == 2
        assert response.text_length == 20