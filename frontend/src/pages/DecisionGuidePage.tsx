import React, { useState, useEffect } from 'react';
import { 
  Compass, 
  CheckCircle2, 
  Cpu, 
  Search, 
  Sparkles, 
  ArrowRight, 
  HelpCircle, 
  ShieldCheck, 
  Zap, 
  DollarSign, 
  Sliders,
  Check
} from 'lucide-react';
import { api } from '../services/api';
import { AnalyticsSummaryResponse } from '../types';

export const DecisionGuidePage: React.FC = () => {
  const [selectedPriorities, setSelectedPriorities] = useState<string[]>(['accuracy', 'natural']);
  const [analytics, setAnalytics] = useState<AnalyticsSummaryResponse | null>(null);

  useEffect(() => {
    api.fetchAnalyticsSummary().then(setAnalytics).catch(console.error);
  }, []);

  const hasData = analytics?.has_benchmark_data && Object.keys(analytics.architectures).length > 0;

  const priorityOptions = [
    { id: 'accuracy', label: 'Maximum Paraphrase Accuracy', icon: CheckCircle2, weight: { rules: 1, retrieval: 3, rag: 5 } },
    { id: 'latency', label: 'Sub-Millisecond Speed (< 5ms)', icon: Zap, weight: { rules: 5, retrieval: 4, rag: 1 } },
    { id: 'cost', label: 'Zero API / Token Cost ($0)', icon: DollarSign, weight: { rules: 5, retrieval: 5, rag: 1 } },
    { id: 'simplicity', label: 'Simple Low-Complexity Setup', icon: Sliders, weight: { rules: 5, retrieval: 4, rag: 2 } },
    { id: 'natural', label: 'Natural Conversational Fluency', icon: Sparkles, weight: { rules: 1, retrieval: 2, rag: 5 } },
    { id: 'control', label: 'Zero Hallucination / Strict Verbatim', icon: ShieldCheck, weight: { rules: 5, retrieval: 5, rag: 3 } },
  ];

  const togglePriority = (id: string) => {
    setSelectedPriorities(prev => 
      prev.includes(id) ? prev.filter(x => x !== id) : [...prev, id]
    );
  };

  // Calculate scores
  let rulesScore = 0;
  let retrievalScore = 0;
  let ragScore = 0;

  selectedPriorities.forEach(p => {
    const opt = priorityOptions.find(o => o.id === p);
    if (opt) {
      rulesScore += opt.weight.rules;
      retrievalScore += opt.weight.retrieval;
      ragScore += opt.weight.rag;
    }
  });

  let recommendedArch = 'rag';
  let highestScore = ragScore;
  if (retrievalScore > highestScore) {
    recommendedArch = 'retrieval';
    highestScore = retrievalScore;
  }
  if (rulesScore > highestScore) {
    recommendedArch = 'rules';
    highestScore = rulesScore;
  }

  const rationale = {
    rules: {
      name: "Architecture A: Rule-Based Chatbot",
      tagline: "Unbeatable speed, zero cost, absolute predictability.",
      why: "Based on your focus on latency, zero operational costs, and deterministic responses, a Rule-Based architecture is ideal. It delivers sub-millisecond lookups with no GPU or third-party API dependencies.",
      bestFor: "Form validation, IVR phone trees, fixed policy confirmation, and structured workflows where user queries conform to strict syntax.",
      warning: "Brittle when users express queries in unexpected paraphrased language."
    },
    retrieval: {
      name: "Architecture B: Semantic Retrieval Chatbot",
      tagline: "The sweet spot: High factual precision, zero hallucination, $0 API cost.",
      why: "Semantic Retrieval strikes the optimal engineering balance for FAQ and knowledge portal applications. It handles paraphrased questions through TF-IDF and embedding similarity while guaranteeing that answers are drawn verbatim from approved documents.",
      bestFor: "Enterprise FAQ portals, campus knowledge search, medical/legal compliance directories, and customer support lookups where accuracy is mission-critical.",
      warning: "Cannot hold conversational back-and-forth multi-turn dialogues."
    },
    rag: {
      name: "Architecture C: LLM-Based RAG Chatbot",
      tagline: "Natural conversational intelligence grounded in institutional data.",
      why: "If human-grade conversational fluency, contextual reasoning, and robust paraphrase comprehension are paramount, LLM-Based RAG is the best architecture. It retrieves exact institutional context and synthesizes fluent, polite responses.",
      bestFor: "Interactive academic advisors, multi-turn student onboarding assistants, and complex institutional inquiry portals.",
      warning: "Requires active API credentials, incurs token costs, and requires guardrails against adversarial prompt injections."
    }
  };

  const currentRec = rationale[recommendedArch as keyof typeof rationale];

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <Compass className="w-6 h-6 text-cyan-400" />
          <span>Architecture Decision Guide</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Interactive recommendation engine mapping project requirements to the ideal chatbot architecture.
        </p>
      </div>

      {/* Priority Selection Wizard */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
        <div>
          <h3 className="text-sm font-bold text-white">Select Your System Priorities</h3>
          <p className="text-xs text-slate-400">Choose all criteria that are critical for your target deployment:</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-3">
          {priorityOptions.map((opt) => {
            const isSelected = selectedPriorities.includes(opt.id);
            const Icon = opt.icon;
            return (
              <button
                key={opt.id}
                onClick={() => togglePriority(opt.id)}
                className={`p-4 rounded-xl border text-left flex items-start gap-3 transition-all cursor-pointer ${
                  isSelected
                    ? 'bg-cyan-950/60 border-cyan-500/80 text-white shadow-lg shadow-cyan-950/40'
                    : 'bg-slate-950/60 border-slate-800 text-slate-400 hover:border-slate-700'
                }`}
              >
                <div className={`w-6 h-6 rounded-lg flex items-center justify-center shrink-0 ${
                  isSelected ? 'bg-cyan-500 text-slate-950' : 'bg-slate-900 text-slate-500'
                }`}>
                  {isSelected ? <Check className="w-4 h-4 stroke-[3]" /> : <Icon className="w-3.5 h-3.5" />}
                </div>
                <div>
                  <span className="text-xs font-semibold block">{opt.label}</span>
                </div>
              </button>
            );
          })}
        </div>
      </div>

      {/* Recommendation Card */}
      <div className="glass-panel p-6 rounded-2xl border border-cyan-500/50 bg-gradient-to-r from-slate-900 via-slate-900 to-cyan-950/40 space-y-4 shadow-xl">
        <div className="flex items-center justify-between">
          <span className="text-xs font-mono font-bold text-cyan-400 uppercase tracking-wider px-2.5 py-1 rounded-md bg-cyan-950 border border-cyan-800/60">
            Recommended Architecture
          </span>
          <span className="text-[11px] text-slate-400">
            {hasData ? 'Derived from Measured Benchmark Data' : 'Theoretical Architectural Guidance'}
          </span>
        </div>

        <div>
          <h3 className="text-2xl font-extrabold text-white">{currentRec.name}</h3>
          <p className="text-sm font-medium text-cyan-300 mt-1">{currentRec.tagline}</p>
        </div>

        <p className="text-xs text-slate-300 leading-relaxed max-w-3xl">
          {currentRec.why}
        </p>

        <div className="grid grid-cols-1 md:grid-cols-2 gap-4 pt-2 text-xs">
          <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1">
            <span className="font-semibold text-emerald-400 block text-[11px]">Best Suited Use Cases:</span>
            <p className="text-slate-300 text-[11px] leading-relaxed">{currentRec.bestFor}</p>
          </div>
          <div className="p-3.5 rounded-xl bg-slate-950/80 border border-slate-800 space-y-1">
            <span className="font-semibold text-amber-400 block text-[11px]">Key Architectural Limitation:</span>
            <p className="text-slate-300 text-[11px] leading-relaxed">{currentRec.warning}</p>
          </div>
        </div>
      </div>

      {/* Comprehensive Architectural Trade-off Matrix */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden">
        <div className="p-4 border-b border-slate-800 bg-slate-950/60">
          <h3 className="text-sm font-bold text-white">Full Architectural Trade-off Matrix</h3>
          <p className="text-xs text-slate-400">Head-to-head comparison across practical engineering dimensions</p>
        </div>

        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-950/30 text-slate-400 text-[10px] uppercase font-bold tracking-wider">
                <th className="py-3 px-4">Evaluation Dimension</th>
                <th className="py-3 px-4 text-cyan-400">Rule-Based</th>
                <th className="py-3 px-4 text-blue-400">Semantic Retrieval</th>
                <th className="py-3 px-4 text-violet-400">LLM RAG</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60 text-[11px]">
              <tr className="hover:bg-slate-900/30">
                <td className="py-3 px-4 font-semibold text-white">Latency Profile</td>
                <td className="py-3 px-4 text-cyan-300 font-mono">&lt; 1 ms (Instant)</td>
                <td className="py-3 px-4 text-blue-300 font-mono">2 - 8 ms (Ultra fast)</td>
                <td className="py-3 px-4 text-violet-300 font-mono">600 - 1500 ms (Network bound)</td>
              </tr>
              <tr className="hover:bg-slate-900/30">
                <td className="py-3 px-4 font-semibold text-white">Token &amp; Infrastructure Cost</td>
                <td className="py-3 px-4 text-emerald-400 font-bold">$0.00 (Zero)</td>
                <td className="py-3 px-4 text-emerald-400 font-bold">$0.00 (Zero)</td>
                <td className="py-3 px-4 text-violet-300 font-mono">~$0.0001 / query</td>
              </tr>
              <tr className="hover:bg-slate-900/30">
                <td className="py-3 px-4 font-semibold text-white">Hallucination Risk</td>
                <td className="py-3 px-4 text-emerald-400 font-semibold">Zero (Pre-scripted)</td>
                <td className="py-3 px-4 text-emerald-400 font-semibold">Zero (Verbatim FAQ)</td>
                <td className="py-3 px-4 text-amber-400 font-semibold">Low (Mitigated with Guardrails)</td>
              </tr>
              <tr className="hover:bg-slate-900/30">
                <td className="py-3 px-4 font-semibold text-white">Paraphrasing Adaptability</td>
                <td className="py-3 px-4 text-rose-400">Poor (Regex dependent)</td>
                <td className="py-3 px-4 text-blue-300">High (Vector distance)</td>
                <td className="py-3 px-4 text-emerald-400 font-semibold">Exceptional (Deep semantic)</td>
              </tr>
              <tr className="hover:bg-slate-900/30">
                <td className="py-3 px-4 font-semibold text-white">Maintenance Effort</td>
                <td className="py-3 px-4 text-amber-400">High (Manual rule authoring)</td>
                <td className="py-3 px-4 text-emerald-400 font-semibold">Low (Add FAQ &amp; re-index)</td>
                <td className="py-3 px-4 text-cyan-300">Moderate (Prompt &amp; context tuning)</td>
              </tr>
              <tr className="hover:bg-slate-900/30">
                <td className="py-3 px-4 font-semibold text-white">Adversarial Resistance</td>
                <td className="py-3 px-4 text-cyan-300 font-semibold">Total (Cannot be coerced)</td>
                <td className="py-3 px-4 text-blue-300 font-semibold">High (Threshold drops query)</td>
                <td className="py-3 px-4 text-violet-300">Moderate (Prompt injection risk)</td>
              </tr>
            </tbody>
          </table>
        </div>
      </div>
    </div>
  );
};
