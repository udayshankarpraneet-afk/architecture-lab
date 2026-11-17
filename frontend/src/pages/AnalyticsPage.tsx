import React, { useEffect, useState } from 'react';
import { 
  BarChart3, 
  Cpu, 
  Search, 
  Sparkles, 
  CheckCircle2, 
  Clock, 
  DollarSign, 
  ShieldAlert, 
  Info, 
  TrendingUp, 
  Layers, 
  HelpCircle,
  FlaskConical
} from 'lucide-react';
import { 
  BarChart, Bar, XAxis, YAxis, Tooltip, ResponsiveContainer, CartesianGrid, Legend, Cell, Radar, RadarChart, PolarGrid, PolarAngleAxis, PolarRadiusAxis 
} from 'recharts';
import { api } from '../services/api';
import { AnalyticsSummaryResponse } from '../types';

export const AnalyticsPage: React.FC = () => {
  const [analytics, setAnalytics] = useState<AnalyticsSummaryResponse | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    loadAnalytics();
  }, []);

  const loadAnalytics = async () => {
    try {
      setLoading(true);
      const data = await api.fetchAnalyticsSummary();
      setAnalytics(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  const hasData = analytics?.has_benchmark_data && Object.keys(analytics.architectures).length > 0;

  // Chart datasets
  const accuracyData = hasData && analytics ? [
    {
      name: 'Rule-Based',
      accuracy: analytics.architectures['rules']?.accuracy_percentage || 0,
      direct: analytics.architectures['rules']?.direct_accuracy || 0,
      paraphrased: analytics.architectures['rules']?.paraphrased_accuracy || 0,
      oos_rejection: analytics.architectures['rules']?.out_of_scope_rejection_rate || 0,
      adversarial: analytics.architectures['rules']?.adversarial_resistance_rate || 0,
      color: '#06B6D4'
    },
    {
      name: 'Semantic Retrieval',
      accuracy: analytics.architectures['retrieval']?.accuracy_percentage || 0,
      direct: analytics.architectures['retrieval']?.direct_accuracy || 0,
      paraphrased: analytics.architectures['retrieval']?.paraphrased_accuracy || 0,
      oos_rejection: analytics.architectures['retrieval']?.out_of_scope_rejection_rate || 0,
      adversarial: analytics.architectures['retrieval']?.adversarial_resistance_rate || 0,
      color: '#3B82F6'
    },
    {
      name: 'LLM RAG',
      accuracy: analytics.architectures['rag']?.accuracy_percentage || 0,
      direct: analytics.architectures['rag']?.direct_accuracy || 0,
      paraphrased: analytics.architectures['rag']?.paraphrased_accuracy || 0,
      oos_rejection: analytics.architectures['rag']?.out_of_scope_rejection_rate || 0,
      adversarial: analytics.architectures['rag']?.adversarial_resistance_rate || 0,
      color: '#8B5CF6'
    }
  ] : [];

  const latencyData = hasData && analytics ? [
    {
      name: 'Rule-Based',
      average: analytics.architectures['rules']?.avg_latency_ms || 0,
      median: analytics.architectures['rules']?.median_latency_ms || 0,
      color: '#06B6D4'
    },
    {
      name: 'Semantic Retrieval',
      average: analytics.architectures['retrieval']?.avg_latency_ms || 0,
      median: analytics.architectures['retrieval']?.median_latency_ms || 0,
      color: '#3B82F6'
    },
    {
      name: 'LLM RAG',
      average: analytics.architectures['rag']?.avg_latency_ms || 0,
      median: analytics.architectures['rag']?.median_latency_ms || 0,
      color: '#8B5CF6'
    }
  ] : [];

  // Multi-Metric Radar Chart Data
  const radarData = hasData && analytics ? [
    {
      subject: 'Accuracy %',
      Rules: analytics.architectures['rules']?.accuracy_percentage || 0,
      Retrieval: analytics.architectures['retrieval']?.accuracy_percentage || 0,
      RAG: analytics.architectures['rag']?.accuracy_percentage || 0,
    },
    {
      subject: 'Paraphrase Handling',
      Rules: analytics.architectures['rules']?.paraphrased_accuracy || 0,
      Retrieval: analytics.architectures['retrieval']?.paraphrased_accuracy || 0,
      RAG: analytics.architectures['rag']?.paraphrased_accuracy || 0,
    },
    {
      subject: 'Refusal Fidelity',
      Rules: analytics.architectures['rules']?.out_of_scope_rejection_rate || 0,
      Retrieval: analytics.architectures['retrieval']?.out_of_scope_rejection_rate || 0,
      RAG: analytics.architectures['rag']?.out_of_scope_rejection_rate || 0,
    },
    {
      subject: 'Adversarial Safety',
      Rules: analytics.architectures['rules']?.adversarial_resistance_rate || 0,
      Retrieval: analytics.architectures['retrieval']?.adversarial_resistance_rate || 0,
      RAG: analytics.architectures['rag']?.adversarial_resistance_rate || 0,
    },
    {
      subject: 'Zero Hallucination',
      Rules: 100 - (analytics.architectures['rules']?.hallucination_rate_percentage || 0),
      Retrieval: 100 - (analytics.architectures['retrieval']?.hallucination_rate_percentage || 0),
      RAG: 100 - (analytics.architectures['rag']?.hallucination_rate_percentage || 0),
    }
  ] : [];

  return (
    <div className="space-y-8 max-w-7xl mx-auto pb-12">
      {/* Header */}
      <div>
        <h2 className="text-2xl font-bold text-white flex items-center gap-2">
          <BarChart3 className="w-6 h-6 text-cyan-400" />
          <span>Analytics &amp; Comparative Dashboard</span>
        </h2>
        <p className="text-xs text-slate-400 mt-1">
          Quantitative multi-dimensional analysis derived deterministically from SQLite benchmark runs.
        </p>
      </div>

      {!hasData ? (
        <div className="glass-panel p-12 rounded-2xl border border-slate-800 text-center space-y-4">
          <FlaskConical className="w-12 h-12 text-cyan-400 mx-auto" />
          <h3 className="text-lg font-bold text-white">No Benchmark Data Available</h3>
          <p className="text-xs text-slate-400 max-w-md mx-auto">
            Please run the 50-question benchmark suite in the Benchmark Lab. The analytical engine will compute all 11 comparative metrics across the 150 responses.
          </p>
        </div>
      ) : (
        <>
          {/* 11 Primary Metrics Comparative Table */}
          <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden">
            <div className="p-4 border-b border-slate-800 bg-slate-950/70 flex items-center justify-between">
              <div>
                <h3 className="text-sm font-bold text-white">Comparative Architecture Scorecard</h3>
                <p className="text-[11px] text-slate-400">All 11 formal evaluation metrics computed over 50 test prompts</p>
              </div>
              <span className="text-xs font-mono text-cyan-400 bg-cyan-950/80 px-2.5 py-1 rounded-lg border border-cyan-800/60 font-semibold">
                Run ID: {analytics?.latest_run_id}
              </span>
            </div>

            <div className="overflow-x-auto">
              <table className="w-full text-left border-collapse text-xs">
                <thead>
                  <tr className="border-b border-slate-800 bg-slate-950/40 text-slate-400 text-[10px] uppercase font-bold tracking-wider">
                    <th className="py-3 px-4">Evaluation Metric</th>
                    <th className="py-3 px-4 text-cyan-400">Architecture A (Rules)</th>
                    <th className="py-3 px-4 text-blue-400">Architecture B (Retrieval)</th>
                    <th className="py-3 px-4 text-violet-400">Architecture C (LLM RAG)</th>
                    <th className="py-3 px-4 text-slate-500">Methodology / Formula</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-slate-800/60 font-mono text-[11px]">
                  <tr className="hover:bg-slate-900/30">
                    <td className="py-3 px-4 font-sans font-semibold text-white">1. Overall Accuracy</td>
                    <td className="py-3 px-4 text-cyan-300 font-bold">{analytics.architectures['rules']?.accuracy_percentage}%</td>
                    <td className="py-3 px-4 text-blue-300 font-bold">{analytics.architectures['retrieval']?.accuracy_percentage}%</td>
                    <td className="py-3 px-4 text-violet-300 font-bold">{analytics.architectures['rag']?.accuracy_percentage}%</td>
                    <td className="py-3 px-4 font-sans text-slate-400 text-[10px]">Correct responses / Total (50) × 100</td>
                  </tr>

                  <tr className="hover:bg-slate-900/30">
                    <td className="py-3 px-4 font-sans font-semibold text-white">2. Average Latency</td>
                    <td className="py-3 px-4 text-cyan-300">{analytics.architectures['rules']?.avg_latency_ms} ms</td>
                    <td className="py-3 px-4 text-blue-300">{analytics.architectures['retrieval']?.avg_latency_ms} ms</td>
                    <td className="py-3 px-4 text-violet-300">{analytics.architectures['rag']?.avg_latency_ms} ms</td>
                    <td className="py-3 px-4 font-sans text-slate-400 text-[10px]">Arithmetic mean elapsed execution time</td>
                  </tr>

                  <tr className="hover:bg-slate-900/30">
                    <td className="py-3 px-4 font-sans font-semibold text-white">3. Median Latency</td>
                    <td className="py-3 px-4 text-cyan-300">{analytics.architectures['rules']?.median_latency_ms} ms</td>
                    <td className="py-3 px-4 text-blue-300">{analytics.architectures['retrieval']?.median_latency_ms} ms</td>
                    <td className="py-3 px-4 text-violet-300">{analytics.architectures['rag']?.median_latency_ms} ms</td>
                    <td className="py-3 px-4 font-sans text-slate-400 text-[10px]">50th percentile response latency</td>
                  </tr>

                  <tr className="hover:bg-slate-900/30">
                    <td className="py-3 px-4 font-sans font-semibold text-white">4. Direct-Query Accuracy</td>
                    <td className="py-3 px-4 text-cyan-300">{analytics.architectures['rules']?.direct_accuracy}%</td>
                    <td className="py-3 px-4 text-blue-300">{analytics.architectures['retrieval']?.direct_accuracy}%</td>
                    <td className="py-3 px-4 text-violet-300">{analytics.architectures['rag']?.direct_accuracy}%</td>
                    <td className="py-3 px-4 font-sans text-slate-400 text-[10px]">Evaluation on 20 literal canonical FAQ questions</td>
                  </tr>

                  <tr className="hover:bg-slate-900/30">
                    <td className="py-3 px-4 font-sans font-semibold text-white">5. Paraphrase Accuracy</td>
                    <td className="py-3 px-4 text-cyan-300">{analytics.architectures['rules']?.paraphrased_accuracy}%</td>
                    <td className="py-3 px-4 text-blue-300">{analytics.architectures['retrieval']?.paraphrased_accuracy}%</td>
                    <td className="py-3 px-4 text-violet-300">{analytics.architectures['rag']?.paraphrased_accuracy}%</td>
                    <td className="py-3 px-4 font-sans text-slate-400 text-[10px]">Evaluation on 15 syntactically altered queries</td>
                  </tr>

                  <tr className="hover:bg-slate-900/30">
                    <td className="py-3 px-4 font-sans font-semibold text-white">6. Out-of-Scope Rejection</td>
                    <td className="py-3 px-4 text-cyan-300">{analytics.architectures['rules']?.out_of_scope_rejection_rate}%</td>
                    <td className="py-3 px-4 text-blue-300">{analytics.architectures['retrieval']?.out_of_scope_rejection_rate}%</td>
                    <td className="py-3 px-4 text-violet-300">{analytics.architectures['rag']?.out_of_scope_rejection_rate}%</td>
                    <td className="py-3 px-4 font-sans text-slate-400 text-[10px]">Successful refusals on 10 external trivia queries</td>
                  </tr>

                  <tr className="hover:bg-slate-900/30">
                    <td className="py-3 px-4 font-sans font-semibold text-white">7. Adversarial Resistance</td>
                    <td className="py-3 px-4 text-cyan-300">{analytics.architectures['rules']?.adversarial_resistance_rate}%</td>
                    <td className="py-3 px-4 text-blue-300">{analytics.architectures['retrieval']?.adversarial_resistance_rate}%</td>
                    <td className="py-3 px-4 text-violet-300">{analytics.architectures['rag']?.adversarial_resistance_rate}%</td>
                    <td className="py-3 px-4 font-sans text-slate-400 text-[10px]">Safety retention on 5 prompt injections/override attempts</td>
                  </tr>

                  <tr className="hover:bg-slate-900/30">
                    <td className="py-3 px-4 font-sans font-semibold text-white">8. Hallucination Rate</td>
                    <td className="py-3 px-4 text-cyan-300">{analytics.architectures['rules']?.hallucination_rate_percentage}%</td>
                    <td className="py-3 px-4 text-blue-300">{analytics.architectures['retrieval']?.hallucination_rate_percentage}%</td>
                    <td className="py-3 px-4 text-violet-300">{analytics.architectures['rag']?.hallucination_rate_percentage}%</td>
                    <td className="py-3 px-4 font-sans text-slate-400 text-[10px]">Unsupported claims / Total evaluated × 100</td>
                  </tr>

                  <tr className="hover:bg-slate-900/30">
                    <td className="py-3 px-4 font-sans font-semibold text-white">9. Cost per Query</td>
                    <td className="py-3 px-4 text-emerald-400 font-bold">$0.00000</td>
                    <td className="py-3 px-4 text-emerald-400 font-bold">$0.00000</td>
                    <td className="py-3 px-4 text-violet-300 font-bold">${analytics.architectures['rag']?.avg_cost_per_query_usd.toFixed(5)}</td>
                    <td className="py-3 px-4 font-sans text-slate-400 text-[10px]">Gemini 2.5 Flash token pricing ($0.075/1M in, $0.30/1M out)</td>
                  </tr>

                  <tr className="hover:bg-slate-900/30">
                    <td className="py-3 px-4 font-sans font-semibold text-white">10. Total Experiment Cost</td>
                    <td className="py-3 px-4 text-emerald-400 font-bold">$0.00</td>
                    <td className="py-3 px-4 text-emerald-400 font-bold">$0.00</td>
                    <td className="py-3 px-4 text-violet-300 font-bold">${analytics.architectures['rag']?.total_cost_usd.toFixed(4)}</td>
                    <td className="py-3 px-4 font-sans text-slate-400 text-[10px]">Cumulative token expenditure over 50 test calls</td>
                  </tr>

                  <tr className="hover:bg-slate-900/30">
                    <td className="py-3 px-4 font-sans font-semibold text-white">11. Setup Complexity</td>
                    <td className="py-3 px-4 text-cyan-300 font-bold">3 / 10 (Low)</td>
                    <td className="py-3 px-4 text-blue-300 font-bold">5 / 10 (Moderate)</td>
                    <td className="py-3 px-4 text-violet-300 font-bold">8 / 10 (High)</td>
                    <td className="py-3 px-4 font-sans text-slate-400 text-[10px]">Architecture dependency &amp; pipeline engineering effort</td>
                  </tr>
                </tbody>
              </table>
            </div>
          </div>

          {/* Charts Grid */}
          <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
            {/* Multi-Metric Radar Chart */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <TrendingUp className="w-4 h-4 text-cyan-400" />
                <span>Multi-Metric Radar Comparison</span>
              </h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <RadarChart cx="50%" cy="50%" outerRadius="80%" data={radarData}>
                    <PolarGrid stroke="#334155" />
                    <PolarAngleAxis dataKey="subject" stroke="#94A3B8" fontSize={11} />
                    <PolarRadiusAxis angle={30} domain={[0, 100]} stroke="#64748B" fontSize={10} />
                    <Radar name="Rule-Based" dataKey="Rules" stroke="#06B6D4" fill="#06B6D4" fillOpacity={0.2} />
                    <Radar name="Retrieval" dataKey="Retrieval" stroke="#3B82F6" fill="#3B82F6" fillOpacity={0.2} />
                    <Radar name="LLM RAG" dataKey="RAG" stroke="#8B5CF6" fill="#8B5CF6" fillOpacity={0.2} />
                    <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                    <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px', fontSize: '11px' }} />
                  </RadarChart>
                </ResponsiveContainer>
              </div>
            </div>

            {/* Category Breakdown Bar Chart */}
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <BarChart3 className="w-4 h-4 text-cyan-400" />
                <span>Accuracy by Question Category</span>
              </h3>
              <div className="h-80">
                <ResponsiveContainer width="100%" height="100%">
                  <BarChart data={accuracyData} margin={{ top: 20, right: 20, left: -20, bottom: 5 }}>
                    <CartesianGrid strokeDasharray="3 3" stroke="#1E293B" vertical={false} />
                    <XAxis dataKey="name" stroke="#64748B" fontSize={11} />
                    <YAxis stroke="#64748B" domain={[0, 100]} fontSize={11} />
                    <Tooltip contentStyle={{ backgroundColor: '#0F172A', borderColor: '#334155', borderRadius: '8px', fontSize: '11px' }} />
                    <Legend wrapperStyle={{ fontSize: '11px', paddingTop: '10px' }} />
                    <Bar dataKey="direct" name="Direct" fill="#06B6D4" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="paraphrased" name="Paraphrased" fill="#3B82F6" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="oos_rejection" name="OOS Refusal" fill="#10B981" radius={[4, 4, 0, 0]} />
                    <Bar dataKey="adversarial" name="Adversarial" fill="#8B5CF6" radius={[4, 4, 0, 0]} />
                  </BarChart>
                </ResponsiveContainer>
              </div>
            </div>
          </div>

          {/* Key Findings Callout */}
          {analytics.key_findings && analytics.key_findings.length > 0 && (
            <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-3">
              <h3 className="text-sm font-bold text-white flex items-center gap-2">
                <Info className="w-4 h-4 text-cyan-400" />
                <span>Synthesized Experimental Findings</span>
              </h3>
              <div className="space-y-2 text-xs text-slate-300">
                {analytics.key_findings.map((f, i) => (
                  <div key={i} className="flex items-start gap-2">
                    <span className="w-1.5 h-1.5 rounded-full bg-cyan-400 mt-1.5 shrink-0" />
                    <p className="leading-relaxed">{f}</p>
                  </div>
                ))}
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
};
