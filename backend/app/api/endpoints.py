import csv
import io
import json
from typing import List, Optional
from fastapi import APIRouter, HTTPException, Query, Response
from fastapi.responses import StreamingResponse
from datetime import datetime, timezone

from backend.app.models.schemas import (
    ChatRequest, ChatResponse, CompareRequest, CompareResponse,
    FAQItem, FAQCreate, FAQUpdate,
    BenchmarkRunStatus, BenchmarkResultItem, BenchmarkReviewUpdate,
    AnalyticsSummaryResponse
)
from backend.app.engines.rule_engine import rule_engine
from backend.app.engines.retrieval_engine import retrieval_engine
from backend.app.engines.rag_engine import rag_engine
from backend.app.services.knowledge_service import KnowledgeService
from backend.app.services.analytics_service import AnalyticsService
from backend.app.benchmark.benchmark_runner import benchmark_runner
from backend.app.core.database import get_db_connection
from backend.app.core.config import settings

router = APIRouter()

# ----------------- CHAT ENDPOINTS -----------------

@router.post("/chat/rules", response_model=ChatResponse, summary="Chat with Rule-Based Chatbot")
def chat_rules(req: ChatRequest):
    return rule_engine.process(req.message)

@router.post("/chat/retrieval", response_model=ChatResponse, summary="Chat with Semantic Retrieval Chatbot")
def chat_retrieval(req: ChatRequest):
    strategy = req.retrieval_strategy or "tfidf"
    threshold = req.confidence_threshold if req.confidence_threshold is not None else 0.25
    top_k = req.top_k or 3
    return retrieval_engine.process(req.message, strategy=strategy, confidence_threshold=threshold, top_k=top_k)

@router.post("/chat/rag", response_model=ChatResponse, summary="Chat with LLM-Based RAG Chatbot")
def chat_rag(req: ChatRequest):
    strategy = req.retrieval_strategy or "tfidf"
    threshold = req.confidence_threshold if req.confidence_threshold is not None else 0.20
    top_k = req.top_k or 3
    max_tokens = req.max_tokens or 512
    return rag_engine.process(
        query=req.message,
        retrieval_strategy=strategy,
        confidence_threshold=threshold,
        top_k=top_k,
        max_tokens=max_tokens
    )

@router.post("/chat/compare", response_model=CompareResponse, summary="Compare all 3 architectures simultaneously")
def chat_compare(req: CompareRequest):
    strategy = req.retrieval_strategy or "tfidf"
    threshold = req.confidence_threshold if req.confidence_threshold is not None else 0.25
    top_k = req.top_k or 3

    rules_res = rule_engine.process(req.message)
    retrieval_res = retrieval_engine.process(req.message, strategy=strategy, confidence_threshold=threshold, top_k=top_k)
    rag_res = rag_engine.process(req.message, retrieval_strategy=strategy, confidence_threshold=threshold, top_k=top_k)

    return CompareResponse(
        question=req.message,
        rules_result=rules_res,
        retrieval_result=retrieval_res,
        rag_result=rag_res,
        timestamp=datetime.now(timezone.utc).isoformat()
    )

# ----------------- KNOWLEDGE BASE ENDPOINTS -----------------

@router.get("/knowledge", response_model=List[FAQItem], summary="List all FAQs with optional search and category filters")
def list_knowledge(search: Optional[str] = Query(None), category: Optional[str] = Query(None)):
    return KnowledgeService.list_faqs(search=search, category=category)

@router.get("/knowledge/export", summary="Export entire knowledge base as JSON")
def export_knowledge():
    faqs = KnowledgeService.export_faqs()
    return faqs

@router.post("/knowledge/import", summary="Import FAQs from JSON payload")
def import_knowledge(items: List[dict]):
    count = KnowledgeService.import_faqs(items)
    return {"message": f"Successfully imported {count} FAQs and refreshed retrieval index."}

@router.get("/knowledge/{faq_id}", response_model=FAQItem, summary="Get single FAQ by ID")
def get_knowledge_item(faq_id: str):
    faq = KnowledgeService.get_faq(faq_id)
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return faq

@router.post("/knowledge", response_model=FAQItem, summary="Create a new FAQ and update index")
def create_knowledge_item(item: FAQCreate):
    return KnowledgeService.create_faq(item)

@router.put("/knowledge/{faq_id}", response_model=FAQItem, summary="Update an existing FAQ and update index")
def update_knowledge_item(faq_id: str, item: FAQUpdate):
    faq = KnowledgeService.update_faq(faq_id, item)
    if not faq:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return faq

@router.delete("/knowledge/{faq_id}", summary="Delete an FAQ and update index")
def delete_knowledge_item(faq_id: str):
    deleted = KnowledgeService.delete_faq(faq_id)
    if not deleted:
        raise HTTPException(status_code=404, detail="FAQ not found")
    return {"message": f"FAQ {faq_id} deleted successfully."}

# ----------------- BENCHMARK ENDPOINTS -----------------

@router.post("/benchmark/start", summary="Start the 50-question benchmark suite (150 responses)")
def start_benchmark(notes: Optional[str] = Query("Standard 50-Question Benchmark")):
    run_id = benchmark_runner.start_benchmark(notes=notes)
    return {"run_id": run_id, "status": "running", "message": "Benchmark started across Rules, Retrieval, and RAG."}

@router.post("/benchmark/cancel", summary="Cancel currently executing benchmark run")
def cancel_benchmark():
    benchmark_runner.cancel_benchmark()
    return {"message": "Benchmark cancellation requested."}

