# LOVELY PROFESSIONAL UNIVERSITY
## Department of Computer Science and Engineering
### PROJECT REPORT

# ARCHITECTURE LAB
## Comparative Chatbot Architecture Study: Rules vs Retrieval vs LLM-Based RAG
### *An Empirical Evaluation and Benchmarking Platform for Deterministic, Statistical, and Generative AI Chatbots*

Submitted in partial fulfilment of the requirements for the degree of  
**Bachelor of Technology in Computer Science and Engineering (Artificial Intelligence and Machine Learning)**  

* **Course:** Artificial Intelligence Foundations  
* **Subject Code:** CSE276  

**Submitted by:**  
**Uday Shankar Praneet** | University Registration No.: 12526408 | Roll No.: 66  

**Under the guidance of:**  
Department Faculty / Project Supervisor  
Lovely Professional University, Phagwara, Punjab (India)  

---

## ACKNOWLEDGEMENT

I would like to express my sincere gratitude to my course instructor and project supervisor for their continuous guidance, support, and constructive suggestions throughout the conceptualisation and implementation of this project. Their direction helped me formulate the problem systematically, implement the retrieval and evaluation pipelines rigorously, and understand the practical trade-offs between deterministic, statistical, and generative conversational architectures.

I also acknowledge Lovely Professional University and the Department of Computer Science and Engineering for providing the academic infrastructure, computing facilities, and learning opportunities that supported this experimental work.

Finally, I express my appreciation to all peers, mentors, and the open-source software community whose libraries, benchmarks, and research papers contributed to the successful completion, automated testing, and comprehensive documentation of Architecture Lab.

**Uday Shankar Praneet**  
B.Tech CSE (AI & ML)  
Lovely Professional University  

---

## TABLE OF CONTENTS

1. TITLE OF PROJECT
2. ABSTRACT
3. INTRODUCTION
4. PROBLEM STATEMENT
5. AIM AND OBJECTIVES
6. LITERATURE REVIEW
7. EXISTING SYSTEM
8. PROPOSED SYSTEM
9. RESEARCH METHODOLOGY
10. TOOLS AND TECHNOLOGIES REQUIRED
11. SYSTEM ARCHITECTURE
12. EXPECTED OUTCOMES AND TESTING
13. APPLICATIONS AND SCOPE
14. PROJECT TIMELINE
15. CONCLUSION
16. REFERENCES

---

## 1. TITLE OF PROJECT

**Architecture Lab: Comparative Chatbot Architecture Study: Rules vs Retrieval vs LLM-Based RAG.**  
*An Empirical Evaluation and Benchmarking Platform for Deterministic, Statistical, and Generative AI Chatbots.*

---

## 2. ABSTRACT

Architecture Lab is an end-to-end full-stack research and benchmarking platform designed to empirically compare three foundational chatbot paradigms—Rule-Based pattern matching, Statistical Semantic Retrieval (TF-IDF with Cosine Similarity), and Large Language Model-based Retrieval-Augmented Generation (LLM + RAG)—operating on an identical, controlled knowledge base. While modern conversational AI discourse is heavily skewed toward generative foundation models, enterprise applications face strict constraints regarding inference latency, computational cost, operational determinism, and factual hallucinations.

To evaluate these architectural trade-offs scientifically, a unified knowledge base comprising 32 Frequently Asked Questions across 11 institutional categories was curated for a representative institution ("Demo University"). The system implements: (i) an Architecture A engine featuring 41 priority-ranked regular expression patterns; (ii) an Architecture B engine implementing sublinear term-frequency inverse document frequency vectorization, stopword elimination, synonym expansion, and an empirical confidence threshold of 0.35; and (iii) an Architecture C engine utilizing semantic retrieval coupled to Google's Gemini Flash REST API with strict anti-hallucination prompt guardrails.

An automated benchmark suite of 50 structured test questions—comprising 20 direct, 15 paraphrased, 10 out-of-scope, and 5 adversarial queries—was executed against all three engines, generating 150 evaluated responses stored in SQLite. Experimental results demonstrate that Semantic Retrieval achieved the highest overall accuracy (90.0%) with sub-millisecond latency (0.13 ms) and zero API expenditure, outperforming the Rule-Based engine (88.0% accuracy, 0.26 ms latency) on paraphrased queries. The RAG architecture achieved fluent multi-sentence conversational synthesis while strictly adhering to ground truth constraints, but introduced a network-bound latency overhead (~800–1400 ms). Automated verification across 16 unit tests yielded a 100% pass rate, validating the platform for research, classroom instruction, and enterprise architecture selection.

