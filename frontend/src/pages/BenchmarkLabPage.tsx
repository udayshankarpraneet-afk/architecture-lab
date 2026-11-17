import React, { useState, useEffect, useRef } from 'react';
import { 
  FlaskConical, 
  Play, 
  Square, 
  RotateCcw, 
  Download, 
  CheckCircle2, 
  XCircle, 
  ShieldAlert, 
  AlertTriangle, 
  Search, 
  Filter, 
  Clock, 
  Layers, 
  Cpu, 
  Sparkles, 
  UserCheck, 
  FileSpreadsheet, 
  FileCode,
  X,
  ExternalLink
} from 'lucide-react';
import { api } from '../services/api';
import { BenchmarkRunStatus, BenchmarkResultItem } from '../types';

export const BenchmarkLabPage: React.FC = () => {
  const [status, setStatus] = useState<BenchmarkRunStatus | null>(null);
  const [results, setResults] = useState<BenchmarkResultItem[]>([]);
  const [loadingResults, setLoadingResults] = useState(false);

  // Filters
  const [archFilter, setArchFilter] = useState('all');
  const [categoryFilter, setCategoryFilter] = useState('all');
  const [searchQuery, setSearchQuery] = useState('');
  const [statusFilter, setStatusFilter] = useState<'all' | 'correct' | 'incorrect' | 'hallucinated'>('all');

  // Review Modal
  const [selectedResult, setSelectedResult] = useState<BenchmarkResultItem | null>(null);
  const [reviewNotes, setReviewNotes] = useState('');

  // Polling ref
  const pollingRef = useRef<any>(null);

  useEffect(() => {
    checkStatus();
    loadResults();
    return () => stopPolling();
  }, []);

  const checkStatus = async () => {
    try {
      const s = await api.fetchBenchmarkStatus();
      setStatus(s);
      if (s.status === 'running') {
        startPolling();
      } else {
        stopPolling();
      }
    } catch (e) {
      console.error(e);
    }
  };

  const startPolling = () => {
    if (pollingRef.current) return;
    pollingRef.current = setInterval(async () => {
      try {
        const s = await api.fetchBenchmarkStatus();
        setStatus(s);
        if (s.status !== 'running') {
          stopPolling();
          loadResults();
        }
      } catch (e) {
        console.error(e);
      }
    }, 1500);
  };

  const stopPolling = () => {
    if (pollingRef.current) {
      clearInterval(pollingRef.current);
      pollingRef.current = null;
    }
  };

  const loadResults = async () => {
    try {
      setLoadingResults(true);
      const data = await api.fetchBenchmarkResults(undefined, archFilter, categoryFilter);
      setResults(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoadingResults(false);
    }
  };

  const handleStartBenchmark = async () => {
    try {
      await api.startBenchmark("Comprehensive 50-Question Academic Benchmark");
      await checkStatus();
      startPolling();
    } catch (err: any) {
      alert(`Error starting benchmark: ${err.message}`);
    }
  };

  const handleCancelBenchmark = async () => {
    try {
      await api.cancelBenchmark();
      await checkStatus();
    } catch (err: any) {
      alert(`Error cancelling benchmark: ${err.message}`);
    }
  };

  const handleExportCSV = () => {
    window.open('/api/benchmark/export/csv', '_blank');
  };

  const handleExportJSON = () => {
    window.open('/api/benchmark/export/json', '_blank');
  };

  const handleSaveReview = async (isCorrect: boolean) => {
    if (!selectedResult) return;
    try {
      await api.updateReview(selectedResult.id, isCorrect, reviewNotes);
      setSelectedResult(null);
      loadResults();
    } catch (err: any) {
      alert(`Failed to save review: ${err.message}`);
    }
  };

  // Filtered Results
  const filteredResults = results.filter((item) => {
    if (archFilter !== 'all' && item.architecture !== archFilter) return false;
    if (categoryFilter !== 'all' && item.question_category !== categoryFilter) return false;
    if (statusFilter === 'correct' && !item.is_correct) return false;
    if (statusFilter === 'incorrect' && item.is_correct) return false;
    if (statusFilter === 'hallucinated' && !item.is_hallucinated) return false;
    if (searchQuery) {
      const q = searchQuery.toLowerCase();
      return (
        item.user_question.toLowerCase().includes(q) ||
        item.generated_answer.toLowerCase().includes(q) ||
        item.test_id.toLowerCase().includes(q)
      );
    }
    return true;
  });

  const isRunning = status?.status === 'running';

  return (
    <div className="space-y-6 max-w-7xl mx-auto pb-12">
      {/* Header and Controls */}
      <div className="glass-panel p-6 rounded-2xl border border-slate-800 space-y-4">
        <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4">
          <div>
            <div className="flex items-center gap-2">
              <FlaskConical className="w-5 h-5 text-cyan-400" />
              <h2 className="text-xl font-bold text-white">Benchmark Lab</h2>
              <span className="text-[10px] font-mono px-2 py-0.5 rounded bg-cyan-950 text-cyan-400 border border-cyan-800 font-bold">
                50 Questions × 3 Architectures = 150 Responses
              </span>
            </div>
            <p className="text-xs text-slate-400 mt-1">
              Rigorous, reproducible test harness evaluating factual accuracy, latency, refusal correctness, and hallucination rate.
            </p>
          </div>

          <div className="flex flex-wrap items-center gap-2">
            {!isRunning ? (
              <button
                onClick={handleStartBenchmark}
                className="px-4 py-2.5 rounded-xl bg-gradient-to-r from-cyan-500 to-blue-600 hover:from-cyan-400 hover:to-blue-500 text-slate-950 font-bold text-xs flex items-center gap-2 shadow-lg shadow-cyan-950/40 transition-all cursor-pointer"
              >
                <Play className="w-4 h-4" />
                <span>{results.length > 0 ? 'Re-Run Benchmark' : 'Start Benchmark'}</span>
              </button>
            ) : (
              <button
                onClick={handleCancelBenchmark}
                className="px-4 py-2.5 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs flex items-center gap-2 transition-all cursor-pointer"
              >
                <Square className="w-4 h-4" />
                <span>Cancel Benchmark</span>
              </button>
            )}

            <button
              onClick={handleExportCSV}
              disabled={results.length === 0}
              className="px-3.5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 disabled:opacity-40 text-slate-300 hover:text-white border border-slate-800 text-xs flex items-center gap-1.5 transition-all cursor-pointer"
            >
              <FileSpreadsheet className="w-4 h-4 text-emerald-400" />
              <span>Export CSV</span>
            </button>
            <button
              onClick={handleExportJSON}
              disabled={results.length === 0}
              className="px-3.5 py-2.5 rounded-xl bg-slate-900 hover:bg-slate-800 disabled:opacity-40 text-slate-300 hover:text-white border border-slate-800 text-xs flex items-center gap-1.5 transition-all cursor-pointer"
            >
              <FileCode className="w-4 h-4 text-cyan-400" />
              <span>Export JSON</span>
            </button>
          </div>
        </div>

        {/* Live Progress Bar if Running */}
        {status && (isRunning || status.completed_responses > 0) && (
          <div className="p-4 rounded-xl bg-slate-950 border border-slate-800/80 space-y-3">
            <div className="flex flex-col sm:flex-row justify-between text-xs gap-2">
              <div className="flex items-center gap-2">
                <span className={`w-2.5 h-2.5 rounded-full ${isRunning ? 'bg-cyan-400 animate-pulse' : 'bg-emerald-400'}`} />
                <span className="font-semibold text-white uppercase tracking-wide">
                  Status: {status.status}
                </span>
                <span className="text-slate-500">|</span>
                <span className="text-slate-300">
                  Run ID: <span className="font-mono text-cyan-400">{status.run_id}</span>
                </span>
              </div>

              <div className="flex items-center gap-4 text-slate-400 font-mono text-[11px]">
                <span>Progress: {status.completed_responses} / {status.total_expected_responses} ({status.progress_percentage}%)</span>
                <span>Elapsed: {status.elapsed_time_sec}s</span>
              </div>
            </div>

            {/* Progress Bar */}
            <div className="w-full h-2.5 rounded-full bg-slate-900 overflow-hidden border border-slate-800">
              <div 
                className="h-full bg-gradient-to-r from-cyan-500 via-blue-500 to-violet-500 transition-all duration-300"
                style={{ width: `${status.progress_percentage}%` }}
              />
            </div>

            {/* Current Question Telemetry */}
            {isRunning && status.current_question_text && (
              <div className="flex items-center justify-between text-xs text-slate-400 pt-1">
                <div className="truncate max-w-lg">
                  <span className="text-cyan-400 font-medium">Q{status.current_question_index}: </span>
                  <span className="text-slate-300">{status.current_question_text}</span>
                </div>
                <div className="font-mono text-violet-400 uppercase font-semibold">
                  Evaluating: {status.current_architecture}
                </div>
              </div>
            )}
          </div>
        )}

        {/* Question Distribution Highlights */}
        <div className="grid grid-cols-2 sm:grid-cols-4 gap-3 text-xs pt-1">
          <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-slate-400 block text-[10px] uppercase font-bold">20 Direct Questions</span>
            <span className="text-white font-medium">Standard FAQ Inquiries</span>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-slate-400 block text-[10px] uppercase font-bold">15 Paraphrased Questions</span>
            <span className="text-white font-medium">Lexical Variations</span>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-slate-400 block text-[10px] uppercase font-bold">10 Out-of-Scope Questions</span>
            <span className="text-white font-medium">Trivia, Sports, Weather</span>
          </div>
          <div className="p-2.5 rounded-xl bg-slate-950/60 border border-slate-800/80">
            <span className="text-slate-400 block text-[10px] uppercase font-bold">5 Adversarial Questions</span>
            <span className="text-white font-medium">Jailbreaks &amp; Leaks</span>
          </div>
        </div>
      </div>

      {/* Results Filter Toolbar */}
      <div className="glass-panel p-4 rounded-2xl border border-slate-800 space-y-3">
        <div className="flex flex-col sm:flex-row gap-3">
          <div className="relative flex-1">
            <Search className="w-4 h-4 text-slate-500 absolute left-3 top-3" />
            <input
              type="text"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              placeholder="Search recorded responses, test IDs, or query text..."
              className="w-full bg-slate-950 border border-slate-800 rounded-xl pl-9 pr-4 py-2 text-xs text-white placeholder-slate-500 focus:outline-none focus:border-cyan-500"
            />
          </div>

          <div className="flex items-center gap-2 flex-wrap">
            {/* Architecture filter */}
            <select
              value={archFilter}
              onChange={(e) => setArchFilter(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none"
            >
              <option value="all">All Architectures</option>
              <option value="rules">Rule-Based</option>
              <option value="retrieval">Semantic Retrieval</option>
              <option value="rag">LLM RAG</option>
            </select>

            {/* Category filter */}
            <select
              value={categoryFilter}
              onChange={(e) => setCategoryFilter(e.target.value)}
              className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none"
            >
              <option value="all">All Categories</option>
              <option value="DIRECT">Direct (20)</option>
              <option value="PARAPHRASED">Paraphrased (15)</option>
              <option value="OUT_OF_SCOPE">Out-of-Scope (10)</option>
              <option value="ADVERSARIAL">Adversarial (5)</option>
            </select>

            {/* Status filter */}
            <select
              value={statusFilter}
              onChange={(e) => setStatusFilter(e.target.value as any)}
              className="bg-slate-950 border border-slate-800 rounded-xl px-3 py-2 text-xs text-white focus:outline-none"
            >
              <option value="all">All Outcomes</option>
              <option value="correct">Correct Only</option>
              <option value="incorrect">Failures Only</option>
              <option value="hallucinated">Hallucinations</option>
            </select>
          </div>
        </div>
      </div>

      {/* Results Table */}
      <div className="glass-panel rounded-2xl border border-slate-800 overflow-hidden">
        <div className="overflow-x-auto">
          <table className="w-full text-left border-collapse text-xs">
            <thead>
              <tr className="border-b border-slate-800 bg-slate-950/70 text-slate-400 font-semibold uppercase tracking-wider text-[10px]">
                <th className="py-3 px-4 w-20">ID</th>
                <th className="py-3 px-4 w-28">Architecture</th>
                <th className="py-3 px-4 w-28">Category</th>
                <th className="py-3 px-4">User Query &amp; Generated Output</th>
                <th className="py-3 px-4 w-24">Latency</th>
                <th className="py-3 px-4 w-28">Evaluation</th>
                <th className="py-3 px-4 w-20 text-right">Review</th>
              </tr>
            </thead>
            <tbody className="divide-y divide-slate-800/60">
              {loadingResults ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-400">
                    <div className="inline-flex items-center gap-2">
                      <div className="w-4 h-4 border-2 border-cyan-400 border-t-transparent rounded-full animate-spin" />
                      <span>Loading benchmark results...</span>
                    </div>
                  </td>
                </tr>
              ) : filteredResults.length === 0 ? (
                <tr>
                  <td colSpan={7} className="py-12 text-center text-slate-400">
                    {results.length === 0 ? (
                      <div className="space-y-2">
                        <p className="font-semibold text-slate-300">No benchmark responses recorded yet.</p>
                        <p className="text-xs text-slate-500">Click "Start Benchmark" above to test all 50 questions across all 3 architectures.</p>
                      </div>
                    ) : (
                      "No responses match the active filters."
                    )}
                  </td>
                </tr>
              ) : (
                filteredResults.map((r) => {
                  const isCorrect = r.human_reviewed && r.human_correct !== null ? r.human_correct : r.is_correct;
                  return (
                    <tr key={r.id} className="hover:bg-slate-900/40 transition-colors">
                      <td className="py-3 px-4 font-mono font-bold text-slate-400">{r.test_id}</td>
                      <td className="py-3 px-4">
                        <span className={`px-2 py-0.5 rounded text-[10px] font-mono font-bold uppercase ${
                          r.architecture === 'rules' ? 'bg-cyan-950 text-cyan-300 border border-cyan-800/60' :
                          r.architecture === 'retrieval' ? 'bg-blue-950 text-blue-300 border border-blue-800/60' :
                          'bg-violet-950 text-violet-300 border border-violet-800/60'
                        }`}>
                          {r.architecture}
                        </span>
                      </td>
                      <td className="py-3 px-4">
                        <span className="text-[10px] font-medium text-slate-300 bg-slate-900 px-2 py-0.5 rounded border border-slate-800">
                          {r.question_category}
                        </span>
                      </td>
                      <td className="py-3 px-4 space-y-1">
                        <div className="font-semibold text-white">{r.user_question}</div>
                        <div className="text-slate-300 text-[11px] line-clamp-2 leading-relaxed" title={r.generated_answer}>
                          {r.generated_answer}
                        </div>
                        {r.failure_reason && (
                          <div className="text-[10px] text-rose-400/90 italic">
                            Reason: {r.failure_reason}
                          </div>
                        )}
                      </td>
                      <td className="py-3 px-4 font-mono text-slate-300 text-[11px]">
                        {r.response_time_ms} ms
                      </td>
                      <td className="py-3 px-4 space-y-1">
                        <div className="flex items-center gap-1.5">
                          {isCorrect ? (
                            <span className="inline-flex items-center gap-1 text-[10px] font-bold text-emerald-400 bg-emerald-950/80 px-2 py-0.5 rounded border border-emerald-800/60">
                              <CheckCircle2 className="w-3 h-3" /> PASS
                            </span>
                          ) : (
                            <span className="inline-flex items-center gap-1 text-[10px] font-bold text-rose-400 bg-rose-950/80 px-2 py-0.5 rounded border border-rose-800/60">
                              <XCircle className="w-3 h-3" /> FAIL
                            </span>
                          )}

                          {r.is_hallucinated && (
                            <span className="inline-flex items-center gap-1 text-[9px] font-bold text-amber-400 bg-amber-950 px-1.5 py-0.5 rounded border border-amber-800">
                              HALLUCINATED
                            </span>
                          )}
                        </div>
                        {r.human_reviewed && (
                          <div className="text-[9px] text-cyan-400 font-mono">
                            Human Verified
                          </div>
                        )}
                      </td>
                      <td className="py-3 px-4 text-right">
                        <button
                          onClick={() => {
                            setSelectedResult(r);
                            setReviewNotes('');
                          }}
                          className="px-2 py-1 rounded bg-slate-900 hover:bg-slate-800 text-slate-300 hover:text-cyan-300 border border-slate-800 text-[10px] font-medium transition-colors cursor-pointer"
                        >
                          Inspect
                        </button>
                      </td>
                    </tr>
                  );
                })
              )}
            </tbody>
          </table>
        </div>
      </div>

      {/* Manual Review Modal */}
      {selectedResult && (
        <div className="fixed inset-0 z-50 bg-slate-950/85 backdrop-blur-sm flex items-center justify-center p-4">
          <div className="glass-panel w-full max-w-2xl rounded-2xl border border-slate-700 p-6 space-y-4 shadow-2xl">
            <div className="flex items-center justify-between border-b border-slate-800 pb-3">
              <div>
                <h3 className="text-base font-bold text-white flex items-center gap-2">
                  <UserCheck className="w-5 h-5 text-cyan-400" />
                  <span>Manual Evaluation Review (Test #{selectedResult.test_id})</span>
                </h3>
                <span className="text-xs font-mono text-cyan-400 uppercase">
                  Architecture: {selectedResult.architecture} | Category: {selectedResult.question_category}
                </span>
              </div>
              <button
                onClick={() => setSelectedResult(null)}
                className="text-slate-400 hover:text-white p-1 cursor-pointer"
              >
                <X className="w-4 h-4" />
              </button>
            </div>

            <div className="space-y-3 text-xs">
              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <span className="text-slate-400 font-semibold block uppercase text-[10px]">User Question</span>
                <p className="text-white font-medium">{selectedResult.user_question}</p>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <span className="text-slate-400 font-semibold block uppercase text-[10px]">Generated Architecture Response</span>
                <p className="text-slate-200 leading-relaxed whitespace-pre-line">{selectedResult.generated_answer}</p>
              </div>

              <div className="p-3 rounded-xl bg-slate-950 border border-slate-800 space-y-1">
                <span className="text-slate-400 font-semibold block uppercase text-[10px]">Expected Answer &amp; Criteria</span>
                <p className="text-emerald-300/90 leading-relaxed">{selectedResult.expected_answer}</p>
              </div>

              <div className="grid grid-cols-2 gap-3 text-[11px]">
                <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                  <span className="text-slate-400">Response Latency:</span>{' '}
                  <span className="font-mono text-white font-bold">{selectedResult.response_time_ms} ms</span>
                </div>
                <div className="p-2.5 rounded-lg bg-slate-900 border border-slate-800">
                  <span className="text-slate-400">Automated Label:</span>{' '}
                  <span className={`font-bold ${selectedResult.is_correct ? 'text-emerald-400' : 'text-rose-400'}`}>
                    {selectedResult.is_correct ? 'PASS' : 'FAIL'}
                  </span>
                </div>
              </div>

              {selectedResult.failure_reason && (
                <div className="p-2.5 rounded-lg bg-rose-950/40 border border-rose-800/60 text-rose-300 text-[11px]">
                  <strong>Identified Failure: </strong> {selectedResult.failure_reason}
                </div>
              )}
            </div>

            {/* Human Decision Buttons */}
            <div className="pt-3 border-t border-slate-800 flex items-center justify-between">
              <div className="text-[11px] text-slate-400">
                Override automated grading with human verdict:
              </div>
              <div className="flex gap-2">
                <button
                  onClick={() => handleSaveReview(false)}
                  className="px-3.5 py-2 rounded-xl bg-rose-600 hover:bg-rose-500 text-white font-bold text-xs flex items-center gap-1.5 transition-all cursor-pointer"
                >
                  <XCircle className="w-3.5 h-3.5" />
                  <span>Mark Incorrect</span>
                </button>
                <button
                  onClick={() => handleSaveReview(true)}
                  className="px-3.5 py-2 rounded-xl bg-emerald-600 hover:bg-emerald-500 text-white font-bold text-xs flex items-center gap-1.5 transition-all cursor-pointer"
                >
                  <CheckCircle2 className="w-3.5 h-3.5" />
                  <span>Mark Correct</span>
                </button>
              </div>
            </div>
          </div>
        </div>
      )}
    </div>
  );
};
