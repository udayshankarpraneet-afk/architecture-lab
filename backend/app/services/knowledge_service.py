import json
import logging
from typing import List, Dict, Any, Optional
from datetime import datetime, timezone
from backend.app.core.database import get_db_connection
from backend.app.models.schemas import FAQItem, FAQCreate, FAQUpdate
from backend.app.engines.retrieval_engine import retrieval_engine

logger = logging.getLogger(__name__)

class KnowledgeService:
    """
    Manages Knowledge Base CRUD operations and triggers automatic
    retrieval index rebuilds on any knowledge mutation.
    """

    @classmethod
    def rebuild_engine_indexes(cls):
        """Loads all FAQs from SQLite and updates retrieval indexes."""
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM faqs ORDER BY id ASC").fetchall()
        conn.close()

        faqs = []
        for r in rows:
            faqs.append({
                "id": r["id"],
                "question": r["question"],
                "answer": r["answer"],
                "category": r["category"],
                "keywords": json.loads(r["keywords_json"]),
                "source": r["source"],
                "last_updated": r["last_updated"],
                "created_at": r["created_at"]
            })

        retrieval_engine.load_and_index(faqs)
        logger.info(f"Rebuilt retrieval index with {len(faqs)} FAQs.")

    @classmethod
    def list_faqs(cls, search: Optional[str] = None, category: Optional[str] = None) -> List[FAQItem]:
        conn = get_db_connection()
        query = "SELECT * FROM faqs WHERE 1=1"
        params = []

        if category and category.lower() != "all":
            query += " AND category = ?"
            params.append(category)

        if search:
            query += " AND (question LIKE ? OR answer LIKE ? OR keywords_json LIKE ?)"
            s = f"%{search}%"
            params.extend([s, s, s])

        query += " ORDER BY category ASC, id ASC"
        rows = conn.execute(query, params).fetchall()
        conn.close()

        results = []
        for r in rows:
            results.append(FAQItem(
                id=r["id"],
                question=r["question"],
                answer=r["answer"],
                category=r["category"],
                keywords=json.loads(r["keywords_json"]),
                source=r["source"],
                last_updated=r["last_updated"],
                created_at=r["created_at"]
            ))
        return results

    @classmethod
    def get_faq(cls, faq_id: str) -> Optional[FAQItem]:
        conn = get_db_connection()
        r = conn.execute("SELECT * FROM faqs WHERE id = ?", (faq_id,)).fetchone()
        conn.close()
        if not r:
            return None
        return FAQItem(
            id=r["id"],
            question=r["question"],
            answer=r["answer"],
            category=r["category"],
            keywords=json.loads(r["keywords_json"]),
            source=r["source"],
            last_updated=r["last_updated"],
            created_at=r["created_at"]
        )

    @classmethod
    def create_faq(cls, item: FAQCreate) -> FAQItem:
        conn = get_db_connection()
        # Generate ID
        prefix = item.category[:3].lower()
        count = conn.execute("SELECT COUNT(*) as c FROM faqs WHERE category = ?", (item.category,)).fetchone()["c"]
        new_id = f"faq-{prefix}-{count + 1:02d}"

        now = datetime.now(timezone.utc).isoformat()
        date_str = now[:10]

        conn.execute("""
        INSERT INTO faqs (id, question, answer, category, keywords_json, source, last_updated, created_at)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        """, (
            new_id, item.question, item.answer, item.category,
            json.dumps(item.keywords), item.source, date_str, now
        ))
        conn.commit()
        conn.close()

        cls.rebuild_engine_indexes()
        return cls.get_faq(new_id)

    @classmethod
    def update_faq(cls, faq_id: str, item: FAQUpdate) -> Optional[FAQItem]:
        conn = get_db_connection()
        existing = conn.execute("SELECT * FROM faqs WHERE id = ?", (faq_id,)).fetchone()
        if not existing:
            conn.close()
            return None

        new_q = item.question if item.question is not None else existing["question"]
        new_a = item.answer if item.answer is not None else existing["answer"]
        new_cat = item.category if item.category is not None else existing["category"]
        new_kw = json.dumps(item.keywords) if item.keywords is not None else existing["keywords_json"]
        new_src = item.source if item.source is not None else existing["source"]
        date_str = datetime.now(timezone.utc).isoformat()[:10]

        conn.execute("""
        UPDATE faqs
        SET question = ?, answer = ?, category = ?, keywords_json = ?, source = ?, last_updated = ?
        WHERE id = ?
        """, (new_q, new_a, new_cat, new_kw, new_src, date_str, faq_id))
        conn.commit()
        conn.close()

        cls.rebuild_engine_indexes()
        return cls.get_faq(faq_id)

    @classmethod
    def delete_faq(cls, faq_id: str) -> bool:
        conn = get_db_connection()
        cursor = conn.execute("DELETE FROM faqs WHERE id = ?", (faq_id,))
        deleted = cursor.rowcount > 0
        conn.commit()
        conn.close()

        if deleted:
            cls.rebuild_engine_indexes()
        return deleted

    @classmethod
    def export_faqs(cls) -> List[Dict[str, Any]]:
        conn = get_db_connection()
        rows = conn.execute("SELECT * FROM faqs ORDER BY category ASC, id ASC").fetchall()
        conn.close()
        return [
            {
                "id": r["id"],
                "question": r["question"],
                "answer": r["answer"],
                "category": r["category"],
                "keywords": json.loads(r["keywords_json"]),
                "source": r["source"],
                "last_updated": r["last_updated"]
            }
            for r in rows
        ]

    @classmethod
    def import_faqs(cls, items: List[Dict[str, Any]]) -> int:
        conn = get_db_connection()
        now = datetime.now(timezone.utc).isoformat()
        count = 0
        for it in items:
            if "id" in it and "question" in it and "answer" in it:
                conn.execute("""
                INSERT OR REPLACE INTO faqs (id, question, answer, category, keywords_json, source, last_updated, created_at)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (
                    it["id"],
                    it["question"],
                    it["answer"],
                    it.get("category", "General"),
                    json.dumps(it.get("keywords", [])),
                    it.get("source", "Imported Document"),
                    it.get("last_updated", now[:10]),
                    now
                ))
                count += 1
        conn.commit()
        conn.close()
        cls.rebuild_engine_indexes()
        return count
