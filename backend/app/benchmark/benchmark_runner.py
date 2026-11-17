import time
import json
import uuid
import threading
import logging
from typing import Dict, Any, List, Optional
from datetime import datetime, timezone
from backend.app.core.database import get_db_connection
from backend.app.models.schemas import BenchmarkQuestion, BenchmarkRunStatus, BenchmarkResultItem
from backend.app.engines.rule_engine import rule_engine
from backend.app.engines.retrieval_engine import retrieval_engine
from backend.app.engines.rag_engine import rag_engine
from backend.app.benchmark.evaluator import BenchmarkEvaluator

logger = logging.getLogger(__name__)

class BenchmarkRunner:
    """
    Coordinates execution of the 50-question benchmark suite across
    all 3 chatbot architectures, producing 150 evaluated responses.
    """

    def __init__(self):
        self.lock = threading.Lock()
        self.current_run: Optional[BenchmarkRunStatus] = None
        self._cancel_requested = False
        self._pause_requested = False
        self._worker_thread: Optional[threading.Thread] = None

    def get_status(self) -> Dict[str, Any]:
        with self.lock:
            if not self.current_run:
                # Check DB for latest run
                conn = get_db_connection()
                row = conn.execute("SELECT * FROM benchmark_runs ORDER BY created_at DESC LIMIT 1").fetchone()
                conn.close()
                if row:
                    return {
                        "run_id": row["id"],
                        "status": row["status"],
                        "total_questions": row["total_questions"],
                        "total_expected_responses": row["total_expected_responses"],
                        "completed_responses": row["completed_responses"],
                        "current_question_index": row["current_question_index"],
                        "current_question_text": row["current_question_text"],
                        "current_architecture": row["current_architecture"],
                        "progress_percentage": row["progress_percentage"],
                        "elapsed_time_sec": row["elapsed_time_sec"],
                        "created_at": row["created_at"]
                    }
                return {
                    "run_id": "none",
                    "status": "idle",
                    "total_questions": 50,
                    "total_expected_responses": 150,
                    "completed_responses": 0,
                    "current_question_index": 0,
                    "current_question_text": None,
                    "current_architecture": None,
                    "progress_percentage": 0.0,
                    "elapsed_time_sec": 0.0,
                    "created_at": datetime.now(timezone.utc).isoformat()
                }

            return self.current_run.dict()

    def start_benchmark(self, notes: str = "Standard 50-Question Benchmark") -> str:
        with self.lock:
            if self.current_run and self.current_run.status == "running":
                return self.current_run.run_id

            run_id = f"run-{uuid.uuid4().hex[:8]}"
            self._cancel_requested = False
            self._pause_requested = False

            self.current_run = BenchmarkRunStatus(
                run_id=run_id,
                status="running",
                total_questions=50,
                total_expected_responses=150,
                completed_responses=0,
                current_question_index=0,
                current_question_text="Initializing benchmark suite...",
                current_architecture="none",
                progress_percentage=0.0,
                elapsed_time_sec=0.0,
                created_at=datetime.now(timezone.utc).isoformat()
            )

            # Insert initial run in DB
            conn = get_db_connection()
            conn.execute("""
            INSERT INTO benchmark_runs (id, status, total_questions, total_expected_responses, completed_responses,
                                       current_question_index, current_question_text, current_architecture,
                                       progress_percentage, elapsed_time_sec, created_at, notes)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
            """, (
                run_id, "running", 50, 150, 0, 0, "Initializing...", "none", 0.0, 0.0, self.current_run.created_at, notes
            ))
            conn.commit()
            conn.close()

            # Start worker thread
            self._worker_thread = threading.Thread(target=self._run_benchmark_worker, args=(run_id,), daemon=True)
            self._worker_thread.start()
            return run_id

    def cancel_benchmark(self):
        with self.lock:
            self._cancel_requested = True
            if self.current_run:
                self.current_run.status = "cancelled"

    def _run_benchmark_worker(self, run_id: str):
        logger.info(f"Starting benchmark run: {run_id}")
        start_wall_time = time.time()

        conn = get_db_connection()
        # Fetch 50 questions
        rows = conn.execute("SELECT * FROM benchmark_questions ORDER BY id ASC").fetchall()
        questions = []
        for r in rows:
            questions.append(BenchmarkQuestion(
                id=r["id"],
                question=r["question"],
                category=r["category"],
                expected_answer=r["expected_answer"],
                expected_behaviour=r["expected_behaviour"],
                relevant_faq_id=r["relevant_faq_id"],
                evaluation_criteria=json.loads(r["evaluation_criteria_json"])
            ))

        total_questions = len(questions)
        total_responses = total_questions * 3
        completed_responses = 0

        architectures = ["rules", "retrieval", "rag"]

        for q_idx, q in enumerate(questions):
            if self._cancel_requested:
                logger.info(f"Benchmark run {run_id} was cancelled by user.")
                break

            for arch in architectures:
                if self._cancel_requested:
                    break

                with self.lock:
                    self.current_run.current_question_index = q_idx + 1
                    self.current_run.current_question_text = q.question
                    self.current_run.current_architecture = arch
                    self.current_run.completed_responses = completed_responses
                    self.current_run.progress_percentage = round((completed_responses / total_responses) * 100.0, 1)
                    self.current_run.elapsed_time_sec = round(time.time() - start_wall_time, 1)

                # Execute architecture under test
                try:
                    if arch == "rules":
                        resp = rule_engine.process(q.question)
                    elif arch == "retrieval":
                        resp = retrieval_engine.process(q.question, strategy="tfidf", confidence_threshold=0.25)
                    else: # "rag"
                        resp = rag_engine.process(q.question, retrieval_strategy="tfidf", confidence_threshold=0.20)

                    # Evaluate response deterministically
                    eval_item = BenchmarkEvaluator.evaluate(q, resp, run_id)

                    # Persist evaluated result to DB
                    conn.execute("""
                    INSERT INTO benchmark_results (
                        run_id, test_id, architecture, question_category, user_question,
                        generated_answer, expected_answer, retrieved_source, similarity_score,
                        response_time_ms, token_usage, estimated_cost, is_correct, is_hallucinated,
                        is_refusal_correct, failure_reason, evaluation_method, human_reviewed, human_correct
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, NULL)
                    """, (
                        eval_item.run_id, eval_item.test_id, eval_item.architecture, eval_item.question_category,
                        eval_item.user_question, eval_item.generated_answer, eval_item.expected_answer,
                        eval_item.retrieved_source, eval_item.similarity_score, eval_item.response_time_ms,
                        eval_item.token_usage, eval_item.estimated_cost,
                        1 if eval_item.is_correct else 0,
                        1 if eval_item.is_hallucinated else 0,
                        1 if eval_item.is_refusal_correct else 0,
                        eval_item.failure_reason, eval_item.evaluation_method
                    ))
                    conn.commit()

                except Exception as e:
                    logger.error(f"Error executing benchmark {q.id} on {arch}: {e}")
                    # Record failure explicitly
                    conn.execute("""
                    INSERT INTO benchmark_results (
                        run_id, test_id, architecture, question_category, user_question,
                        generated_answer, expected_answer, retrieved_source, similarity_score,
                        response_time_ms, token_usage, estimated_cost, is_correct, is_hallucinated,
                        is_refusal_correct, failure_reason, evaluation_method, human_reviewed, human_correct
                    ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 0, 0, 0, ?, 'automated', 0, NULL)
                    """, (
                        run_id, q.id, arch, q.category, q.question,
                        f"Runtime Execution Error: {str(e)}", q.expected_answer,
                        None, 0.0, 0.0, 0, 0.0, f"Exception: {str(e)}"
                    ))
                    conn.commit()

                completed_responses += 1

                # Update run record in DB periodically
                conn.execute("""
                UPDATE benchmark_runs
                SET completed_responses = ?, current_question_index = ?, current_question_text = ?,
                    current_architecture = ?, progress_percentage = ?, elapsed_time_sec = ?
                WHERE id = ?
                """, (
                    completed_responses, q_idx + 1, q.question, arch,
                    round((completed_responses / total_responses) * 100.0, 1),
                    round(time.time() - start_wall_time, 1),
                    run_id
                ))
                conn.commit()

        final_status = "cancelled" if self._cancel_requested else "completed"
        elapsed_sec = round(time.time() - start_wall_time, 1)

        conn.execute("""
        UPDATE benchmark_runs
        SET status = ?, completed_responses = ?, progress_percentage = ?, elapsed_time_sec = ?
        WHERE id = ?
        """, (
            final_status, completed_responses,
            round((completed_responses / total_responses) * 100.0, 1),
            elapsed_sec, run_id
        ))
        conn.commit()
        conn.close()

        with self.lock:
            if self.current_run:
                self.current_run.status = final_status
                self.current_run.completed_responses = completed_responses
                self.current_run.progress_percentage = 100.0 if final_status == "completed" else round((completed_responses / total_responses) * 100.0, 1)
                self.current_run.elapsed_time_sec = elapsed_sec

        logger.info(f"Benchmark run {run_id} finished with status: {final_status}")

# Global singleton
benchmark_runner = BenchmarkRunner()
