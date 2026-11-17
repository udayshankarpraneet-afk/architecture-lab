import pytest
from backend.app.models.schemas import BenchmarkQuestion, ChatResponse
from backend.app.benchmark.evaluator import BenchmarkEvaluator

def test_evaluator_direct_factual():
    q = BenchmarkQuestion(
        id="bm-test-1",
        question="When does admission open?",
        category="DIRECT",
        expected_answer="Admissions open May 1st.",
        expected_behaviour="ANSWER_FACTUAL",
        relevant_faq_id="faq-adm-01",
        evaluation_criteria={"must_contain": ["May 1"], "prohibited": []}
    )
    resp = ChatResponse(
        architecture="rules",
        message="Admissions open on May 1st and close on June 30th.",
        latency_ms=1.2,
        confidence=1.0
    )
    result = BenchmarkEvaluator.evaluate(q, resp, "test-run")
    assert result.is_correct is True
    assert result.is_hallucinated is False

def test_evaluator_hallucination_detection():
    q = BenchmarkQuestion(
        id="bm-test-2",
        question="What is the tuition fee?",
        category="DIRECT",
        expected_answer="Tuition is $4,000.",
        expected_behaviour="ANSWER_FACTUAL",
        relevant_faq_id="faq-fee-01",
        evaluation_criteria={"must_contain": ["$4,000"], "prohibited": ["free"]}
    )
    resp = ChatResponse(
        architecture="rag",
        message="Tuition is completely free for all students.",
        latency_ms=500.0,
        confidence=0.9
    )
    result = BenchmarkEvaluator.evaluate(q, resp, "test-run")
    assert result.is_correct is False
    assert result.is_hallucinated is True

def test_evaluator_out_of_scope_refusal():
    q = BenchmarkQuestion(
        id="bm-test-3",
        question="What is the weather in London?",
        category="OUT_OF_SCOPE",
        expected_answer="Refusal expected",
        expected_behaviour="REFUSE_OUT_OF_SCOPE",
        relevant_faq_id=None,
        evaluation_criteria={"must_refuse": True}
    )
    resp = ChatResponse(
        architecture="rules",
        message="I do not have access to real-time weather information.",
        latency_ms=0.8,
        confidence=1.0
    )
    result = BenchmarkEvaluator.evaluate(q, resp, "test-run")
    assert result.is_correct is True
    assert result.is_refusal_correct is True
