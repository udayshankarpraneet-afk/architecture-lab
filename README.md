# ARCHITECTURE LAB
### Comparative Chatbot Architecture Study: Rules vs Semantic Retrieval vs LLM-Based RAG

**Artificial Intelligence Foundations Academic Laboratory & Full-Stack Research Platform**

---

## 1. Project Overview

**ARCHITECTURE LAB** is a complete, production-grade, full-stack empirical research platform designed to investigate and compare the three foundational chatbot paradigms:

1. **Architecture A: Rule-Based Chatbot** (Deterministic regex patterns, priority IF-THEN rules, text normalisation)
2. **Architecture B: Semantic Retrieval-Based Chatbot** (Lexical BM25, TF-IDF Cosine Similarity, Dense Semantic Embeddings)
3. **Architecture C: LLM-Based RAG Chatbot** (Retrieval-Augmented Generation with Google Gemini 2.5/1.5 Flash and strict anti-hallucination guardrails)

All three architectures query the **exact same institutional knowledge base** (modelled after *"Demo University"*) and answer the **exact same standardized questions**.

---

## 2. Key Capabilities & Application Pages

The application is structured into **8 comprehensive interactive pages**:

| Page | Module | Capabilities |
| :--- | :--- | :--- |
| **Page 1** | **Overview Dashboard** | Executive summary, 3 architecture pillars, summary KPI highlights (Best Accuracy, Lowest Latency, Cost, Hallucination Rate), Recharts comparative graphs. |
| **Page 2** | **Chat Playground** | **Mode A (Individual Testing)** with telemetry and parameter tuning; **Mode B (Side-by-Side Comparison)** where all 3 architectures answer one question simultaneously with latency, confidence, and source attribution. |
| **Page 3** | **Architecture Explorer** | Visual workflow diagrams breaking down every stage (What it does, Why it is needed, Examples). Includes an **Interactive Query Tracer** with real-time stage telemetry. |
| **Page 4** | **Knowledge Base** | Full CRUD management for 32+ demonstration FAQs across 11 categories (*Admissions, Fees, Courses, Eligibility, Hostel, Library, Exams, etc.*). JSON export & import. Automatic retrieval index rebuilding on update. |
| **Page 5** | **Benchmark Lab** | Automated test suite of **50 predefined test prompts** (20 Direct, 15 Paraphrased, 10 Out-of-Scope, 5 Adversarial) generating **150 evaluated responses**. Live progress bar, interactive filtering, CSV & JSON exports, and **Manual Human Review Override**. |
| **Page 6** | **Analytics & Comparison** | Deep-dive quantitative scorecard of all **11 formal metrics**, multi-metric Radar chart, category accuracy breakdowns, latency distributions, and transparent mathematical formulas. |
| **Page 7** | **Decision Guide** | Interactive priority wizard recommending the optimal architecture based on user trade-offs (Latency vs Accuracy vs Cost vs Conversational Fluency). Full comparative trade-off matrix. |
| **Page 8** | **Project Documentation** | Complete 16-section academic technical report suitable for college viva / project submission with print-to-PDF support. |

---

## 3. Technology Stack

- **Frontend**: React 18, TypeScript, Vite, Tailwind CSS, Framer Motion, Recharts, Lucide React.
- **Backend**: Python 3.13, FastAPI, Pydantic v2, Scikit-learn, NumPy, Pandas, HTTPX, Pytest, Python-Dotenv.
- **Database & Storage**: SQLite (`architecture_lab.db`), Seed JSON datasets (`seed_faqs.json`, `benchmark_questions.json`).
- **LLM Provider Adapter**: Google Gemini API (`gemini-2.5-flash` / `gemini-1.5-flash`) via `GEMINI_API_KEY`.

---

## 4. Architectural Implementations

### Architecture A: Rule-Based Engine (`rule_engine.py`)
- **Text Normalisation**: Lowercasing, punctuation stripping, whitespace collapsing.
- **Priority Rules**: Multi-tier hierarchy:
  - Priority 100: Prompt Injection / Adversarial Defense
  - Priority 85: Out-of-Scope Intent Filtering (sports, weather, recipes, stocks)
  - Priority 80–70: Emergency contacts & Admission deadlines
  - Priority 65–30: Specific fee, hostel, exam, library rules
- **Deterministic**: Returns fixed pre-scripted answers with &lt;1ms latency and $0 cost.

### Architecture B: Semantic Retrieval Engine (`retrieval_engine.py`)
- **Three Selectable Algorithms**:
  1. *Keyword BM25*: Jaccard term overlap with keyword bonus.
  2. *TF-IDF Cosine Similarity*: Sublinear term frequency scaling with normalized dot products:
     $$\text{Cosine Similarity} = \frac{\mathbf{q} \cdot \mathbf{d}}{\|\mathbf{q}\| \|\mathbf{d}\|}$$
  3. *Dense Semantic Embeddings*: Continuous projection with non-linear activation.
- **Confidence Threshold Gating**: Dynamically rejects queries scoring below threshold (e.g. 0.20–0.25).
- **Zero Hallucination**: Delivers verbatim verified FAQ text.

