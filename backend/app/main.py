import logging
from contextlib import asynccontextmanager
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from backend.app.core.config import settings
from backend.app.core.database import init_db
from backend.app.services.knowledge_service import KnowledgeService
from backend.app.api.endpoints import router as api_router

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(name)s: %(message)s")
logger = logging.getLogger("architecture_lab")

@asynccontextmanager
async def lifespan(app: FastAPI):
    logger.info("Initializing ARCHITECTURE LAB backend...")
    init_db()
    KnowledgeService.rebuild_engine_indexes()
    logger.info("Backend engines initialized and ready.")
    yield
    logger.info("Shutting down ARCHITECTURE LAB backend...")

app = FastAPI(
    title="ARCHITECTURE LAB — Comparative Chatbot Architecture API",
    description="Comparative study platform for Rules vs Retrieval vs LLM-Based RAG for Artificial Intelligence Foundations.",
    version="1.0.0",
    lifespan=lifespan
)

# CORS configuration for local development and demonstration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Mount API routes
app.include_router(api_router, prefix="/api")

# Serve frontend build if present
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
from pathlib import Path

dist_dir = Path(__file__).resolve().parent.parent.parent / "frontend" / "dist"
if dist_dir.exists():
    app.mount("/assets", StaticFiles(directory=dist_dir / "assets"), name="assets")

    @app.get("/{full_path:path}")
    def serve_spa(full_path: str):
        file_path = dist_dir / full_path
        if file_path.is_file():
            return FileResponse(file_path)
        return FileResponse(dist_dir / "index.html")
else:
    @app.get("/")
    def root():
        return {
            "message": "ARCHITECTURE LAB Backend API is running.",
            "docs_url": "/docs",
            "health_url": "/api/health"
        }
