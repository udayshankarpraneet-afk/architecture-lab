@echo off
title ARCHITECTURE LAB - Unified Server
color 0B

echo ======================================================================
echo             ARCHITECTURE LAB - FULL-STACK SYSTEM STARTUP
echo    Comparative Chatbot Study: Rules vs Retrieval vs LLM RAG
echo ======================================================================
echo.

:: Ensure Python is available
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python was not found in your system PATH.
    echo Please install Python 3.10+ and add it to PATH.
    pause
    exit /b 1
)

echo [1/3] Verifying database and indexing...
python -c "import sys; sys.path.insert(0, '.'); from backend.app.core.database import init_db; from backend.app.services.knowledge_service import KnowledgeService; init_db(); KnowledgeService.rebuild_engine_indexes(); print('Database ready with 32 FAQs.')"

echo.
echo [2/3] Starting Unified Server on http://localhost:8000 ...
echo [INFO] API Swagger Docs: http://localhost:8000/docs
echo [INFO] Full-Stack App:   http://localhost:8000/
echo.
echo [3/3] Opening your browser...
start http://localhost:8000/

python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
pause
