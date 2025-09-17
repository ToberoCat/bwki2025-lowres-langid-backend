# Language Identification Backend

A FastAPI backend service for language identification using FastText model. This API can identify languages from text input and supports 176 different languages.

## Features

- 🚀 **FastAPI** - Modern, fast web framework for building APIs
- 🧠 **FastText** - Facebook's language identification model (lid.176.bin)
- 🐳 **Docker** - Containerized deployment
- 🔄 **GitHub Actions** - Automated CI/CD pipeline
- 📊 **176 Languages** - Supports detection of 176 different languages
- 🏥 **Health Checks** - Built-in health monitoring
- 📚 **Auto Documentation** - Interactive API docs with Swagger UI
- 🧪 **Testing** - Comprehensive test suite

## Quick Start

### Using Docker (Recommended)

1. **Build and run with Docker Compose:**
   ```bash
   docker-compose up --build
   ```

2. **Or build and run manually:**
   ```bash
   docker build -t langid-api .
   docker run -p 8000:8000 langid-api
   ```

3. **Access the API:**
   - API: http://localhost:8000
   - Documentation: http://localhost:8000/docs
   - Alternative docs: http://localhost:8000/redoc

### Local Development

1. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

2. **Run the server:**
   ```bash
   python main.py
   ```
   or
   ```bash
   uvicorn main:app --host 0.0.0.0 --port 8000 --reload
   ```

## API Endpoints

### POST /predict
Predict the language of given text.

**Request:**
```json
{
  "text": "Hello, how are you today?"
}
```

**Response:**
```json
{
  "predictions": [
    {
      "language": "en",
      "confidence": 0.9999
    },
    {
      "language": "de", 
      "confidence": 0.0001
    }
  ],
  "text_length": 26
}
```

### GET /health
Check the health status of the API and model.

**Response:**
```json
{
  "status": "healthy",
  "model_loaded": true
}
```

### GET /supported-languages
Get list of all supported languages.

**Response:**
```json
{
  "total_languages": 176,
  "languages": ["af", "als", "am", "ar", ...],
  "note": "This is the FastText lid.176 model supporting 176 languages"
}
```

### GET /
Get basic API information and available endpoints.

## Usage Examples

### Using curl

```bash
# Predict language
curl -X POST "http://localhost:8000/predict" \
     -H "Content-Type: application/json" \
     -d '{"text": "Bonjour, comment allez-vous?"}'

# Check health
curl http://localhost:8000/health

# Get supported languages
curl http://localhost:8000/supported-languages
```

### Using Python requests

```python
import requests

# Predict language
response = requests.post(
    "http://localhost:8000/predict",
    json={"text": "Hola, ¿cómo estás?"}
)
result = response.json()
print(f"Detected language: {result['predictions'][0]['language']}")
print(f"Confidence: {result['predictions'][0]['confidence']:.4f}")
```

### Using JavaScript fetch

```javascript
// Predict language
fetch('http://localhost:8000/predict', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'Wie geht es dir heute?'
  })
})
.then(response => response.json())
.then(data => {
  console.log('Detected language:', data.predictions[0].language);
  console.log('Confidence:', data.predictions[0].confidence);
});
```

## Supported Languages

The FastText lid.176 model supports 176 languages including:

- **Major Languages**: English (en), Spanish (es), French (fr), German (de), Chinese (zh), Arabic (ar), Russian (ru), Japanese (ja), Korean (ko), Portuguese (pt), Italian (it), Dutch (nl), Hindi (hi), etc.
- **Regional Languages**: Many regional and less common languages
- **Complete list**: Available via `/supported-languages` endpoint

## Development

### Running Tests

```bash
# Install development dependencies
pip install -r requirements-dev.txt

# Run tests
pytest tests/ -v

# Run tests with coverage
pytest tests/ -v --cov=main --cov-report=html
```

### Code Formatting

```bash
# Format code
black main.py tests/

# Sort imports
isort main.py tests/

# Lint code
flake8 main.py tests/
```

### Model Information

The API automatically downloads the FastText language identification model:
- **Model**: lid.176.bin
- **Size**: ~131MB
- **Languages**: 176
- **Source**: https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin

## Deployment

### GitHub Container Registry

The GitHub Actions workflow automatically builds and pushes Docker images to GitHub Container Registry on:
- Push to `main` branch
- Push to `develop` branch  
- Pull requests to `main`
- Release creation

**Pull the image:**
```bash
docker pull ghcr.io/toberocat/bwki2025-lowres-langid-backend:latest
```

### Manual Deployment

1. **Build the image:**
   ```bash
   docker build -t langid-api .
   ```

2. **Run the container:**
   ```bash
   docker run -d -p 8000:8000 --name langid-api langid-api
   ```

3. **With custom port:**
   ```bash
   docker run -d -p 3000:8000 --name langid-api langid-api
   ```

## Configuration

### Environment Variables

- `PYTHONDONTWRITEBYTECODE=1` - Prevent Python from writing .pyc files
- `PYTHONUNBUFFERED=1` - Force stdout and stderr to be unbuffered
- `PYTHONPATH=/app` - Set Python path

### Model Configuration

The model is automatically downloaded on first startup. You can also:

1. **Pre-download the model:**
   ```bash
   mkdir models
   wget https://dl.fbaipublicfiles.com/fasttext/supervised-models/lid.176.bin -O models/lid.176.bin
   ```

2. **Mount model volume:**
   ```bash
   docker run -v ./models:/app/models -p 8000:8000 langid-api
   ```

## Security

- ✅ Non-root user in Docker container
- ✅ Security scanning with Trivy
- ✅ Input validation with Pydantic
- ✅ CORS configuration available
- ✅ Health checks enabled

## Performance

- **Startup time**: ~10-30 seconds (model download + loading)
- **Memory usage**: ~500MB (including model)
- **Response time**: ~10-50ms per prediction
- **Throughput**: 100+ requests/second

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Run tests and linting
6. Submit a pull request

## License

This project is licensed under the GNU General Public License v3.0 - see the [LICENSE](LICENSE) file for details.

## Support

For questions and support:
- 📖 Check the [API documentation](http://localhost:8000/docs)
- 🐛 [Report issues](https://github.com/ToberoCat/bwki2025-lowres-langid-backend/issues)
- 💬 [Discussions](https://github.com/ToberoCat/bwki2025-lowres-langid-backend/discussions)
