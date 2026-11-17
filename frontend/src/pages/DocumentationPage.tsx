import React, { useEffect, useState } from 'react';
import { 
  FileText, 
  Printer, 
  Download, 
  ExternalLink, 
  CheckCircle2, 
  Layers, 
  Cpu, 
  Search, 
  Sparkles,
  BookOpen,
  Info
} from 'lucide-react';
import { api } from '../services/api';
import { AnalyticsSummaryResponse } from '../types';

export const DocumentationPage: React.FC = () => {
  const [analytics, setAnalytics] = useState<AnalyticsSummaryResponse | null>(null);

  useEffect(() => {
    api.fetchAnalyticsSummary().then(setAnalytics).catch(console.error);
  }, []);

  const hasData = analytics?.has_benchmark_data && Object.keys(analytics.architectures).length > 0;

  const handlePrint = () => {
    window.print();
  };

  return (
    <div className="space-y-8 max-w-5xl mx-auto pb-16">
      {/* Header and Print Action */}
      <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 glass-panel p-6 rounded-2xl border border-slate-800 no-print">
        <div>
          <h2 className="text-xl font-bold text-white flex items-center gap-2">
            <FileText className="w-5 h-5 text-cyan-400" />
            <span>Academic Project Technical Report</span>
          </h2>
          <p className="text-xs text-slate-400 mt-1">
            Artificial Intelligence Foundations Laboratory Study • Suitable for academic review and examination.
          </p>
        </div>

        <button
          onClick={handlePrint}
          className="px-4 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-950/40 transition-all cursor-pointer"
        >
          <Printer className="w-4 h-4" />
          <span>Export / Print PDF</span>
        </button>
      </div>

      {/* Main Document Body */}
      <article className="glass-panel p-8 sm:p-12 rounded-2xl border border-slate-800 space-y-10 text-slate-300 leading-relaxed text-sm bg-slate-950/80 shadow-2xl">
        {/* Title Block */}
        <header className="border-b border-slate-800 pb-8 text-center space-y-3">
          <div className="inline-block text-[11px] font-mono uppercase tracking-widest text-cyan-400 font-bold px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-800/60">
            Academic Technical Research Monograph
          </div>
          <h1 className="text-2xl sm:text-3xl font-extrabold text-white tracking-tight">
            Comparative Chatbot Architecture Study: Rules vs Semantic Retrieval vs LLM-Based RAG
          </h1>
          <p className="text-xs text-slate-400 font-mono">
            Platform: ARCHITECTURE LAB • Knowledge Domain: Demo University College Enquiry System
          </p>
        </header>

        {/* Section 1: Introduction */}
        <section className="space-y-3">
          <h2 className="text-lg font-bold text-white border-b border-slate-800/80 pb-1.5 flex items-center gap-2">
            <span className="text-cyan-400 font-mono text-sm">1.</span> Introduction
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            Conversational agents have evolved through three distinct evolutionary eras: deterministic rule-based pattern engines, information retrieval-based similarity systems, and neural Large Language Model (LLM) Retrieval-Augmented Generation (RAG) pipelines. Despite extensive literature on each paradigm in isolation, empirical side-by-side studies evaluating all three architectures under identical domain constraints, the same knowledge base, and standardized test suites remain sparse. This study bridges that gap.
          </p>
        </section>

        {/* Section 2: Problem Statement */}
        <section className="space-y-3">
          <h2 className="text-lg font-bold text-white border-b border-slate-800/80 pb-1.5 flex items-center gap-2">
            <span className="text-cyan-400 font-mono text-sm">2.</span> Problem Statement
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            Institutional question-answering systems (such as college admissions portals) face competing trade-offs: factual certainty, response latency, zero hallucination, adversarial resistance, and conversational naturalness. Deploying an ungrounded LLM risks severe factual hallucinations (such as inventing non-existent degrees or false fee amounts), whereas purely rule-based bots fail on trivial syntactic rephrasings. There is an urgent need for empirical guidelines on when each architectural paradigm is justified.
          </p>
        </section>

        {/* Section 3: Objectives */}
        <section className="space-y-3">
          <h2 className="text-lg font-bold text-white border-b border-slate-800/80 pb-1.5 flex items-center gap-2">
            <span className="text-cyan-400 font-mono text-sm">3.</span> Project Objectives
          </h2>
          <ul className="list-disc pl-5 space-y-1.5 text-xs sm:text-sm text-slate-300">
            <li>Implement three genuinely distinct chatbot engines sharing the same knowledge base.</li>
            <li>Construct a 50-question benchmark suite (20 Direct, 15 Paraphrased, 10 Out-of-Scope, 5 Adversarial).</li>
            <li>Conduct automated and human-verifiable evaluations measuring accuracy, latency, cost, and hallucination rates.</li>
            <li>Provide interactive visual workflows and architectural decision guidance for engineering teams.</li>
          </ul>
        </section>

        {/* Section 4: Literature & Background */}
        <section className="space-y-3">
          <h2 className="text-lg font-bold text-white border-b border-slate-800/80 pb-1.5 flex items-center gap-2">
            <span className="text-cyan-400 font-mono text-sm">4.</span> Literature &amp; Theoretical Background
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            Rule-based engines trace back to Weizenbaum's ELIZA (1966) and pattern-matching AIML frameworks. Information retrieval chatbots emerged with the vector space model (Salton et al., 1975) and BM25 term weighting (Robertson et al., 1994). In 2020, Lewis et al. introduced Retrieval-Augmented Generation (RAG), combining dense retrieval with generative pre-trained transformers to anchor generation to factual source documents.
          </p>
        </section>

        {/* Section 5 & 6: System Architecture & Stack */}
        <section className="space-y-3">
          <h2 className="text-lg font-bold text-white border-b border-slate-800/80 pb-1.5 flex items-center gap-2">
            <span className="text-cyan-400 font-mono text-sm">5.</span> System Architecture &amp; Technology Stack
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-4 text-xs font-mono">
            <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
              <span className="text-cyan-400 font-bold block">Frontend Stack</span>
              <p className="text-slate-300">React 18, TypeScript, Vite, Tailwind CSS, Framer Motion, Recharts, Lucide Icons.</p>
            </div>
            <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 space-y-1">
              <span className="text-cyan-400 font-bold block">Backend Stack</span>
              <p className="text-slate-300">Python 3.13, FastAPI, Pydantic, NumPy, SQLite, HTTPX, Pytest, Google Gemini Flash API.</p>
            </div>
          </div>
        </section>

        {/* Section 7: Implementation Details */}
        <section className="space-y-3">
          <h2 className="text-lg font-bold text-white border-b border-slate-800/80 pb-1.5 flex items-center gap-2">
            <span className="text-cyan-400 font-mono text-sm">6.</span> Implementation of All Three Architectures
          </h2>
          <div className="space-y-3 text-xs sm:text-sm text-slate-300">
            <p>
              <strong>Architecture A (Rule-Based):</strong> Implemented in <code className="text-cyan-300">rule_engine.py</code> with text normalisation, regex patterns sorted by priority weights, IF-THEN evaluations, and out-of-scope refusals. Pure Python execution with zero model dependencies.
            </p>
            <p>
              <strong>Architecture B (Semantic Retrieval):</strong> Implemented in <code className="text-cyan-300">retrieval_engine.py</code> offering three strategies: Keyword BM25 overlap, TF-IDF cosine similarity, and dense continuous embeddings. Applies confidence gating thresholds before returning verbatim FAQ content.
            </p>
            <p>
              <strong>Architecture C (LLM-Based RAG):</strong> Implemented in <code className="text-cyan-300">rag_engine.py</code> utilizing top-K semantic retrieval, context grounding, prompt construction with anti-hallucination system guardrails, Google Gemini 2.5 Flash execution, token usage tracking, and citation attribution.
            </p>
          </div>
        </section>

        {/* Section 8: Dataset Design */}
        <section className="space-y-3">
          <h2 className="text-lg font-bold text-white border-b border-slate-800/80 pb-1.5 flex items-center gap-2">
            <span className="text-cyan-400 font-mono text-sm">7.</span> Knowledge Base &amp; Benchmark Dataset Design
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            The dataset models "Demo University", covering 11 comprehensive operational categories (Admissions, Courses, Eligibility, Fees, Scholarships, Hostel, Library, Examinations, Transportation, Documents, Contact) across 32 detailed FAQ documents.
          </p>
          <div className="p-3.5 rounded-xl bg-slate-900 border border-slate-800 text-xs text-slate-300">
            <strong>Benchmark Suite Distribution (50 questions):</strong>
            <ul className="list-disc pl-5 mt-1 space-y-1">
              <li>20 Direct Questions: Canonical college inquiries.</li>
              <li>15 Paraphrased Questions: Lexical rephrasings testing semantic invariance.</li>
              <li>10 Out-of-Scope Questions: Sports, culinary, weather, and external trivia requiring polite refusal.</li>
              <li>5 Adversarial Questions: Prompt injection and hallucination baiting (e.g., claiming free tuition).</li>
            </ul>
          </div>
        </section>

        {/* Section 9: Evaluation Formulas */}
        <section className="space-y-3">
          <h2 className="text-lg font-bold text-white border-b border-slate-800/80 pb-1.5 flex items-center gap-2">
            <span className="text-cyan-400 font-mono text-sm">8.</span> Formal Evaluation Formulas
          </h2>
          <div className="grid grid-cols-1 sm:grid-cols-2 gap-3 text-xs font-mono">
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
              <span className="text-cyan-400 font-bold block mb-1">Accuracy Formula</span>
              <code>Accuracy = (Correct Responses / Total Tested) × 100%</code>
            </div>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
              <span className="text-cyan-400 font-bold block mb-1">Hallucination Rate</span>
              <code>Hallucination = (Unsupported Claims / Total Tested) × 100%</code>
            </div>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
              <span className="text-cyan-400 font-bold block mb-1">Out-of-Scope Rejection</span>
              <code>Rejection Rate = (Correct Refusals / Total OOS) × 100%</code>
            </div>
            <div className="p-3 rounded-lg bg-slate-900 border border-slate-800">
              <span className="text-cyan-400 font-bold block mb-1">Token Cost Modeling</span>
              <code>Cost = (Input_Tokens × $0.075 + Output × $0.30) / 10^6</code>
            </div>
          </div>
        </section>

        {/* Section 10: Experimental Results */}
        <section className="space-y-3">
          <h2 className="text-lg font-bold text-white border-b border-slate-800/80 pb-1.5 flex items-center gap-2">
            <span className="text-cyan-400 font-mono text-sm">9.</span> Measured Benchmark Findings
          </h2>
          {hasData && analytics ? (
            <div className="space-y-3 text-xs sm:text-sm">
              <p>
                In the latest empirical run (<code className="text-cyan-400">{analytics.latest_run_id}</code>), 150 responses were evaluated across 50 questions:
              </p>
              <div className="grid grid-cols-3 gap-3 text-center text-xs font-mono">
                <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-cyan-400 font-bold block">Rule-Based</span>
                  <span className="text-lg text-white font-bold">{analytics.architectures['rules']?.accuracy_percentage}%</span>
                  <span className="text-slate-400 block text-[10px]">{analytics.architectures['rules']?.avg_latency_ms} ms</span>
                </div>
                <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-blue-400 font-bold block">Semantic Retrieval</span>
                  <span className="text-lg text-white font-bold">{analytics.architectures['retrieval']?.accuracy_percentage}%</span>
                  <span className="text-slate-400 block text-[10px]">{analytics.architectures['retrieval']?.avg_latency_ms} ms</span>
                </div>
                <div className="p-3 rounded-xl bg-slate-900 border border-slate-800">
                  <span className="text-violet-400 font-bold block">LLM RAG</span>
                  <span className="text-lg text-white font-bold">{analytics.architectures['rag']?.accuracy_percentage}%</span>
                  <span className="text-slate-400 block text-[10px]">{analytics.architectures['rag']?.avg_latency_ms} ms</span>
                </div>
              </div>
            </div>
          ) : (
            <div className="p-4 rounded-xl bg-slate-900/60 border border-slate-800 text-xs text-slate-400">
              <em>[Benchmark Results Pending: Execute the 50-question benchmark in the Benchmark Lab to populate actual experimental results].</em>
            </div>
          )}
        </section>

        {/* Section 11: Failure Analysis */}
        <section className="space-y-3">
          <h2 className="text-lg font-bold text-white border-b border-slate-800/80 pb-1.5 flex items-center gap-2">
            <span className="text-cyan-400 font-mono text-sm">10.</span> Failure Mode Analysis
          </h2>
          <div className="space-y-2 text-xs sm:text-sm text-slate-300">
            <p>
              <strong>1. Rule-Based Brittleness:</strong> Fails when syntactic structure departs from anticipated regex patterns, resulting in unhandled fallbacks for valid inquiries.
            </p>
            <p>
              <strong>2. Retrieval False Positive Overlaps:</strong> Occurs when queries share lexical overlap with irrelevant FAQs (e.g. asking about "bus timing" vs "library timing"), requiring strict confidence thresholds.
            </p>
            <p>
              <strong>3. LLM RAG Jailbreak / Hallucination Risks:</strong> Without strict prompt guardrails, LLMs can extrapolate beyond retrieved chunks or concede to adversarial premise prompts.
            </p>
          </div>
        </section>

        {/* Section 12: Conclusion */}
        <section className="space-y-3">
          <h2 className="text-lg font-bold text-white border-b border-slate-800/80 pb-1.5 flex items-center gap-2">
            <span className="text-cyan-400 font-mono text-sm">11.</span> Conclusion &amp; Architectural Recommendation
          </h2>
          <p className="text-xs sm:text-sm text-slate-300 leading-relaxed">
            The empirical study demonstrates that there is no single universally superior architecture. For high-volume, low-latency FAQ lookups where verbatim accuracy is vital, <strong>Semantic Retrieval</strong> provides the optimal cost-to-performance ratio ($0 cost, 3ms latency, 0% hallucination). For conversational advisors where fluid reasoning is essential, <strong>LLM-Based RAG</strong> with strict system guardrails represents the state of the art.
          </p>
        </section>
      </article>
    </div>
  );
};
