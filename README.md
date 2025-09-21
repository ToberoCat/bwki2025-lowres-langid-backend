# BWKI 2025: Sprachidentifikation seltener Sprachen - Backend

Eine FastAPI-basierte Backend-Anwendung zur automatischen Identifikation von 2000+ Sprachen basierend auf
FastText-Modellen. Dieses Projekt ist Teil der BWKI 2025 Submission zum Thema "Sprachidentifikation seltener Sprachen".

## Table of Contents

- [🚀 Live Demo](#-live-demo)
- [🏗️ Architektur](#️-architektur)
- [🛠️ Lokale Installation](#️-lokale-installation)
- [📊 API-Nutzung](#-api-nutzung)
- [🔧 Konfiguration](#-konfiguration)
- [👥 Team](#-team)

## 🚀 Live Demo

Die Anwendung läuft live auf: **https://toberocat.github.io/bwki2025-lowres-langid-ui/**

### Schneller Test der API:

> Bitte beachten: Die öffentliche Instanz ist für Demonstrationszwecke gedacht und kann Verzögerungen aufweisen. Um
> kosten zu reduzieren, wird die Maschine nach 5 Minuten automatisch heruntergefahren und bei Bedarf neu gestartet -
> Dies kann zu längeren Wartezeiten führen.

```bash
# Health Check
curl https://bwki2025-lowres-langid-backend.fly.dev/health

# Sprachidentifikation testen
curl -X POST "https://bwki2025-lowres-langid-backend.fly.dev/api/v1/classify" \
  -H "Content-Type: application/json" \
  -d '{"text":"Ciao, come stai oggi?","locale":"de"}'
```

## 🏗️ Architektur

```
app/
├── api/v1/           # API Routen und Schemas
│   ├── routes/       # Endpoint-Implementierungen
│   └── schemas/      # Pydantic-Modelle für Request/Response
├── core/             # Kernkonfiguration und Container
├── domain/           # Domain-Modelle und Entities
├── repositories/     # Datenmodell-Abstraktion
├── services/         # Business Logic
└── main.py          # FastAPI-Anwendung
```

## 🛠️ Lokale Installation

Bei einer Lokalen Installation stehen zwei Optionen zur Verfügung:

- Docker
- Lokale Python-Installation

Bei beiden Methoden müssen die FastText-Modelle heruntergeladen werden. Diese sind nicht im Repository enthalten, um die Größe gering zu halten.
Ein Download-Skript ist im `tools/` Verzeichnis enthalten - Dies wird jedoch in jeder Methode extra angeführt.

### Option 1: Docker (Empfohlen)

Die einfachste Methode ist Docker Compose:

```bash
# Im Projektverzeichnis

# Mit Docker Compose starten
docker-compose up --build

# Die API ist dann verfügbar unter: http://localhost:8000
```

### Option 2: Lokale Python-Installation

**Voraussetzungen:**

- Python 3.11+
- UV Package Manager (empfohlen) oder pip

```bash
# Im Projektverzeichnis

# UV installieren (falls nicht vorhanden)
curl -LsSf https://astral.sh/uv/install.sh | sh

# Packages Installieren (Linux, Ubuntu) für pyicu
sudo apt-get install pkg-config libicu-dev build-essential python3-dev

# Abhängigkeiten installieren
uv sync

# Umgebungsvariablen konfigurieren
cp .env.example .env

# Modelle herunterladen
uv run python tools/download_models.py

# Server starten
./start.sh
# oder manuell:
uv run uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Die API ist dann verfügbar unter `http://localhost:8000`

## 📊 API-Nutzung

### Interactive Dokumentation

Nach dem Start ist die vollständige API-Dokumentation verfügbar:

- **Swagger UI**: http://localhost:8000/docs (oder https://bwki2025-lowres-langid-backend.fly.dev/docs)

### Beispiel API-Aufrufe

**Text klassifizieren:**

```bash
curl -X POST "http://localhost:8000/api/v1/classify" \
  -H "Content-Type: application/json" \
  -d '{"text":"Ciao, come stai oggi?","locale":"de"}'
```

**Antwort:**

```json
{
  "predictions": [
    {
      "language_id": "ita",
      "language_name": "Italienisch",
      "probability": 0.9876
    }
  ],
  "writing_system": "Latn"
}
```

**Gesundheitscheck:**

```bash
curl http://localhost:8000/health
# Antwort: {"status": "ok"}
```

## 🔧 Konfiguration

Die Anwendung kann über Umgebungsvariablen konfiguriert werden:

```bash
# .env Datei
PROJECT_NAME="bwki2025-lowres-langid-backend" # Projektname
MODELS_DIR=./models # Verzeichnis für Modelle
```

## 👥 Team

Tobias Madlberger, Florian Schwanzer, Fabian Popov; HTL St. Pölten
Entwickelt für den Bundesweiten Informatikwettbewerb (BWKI) 2025.
In kooperation mit [DIGILINGDIV](https://digiling.univie.ac.at/digilingdiv/)
