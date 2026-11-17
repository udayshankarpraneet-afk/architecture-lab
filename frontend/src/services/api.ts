import {
  ChatResponse,
  CompareResponse,
  FAQItem,
  FAQCreate,
  BenchmarkRunStatus,
  BenchmarkResultItem,
  AnalyticsSummaryResponse,
  RetrievalStrategy
} from '../types';

const API_BASE = '/api';

export const api = {
  // Chat APIs
  async chatRules(message: string): Promise<ChatResponse> {
    const res = await fetch(`${API_BASE}/chat/rules`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message })
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async chatRetrieval(
    message: string,
    strategy: RetrievalStrategy = 'tfidf',
    confidenceThreshold = 0.25,
    topK = 3
  ): Promise<ChatResponse> {
    const res = await fetch(`${API_BASE}/chat/retrieval`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        retrieval_strategy: strategy,
        confidence_threshold: confidenceThreshold,
        top_k: topK
      })
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async chatRAG(
    message: string,
    strategy: RetrievalStrategy = 'tfidf',
    confidenceThreshold = 0.20,
    topK = 3,
    maxTokens = 512
  ): Promise<ChatResponse> {
    const res = await fetch(`${API_BASE}/chat/rag`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        retrieval_strategy: strategy,
        confidence_threshold: confidenceThreshold,
        top_k: topK,
        max_tokens: maxTokens
      })
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async chatCompare(
    message: string,
    strategy: RetrievalStrategy = 'tfidf',
    confidenceThreshold = 0.25,
    topK = 3
  ): Promise<CompareResponse> {
    const res = await fetch(`${API_BASE}/chat/compare`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({
        message,
        retrieval_strategy: strategy,
        confidence_threshold: confidenceThreshold,
        top_k: topK
      })
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  // Knowledge Base APIs
  async fetchKnowledge(search?: string, category?: string): Promise<FAQItem[]> {
    const params = new URLSearchParams();
    if (search) params.append('search', search);
    if (category && category !== 'All') params.append('category', category);
    const res = await fetch(`${API_BASE}/knowledge?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async createFAQ(item: FAQCreate): Promise<FAQItem> {
    const res = await fetch(`${API_BASE}/knowledge`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(item)
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async updateFAQ(faqId: string, item: Partial<FAQCreate>): Promise<FAQItem> {
    const res = await fetch(`${API_BASE}/knowledge/${faqId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(item)
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async deleteFAQ(faqId: string): Promise<void> {
    const res = await fetch(`${API_BASE}/knowledge/${faqId}`, {
      method: 'DELETE'
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
  },

  async exportKnowledge(): Promise<FAQItem[]> {
    const res = await fetch(`${API_BASE}/knowledge/export`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async importKnowledge(items: any[]): Promise<{ message: string }> {
    const res = await fetch(`${API_BASE}/knowledge/import`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(items)
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  // Benchmark APIs
  async startBenchmark(notes?: string): Promise<{ run_id: string; message: string }> {
    const params = new URLSearchParams();
    if (notes) params.append('notes', notes);
    const res = await fetch(`${API_BASE}/benchmark/start?${params.toString()}`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async cancelBenchmark(): Promise<{ message: string }> {
    const res = await fetch(`${API_BASE}/benchmark/cancel`, {
      method: 'POST'
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async fetchBenchmarkStatus(): Promise<BenchmarkRunStatus> {
    const res = await fetch(`${API_BASE}/benchmark/status`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async fetchBenchmarkResults(
    runId?: string,
    architecture?: string,
    category?: string
  ): Promise<BenchmarkResultItem[]> {
    const params = new URLSearchParams();
    if (runId) params.append('run_id', runId);
    if (architecture && architecture !== 'all') params.append('architecture', architecture);
    if (category && category !== 'all') params.append('category', category);
    const res = await fetch(`${API_BASE}/benchmark/results?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async updateReview(
    resultId: number,
    humanCorrect: boolean,
    notes?: string
  ): Promise<{ message: string }> {
    const res = await fetch(`${API_BASE}/benchmark/review/${resultId}`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ result_id: resultId, human_correct: humanCorrect, notes })
    });
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  // Analytics APIs
  async fetchAnalyticsSummary(runId?: string): Promise<AnalyticsSummaryResponse> {
    const params = new URLSearchParams();
    if (runId) params.append('run_id', runId);
    const res = await fetch(`${API_BASE}/analytics/summary?${params.toString()}`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  },

  async fetchHealth(): Promise<any> {
    const res = await fetch(`${API_BASE}/health`);
    if (!res.ok) throw new Error(`HTTP error ${res.status}`);
    return res.json();
  }
};