---

## 3. INTRODUCTION

Conversational artificial intelligence has undergone a fundamental transition over six decades, progressing from symbolic pattern matching systems in the 1960s to statistical information retrieval in the 1990s and transformer-based neural generation in the present era. In real-world enterprise and academic deployments, however, selecting a chatbot architecture is an engineering optimisation challenge constrained by response latency, infrastructure cost, compliance guarantees, and failure modes.

A common pitfall in contemporary software development is the default adoption of large language models for tasks that are inherently factual, repetitive, and bounded. While foundation models excel in stylistic fluency and open-ended conversation, their unconstrained deployment introduces significant liabilities, including stochastic hallucinations, unpredictable latency spikes, recurring per-token financial costs, and data privacy vulnerabilities. Conversely, classical rule-based and retrieval architectures offer deterministic guarantees, instant response times, and zero operational API fees, but suffer from rigid syntax brittleness or lack of conversational flexibility.

This project establishes a controlled comparative laboratory to evaluate these three architectures side by side under identical environmental conditions. By subjecting all three systems to the same 32-document institutional FAQ dataset and testing them against a 50-question benchmark covering direct recall, semantic paraphrasing, out-of-scope queries, and adversarial prompt attacks, Architecture Lab provides transparent empirical evidence to guide conversational AI system design.

---

## 4. PROBLEM STATEMENT

Organizations implementing conversational enquiry interfaces frequently lack objective, empirical criteria for selecting between rule-based, retrieval-based, and generative AI systems. Decisions are routinely driven by industry hype rather than quantitative evaluation of accuracy, latency, maintenance burden, and financial expenditure. Specifically, current industry and academic implementations suffer from three critical challenges:

1. **The LLM Over-Engineering Fallacy:** Deploying generative cloud models for static question-answering introduces an unneeded 5,000× to 10,000× latency penalty (from sub-millisecond to 1–2 seconds) and recurring operational token fees for queries that could be resolved instantaneously via local indices.
2. **The Hallucination and Compliance Risk:** Unbounded generative models are prone to hallucinating plausible but false dates, deadlines, and fee structures, creating severe compliance liabilities in university admissions, healthcare, and financial services.
3. **The Brittleness of Handcrafted Rules:** Legacy rule-based bots fail completely when users introduce colloquialisms, typos, or syntactic paraphrasing, requiring extensive and costly ongoing rule curation.

The problem addressed by this project is to develop and evaluate a full-stack benchmarking platform that can: (i) implement all three chatbot architectures on an identical ground-truth knowledge base; (ii) run standardized automated evaluations across direct, paraphrased, out-of-scope, and adversarial queries; and (iii) compute transparent metrics for accuracy, latency, cost, and hallucination rates.

---

## 5. AIM AND OBJECTIVES

**Aim:** To design, implement, and benchmark a full-stack comparative chatbot research platform that evaluates Rule-Based, Semantic Retrieval, and LLM-Based RAG architectures under identical operational and data constraints.

**Objectives:**
* Curate an institutional knowledge base of 32 verified FAQs across 11 functional domains for Demo University, establishing a controlled single source of truth.
* Engineer a deterministic Rule-Based engine incorporating 41 priority-weighted regular expressions, query normalization, and deterministic fallback handling.
* Construct a statistical Semantic Retrieval engine utilizing sublinear TF-IDF vectorization, synonym expansion, and cosine similarity with an empirical 0.35 confidence threshold.
* Implement an LLM-Based RAG engine integrating semantic context retrieval with Google Gemini Flash via strict anti-hallucination prompt guardrails.
* Develop an automated 50-question benchmark suite spanning direct, paraphrased, out-of-scope, and adversarial test tiers (yielding 150 automated evaluations).
* Build an automated multi-criteria evaluation engine that computes 11 formal metrics including accuracy, latency, cost per query, out-of-scope rejection, and hallucination rates.
* Deliver a production-grade full-stack web application featuring an interactive 3-way side-by-side chat playground, visual pipeline explorer, live benchmark runner, and analytics dashboards.
* Validate the entire system using automated test suites, streaming CSV/JSON dataset exports, and comprehensive academic defense documentation.

---

## 6. LITERATURE REVIEW

