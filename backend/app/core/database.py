import sqlite3
import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from backend.app.core.config import settings

logger = logging.getLogger(__name__)

def get_db_connection() -> sqlite3.Connection:
    conn = sqlite3.connect(settings.database_url)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_db_connection()
    cursor = conn.cursor()

    # 1. FAQs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS faqs (
        id TEXT PRIMARY KEY,
        question TEXT NOT NULL,
        answer TEXT NOT NULL,
        category TEXT NOT NULL,
        keywords_json TEXT NOT NULL,
        source TEXT NOT NULL,
        last_updated TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    # 2. Benchmark Questions Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS benchmark_questions (
        id TEXT PRIMARY KEY,
        question TEXT NOT NULL,
        category TEXT NOT NULL,
        expected_answer TEXT NOT NULL,
        expected_behaviour TEXT NOT NULL,
        relevant_faq_id TEXT,
        evaluation_criteria_json TEXT NOT NULL
    )
    """)

    # 3. Benchmark Runs Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS benchmark_runs (
        id TEXT PRIMARY KEY,
        status TEXT NOT NULL,
        total_questions INTEGER NOT NULL,
        total_expected_responses INTEGER NOT NULL,
        completed_responses INTEGER NOT NULL,
        current_question_index INTEGER NOT NULL,
        current_question_text TEXT,
        current_architecture TEXT,
        progress_percentage REAL NOT NULL,
        elapsed_time_sec REAL NOT NULL,
        created_at TEXT NOT NULL,
        notes TEXT
    )
    """)

    # 4. Benchmark Results Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS benchmark_results (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        run_id TEXT NOT NULL,
        test_id TEXT NOT NULL,
        architecture TEXT NOT NULL,
        question_category TEXT NOT NULL,
        user_question TEXT NOT NULL,
        generated_answer TEXT NOT NULL,
        expected_answer TEXT NOT NULL,
        retrieved_source TEXT,
        similarity_score REAL,
        response_time_ms REAL NOT NULL,
        token_usage INTEGER DEFAULT 0,
        estimated_cost REAL DEFAULT 0.0,
        is_correct INTEGER NOT NULL,
        is_hallucinated INTEGER NOT NULL,
        is_refusal_correct INTEGER NOT NULL,
        failure_reason TEXT,
        evaluation_method TEXT NOT NULL,
        human_reviewed INTEGER DEFAULT 0,
        human_correct INTEGER,
        FOREIGN KEY (run_id) REFERENCES benchmark_runs(id)
    )
    """)

    # 5. Chat History Table
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS chat_messages (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        session_id TEXT NOT NULL,
        architecture TEXT NOT NULL,
        role TEXT NOT NULL,
        content TEXT NOT NULL,
        latency_ms REAL,
        confidence REAL,
        source_docs_json TEXT,
        timestamp TEXT NOT NULL
    )
    """)

    conn.commit()

    # Seed FAQs if empty
    cursor.execute("SELECT COUNT(*) as count FROM faqs")
    faq_count = cursor.fetchone()["count"]
    if faq_count == 0:
        seed_faqs_from_file(conn)

    # Seed Benchmark questions if empty
    cursor.execute("SELECT COUNT(*) as count FROM benchmark_questions")
    bm_count = cursor.fetchone()["count"]
    if bm_count == 0:
        seed_benchmark_questions_from_file(conn)

    conn.close()
    logger.info("Database initialized successfully.")

def seed_faqs_from_file(conn: sqlite3.Connection):
    try:
        with open(settings.seed_faqs_path, "r", encoding="utf-8") as f:
            faqs = json.load(f)
        now = datetime.now(timezone.utc).isoformat()
        cursor = conn.cursor()
        for item in faqs:
            cursor.execute("""
            INSERT OR REPLACE INTO faqs (id, question, answer, category, keywords_json, source, last_updated, created_at)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                item["id"],
                item["question"],
                item["answer"],
                item["category"],
                json.dumps(item.get("keywords", [])),
                item.get("source", "Demo University Handbook"),
                item.get("last_updated", now[:10]),
                now
            ))
        conn.commit()
        logger.info(f"Seeded {len(faqs)} FAQs.")
    except Exception as e:
        logger.error(f"Error seeding FAQs: {e}")

def seed_benchmark_questions_from_file(conn: sqlite3.Connection):
    try:
        with open(settings.benchmark_questions_path, "r", encoding="utf-8") as f:
            questions = json.load(f)
        cursor = conn.cursor()
        for q in questions:
            cursor.execute("""
            INSERT OR REPLACE INTO benchmark_questions (id, question, category, expected_answer, expected_behaviour, relevant_faq_id, evaluation_criteria_json)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                q["id"],
                q["question"],
                q["category"],
                q["expected_answer"],
                q["expected_behaviour"],
                q.get("relevant_faq_id"),
                json.dumps(q.get("evaluation_criteria", {}))
            ))
        conn.commit()
        logger.info(f"Seeded {len(questions)} Benchmark Questions.")
    except Exception as e:
        logger.error(f"Error seeding Benchmark questions: {e}")
