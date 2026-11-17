import pytest
from backend.app.engines.retrieval_engine import RetrievalEngine

@pytest.fixture
def sample_engine():
    engine = RetrievalEngine()
    faqs = [
        {
            "id": "faq-1",
            "question": "When do admissions open and close?",
            "answer": "Admissions open May 1st and close June 30th.",
            "category": "Admissions",
            "keywords": ["admissions", "deadline", "open", "close"],
            "source": "Academic Handbook"
        },
        {
            "id": "faq-2",
            "question": "What is the annual hostel fee?",
            "answer": "Hostel fee ranges from $1,200 to $2,200 per year.",
            "category": "Hostel",
            "keywords": ["hostel", "fee", "rooms", "accommodation"],
            "source": "Hostel Board"
        }
    ]
    engine.load_and_index(faqs)
    return engine

def test_keyword_retrieval(sample_engine):
    docs = sample_engine.retrieve("admissions deadline", strategy="keyword", top_k=1)
    assert len(docs) == 1
    assert docs[0].faq_id == "faq-1"
    assert docs[0].similarity_score > 0.0

def test_tfidf_retrieval(sample_engine):
    docs = sample_engine.retrieve("how much does hostel accommodation cost", strategy="tfidf", top_k=1)
    assert len(docs) == 1
    assert docs[0].faq_id == "faq-2"
    assert docs[0].similarity_score > 0.0

def test_embedding_retrieval(sample_engine):
    docs = sample_engine.retrieve("when to apply for college", strategy="embedding", top_k=1)
    assert len(docs) == 1
    assert docs[0].faq_id == "faq-1"

def test_threshold_refusal(sample_engine):
    resp = sample_engine.process("something completely irrelevant like baking pizza pasta", strategy="tfidf", confidence_threshold=0.8)
    assert resp.is_supported is False
    assert "could not find an faq" in resp.message.lower()
