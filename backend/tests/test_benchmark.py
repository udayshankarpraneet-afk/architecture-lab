import pytest
from backend.app.core.database import init_db, get_db_connection
from backend.app.services.knowledge_service import KnowledgeService
from backend.app.services.analytics_service import AnalyticsService
from backend.app.engines.rule_engine import rule_engine
from backend.app.engines.retrieval_engine import retrieval_engine

def test_init_db_and_seeding():
    init_db()
    KnowledgeService.rebuild_engine_indexes()
    conn = get_db_connection()
    faq_count = conn.execute("SELECT COUNT(*) as c FROM faqs").fetchone()["c"]
    bm_count = conn.execute("SELECT COUNT(*) as c FROM benchmark_questions").fetchone()["c"]
    conn.close()

    assert faq_count >= 30
    assert bm_count == 50

def test_knowledge_crud():
    faqs_initial = KnowledgeService.list_faqs()
    assert len(faqs_initial) >= 30

    # Search
    search_res = KnowledgeService.list_faqs(search="tuition")
    assert len(search_res) > 0

    # Category filter
    cat_res = KnowledgeService.list_faqs(category="Hostel")
    assert len(cat_res) >= 3

def test_analytics_empty_state_or_summary():
    summary = AnalyticsService.get_summary()
    assert summary.total_benchmark_questions == 50
    assert isinstance(summary.key_findings, list)