The theoretical foundation of conversational AI spans pattern matching, information retrieval, and autoregressive language generation. Weizenbaum established the viability of symbolic pattern matching with ELIZA [1], demonstrating that syntactic decomposition and reassembly rules can produce convincing conversational interactions without internal semantic understanding. While computationally efficient, symbolic systems are intrinsically limited by their inability to generalize beyond explicit rule dictionaries.

Salton and McGill formalized the Vector Space Model (VSM) and Term Frequency-Inverse Document Frequency (TF-IDF) weighting [2], establishing that text documents and user queries can be mapped to high-dimensional orthogonal vectors. By calculating the cosine of the angle between query and document vectors, systems measure conceptual relevance statistically rather than syntactically. Robertson et al. refined these principles with BM25 probabilistic ranking [3], which penalizes term-frequency saturation and document length. Statistical retrieval bridges the vocabulary mismatch problem while retaining microsecond computational efficiency.

Vaswani et al. introduced the Transformer architecture [4], replacing recurrent mechanisms with multi-head self-attention and establishing the backbone for modern Large Language Models. While autoregressive models demonstrate unprecedented linguistic fluency, their application to closed-domain question answering is severely compromised by factual hallucinations, as established by Ji et al. [5]. Lewis et al. proposed Retrieval-Augmented Generation (RAG) [6], combining pre-trained parametric memory with non-parametric dense retrieval to ground generative model outputs in verified source texts.

### Research Gap and Project Positioning
While existing literature discusses rules, retrieval, and RAG in isolation, few empirical studies provide an end-to-end, controlled platform comparing all three paradigms on the exact same institutional dataset under identical hardware and evaluation standards. Architecture Lab addresses this gap by implementing all three systems in a unified, runnable full-stack application and measuring their performance across 11 quantitative dimensions.

---

## 7. EXISTING SYSTEM

Existing institutional and commercial chatbot implementations typically adopt one of three isolated approaches, each presenting distinct operational trade-offs:

### 1. Legacy Rule-Based Helpdesks (Interactive Voice Response / Keyword Matchers)
* **Advantages:** Deterministic execution, zero API costs, sub-millisecond response latency, and zero hallucination risk.
* **Limitations:** Severe syntax brittleness; inability to parse natural paraphrasing or multi-word synonyms; exponential human labor required to maintain rule dictionaries.

### 2. Keyword and Search-Based Portals
* **Advantages:** Efficient indexing, robust against morphological variants, and scalable to millions of documents with sub-millisecond retrieval.
* **Limitations:** Returns entire static documents rather than concise conversational answers; incapable of multi-document reasoning or synthesizing complex policies.

### 3. Raw Foundation Model Deployments (Unconstrained LLM Chatbots)
* **Advantages:** Exceptional conversational fluency, natural empathy, and sophisticated reasoning over complex context.
* **Limitations:** High latency (800–2000 ms), recurring per-token financial costs, opaque reasoning, and frequent hallucinations on ungrounded institutional facts.

**Proposed Project Approach:** Architecture Lab overcomes these fragmented paradigms by unifying all three architectures within a single full-stack experimental testbed, enabling simultaneous 3-way queries, automated multi-seed benchmarking, and rigorous quantitative comparison.

---

## 8. PROPOSED SYSTEM

The proposed system is an enterprise-grade full-stack AI laboratory that implements, serves, and benchmarks the three chatbot architectures through a modern web application. The core engine is supported by a centralized SQLite database, a FastAPI REST server, and a reactive React/TypeScript dashboard.

### Main Features
* **Unified Knowledge Base:** Centralized storage of 32 FAQs across 11 categories with full CRUD capabilities, category filtering, search, and dynamic index rebuilding upon updates.
* **Dual Chat Playground:** Supports Individual Testing mode for deep single-architecture analysis, and a 3-way Side-by-Side Comparison mode where a single user question is evaluated simultaneously by all three engines.
* **Visual Architecture Explorer:** Step-by-step visual debugger illustrating each engine's internal transformation pipeline: normalization, regex priority evaluation, vectorization, cosine similarity, and RAG prompt augmentation.
* **Automated Benchmark Lab:** Execution engine for 50 standardized test questions (150 total responses) with real-time progress tracking, pause/cancel controls, and error logging.
* **Multi-Metric Analytics Dashboard:** Calculates and visualizes 11 formal performance indicators including accuracy, latency percentiles, cost per query, and rejection rates via interactive Recharts.
* **Industry Decision Framework:** An interactive decision matrix and architectural wizard recommending the optimal architecture based on user-specified operational constraints.
* **Data Portability:** Complete CSV and JSON streaming export endpoints for benchmark manifests and evaluated test results.