@router.get("/benchmark/status", summary="Get status of current or most recent benchmark run")
def get_benchmark_status():
    return benchmark_runner.get_status()

@router.get("/benchmark/results", summary="Get detailed results for a benchmark run")
def get_benchmark_results(
    run_id: Optional[str] = Query(None),
    architecture: Optional[str] = Query(None),
    category: Optional[str] = Query(None)
):
    # Handle direct python function calls
    arch_val = architecture if isinstance(architecture, str) else None
    cat_val = category if isinstance(category, str) else None
    target_run = run_id if isinstance(run_id, str) else None

    conn = get_db_connection()
    if not target_run:
        latest = conn.execute("SELECT id FROM benchmark_runs ORDER BY created_at DESC LIMIT 1").fetchone()
        if not latest:
            conn.close()
            return []
        target_run_id = latest["id"]
    else:
        target_run_id = target_run

    query = "SELECT * FROM benchmark_results WHERE run_id = ?"
    params = [target_run_id]

    if arch_val and arch_val.lower() != "all":
        query += " AND architecture = ?"
        params.append(arch_val)

    if cat_val and cat_val.lower() != "all":
        query += " AND question_category = ?"
        params.append(cat_val)

    query += " ORDER BY id ASC"
    rows = conn.execute(query, params).fetchall()
    conn.close()

    results = []
    for r in rows:
        results.append({
            "id": r["id"],
            "run_id": r["run_id"],
            "test_id": r["test_id"],
            "architecture": r["architecture"],
            "question_category": r["question_category"],
            "user_question": r["user_question"],
            "generated_answer": r["generated_answer"],
            "expected_answer": r["expected_answer"],
            "retrieved_source": r["retrieved_source"],
            "similarity_score": r["similarity_score"],
            "response_time_ms": r["response_time_ms"],
            "token_usage": r["token_usage"],
            "estimated_cost": r["estimated_cost"],
            "is_correct": bool(r["is_correct"]),
            "is_hallucinated": bool(r["is_hallucinated"]),
            "is_refusal_correct": bool(r["is_refusal_correct"]),
            "failure_reason": r["failure_reason"],
            "evaluation_method": r["evaluation_method"],
            "human_reviewed": bool(r["human_reviewed"]),
            "human_correct": r["human_correct"]
        })
    return results

@router.put("/benchmark/review/{result_id}", summary="Manual human evaluation override")
def update_benchmark_review(result_id: int, review: BenchmarkReviewUpdate):
    conn = get_db_connection()
    res = conn.execute("SELECT * FROM benchmark_results WHERE id = ?", (result_id,)).fetchone()
    if not res:
        conn.close()
        raise HTTPException(status_code=404, detail="Benchmark result not found")

    human_correct_int = 1 if review.human_correct else 0
    conn.execute("""
    UPDATE benchmark_results
    SET human_reviewed = 1, human_correct = ?, is_correct = ?
    WHERE id = ?
    """, (human_correct_int, human_correct_int, result_id))
    conn.commit()
    conn.close()
    return {"message": f"Result {result_id} updated with human evaluation."}

@router.get("/benchmark/export/csv", summary="Export benchmark results to CSV format")
def export_benchmark_csv(run_id: Optional[str] = Query(None)):
    results = get_benchmark_results(run_id=run_id)
    if not results:
        raise HTTPException(status_code=404, detail="No benchmark results found to export.")

    output = io.StringIO()
    writer = csv.writer(output)
    writer.writerow([
        "ID", "Run ID", "Test ID", "Architecture", "Category", "Question",
        "Generated Answer", "Expected Answer", "Retrieved Source", "Similarity Score",
        "Latency (ms)", "Token Usage", "Estimated Cost ($)", "Is Correct",
        "Is Hallucinated", "Is Refusal Correct", "Failure Reason", "Evaluation Method",
        "Human Reviewed", "Human Correct"
    ])

    for r in results:
        writer.writerow([
            r["id"], r["run_id"], r["test_id"], r["architecture"], r["question_category"],
            r["user_question"], r["generated_answer"], r["expected_answer"],
            r["retrieved_source"] or "N/A", r["similarity_score"] or 0.0,
            r["response_time_ms"], r["token_usage"] or 0, r["estimated_cost"] or 0.0,
            r["is_correct"], r["is_hallucinated"], r["is_refusal_correct"],
            r["failure_reason"] or "", r["evaluation_method"],
            r["human_reviewed"], r["human_correct"]
        ])

    output.seek(0)
    return StreamingResponse(
        iter([output.getvalue()]),
        media_type="text/csv",
        headers={"Content-Disposition": f"attachment; filename=benchmark_{run_id or 'latest'}.csv"}
    )

@router.get("/benchmark/export/json", summary="Export benchmark results to JSON format")
def export_benchmark_json(run_id: Optional[str] = Query(None)):
    results = get_benchmark_results(run_id=run_id)
    return results

# ----------------- ANALYTICS & HEALTH -----------------

@router.get("/analytics/summary", response_model=AnalyticsSummaryResponse, summary="Get high-level analytical performance metrics")
def get_analytics_summary(run_id: Optional[str] = Query(None)):
    return AnalyticsService.get_summary(run_id=run_id)

@router.get("/health", summary="Health check and configuration status")
def get_health():
    api_key_configured = bool(settings.gemini_api_key.strip())
    faqs = KnowledgeService.list_faqs()
    return {
        "status": "healthy",
        "app_name": settings.app_name,
        "version": settings.version,
        "gemini_api_key_configured": api_key_configured,
        "gemini_model": settings.gemini_model,
        "faqs_count": len(faqs),
        "database_connected": True
    }
