import React, { useState } from 'react';
import { 
  GitFork, 
  Cpu, 
  Search, 
  Sparkles, 
  ArrowRight, 
  CheckCircle2, 
  Clock, 
  HelpCircle, 
  Play, 
  Layers,
  ChevronRight,
  ShieldCheck,
  Code2
} from 'lucide-react';
import { api } from '../services/api';
import { ChatResponse, RetrievalStrategy } from '../types';

export const ExplorerPage: React.FC = () => {
  const [activeTab, setActiveTab] = useState<'rules' | 'retrieval' | 'rag'>('rules');
  const [retrievalStrategy, setRetrievalStrategy] = useState<RetrievalStrategy>('tfidf');
  const [traceQuery, setTraceQuery] = useState('When does the admission process start and what is the last date to apply?');
  const [tracing, setTracing] = useState(false);
  const [traceResult, setTraceResult] = useState<ChatResponse | null>(null);

  const runTracer = async () => {
    if (!traceQuery.trim() || tracing) return;
    setTracing(true);
    try {
      let res: ChatResponse;
      if (activeTab === 'rules') {
        res = await api.chatRules(traceQuery);
      } else if (activeTab === 'retrieval') {
        res = await api.chatRetrieval(traceQuery, retrievalStrategy, 0.25, 3);
      } else {
        res = await api.chatRAG(traceQuery, retrievalStrategy, 0.20, 3);
      }
      setTraceResult(res);
    } catch (e) {
      console.error(e);
    } finally {
      setTracing(false);
    }
  };

  const stagesData = {
    rules: [
      {
        step: 1,
        title: "Text Normalisation",
        what: "Strips punctuation, converts query to lowercase, and trims extraneous whitespace.",
        why: "Ensures regex expressions and string matches are invariant to casing and minor punctuation differences.",
        example: `"When DOES Admission START???" → "when does admission start"`
      },
      {
        step: 2,
        title: "Keyword & Regex Matching",
        what: "Scans normalized query against pre-compiled regex patterns (admissions, fees, curfew, etc.).",
        why: "Identifies known intent tokens without any mathematical vector operations.",
        example: `r"(when\\s+do(es)?\\s+admission.*start)" matches "when does admission start"`
      },
      {
        step: 3,
        title: "Priority Rule Evaluation",
        what: "Executes IF-THEN checks in order of priority (Emergency > Jailbreaks > Fees > Dates > General > Fallback).",
        why: "Guarantees safety guardrails and critical emergency instructions always take precedence over broad queries.",
        example: `Priority 100 (Jailbreak defense) evaluated before Priority 70 (Admission dates)`
      },
      {
        step: 4,
        title: "Predefined Response Lookup",
        what: "Retrieves the exact deterministic text mapped to the matched rule ID.",
        why: "Prevents hallucination and guarantees 100% compliance with approved institutional policies.",
        example: `Rule "rule-admission-dates" returns official Demo University calendar dates verbatim.`
      },
      {
        step: 5,
        title: "Output Delivery",
        what: "Returns verified message, latency (&lt;1ms), and matched rule metadata.",
        why: "Instant response with absolute zero GPU/LLM cost.",
        example: `"Admissions open May 1st and close June 30th..."`
      }
    ],
    retrieval: [
      {
        step: 1,
        title: "Text Preprocessing & Tokenization",
        what: "Breaks user query into individual word tokens, filters punctuation, and handles case normalization.",
        why: "Transforms unstructured user query into standard lexical tokens ready for vectorization.",
        example: `"What is the annual hostel fee?" → ["annual", "hostel", "fee"]`
      },
      {
        step: 2,
        title: "Vectorisation (TF-IDF / Embeddings)",
        what: "Converts text tokens into mathematical vectors using Term Frequency-Inverse Document Frequency or dense embedding coordinates.",
        why: "Enables mathematical comparison between queries and indexed FAQ documents.",
        example: `TF-IDF vector of length |V|=240 with weights: hostel=2.45, fee=1.92`
      },
      {
        step: 3,
        title: "Cosine Similarity Calculation",
        what: "Computes dot product of normalized query vector against all 32 pre-indexed FAQ document vectors.",
        why: "Quantifies semantic orientation regardless of document length: cos(θ) = (A · B) / (||A|| ||B||).",
        example: `faq-hos-02 similarity = 0.841, faq-fee-01 similarity = 0.412, faq-adm-01 = 0.051`
      },
      {
        step: 4,
        title: "Ranking & Top-K Selection",
        what: "Sorts candidate documents by similarity score in descending order.",
        why: "Surfaces the most relevant FAQ entry to the top.",
        example: `Rank 1: faq-hos-02 ("What is the annual hostel and mess fee?")`
      },
      {
        step: 5,
        title: "Confidence Threshold Gating",
        what: "Compares top similarity score against configurable threshold (e.g. 0.25).",
        why: "Prevents returning irrelevant FAQ answers for out-of-scope queries (e.g., sports, cooking).",
        example: `Score 0.84 >= 0.25 → Approved! (If score < 0.25 → Return polite rejection)`
      },
      {
        step: 6,
        title: "FAQ Answer Retrieval",
        what: "Returns the verbatim verified answer stored in the chosen FAQ document.",
        why: "Delivers factual certainty with zero hallucination risk.",
        example: `"The annual hostel fee ranges from $1,200 to $2,200..."`
      }
    ],
    rag: [
      {
        step: 1,
        title: "Query Vectorisation & Retrieval",
        what: "Encodes user question and performs semantic vector search across the Demo University knowledge base.",
        why: "Finds the most pertinent factual grounding context before prompting the LLM.",
        example: `Query retrieved top 3 FAQs with similarity scores [0.89, 0.54, 0.32]`
      },
      {
        step: 2,
        title: "Context Selection & Filtering",
        what: "Filters retrieved documents by confidence threshold and packages them as clean context chunks with citations.",
        why: "Supplies the language model with exact ground-truth facts to prevent guessing or hallucination.",
        example: `Context: [FAQ ID: faq-fee-01 | Annual B.Tech fee is $4,000 / INR 3,20,000]`
      },
      {
        step: 3,
        title: "Grounded Prompt Construction",
        what: "Injects strict system guardrails, the retrieved context, and the user prompt into a structured payload.",
        why: "Instructs the LLM to answer ONLY from context, cite sources, and refuse adversarial/out-of-scope prompts.",
        example: `"CRITICAL RULE: Never invent fees. If context is missing, report information not available."`
      },
      {
        step: 4,
        title: "Gemini LLM Inference",
        what: "Sends prompt payload to Google Gemini 2.5/1.5 Flash API with temperature=0.0 for deterministic output.",
        why: "Leverages natural language understanding to synthesize a fluid, conversational response based on facts.",
        example: `Gemini generates response in 720ms using 214 prompt tokens and 64 candidate tokens.`
      },
      {
        step: 5,
        title: "Source Attribution & Output",
        what: "Returns grounded conversational answer alongside tracked latency, token usage, cost, and citation sources.",
        why: "Combines conversational elegance with academic verifiability.",
        example: `"The annual tuition fee for B.Tech programs is $4,000... (Source: Finance Office Fee Schedule)"`
      }
    ]
  };

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <span>Architecture Explorer</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Visual workflows, internal pipeline mechanisms, and interactive execution tracing across all three paradigms.
        </p>
      </div>

      {/* Tabs */}
      <div className="flex border-b border-slate-800 space-x-2">
        {[
          { id: 'rules', label: 'Architecture A: Rule-Based', icon: Cpu, color: 'text-cyan-400' },
          { id: 'retrieval', label: 'Architecture B: Semantic Retrieval', icon: Search, color: 'text-blue-400' },
          { id: 'rag', label: 'Architecture C: LLM-Based RAG', icon: Sparkles, color: 'text-violet-400' }
        ].map((tab) => (
          <button
            key={tab.id}
            onClick={() => {
              setActiveTab(tab.id as any);
              setTraceResult(null);
            }}
            className={`flex items-center gap-2 px-4 py-3 text-xs font-semibold border-b-2 transition-all cursor-pointer ${
              activeTab === tab.id
                ? 'border-cyan-400 text-white bg-slate-900/40'
                : 'border-transparent text-slate-400 hover:text-slate-200'
            }`}
          >
            <tab.icon className={`w-4 h-4 ${tab.color}`} />
            <span>{tab.label}</span>
          </button>
        ))}
      </div>

      {/* Strategy Switcher for Retrieval */}
      {activeTab === 'retrieval' && (
        <div className="glass-panel p-4 rounded-xl border border-slate-800 flex flex-col sm:flex-row items-center justify-between gap-4">
          <div className="text-xs">
            <span className="font-bold text-white">Compare Retrieval Vector Algorithms:</span>
            <p className="text-slate-400">Select which mathematical representation drives the retrieval stage.</p>
          </div>
          <div className="flex bg-slate-950 p-1 rounded-xl border border-slate-800 text-xs">
            {[
              { id: 'keyword', label: '1. Keyword (BM25)' },
              { id: 'tfidf', label: '2. TF-IDF Cosine' },
              { id: 'embedding', label: '3. Dense Embeddings' }
            ].map((strat) => (
              <button
                key={strat.id}
                onClick={() => setRetrievalStrategy(strat.id as any)}
                className={`px-3 py-1.5 rounded-lg font-medium transition-all cursor-pointer ${
                  retrievalStrategy === strat.id
                    ? 'bg-blue-600 text-white shadow-sm'
                    : 'text-slate-400 hover:text-white'
                }`}
              >
                {strat.label}
              </button>
            ))}
          </div>
        </div>
      )}

      {/* Workflow Diagram & Stage Cards */}
      <div className="space-y-4">
        <h3 className="text-sm font-bold text-slate-200 uppercase tracking-wider flex items-center gap-2">
          <span>Workflow Execution Pipeline</span>
          <span className="text-[10px] text-cyan-400 font-mono">({stagesData[activeTab].length} stages)</span>
        </h3>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
          {stagesData[activeTab].map((s) => (
            <div key={s.step} className="glass-panel p-5 rounded-2xl border border-slate-800/80 space-y-3 relative overflow-hidden group hover:border-cyan-800/60 transition-all">
              <div className="flex items-center justify-between">
                <span className="w-6 h-6 rounded-lg bg-cyan-950 text-cyan-400 border border-cyan-800/60 font-mono text-xs flex items-center justify-center font-bold">
                  {s.step}
                </span>
                <span className="text-[10px] text-slate-400 font-mono uppercase">Stage {s.step}</span>
              </div>

              <div>
                <h4 className="text-sm font-bold text-white group-hover:text-cyan-300 transition-colors">
                  {s.title}
                </h4>
                <p className="text-xs text-slate-300 mt-1 leading-relaxed">
                  {s.what}
                </p>
              </div>

              <div className="pt-2 border-t border-slate-800/60 space-y-1.5 text-[11px]">
                <div>
                  <span className="text-cyan-400/90 font-semibold">Why Needed: </span>
                  <span className="text-slate-400">{s.why}</span>
                </div>
                <div className="p-2 rounded-lg bg-slate-950/70 border border-slate-900 font-mono text-[10px] text-slate-300 break-words">
                  <span className="text-slate-400">Ex: </span>{s.example}
                </div>
              </div>
            </div>
          ))}
        </div>
      </div>

      {/* Interactive Query Tracer */}
      <div className="glass-panel rounded-2xl p-6 border border-slate-800 space-y-6">
        <div>
          <h3 className="text-base font-bold text-white flex items-center gap-2">
            <Code2 className="w-5 h-5 text-cyan-400" />
            <span>Interactive Query Tracer</span>
          </h3>
          <p className="text-xs text-slate-400 mt-1">
            Execute a sample query through {activeTab.toUpperCase()} and inspect the exact runtime stage telemetry.
          </p>
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={traceQuery}
            onChange={(e) => setTraceQuery(e.target.value)}
            placeholder="Enter question to trace..."
            className="flex-1 bg-slate-950 border border-slate-800 rounded-xl px-4 py-2.5 text-xs text-white focus:outline-none focus:border-cyan-500"
          />
          <button
            onClick={runTracer}
            disabled={tracing || !traceQuery.trim()}
            className="px-4 py-2.5 rounded-xl bg-cyan-500 hover:bg-cyan-400 disabled:opacity-50 text-slate-950 font-bold text-xs flex items-center gap-2 cursor-pointer transition-all"
          >
            {tracing ? <div className="w-3.5 h-3.5 border-2 border-slate-950 border-t-transparent rounded-full animate-spin" /> : <Play className="w-3.5 h-3.5" />}
            <span>Trace Execution</span>
          </button>
        </div>

        {/* Trace Output */}
        {traceResult && (
          <div className="space-y-4 pt-2">
            <div className="p-4 rounded-xl bg-slate-950 border border-slate-800 text-xs space-y-3">
              <div className="flex items-center justify-between border-b border-slate-800/80 pb-2">
                <span className="font-bold text-white">Execution Result Summary</span>
                <span className="font-mono text-cyan-400">Latency: {traceResult.latency_ms} ms</span>
              </div>
              <p className="text-slate-200 whitespace-pre-line leading-relaxed">{traceResult.message}</p>
            </div>

            {/* Stages Telemetry Steps */}
            {traceResult.trace_steps && traceResult.trace_steps.length > 0 && (
              <div className="space-y-2">
                <h4 className="text-xs font-semibold text-slate-300 uppercase tracking-wider">
                  Internal Processing Telemetry
                </h4>
                <div className="space-y-2">
                  {traceResult.trace_steps.map((step, idx) => (
                    <div key={idx} className="p-3 rounded-xl bg-slate-900/60 border border-slate-800 text-xs space-y-1">
                      <div className="flex items-center justify-between">
                        <span className="font-bold text-cyan-300">
                          Stage {idx + 1}: {step.stage}
                        </span>
                        <span className="text-[10px] text-slate-400 font-mono">COMPLETE</span>
                      </div>
                      <p className="text-slate-300 text-[11px]">{step.description}</p>
                      {step.data && (
                        <pre className="p-2 rounded bg-slate-950 text-[10px] font-mono text-slate-300 overflow-x-auto">
                          {JSON.stringify(step.data, null, 2)}
                        </pre>
                      )}
                    </div>
                  ))}
                </div>
              </div>
            )}
          </div>
        )}
      </div>
    </div>
  );
};
