import React, { useEffect, useState } from 'react';
import { 
  Cpu, 
  Search, 
  Sparkles, 
  CheckCircle2, 
  Zap, 
  DollarSign, 
  ShieldAlert, 
  FlaskConical, 
  ArrowRight,
  BarChart3,
  Layers,
  Database
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend, Cell 
} from 'recharts';
import { api } from '../services/api';
import { AnalyticsSummaryResponse } from '../types';

interface OverviewPageProps {
  onNavigateToBenchmark: () => void;
  onNavigateToPlayground: () => void;
}

export const OverviewPage: React.FC<OverviewPageProps> = ({ 
  onNavigateToBenchmark, 
  onNavigateToPlayground 
}) => {
  const [analytics, setAnalytics] = useState<AnalyticsSummaryResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadSummary();
  }, []);

  const loadSummary = async () => {
    try {
      setLoading(true);
      const data = await api.fetchAnalyticsSummary();
      setAnalytics(data);
    } catch (err) {
      console.error("Failed to load analytics summary:", err);
    } finally {
      setLoading(false);
    }
  };

  const hasData = analytics?.has_benchmark_data && Object.keys(analytics.architectures).length > 0;

  // Derive summary highlights
  let bestAccuracy = { arch: 'N/A', val: 0 };
  let fastest = { arch: 'N/A', val: 0 };
  let lowestCost = { arch: 'N/A', val: '$0.00' };
  let lowestHallucination = { arch: 'N/A', val: 0 };

  if (hasData && analytics) {
    const archs = Object.values(analytics.architectures);
    if (archs.length > 0) {
      const sortedAcc = [...archs].sort((a, b) => b.accuracy_percentage - a.accuracy_percentage);
      bestAccuracy = { arch: sortedAcc[0].architecture.toUpperCase(), val: sortedAcc[0].accuracy_percentage };

      const sortedLat = [...archs].sort((a, b) => a.avg_latency_ms - b.avg_latency_ms);
      fastest = { arch: sortedLat[0].architecture.toUpperCase(), val: sortedLat[0].avg_latency_ms };

      lowestCost = { arch: 'RULES / RETRIEVAL', val: '$0.00' };

      const sortedHal = [...archs].sort((a, b) => a.hallucination_rate_percentage - b.hallucination_rate_percentage);
      lowestHallucination = { arch: sortedHal[0].architecture.toUpperCase(), val: sortedHal[0].hallucination_rate_percentage };
    }
  }

  // Chart data preparation
  const chartData = hasData && analytics ? [
    {
      name: 'Rule-Based',
      accuracy: analytics.architectures['rules']?.accuracy_percentage || 0,
      latency: analytics.architectures['rules']?.avg_latency_ms || 0,
      hallucination: analytics.architectures['rules']?.hallucination_rate_percentage || 0,
      fill: '#06B6D4'
    },
    {
      name: 'Semantic Retrieval',
      accuracy: analytics.architectures['retrieval']?.accuracy_percentage || 0,
      latency: analytics.architectures['retrieval']?.avg_latency_ms || 0,
      hallucination: analytics.architectures['retrieval']?.hallucination_rate_percentage || 0,
      fill: '#3B82F6'
    },
    {
      name: 'LLM RAG',
      accuracy: analytics.architectures['rag']?.accuracy_percentage || 0,
      latency: analytics.architectures['rag']?.avg_latency_ms || 0,
      hallucination: analytics.architectures['rag']?.hallucination_rate_percentage || 0,
      fill: '#8B5CF6'
    }
  ] : [];

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Hero Header */}
      <div className="relative rounded-2xl bg-gradient-to-r from-slate-900 via-slate-900/90 to-slate-950 border border-slate-800 p-8 overflow-hidden shadow-2xl">
        <div className="absolute -right-20 -top-20 w-80 h-80 bg-cyan-500/10 rounded-full blur-3xl pointer-events-none" />
        <div className="absolute right-40 -bottom-20 w-80 h-80 bg-violet-500/10 rounded-full blur-3xl pointer-events-none" />

        <div className="relative z-10 max-w-3xl space-y-4">
          <div className="inline-flex items-center gap-2 px-3 py-1 rounded-full bg-cyan-950/60 border border-cyan-800/60 text-cyan-300 text-xs font-medium">
            <FlaskConical className="w-3.5 h-3.5 text-cyan-400" />
            Artificial Intelligence Foundations Laboratory Study
          </div>

          <h1 className="text-3xl sm:text-4xl font-extrabold tracking-tight text-white">
            ARCHITECTURE LAB
          </h1>
          <p className="text-lg text-cyan-400/90 font-medium tracking-tight">
            Understanding Intelligence Through Comparison.
          </p>
          <p className="text-slate-300 text-sm sm:text-base leading-relaxed">
            A comprehensive, empirical evaluation comparing three fundamentally different chatbot architectures—<strong>Rule-Based</strong>, <strong>Semantic Retrieval</strong>, and <strong>LLM-Based RAG</strong>—answering identical questions over the same institutional knowledge base.
          </p>

          <div className="flex flex-wrap gap-3 pt-2">
            <button
              onClick={onNavigateToPlayground}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-semibold text-xs shadow-lg shadow-cyan-950/50 transition-all cursor-pointer"
            >
              <span>Test Chat Playground</span>
              <ArrowRight className="w-4 h-4" />
            </button>
            <button
              onClick={onNavigateToBenchmark}
              className="inline-flex items-center gap-2 px-4 py-2.5 rounded-xl bg-slate-800/80 hover:bg-slate-800 text-white font-medium text-xs border border-slate-700/80 transition-all cursor-pointer"
            >
              <FlaskConical className="w-4 h-4 text-cyan-400" />
              <span>Open Benchmark Lab (50 Tests)</span>
            </button>
          </div>
        </div>
      </div>

      {/* 3 Architecture Pillar Cards */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-5">
        {/* Arch A: Rule-Based */}
        <div className="glass-panel glass-panel-hover rounded-2xl p-6 relative flex flex-col justify-between border-t-2 border-t-cyan-500">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="w-10 h-10 rounded-xl bg-cyan-950/80 border border-cyan-800/60 flex items-center justify-center text-cyan-400">
                <Cpu className="w-5 h-5" />
              </div>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-cyan-950/90 text-cyan-400 border border-cyan-800/60 font-semibold">
                ARCHITECTURE A
              </span>
            </div>
            <h3 className="text-lg font-bold text-white mb-1">Rule-Based Chatbot</h3>
            <p className="text-xs text-slate-400 mb-4 leading-relaxed">
              Deterministic IF-THEN rules, priority regex patterns, and text normalisation. Returns fixed pre-scripted responses with zero neural inference.
            </p>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-300">
                <span className="text-slate-400">Processing Latency:</span>
                <span className="font-mono text-cyan-300 font-semibold">&lt; 1 ms</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-300">
                <span className="text-slate-400">Token / API Cost:</span>
                <span className="font-mono text-emerald-400 font-semibold">$0.00</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-300">
                <span className="text-slate-400">Paraphrase Handling:</span>
                <span className="text-rose-400 font-medium">Brittle / Regex only</span>
              </div>
            </div>
          </div>
        </div>

        {/* Arch B: Semantic Retrieval */}
        <div className="glass-panel glass-panel-hover rounded-2xl p-6 relative flex flex-col justify-between border-t-2 border-t-blue-500">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="w-10 h-10 rounded-xl bg-blue-950/80 border border-blue-800/60 flex items-center justify-center text-blue-400">
                <Search className="w-5 h-5" />
              </div>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-blue-950/90 text-blue-400 border border-blue-800/60 font-semibold">
                ARCHITECTURE B
              </span>
            </div>
            <h3 className="text-lg font-bold text-white mb-1">Semantic Retrieval</h3>
            <p className="text-xs text-slate-400 mb-4 leading-relaxed">
              Statistical vector similarity matching queries against indexed FAQs using TF-IDF, Cosine Similarity, and dense semantic embeddings.
            </p>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-300">
                <span className="text-slate-400">Processing Latency:</span>
                <span className="font-mono text-blue-300 font-semibold">2 - 8 ms</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-300">
                <span className="text-slate-400">Token / API Cost:</span>
                <span className="font-mono text-emerald-400 font-semibold">$0.00</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-300">
                <span className="text-slate-400">Hallucination Risk:</span>
                <span className="text-emerald-400 font-semibold">Zero (Verbatim)</span>
              </div>
            </div>
          </div>
        </div>

        {/* Arch C: LLM-Based RAG */}
        <div className="glass-panel glass-panel-hover rounded-2xl p-6 relative flex flex-col justify-between border-t-2 border-t-violet-500">
          <div>
            <div className="flex items-center justify-between mb-4">
              <div className="w-10 h-10 rounded-xl bg-violet-950/80 border border-violet-800/60 flex items-center justify-center text-violet-400">
                <Sparkles className="w-5 h-5" />
              </div>
              <span className="text-[11px] font-mono px-2 py-0.5 rounded bg-violet-950/90 text-violet-400 border border-violet-800/60 font-semibold">
                ARCHITECTURE C
              </span>
            </div>
            <h3 className="text-lg font-bold text-white mb-1">LLM-Based RAG</h3>
            <p className="text-xs text-slate-400 mb-4 leading-relaxed">
              Retrieval-Augmented Generation pairing semantic knowledge context with Google Gemini Flash to synthesize fluid, grounded conversational responses.
            </p>
            <div className="space-y-2 text-xs">
              <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-300">
                <span className="text-slate-400">Processing Latency:</span>
                <span className="font-mono text-violet-300 font-semibold">600 - 1500 ms</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-300">
                <span className="text-slate-400">Token Cost:</span>
                <span className="font-mono text-violet-300 font-semibold">Variable (API)</span>
              </div>
              <div className="flex justify-between py-1 border-b border-slate-800/80 text-slate-300">
                <span className="text-slate-400">Paraphrase Handling:</span>
                <span className="text-emerald-400 font-semibold">Superior / Natural</span>
              </div>
            </div>
          </div>
        </div>
      </div>

      {/* Summary KPI Cards */}
      <div className="grid grid-cols-2 sm:grid-cols-4 gap-4">
        <div className="glass-panel rounded-xl p-4 border border-slate-800">
          <div className="flex items-center gap-2 text-slate-400 text-xs mb-1">
            <CheckCircle2 className="w-4 h-4 text-emerald-400" />
            <span>Highest Accuracy</span>
          </div>
          <div className="text-xl font-bold text-white">{hasData ? `${bestAccuracy.val}%` : 'Pending'}</div>
          <div className="text-[11px] text-slate-400">{hasData ? bestAccuracy.arch : 'Run benchmark'}</div>
        </div>

        <div className="glass-panel rounded-xl p-4 border border-slate-800">
          <div className="flex items-center gap-2 text-slate-400 text-xs mb-1">
            <Zap className="w-4 h-4 text-cyan-400" />
            <span>Fastest Latency</span>
          </div>
          <div className="text-xl font-bold text-white">{hasData ? `${fastest.val} ms` : 'Pending'}</div>
          <div className="text-[11px] text-slate-400">{hasData ? fastest.arch : 'Run benchmark'}</div>
        </div>

        <div className="glass-panel rounded-xl p-4 border border-slate-800">
          <div className="flex items-center gap-2 text-slate-400 text-xs mb-1">
            <DollarSign className="w-4 h-4 text-emerald-400" />
            <span>Lowest Cost</span>
          </div>
          <div className="text-xl font-bold text-white">{hasData ? lowestCost.val : '$0.00'}</div>
          <div className="text-[11px] text-slate-400">Rules &amp; Retrieval</div>
        </div>

        <div className="glass-panel rounded-xl p-4 border border-slate-800">
          <div className="flex items-center gap-2 text-slate-400 text-xs mb-1">
            <ShieldAlert className="w-4 h-4 text-rose-400" />
            <span>Min Hallucination</span>
          </div>
          <div className="text-xl font-bold text-white">{hasData ? `${lowestHallucination.val}%` : 'Pending'}</div>
          <div className="text-[11px] text-slate-400">{hasData ? lowestHallucination.arch : 'Run benchmark'}</div>
        </div>
      </div>

      {/* Experimental Charts / Empty State */}
      <div className="glass-panel rounded-2xl p-6 border border-slate-800">
        <div className="flex items-center justify-between mb-6">
          <div>
            <h3 className="text-base font-bold text-white">Comparative Benchmark Metrics</h3>
            <p className="text-xs text-slate-400">
              Evaluated across 50 questions (20 Direct, 15 Paraphrased, 10 Out-of-Scope, 5 Adversarial)
            </p>
          </div>
          <div className="text-xs font-mono text-slate-400 bg-slate-900 px-3 py-1.5 rounded-lg border border-slate-800">
            Total Responses: <span className="text-cyan-400 font-semibold">{hasData ? '150 evaluated' : '0 recorded'}</span>
          </div>
        </div>

        {hasData ? (
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Accuracy Chart */}
            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
              <h4 className="text-xs font-semibold text-slate-300 mb-3 flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-cyan-400" />
                <span>Accuracy Percentage (%)</span>
              </h4>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" vertical={false} />
                    <XAxis dataKey="name" stroke="#64748B" fontSize={11} tickLine={false} />
                    <YAxis stroke="#64748B" fontSize={11} domain={[0, 100]} tickLine={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
                      formatter={(val: any) => [`${val}%`, 'Accuracy']}
                    />
                    <Bar dataKey="accuracy" radius={[6, 6, 0, 0]}>
                      {chartData.map((entry, index) => (
                        <Cell key={`cell-${index}`} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Latency Chart */}
            <div className="bg-slate-950/60 p-4 rounded-xl border border-slate-800/80">
              <h4 className="text-xs font-semibold text-slate-300 mb-3 flex items-center gap-2">
                <Zap className="w-4 h-4 text-cyan-400" />
                <span>Average Response Latency (ms)</span>
              </h4>
              <div className="h-64">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={chartData} margin={{ top: 10, right: 10, left: -20, bottom: 0 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" vertical={false} />
                    <XAxis dataKey="name" stroke="#64748B" fontSize={11} tickLine={false} />
                    <YAxis stroke="#64748B" fontSize={11} tickLine={false} />
                    <Tooltip 
                      contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px', fontSize: '12px' }}
                      formatter={(val: any) => [`${val} ms`, 'Latency']}
                    />
                    <Bar dataKey="latency" radius={[6, 6, 0, 0]}>
                      {chartData.map((entry, index) => (
                        <Cell key={`cell-lat-${index}`} fill={entry.fill} />
                      ))}
                    </Bar>
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>
        ) : (
          /* Honest Empty State (No Fabricated Data) */
          <div className="py-12 px-4 text-center rounded-xl bg-slate-950/40 border border-dashed border-slate-800 flex flex-col items-center justify-center space-y-4">
            <div className="w-12 h-12 rounded-2xl bg-cyan-950/40 border border-cyan-800/50 flex items-center justify-center text-cyan-400">
              <FlaskConical className="w-6 h-6" />
            </div>
            <div className="max-w-md space-y-1">
              <h4 className="text-base font-bold text-white">No Benchmark Results Recorded Yet</h4>
              <p className="text-xs text-slate-400 leading-relaxed">
                To maintain academic rigor, this platform never fabricates experimental charts. Execute the 50-question benchmark in the Benchmark Lab to populate real experimental data across all three architectures.
              </p>
            </div>
            <button
              onClick={onNavigateToBenchmark}
              className="inline-flex items-center gap-2 px-4 py-2 rounded-xl bg-cyan-500 hover:bg-cyan-400 text-slate-950 font-semibold text-xs shadow-md transition-all cursor-pointer"
            >
              <FlaskConical className="w-3.5 h-3.5" />
              <span>Launch Benchmark Lab</span>
            </button>
          </div>
        )}
      </div>
    </div>
  );
};