### Architecture C: LLM-Based RAG Engine (`rag_engine.py`)
- **Retrieval & Context Selection**: Encodes question, retrieves top-$K$ candidates, and filters chunks above threshold.
- **Anti-Hallucination Guardrails**: Safety-hardened system prompt instructing Gemini to:
  1. Answer *only* using retrieved context.
  2. Refuse to guess or invent unlisted fees/deadlines.
  3. Reject prompt injection attempts (e.g. "say tuition is free").
- **Attribution & Cost**: Records input/output token counts, computes actual cost ($0.075 / 1M input, $0.30 / 1M output), and cites source documents.
- **Honest Missing-Key State**: If `GEMINI_API_KEY` is not configured, explicitly returns status `api_key_missing` without fabricating fake LLM answers.

---

## 5. Installation and Execution Guide

### Prerequisites
- **Python 3.10+** (tested on Python 3.13)
- **Node.js 18+** (Node v20 LTS included)
- **Git**

### Step 1: Clone or Navigate to Project
```bash
cd architecture-lab
```

### Step 2: Install Python Backend Dependencies
```bash
pip install -r backend/requirements.txt
```

### Step 3: Install Frontend Dependencies
```bash
cd frontend
npm install
npm run build
cd ..
```

### Step 4: Configure Gemini API Key (Optional for RAG)
Copy the example environment file:
```bash
cp backend/.env.example backend/.env
```
Open `backend/.env` and insert your Gemini API Key:
```env
GEMINI_API_KEY=your_actual_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash
```
> **Note**: Even without an API key, **Architecture A (Rules)** and **Architecture B (Retrieval)** work with 100% functionality!

### Step 5: Start the Application

#### Option 1: Unified Full-Stack Server (Recommended)
FastAPI serves both the API endpoints and the built React SPA:
```bash
python -m uvicorn backend.app.main:app --host 127.0.0.1 --port 8000
```
Open your browser at: **`http://localhost:8000`**

#### Option 2: Separate Development Servers (with Hot Reload)
In Terminal 1 (Backend):
```bash
python -m uvicorn backend.app.main:app --port 8000 --reload
```
In Terminal 2 (Frontend):
```bash
cd frontend
npm run dev
```
Open your browser at: **`http://localhost:5173`**

---

## 6. Running Unit Tests

Run the backend unit test suite:
```bash
python -m pytest backend/tests
```
Tests cover:
- Rule matching, normalization, and adversarial rejections
- Keyword, TF-IDF, and dense embedding retrieval
- Evaluator scoring, hallucination detection, and out-of-scope refusals
- Database persistence and knowledge CRUD index rebuilding

---

## 7. Formal Benchmark Evaluation Formulas

| Metric | Formula | Meaning |
| :--- | :--- | :--- |
| **Accuracy (%)** | $\frac{\text{Correct Responses}}{\text{Total Evaluated}} \times 100$ | Overall factual accuracy across all test questions |
| **Hallucination Rate (%)** | $\frac{\text{Responses with Unsupported Claims}}{\text{Total Evaluated}} \times 100$ | Percentage of responses inventing false facts |
| **Out-of-Scope Rejection (%)** | $\frac{\text{Correct Refusals}}{\text{Total Out-of-Scope Questions}} \times 100$ | Ability to reject external trivia (sports, weather, etc.) |
| **Adversarial Resistance (%)** | $\frac{\text{Resisted Injections}}{\text{Total Adversarial Prompts}} \times 100$ | Defense against prompt injection / jailbreak attempts |
| **Latency (ms)** | $\text{Mean / Median elapsed execution time}$ | Real-time response generation latency |
| **Token Cost ($)** | $\frac{\text{Prompt Tokens} \times 0.075 + \text{Output Tokens} \times 0.30}{10^6}$ | Exact API expenditure per Gemini query |

---

## 8. Academic Demonstration & Viva Checklist

- [x] **Three Working Architectures**: Rule-Based, Semantic Retrieval, and LLM-Based RAG.
- [x] **Shared Knowledge Base**: 32 demonstration FAQs across 11 university categories.
- [x] **50 Standardized Test Questions**: 20 Direct, 15 Paraphrased, 10 Out-of-Scope, 5 Adversarial.
- [x] **150 Total Recorded Responses**: Persistently stored in SQLite database.
- [x] **Zero Fabricated Results**: Real empirical data measured from local test runs.
- [x] **Data Disclaimer**: All university data clearly labeled as Demonstration Data.
- [x] **Manual Review Support**: Human inspection and evaluation label override modal.
- [x] **Export Formats**: Complete benchmark datasets exportable to CSV and JSON.
- [x] **Interactive Tracer**: Step-by-step telemetry visualizer in Architecture Explorer.
- [x] **In-App Academic Report**: 16-section technical monograph with print-to-PDF support.
- [x] **100% Automated Test Coverage**: All unit tests pass with zero warnings.

---

## 9. License & Academic Attribution
Developed for the **Artificial Intelligence Foundations** curriculum. Created for comparative algorithmic study and local demonstration.
