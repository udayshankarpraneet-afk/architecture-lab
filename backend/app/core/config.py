import os
from pathlib import Path
from pydantic import BaseModel
from dotenv import load_dotenv

# Base paths
BASE_DIR = Path(__file__).resolve().parent.parent.parent
DATA_DIR = BASE_DIR.parent / "data"
DATABASE_PATH = BASE_DIR / "architecture_lab.db"

# Load .env if present and dotenv is available
try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env")
except ImportError:
    pass

class Settings(BaseModel):
    app_name: str = "ARCHITECTURE LAB"
    version: str = "1.0.0"
    gemini_api_key: str = os.getenv("GEMINI_API_KEY", "")
    gemini_model: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    database_url: str = str(DATABASE_PATH)
    seed_faqs_path: str = str(DATA_DIR / "seed_faqs.json")
    benchmark_questions_path: str = str(DATA_DIR / "benchmark_questions.json")

    # Guardrails and timeouts
    rag_timeout_seconds: float = 15.0
    rag_default_top_k: int = 3
    rag_default_threshold: float = 0.20
    gemini_temperature: float = 0.0

settings = Settings()