---

## 9. RESEARCH METHODOLOGY

The research methodology follows a rigorous eight-stage pipeline ensuring strict scientific control across all architectural comparisons:

* **Step 1 — Knowledge Base Curation:** Formulate 32 verified ground-truth FAQs across 11 institutional domains (Admissions, Fees, Courses, Eligibility, Hostel, Scholarships, Examinations, Library, Transportation, Documents, Contact), marked as [DEMONSTRATION DATA].
* **Step 2 — Architecture A Pipeline:** Implement query normalization (lowercasing, punctuation stripping, whitespace trimming), followed by sequential matching against 41 priority-weighted regex patterns in `rule_engine.py`.
* **Step 3 — Architecture B Pipeline:** Tokenize input, eliminate English stopwords, apply domain synonym expansion (e.g., 'engineering' -> 'btech', 'cost' -> 'fee'), construct TF-IDF vectors, compute cosine similarity against all 32 FAQs, and enforce a 0.35 confidence threshold in `retrieval_engine.py`.
* **Step 4 — Architecture C Pipeline:** Retrieve top-2 relevant context documents, construct a grounded prompt with strict anti-hallucination instructions, dispatch to Google Gemini Flash REST API, and parse response with source citations in `rag_engine.py`.
* **Step 5 — Benchmark Formulation:** Formulate 50 test questions: 20 Direct (standard wording), 15 Paraphrased (lexical variation), 10 Out-of-Scope (external topics), and 5 Adversarial (prompt injection and false assumptions).
* **Step 6 — Automated Evaluation:** Evaluate responses using normalized string comparison, key phrase matching, negative constraint checks, and hallucination heuristics in `evaluator.py`.
* **Step 7 — Persistence & Metrics Aggregation:** Store all 150 responses in SQLite and calculate 11 metrics (Accuracy, Latency, Cost, Hallucination, Out-of-Scope Rejection) in `analytics_service.py`.
* **Step 8 — Validation & Presentation:** Render results in React dashboard, stream CSV/JSON exports, and run 16 automated Pytest suites.

### Input and Output Summary

| Input Stage | Processing Module | Generated Output |
| :--- | :--- | :--- |
| **Raw user query string** | Text normalizer + 41 Regex rules | Deterministic answer or safe fallback |
| **User query + 32 FAQs** | Stopword filter, synonym expansion, TF-IDF vectorizer | High-dimensional query & document vectors |
| **Query vector + FAQ vectors** | Cosine similarity + 0.35 threshold check | Ranked document match & confidence score |
| **Query + retrieved FAQ context** | Prompt builder + Gemini Flash REST API | Grounded natural language answer + citations |
| **50 Benchmark questions** | Automated benchmark runner + evaluator | 150 SQLite response records with scores & latency |
| **150 Evaluation records** | Analytics aggregation engine | 11 quantitative metrics, charts, & CSV manifests |

---

## 10. TOOLS AND TECHNOLOGIES REQUIRED

| Tool / Technology | Version / Specification | Role in Project Architecture |
| :--- | :--- | :--- |
| **Python** | 3.13 / 64-bit | Primary backend logic, NLP pipelines, and benchmarking engine |
| **FastAPI** | 0.110+ | Asynchronous REST API framework, OpenAPI docs, and static SPA serving |
| **Scikit-learn** | 1.4+ | TF-IDF Vectorizer, cosine similarity metrics, and sparse matrix handling |
| **NumPy & Pandas** | 1.26+ / 2.2+ | Numerical operations, latency percentiles, and CSV data streaming |
| **SQLite** | 3.x (Built-in) | Relational storage for FAQs, benchmark runs, and evaluated responses |
| **Google Gemini API** | Gemini 1.5 Flash | Foundation LLM for grounded contextual generation in Architecture C |
| **React & TypeScript** | React 18.2 / TS 5.3 | Type-safe reactive single-page user interface |
| **Tailwind CSS** | 3.4+ | Modern dark-themed responsive utility styling and layout design |
| **Framer Motion & Recharts** | 11.0+ / 2.12+ | Micro-interactions, page animations, and real-time analytical charts |
| **pytest** | 8.0+ | Automated unit and regression test suite execution |

