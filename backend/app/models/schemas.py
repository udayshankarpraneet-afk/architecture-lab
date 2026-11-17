from typing import List, Optional, Dict, Any, Literal
from pydantic import BaseModel, Field
from datetime import datetime

class FAQItem(BaseModel):
    id: str
    question: str
    answer: str
    category: str
    keywords: List[str] = Field(default_factory=list)
    source: str
    last_updated: str
    created_at: Optional[str] = None

class FAQCreate(BaseModel):
    question: str
    answer: str
    category: str
    keywords: List[str] = Field(default_factory=list)
    source: str

class FAQUpdate(BaseModel):
    question: Optional[str] = None
    answer: Optional[str] = None
    category: Optional[str] = None
    keywords: Optional[List[str]] = None
    source: Optional[str] = None

class RetrievedDocument(BaseModel):
    faq_id: str
    question: str
    answer: str
    category: str
    source: str
    similarity_score: float

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str] = "default-session"
    retrieval_strategy: Optional[Literal["keyword", "tfidf", "embedding"]] = "tfidf"
    confidence_threshold: Optional[float] = 0.25
    top_k: Optional[int] = 3
    max_tokens: Optional[int] = 512

class ChatResponse(BaseModel):
    architecture: Literal["rules", "retrieval", "rag"]
    message: str
    latency_ms: float
    confidence: float
    retrieved_sources: List[RetrievedDocument] = Field(default_factory=list)
    matched_rule: Optional[str] = None
    is_supported: bool = True
    token_usage: Optional[Dict[str, int]] = None
    estimated_cost: Optional[float] = 0.0
    trace_steps: Optional[List[Dict[str, Any]]] = Field(default_factory=list)
    warning_or_error: Optional[str] = None

class CompareRequest(BaseModel):
    message: str
    retrieval_strategy: Optional[Literal["keyword", "tfidf", "embedding"]] = "tfidf"
    confidence_threshold: Optional[float] = 0.25
    top_k: Optional[int] = 3

class CompareResponse(BaseModel):
    question: str
    rules_result: ChatResponse
    retrieval_result: ChatResponse
    rag_result: ChatResponse
    timestamp: str

class BenchmarkQuestion(BaseModel):
    id: str
    question: str
    category: Literal["DIRECT", "PARAPHRASED", "OUT_OF_SCOPE", "ADVERSARIAL"]
    expected_answer: str
    expected_behaviour: Literal["ANSWER_FACTUAL", "REFUSE_OUT_OF_SCOPE", "REFUSE_ADVERSARIAL"]
    relevant_faq_id: Optional[str] = None
    evaluation_criteria: Dict[str, Any] = Field(default_factory=dict)

class BenchmarkResultItem(BaseModel):
    id: Optional[int] = None
    run_id: str
    test_id: str
    architecture: str
    question_category: str
    user_question: str
    generated_answer: str
    expected_answer: str
    retrieved_source: Optional[str] = None
    similarity_score: Optional[float] = None
    response_time_ms: float
    token_usage: Optional[int] = 0
    estimated_cost: Optional[float] = 0.0
    is_correct: bool
    is_hallucinated: bool
    is_refusal_correct: bool
    failure_reason: Optional[str] = None
    evaluation_method: str = "automated"
    human_reviewed: bool = False
    human_correct: Optional[bool] = None

class BenchmarkRunStatus(BaseModel):
    run_id: str
    status: Literal["idle", "running", "paused", "completed", "cancelled", "failed"]
    total_questions: int
    total_expected_responses: int
    completed_responses: int
    current_question_index: int
    current_question_text: Optional[str] = None
    current_architecture: Optional[str] = None
    progress_percentage: float
    elapsed_time_sec: float
    created_at: str

class BenchmarkReviewUpdate(BaseModel):
    result_id: int
    human_correct: bool
    human_hallucinated: Optional[bool] = None
    notes: Optional[str] = None

class ArchitectureMetrics(BaseModel):
    architecture: str
    total_evaluated: int
    correct_count: int
    accuracy_percentage: float
    avg_latency_ms: float
    median_latency_ms: float
    min_latency_ms: float
    max_latency_ms: float
    hallucination_count: int
    hallucination_rate_percentage: float
    out_of_scope_total: int
    out_of_scope_refused: int
    out_of_scope_rejection_rate: float
    direct_accuracy: float
    paraphrased_accuracy: float
    adversarial_resistance_rate: float
    total_tokens: int
    total_cost_usd: float
    avg_cost_per_query_usd: float
    setup_complexity_score: int # 1 to 10 scale

class AnalyticsSummaryResponse(BaseModel):
    has_benchmark_data: bool
    total_runs: int
    latest_run_id: Optional[str] = None
    latest_run_timestamp: Optional[str] = None
    total_benchmark_questions: int = 50
    architectures: Dict[str, ArchitectureMetrics] = Field(default_factory=dict)
    category_breakdown: Dict[str, Dict[str, float]] = Field(default_factory=dict)
    latency_distribution: Dict[str, List[float]] = Field(default_factory=dict)
    key_findings: List[str] = Field(default_factory=list)
