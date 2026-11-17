import sqlite3
import numpy as np
from typing import Dict, Any, List, Optional
from backend.app.core.database import get_db_connection
from backend.app.models.schemas import AnalyticsSummaryResponse, ArchitectureMetrics

class AnalyticsService:
    """
    Computes all analytical benchmarks, metrics, and comparisons
    from the persistent SQLite benchmark database.
    """

    @staticmethod
    def get_summary(run_id: Optional[str] = None) -> AnalyticsSummaryResponse:
        conn = get_db_connection()

        # Find run
        if run_id and run_id != "latest":
            run_row = conn.execute("SELECT * FROM benchmark_runs WHERE id = ?", (run_id,)).fetchone()
        else:
            run_row = conn.execute("SELECT * FROM benchmark_runs ORDER BY created_at DESC LIMIT 1").fetchone()

        if not run_row:
            conn.close()
            return AnalyticsSummaryResponse(
                has_benchmark_data=False,
                total_runs=0,
                latest_run_id=None,
                latest_run_timestamp=None,
                total_benchmark_questions=50,
                architectures={},
                category_breakdown={},
                latency_distribution={},
                key_findings=[
                    "No benchmark experiments have been executed yet.",
                    "Run the 50-question benchmark in the Benchmark Lab to generate real experimental comparisons."
                ]
            )

        active_run_id = run_row["id"]
        total_runs = conn.execute("SELECT COUNT(*) as c FROM benchmark_runs").fetchone()["c"]

        # Fetch all results for this run
        rows = conn.execute("SELECT * FROM benchmark_results WHERE run_id = ?", (active_run_id,)).fetchall()
        conn.close()

        if not rows:
            return AnalyticsSummaryResponse(
                has_benchmark_data=False,
                total_runs=total_runs,
                latest_run_id=active_run_id,
                latest_run_timestamp=run_row["created_at"],
                total_benchmark_questions=50,
                architectures={},
                category_breakdown={},
                latency_distribution={},
                key_findings=["Benchmark run is in progress or has 0 recorded results."]
            )

        architectures_list = ["rules", "retrieval", "rag"]
        arch_metrics: Dict[str, ArchitectureMetrics] = {}
        category_breakdown: Dict[str, Dict[str, float]] = {
            "DIRECT": {},
            "PARAPHRASED": {},
            "OUT_OF_SCOPE": {},
            "ADVERSARIAL": {}
        }
        latency_dist: Dict[str, List[float]] = {}

        # Setup complexity rubric (1-10)
        complexity_scores = {"rules": 3, "retrieval": 5, "rag": 8}

        for arch in architectures_list:
            arch_rows = [r for r in rows if r["architecture"] == arch]
            total_eval = len(arch_rows)
            if total_eval == 0:
                continue

            # Check human override if present
            def is_item_correct(item) -> bool:
                if item["human_reviewed"] and item["human_correct"] is not None:
                    return bool(item["human_correct"])
                return bool(item["is_correct"])

            correct_count = sum(1 for r in arch_rows if is_item_correct(r))
            accuracy = round((correct_count / total_eval) * 100.0, 1)

            latencies = [float(r["response_time_ms"]) for r in arch_rows]
            avg_lat = round(float(np.mean(latencies)), 2)
            med_lat = round(float(np.median(latencies)), 2)
            min_lat = round(float(np.min(latencies)), 2)
            max_lat = round(float(np.max(latencies)), 2)
            latency_dist[arch] = [round(l, 1) for l in latencies]

            hallucinations = sum(1 for r in arch_rows if r["is_hallucinated"])
            hallucination_rate = round((hallucinations / total_eval) * 100.0, 1)

            # Category filtering
            direct_items = [r for r in arch_rows if r["question_category"] == "DIRECT"]
            para_items = [r for r in arch_rows if r["question_category"] == "PARAPHRASED"]
            oos_items = [r for r in arch_rows if r["question_category"] == "OUT_OF_SCOPE"]
            adv_items = [r for r in arch_rows if r["question_category"] == "ADVERSARIAL"]

            direct_acc = round((sum(1 for r in direct_items if is_item_correct(r)) / len(direct_items) * 100.0), 1) if direct_items else 0.0
            para_acc = round((sum(1 for r in para_items if is_item_correct(r)) / len(para_items) * 100.0), 1) if para_items else 0.0
            adv_res = round((sum(1 for r in adv_items if is_item_correct(r)) / len(adv_items) * 100.0), 1) if adv_items else 0.0

            oos_refused = sum(1 for r in oos_items if r["is_refusal_correct"])
            oos_rate = round((oos_refused / len(oos_items) * 100.0), 1) if oos_items else 0.0

            total_tokens = sum(r["token_usage"] or 0 for r in arch_rows)
            total_cost = round(sum(r["estimated_cost"] or 0.0 for r in arch_rows), 5)
            avg_cost = round(total_cost / total_eval, 6)

            arch_metrics[arch] = ArchitectureMetrics(
                architecture=arch,
                total_evaluated=total_eval,
                correct_count=correct_count,
                accuracy_percentage=accuracy,
                avg_latency_ms=avg_lat,
                median_latency_ms=med_lat,
                min_latency_ms=min_lat,
                max_latency_ms=max_lat,
                hallucination_count=hallucinations,
                hallucination_rate_percentage=hallucination_rate,
                out_of_scope_total=len(oos_items),
                out_of_scope_refused=oos_refused,
                out_of_scope_rejection_rate=oos_rate,
                direct_accuracy=direct_acc,
                paraphrased_accuracy=para_acc,
                adversarial_resistance_rate=adv_res,
                total_tokens=total_tokens,
                total_cost_usd=total_cost,
                avg_cost_per_query_usd=avg_cost,
                setup_complexity_score=complexity_scores.get(arch, 5)
            )

            category_breakdown["DIRECT"][arch] = direct_acc
            category_breakdown["PARAPHRASED"][arch] = para_acc
            category_breakdown["OUT_OF_SCOPE"][arch] = oos_rate
            category_breakdown["ADVERSARIAL"][arch] = adv_res

        # Key analytical findings synthesized from measured data
        findings = []
        if "rules" in arch_metrics and "retrieval" in arch_metrics:
            speedup = round(arch_metrics["retrieval"].avg_latency_ms / max(arch_metrics["rules"].avg_latency_ms, 0.001), 1)
            findings.append(f"Rule-Based architecture is the fastest, executing in {arch_metrics['rules'].avg_latency_ms:.1f}ms on average.")
        if "retrieval" in arch_metrics:
            findings.append(f"Semantic Retrieval achieved {arch_metrics['retrieval'].accuracy_percentage}% accuracy with zero LLM API token cost.")
        if "rag" in arch_metrics:
            findings.append(f"LLM-Based RAG demonstrated {arch_metrics['rag'].paraphrased_accuracy}% accuracy on paraphrased natural language questions.")

        return AnalyticsSummaryResponse(
            has_benchmark_data=True,
            total_runs=total_runs,
            latest_run_id=active_run_id,
            latest_run_timestamp=run_row["created_at"],
            total_benchmark_questions=50,
            architectures=arch_metrics,
            category_breakdown=category_breakdown,
            latency_distribution=latency_dist,
            key_findings=findings
        )