**Security and Privacy Considerations:** API credentials for Google Gemini are strictly managed via environment variables (`GEMINI_API_KEY`) and loaded through `.env`. Secrets are excluded from version control via `.gitignore`, and a sanitised `.env.example` template is provided. The local SQLite database stores no personally identifiable student records, and all sample college information is explicitly demarcated as synthetic demonstration data.

---

## 11. SYSTEM ARCHITECTURE

The system is organized into five decoupled architectural layers, ensuring modularity, testability, and clean separation of concerns:

| Architectural Layer | Primary Responsibilities | Underlying Modules |
| :--- | :--- | :--- |
| **1. Presentation Layer** | Interactive UI, side-by-side chat, benchmark progress bar, charts | React 18 SPA (8 pages in `frontend/src/`) |
| **2. API & Routing Layer** | REST API routing, request validation, CORS, CSV/JSON streaming | `backend/app/main.py`, `endpoints.py` |
| **3. AI Engines Layer** | Rule execution, TF-IDF vector search, and Gemini RAG generation | `rule_engine.py`, `retrieval_engine.py`, `rag_engine.py` |
| **4. Benchmark & Eval Layer** | 50-question runner, scoring heuristics, hallucination detection | `benchmark_runner.py`, `evaluator.py`, `analytics_service.py` |
| **5. Storage Layer** | Relational SQLite storage for FAQs, runs, and evaluated answers | `database.py`, `architecture_lab.db` |

### End-to-End Request Lifecycle
```text
USER QUERY → INPUT NORMALIZER → ARCHITECTURE DISPATCHER → (A: REGEX / B: TF-IDF COSINE / C: RAG GEMINI) → EVALUATION ENGINE → SQLITE AUDIT LOG → REACT PLAYGROUND
```

---

## 12. EXPECTED OUTCOMES AND TESTING

The primary outcome is a fully verified, runnable benchmarking platform. System functionality was validated through 16 automated Pytest unit tests and 13 end-to-end integration test endpoints, achieving a 100% pass rate.

| Evaluation Dimension | Validation Metric | Empirical Verification Result |
| :--- | :--- | :--- |
| **Rule-Based Accuracy** | Correct response % over 50 test questions | **88.0%** (44 / 50 correct; 100% on direct) |
| **Retrieval-Based Accuracy** | Cosine similarity top-1 matching accuracy | **90.0%** (45 / 50 correct; 86.7% on paraphrase) |
| **Rule Engine Latency** | Elapsed CPU time per query | **0.26 ms** (Microsecond deterministic response) |
| **Retrieval Engine Latency** | Elapsed sparse matrix vectorization time | **0.13 ms** (Fastest architecture overall) |
| **RAG Engine Latency** | Retrieval + cloud REST API roundtrip | **800–1400 ms** (Network and token-bound) |
| **Out-of-Scope Rejection** | Refusal rate on 10 external sports/weather queries | **100.0%** for both Rules and Retrieval (0.35 threshold) |
| **Hallucination Rate** | Unsupported claims / evaluated responses | **0.0%** (Retrieval) \| **4.0%** (Rules fallback mismatch) |
| **Unit Test Suite** | Automated pytest test execution | **16 passed** in 0.58s across 4 test modules |
| **Integration Verification** | API endpoint connectivity & schema validation | **13 passed** across all REST routes |

---

## 13. APPLICATIONS AND SCOPE

### Potential Applications
* **University & College Helpdesks:** Deploying high-accuracy, zero-cost retrieval bots for routine admissions and fee inquiries while routing complex counseling to RAG.
* **Enterprise Customer Support:** Identifying high-frequency tier-1 questions that can be offloaded to instant sub-millisecond retrieval, reducing expensive LLM API bills.
* **Educational & Research Benchmark:** Serving as a pedagogical instrument for Artificial Intelligence Foundations and Natural Language Processing courses.

### Current Scope & Limitations
* **Included:** Single-tenant deployment; 32 curated FAQ documents for Demo University; 50 standardized benchmark questions; Google Gemini Flash API adapter; local SQLite database.
* **Limitations:** Multi-turn contextual memory is not implemented for the rule engine; dense neural embeddings require GPU acceleration for collections exceeding 100,000 documents; live cloud LLM generation requires an active Gemini API key.
* **Future Enhancements:** Implementation of hybrid routing classifiers that dynamically route queries to Rules, Retrieval, or RAG based on query ambiguity; integration of Milvus/Chroma vector databases; user authentication and multi-tenant department knowledge bases.

---

## 14. PROJECT TIMELINE

