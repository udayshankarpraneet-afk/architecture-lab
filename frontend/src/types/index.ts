export type ArchitectureType = 'rules' | 'retrieval' | 'rag';
export type RetrievalStrategy = 'keyword' | 'tfidf' | 'embedding';

export interface RetrievedDocument {
  faq_id: string;
  question: string;
  answer: string;
  category: string;
  source: string;
  similarity_score: number;
}

export interface TraceStep {
  stage: string;
  description: string;
  data: Record<string, any>;
}

export interface ChatResponse {
  architecture: ArchitectureType;
  message: string;
  latency_ms: number;
  confidence: number;
  retrieved_sources: RetrievedDocument[];
  matched_rule?: string | null;
  is_supported: boolean;
  token_usage?: {
    input_tokens: number;
    output_tokens: number;
    total_tokens?: number;
  };
  estimated_cost?: number;
  trace_steps?: TraceStep[];
  warning_or_error?: string | null;
}

export interface CompareResponse {
  question: string;
  rules_result: ChatResponse;
  retrieval_result: ChatResponse;
  rag_result: ChatResponse;
  timestamp: string;
}

export interface FAQItem {
  id: string;
  question: string;
  answer: string;
  category: string;
  keywords: string[];
  source: string;
  last_updated: string;
  created_at?: string;
}

export interface FAQCreate {
  question: string;
  answer: string;
  category: string;
  keywords: string[];
  source: string;
}

export interface BenchmarkQuestion {
  id: string;
  question: string;
  category: 'DIRECT' | 'PARAPHRASED' | 'OUT_OF_SCOPE' | 'ADVERSARIAL';
  expected_answer: string;
  expected_behaviour: 'ANSWER_FACTUAL' | 'REFUSE_OUT_OF_SCOPE' | 'REFUSE_ADVERSARIAL';
  relevant_faq_id?: string | null;
  evaluation_criteria?: Record<string, any>;
}

export interface BenchmarkResultItem {
  id: number;
  run_id: string;
  test_id: string;
  architecture: string;
  question_category: string;
  user_question: string;
  generated_answer: string;
  expected_answer: string;
  retrieved_source?: string | null;
  similarity_score?: number | null;
  response_time_ms: number;
  token_usage?: number;
  estimated_cost?: number;
  is_correct: boolean;
  is_hallucinated: boolean;
  is_refusal_correct: boolean;
  failure_reason?: string | null;
  evaluation_method: string;
  human_reviewed: boolean;
  human_correct?: boolean | null;
}

export interface BenchmarkRunStatus {
  run_id: string;
  status: 'idle' | 'running' | 'paused' | 'completed' | 'cancelled' | 'failed';
  total_questions: number;
  total_expected_responses: number;
  completed_responses: number;
  current_question_index: number;
  current_question_text?: string | null;
  current_architecture?: string | null;
  progress_percentage: number;
  elapsed_time_sec: number;
  created_at: string;
}

export interface ArchitectureMetrics {
  architecture: string;
  total_evaluated: number;
  correct_count: number;
  accuracy_percentage: number;
  avg_latency_ms: number;
  median_latency_ms: number;
  min_latency_ms: number;
  max_latency_ms: number;
  hallucination_count: number;
  hallucination_rate_percentage: number;
  out_of_scope_total: number;
  out_of_scope_refused: number;
  out_of_scope_rejection_rate: number;
  direct_accuracy: number;
  paraphrased_accuracy: number;
  adversarial_resistance_rate: number;
  total_tokens: number;
  total_cost_usd: number;
  avg_cost_per_query_usd: number;
  setup_complexity_score: number;
}

export interface AnalyticsSummaryResponse {
  has_benchmark_data: boolean;
  total_runs: number;
  latest_run_id?: string | null;
  latest_run_timestamp?: string | null;
  total_benchmark_questions: number;
  architectures: Record<string, ArchitectureMetrics>;
  category_breakdown: Record<string, Record<string, number>>;
  latency_distribution: Record<string, number[]>;
  key_findings: string[];
}