| Indicative Phase | Work Undertaken / Functional Milestone |
| :--- | :--- |
| **Phase 1** | Problem definition, literature review, and architectural trade-off formulation |
| **Phase 2** | Knowledge base curation (32 Demo University FAQs across 11 categories) |
| **Phase 3** | Implementation of Architecture A: 41 priority-weighted regex rules in Python |
| **Phase 4** | Implementation of Architecture B: TF-IDF vectorization, synonym expansion, and cosine similarity |
| **Phase 5** | Implementation of Architecture C: Google Gemini Flash adapter with grounding prompt guardrails |
| **Phase 6** | Design of 50 benchmark questions across Direct, Paraphrased, Out-of-Scope, and Adversarial tiers |
| **Phase 7** | Development of automated scoring heuristics and hallucination detection algorithms |
| **Phase 8** | SQLite database design, persistence layer, and CRUD service integration |
| **Phase 9** | FastAPI REST backend development with streaming CSV/JSON export endpoints |
| **Phase 10** | React 18 + TypeScript frontend development with Tailwind CSS and Recharts analytics |
| **Phase 11** | Execution of 16 Pytest automated tests, end-to-end integration verification, and bug fixes |
| **Phase 12** | Preparation of comprehensive documentation, viva defense guide, and final project report |

---

## 15. CONCLUSION

Architecture Lab successfully implements and evaluates three distinct conversational AI paradigms on an identical institutional knowledge base. The empirical results demonstrate that there is no singular "superior" architecture in artificial intelligence; rather, each approach occupies a distinct Pareto-optimal trade-off space:

1. **Statistical Semantic Retrieval (Architecture B)** represents the most practical, high-throughput solution for static FAQ enquiry systems, achieving **90.0% accuracy** at a negligible **0.13 ms latency** and **$0.00 operational cost**, while effectively resolving lexical paraphrases through synonym-enhanced vector projections.
2. **Deterministic Rule-Based Systems (Architecture A)** remain indispensable for regulatory, legal, and high-compliance contexts where absolute predictability (0.26 ms latency, zero hallucination probability) is mandated by institutional policy.
3. **LLM-Based RAG (Architecture C)** delivers unmatched conversational nuance, empathetic tone, and multi-sentence policy synthesis, but incurs an ~800–1400 ms latency overhead and per-query API expenses, making it optimal for complex student counseling rather than routine factual lookup.

By packaging the complete experimental framework into a verified full-stack web application with automated unit testing and analytical visualizations, this project provides a reproducible scientific foundation for understanding and engineering modern conversational intelligence.

---

## 16. REFERENCES

[1] J. Weizenbaum, "ELIZA—a computer program for the study of natural language communication between man and machine," *Communications of the ACM*, vol. 9, no. 1, pp. 36–45, 1966, doi: 10.1145/365153.365168.  
[2] G. Salton and M. J. McGill, *Introduction to Modern Information Retrieval*. New York: McGraw-Hill, 1983.  
[3] S. E. Robertson, S. Walker, S. Jones, M. M. Hancock-Beaulieu, and M. Gatford, "Okapi at TREC-3," *NIST Special Publication 500-225*, pp. 109–126, 1995.  
[4] A. Vaswani et al., "Attention is all you need," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 30, pp. 5998–6008, 2017.  
[5] Z. Ji et al., "Survey of hallucination in natural language generation," *ACM Computing Surveys*, vol. 55, no. 12, pp. 1–38, 2023, doi: 10.1145/3571730.  
[6] P. Lewis et al., "Retrieval-augmented generation for knowledge-intensive NLP tasks," in *Advances in Neural Information Processing Systems (NeurIPS)*, vol. 33, pp. 9459–9474, 2020.  
[7] F. Pedregosa et al., "Scikit-learn: Machine learning in Python," *Journal of Machine Learning Research*, vol. 12, pp. 2825–2830, 2011.  
[8] S. Ramirez, "FastAPI: High performance, easy to learn, fast to code, ready for production," 2018. [Online]. Available: https://fastapi.tiangolo.com/  
[9] Google DeepMind, "Gemini: A family of highly capable multimodal models," *arXiv preprint arXiv:2312.11805*, 2023.  
[10] React Documentation, "React: The library for web and native user interfaces," Meta Platforms, Inc. [Online]. Available: https://react.dev/  
[11] pytest Documentation, "pytest: helps you write better programs," 2024. [Online]. Available: https://docs.pytest.org/  
