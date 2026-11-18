import os
import shutil
from reportlab.lib.pagesizes import A4
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, Image, KeepTogether
)
from reportlab.pdfgen import canvas

A4_WIDTH, A4_HEIGHT = A4 # 595.2756, 841.8898

class ExactCanvas(canvas.Canvas):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_footer(num_pages)
            super().showPage()
        super().save()

    def draw_footer(self, total_pages):
        self.saveState()
        self.setFont("Times-Roman", 7.994)
        self.setFillColor(colors.HexColor("#555555"))
        # Footer text left at x=51.0, y=29.9
        self.drawString(51.0, 29.9, "Artificial Intelligence Foundations | CSE276")
        # Footer page number right at x=540.3, y=29.9
        self.drawRightString(545.0, 29.9, str(self._pageNumber))
        self.restoreState()

def build_pdf():
    pdf_path = r"C:\Users\Uday Shankar Praneet\.gemini\antigravity\scratch\architecture-lab\PROJECT_REPORT_EXACT.pdf"
    
    # Margins matching reference: left=57, right=57, top=65, bottom=50
    doc = SimpleDocTemplate(
        pdf_path,
        pagesize=A4,
        leftMargin=57.0,
        rightMargin=57.0,
        topMargin=60.0,
        bottomMargin=45.0
    )

    PRIMARY_COLOR = colors.HexColor("#1f3750") # Deep navy table header from reference PDF
    BORDER_GRAY = colors.HexColor("#808080")   # Gray 50% border from reference PDF
    ALT_ROW = colors.HexColor("#f8fafc")       # Subtle alternating row

    # Paragraph Styles exactly matching reference fonts and leading
    p_section_title = ParagraphStyle(
        'SectionTitle',
        fontName='Times-Bold',
        fontSize=14.0,
        leading=18.0,
        textColor=colors.black,
        spaceBefore=14.0,
        spaceAfter=5.0,
        keepWithNext=True
    )

    p_body = ParagraphStyle(
        'ExactBody',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.0,
        textColor=colors.black,
        spaceAfter=4.5,
        alignment=4 # Justify
    )

    p_body_left = ParagraphStyle(
        'ExactBodyLeft',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.0,
        textColor=colors.black,
        spaceAfter=4.5,
        alignment=0 # Left
    )

    p_bullet = ParagraphStyle(
        'ExactBullet',
        fontName='Times-Roman',
        fontSize=9.5,
        leading=13.0,
        textColor=colors.black,
        leftIndent=14.0,
        firstLineIndent=-10.0,
        spaceAfter=2.5,
        alignment=4 # Justify
    )

    p_subhead = ParagraphStyle(
        'ExactSubhead',
        fontName='Times-Bold',
        fontSize=9.5,
        leading=13.0,
        textColor=colors.black,
        spaceBefore=6.0,
        spaceAfter=3.0,
        keepWithNext=True
    )

    th_style = ParagraphStyle(
        'TableHead',
        fontName='Times-Bold',
        fontSize=9.0,
        leading=12.0,
        textColor=colors.white,
        alignment=0
    )

    td_style = ParagraphStyle(
        'TableData',
        fontName='Times-Roman',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.black,
        alignment=0
    )

    td_bold = ParagraphStyle(
        'TableDataBold',
        fontName='Times-Bold',
        fontSize=8.5,
        leading=11.5,
        textColor=colors.black,
        alignment=0
    )

    story = []

    # ==========================================================
    # PAGE 1: TITLE PAGE (Matching Reference PDF exactly)
    # ==========================================================
    logo_path = r"C:\Users\Uday Shankar Praneet\.gemini\antigravity\scratch\architecture-lab\scratch\extracted_imgs\Im43.png"
    if os.path.exists(logo_path):
        # 304.157 pt x 108.964 pt
        story.append(Spacer(1, 15))
        img = Image(logo_path, width=280, height=100)
        img.hAlign = 'CENTER'
        story.append(img)
        story.append(Spacer(1, 20))
    else:
        story.append(Spacer(1, 40))
        story.append(Paragraph("LOVELY PROFESSIONAL UNIVERSITY", ParagraphStyle('LPU', fontName='Times-Bold', fontSize=18, alignment=1)))
        story.append(Spacer(1, 40))

    story.append(Paragraph("PROJECT REPORT", ParagraphStyle('PR', fontName='Times-Bold', fontSize=18.0, alignment=1, spaceAfter=18.0)))
    
    story.append(Paragraph("ARCHITECTURE LAB: COMPARATIVE CHATBOT ARCHITECTURE STUDY", ParagraphStyle('PTitle', fontName='Times-Bold', fontSize=16.0, leading=20.0, alignment=1)))
    story.append(Spacer(1, 6))
    story.append(Paragraph("A Comparative Evaluation of Rule-Based, Semantic Retrieval and LLM-Based RAG Systems Using an Institutional FAQ Knowledge Base", ParagraphStyle('PSub', fontName='Times-Italic', fontSize=10.0, leading=14.0, alignment=1)))
    story.append(Spacer(1, 45))

    story.append(Paragraph("Submitted in partial fulfilment of the requirements for the degree of", ParagraphStyle('SubReq', fontName='Times-Roman', fontSize=9.0, alignment=1)))
    story.append(Spacer(1, 4))
    story.append(Paragraph("Bachelor of Technology", ParagraphStyle('BTech', fontName='Times-Bold', fontSize=9.0, alignment=1)))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Computer Science and Engineering (Artificial Intelligence and Machine Learning)", ParagraphStyle('Dept', fontName='Times-Roman', fontSize=9.0, alignment=1)))
    story.append(Spacer(1, 35))

    story.append(Paragraph("Course: Artificial Intelligence Foundations", ParagraphStyle('CName', fontName='Times-Bold', fontSize=9.0, alignment=1)))
    story.append(Spacer(1, 2))
    story.append(Paragraph("Subject Code: CSE276", ParagraphStyle('CCode', fontName='Times-Bold', fontSize=9.0, alignment=1)))
    story.append(Spacer(1, 35))

    story.append(Paragraph("Submitted by", ParagraphStyle('SubBy', fontName='Times-Bold', fontSize=9.0, alignment=1)))
    story.append(Spacer(1, 5))
    story.append(Paragraph("Lakshay Parashar &nbsp;|&nbsp; University Registration No.: 12523688 &nbsp;|&nbsp; Roll No.: 40", ParagraphStyle('S1', fontName='Times-Roman', fontSize=9.0, alignment=1)))
    story.append(Paragraph("Rishabh Pandey &nbsp;|&nbsp; University Registration No.: 12523544 &nbsp;|&nbsp; Roll No.: 41", ParagraphStyle('S2', fontName='Times-Roman', fontSize=9.0, alignment=1)))
    story.append(Paragraph("Uday Shankar Praneet &nbsp;|&nbsp; University Registration No.: 12524685 &nbsp;|&nbsp; Roll No.: 42", ParagraphStyle('S3', fontName='Times-Roman', fontSize=9.0, alignment=1)))
    story.append(Spacer(1, 40))

    story.append(Paragraph("Under the guidance of", ParagraphStyle('UnderG', fontName='Times-Bold', fontSize=9.0, alignment=1)))
    story.append(Spacer(1, 3))
    story.append(Paragraph("Ms. Priyanshi Saxena", ParagraphStyle('GName', fontName='Times-Roman', fontSize=9.0, alignment=1)))
    story.append(Spacer(1, 40))

    story.append(Paragraph("Lovely Professional University", ParagraphStyle('UnivBottom', fontName='Times-Roman', fontSize=9.0, alignment=1)))
    story.append(PageBreak())

    # ==========================================================
    # PAGE 2: ACKNOWLEDGEMENT (Exact Layout)
    # ==========================================================
    story.append(Paragraph("ACKNOWLEDGEMENT", ParagraphStyle('AckTitle', fontName='Times-Bold', fontSize=14.0, leading=18.0, spaceAfter=14.0)))
    story.append(Paragraph(
        "We would like to express our sincere gratitude to Ms. Priyanshi Saxena for her guidance, support and valuable suggestions "
        "during the development of this project. Her direction helped us approach the problem systematically and improve our "
        "understanding of natural language processing, semantic retrieval, and large language model architectures.",
        p_body
    ))
    story.append(Spacer(1, 4))
    story.append(Paragraph(
        "We also acknowledge Lovely Professional University and the Department of Computer Science and Engineering for providing "
        "the academic environment and learning opportunities that supported this work. Finally, we thank all group members for their "
        "contributions to the planning, implementation, testing and documentation of the Architecture Lab Comparative Chatbot Study.",
        p_body
    ))
    story.append(PageBreak())

    # ==========================================================
    # PAGE 3: TABLE OF CONTENTS (Exact Layout)
    # ==========================================================
    story.append(Paragraph("TABLE OF CONTENTS", ParagraphStyle('TOCTitle', fontName='Times-Bold', fontSize=14.0, leading=18.0, spaceAfter=14.0)))

    toc_list = [
        ("1. TITLE OF PROJECT", "4"),
        ("2. ABSTRACT", "4"),
        ("3. INTRODUCTION", "4"),
        ("4. PROBLEM STATEMENT", "4"),
        ("5. AIM AND OBJECTIVES", "5"),
        ("6. LITERATURE REVIEW", "5"),
        ("7. EXISTING SYSTEM", "5"),
        ("8. PROPOSED SYSTEM", "6"),
        ("9. RESEARCH METHODOLOGY", "7"),
        ("10. TOOLS AND TECHNOLOGIES REQUIRED", "8"),
        ("11. SYSTEM ARCHITECTURE", "8"),
        ("12. EXPECTED OUTCOMES AND TESTING", "9"),
        ("13. APPLICATIONS AND SCOPE", "9"),
        ("14. PROJECT TIMELINE", "10"),
        ("15. CONCLUSION", "10"),
        ("16. REFERENCES", "11"),
    ]

    toc_data = []
    for title_txt, pg in toc_list:
        toc_data.append([
            Paragraph(title_txt, td_bold),
            Paragraph(pg, ParagraphStyle('TOCPg', parent=td_style, alignment=2))
        ])

    toc_t = Table(toc_data, colWidths=[420, 61.28])
    toc_t.setStyle(TableStyle([
        ('VALIGN', (0,0), (-1,-1), 'MIDDLE'),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('LEFTPADDING', (0,0), (-1,-1), 0),
        ('RIGHTPADDING', (0,0), (-1,-1), 0),
    ]))
    story.append(toc_t)
    story.append(PageBreak())

    # ==========================================================
    # PAGE 4: SECTIONS 1, 2, 3, 4 (Exact Layout)
    # ==========================================================
    story.append(Paragraph("1. TITLE OF PROJECT", p_section_title))
    story.append(Paragraph(
        "Architecture Lab: Comparative Chatbot Architecture Study: Rules vs Retrieval vs LLM-Based RAG.",
        p_body
    ))

    story.append(Paragraph("2. ABSTRACT", p_section_title))
    story.append(Paragraph(
        "The Architecture Lab is a software system designed to assist educational institutions and enterprise developers in evaluating "
        "and selecting conversational enquiry architectures. The system combines pattern matching, information retrieval and generative "
        "large language models to process user queries, estimate similarity against an institutional knowledge base, construct grounded "
        "responses and compare alternative conversational architectures.",
        p_body
    ))
    story.append(Paragraph(
        "The rule-processing module uses regular expressions and priority weighting to identify direct factual enquiries across institutional domains. "
        "Patterns are matched against normalized user strings to execute deterministic lookup. The retrieval module uses sublinear TF-IDF vectorization "
        "and cosine similarity to search an institutional FAQ collection, then applies an empirical confidence threshold of 0.35 to verify answer relevance.",
        p_body
    ))
    story.append(Paragraph(
        "The generative module models conversational question answering as a Retrieval-Augmented Generation (RAG) pipeline. It combines "
        "semantic search with Google's Gemini Flash model to synthesize natural language answers from retrieved context. Schedule simulation accounts "
        "for response latency, operational API token cost, hallucination detection, out-of-scope rejection and setup maintenance effort. A React web "
        "interface and a FastAPI REST service are included in the project source.",
        p_body
    ))
    story.append(Paragraph(
        "The source repository includes automated tests for rule, retrieval, evaluator and benchmark modules. Running the listed test modules in "
        "the supplied project archive produced 16 passing tests. The software also includes 50-question multi-tier benchmarking and analytics "
        "visualisation functionality; numerical comparative performance results demonstrate 88.0% accuracy for rules and 90.0% accuracy for semantic retrieval.",
        p_body
    ))

    story.append(Paragraph("3. INTRODUCTION", p_section_title))
    story.append(Paragraph(
        "Conversational AI systems serve as primary communication interfaces between organizations and end users. This interaction involves "
        "diverse user queries and can become operationally difficult when questions use colloquial phrasing and organizations have strict factual constraints.",
        p_body
    ))
    story.append(Paragraph(
        "A response that appears fluent may be impractical if it hallucinates non-existent college policies or incorrect fee amounts. "
        "Similarly, a rule-based engine with low latency may still perform poorly if a student expresses their query with unanticipated vocabulary. A "
        "useful enquiry system therefore needs to consider both the linguistic flexibility of the model and the factual constraints associated "
        "with institutional policies.",
        p_body
    ))
    story.append(Paragraph(
        "This project addresses the problem by treating the FAQ database as a controlled knowledge base. Text pre-processing normalizes user queries, "
        "while vectorization extracts statistical term weights. Cosine similarity is then applied to the FAQ collection to estimate semantic relevance. "
        "These distances and context snippets are passed to an LLM prompt builder, which compares different retrieval and generation paradigms.",
        p_body
    ))
    story.append(Paragraph(
        "The system is intended as a decision-support prototype. It allows a user to explore individual architectures or run side-by-side comparisons, "
        "execute standardized 50-question benchmarks, and inspect comparative metrics through an interactive graphical interface.",
        p_body
    ))

    story.append(Paragraph("4. PROBLEM STATEMENT", p_section_title))
    story.append(Paragraph(
        "Educational institutions may deploy conversational chatbots manually or rely on generative models that do not ground responses in verified policies. "
        "Manual planning becomes harder as the number of student queries increases, particularly when each inquiry requires strict policy adherence. A generative "
        "chatbot may fabricate tuition fees or deadlines if unconstrained, or may incur avoidable latency and API expense if simple queries are routed to massive LLMs.",
        p_body
    ))
    story.append(Paragraph(
        "The problem addressed by this project is to develop a system that can: (i) ingest a verified 32-document institutional FAQ database; (ii) implement "
        "deterministic rule matching, statistical vector retrieval, and LLM-based RAG under identical constraints; (iii) evaluate response latency and "
        "factual accuracy; and (iv) determine and compare architectural trade-offs using a standardized 50-question benchmark suite.",
        p_body
    ))
    story.append(PageBreak())

    # ==========================================================
    # PAGE 5: SECTIONS 4(cont), 5, 6, 7 (Exact Layout)
    # ==========================================================
    story.append(Paragraph(
        "The system uses a single-institution FAQ knowledge base model. It is not presented as a live multi-tenant university enterprise system, an "
        "unbounded open-web search crawler or an automated admissions transactional portal.",
        p_body
    ))

    story.append(Paragraph("5. AIM AND OBJECTIVES", p_section_title))
    story.append(Paragraph(
        "<b>Aim:</b> To develop a comparative chatbot benchmarking prototype that combines rule-based pattern matching, statistical semantic retrieval "
        "and LLM-based RAG optimisation.",
        p_body
    ))
    story.append(Paragraph("<b>Objectives:</b>", p_subhead))
    story.append(Paragraph("• Curate an institutional knowledge base of 32 verified FAQs across 11 categories for Demo University.", p_bullet))
    story.append(Paragraph("• Engineer a deterministic rule engine incorporating 41 priority-weighted regular expression patterns.", p_bullet))
    story.append(Paragraph("• Implement a statistical retrieval engine using TF-IDF vectorization, synonym expansion, and cosine similarity.", p_bullet))
    story.append(Paragraph("• Establish an empirical confidence threshold of 0.35 to reject out-of-scope inquiries reliably.", p_bullet))
    story.append(Paragraph("• Integrate an LLM-based RAG pipeline using Google's Gemini Flash model with anti-hallucination prompt guardrails.", p_bullet))
    story.append(Paragraph("• Implement and compare three chatbot architectures across direct, paraphrased, out-of-scope, and adversarial queries.", p_bullet))
    story.append(Paragraph("• Provide interactive interfaces for single-architecture testing, 3-way side-by-side comparison, and analytics.", p_bullet))
    story.append(Paragraph("• Include automated unit tests and benchmarking utilities to support functional validation and architectural comparison.", p_bullet))

    story.append(Paragraph("6. LITERATURE REVIEW", p_section_title))
    story.append(Paragraph(
        "Conversational AI has evolved across pattern matching, statistical retrieval and transformer-based generation. Weizenbaum introduced "
        "ELIZA, demonstrating that regular expressions and keyword decomposition can simulate human dialogue without semantic comprehension [1]. "
        "Baker and Colby examined the boundaries of syntactic chatbots, establishing their efficiency in highly structured domains [2].",
        p_body
    ))
    story.append(Paragraph(
        "Salton and McGill formalized the Vector Space Model (VSM) and Term Frequency-Inverse Document Frequency (TF-IDF) weighting, mapping text "
        "to high-dimensional sparse vectors [3]. Robertson et al. extended statistical retrieval with BM25 probabilistic ranking [4]. These works "
        "demonstrate that statistical similarity can resolve vocabulary mismatches without requiring manual syntactic rule definitions.",
        p_body
    ))
    story.append(Paragraph(
        "Vaswani et al. introduced the Transformer architecture, enabling large language models to generate fluent, context-aware prose [5]. "
        "Ji et al. surveyed hallucinations in natural language generation, highlighting that unconstrained LLMs frequently invent plausible but "
        "factually incorrect claims [6]. Lewis et al. proposed Retrieval-Augmented Generation (RAG) to ground LLM generation in verified documents [7].",
        p_body
    ))
    story.append(Paragraph("<b>Research gap and project positioning:</b>", p_subhead))
    story.append(Paragraph(
        "The reviewed work establishes the theoretical basis for pattern matching, statistical retrieval and augmented generation. The project "
        "combines these elements in a practical comparative prototype: rather than evaluating models in isolation, it exposes all three to the "
        "identical FAQ knowledge base, executes identical benchmark questions and evaluates response latency, cost, and accuracy under unified metrics. "
        "This is an implementation-oriented integration; it is not claimed to introduce a new language foundation model.",
        p_body
    ))

    story.append(Paragraph("7. EXISTING SYSTEM", p_section_title))
    story.append(Paragraph(
        "Common approaches to conversational inquiry systems include manual rule matching, unconstrained generative LLMs, and keyword-based search "
        "portals. Each approach has limitations when applied to institutional question-answering.",
        p_body
    ))
    story.append(Paragraph("<b>Manual rule-based planning:</b>", p_subhead))
    story.append(Paragraph("• Advantages: simple to start, deterministic, zero operational API cost, and sub-millisecond response time.", p_bullet))
    story.append(PageBreak())

    # ==========================================================
    # PAGE 6: SECTIONS 7(cont), 8 (Exact Layout)
    # ==========================================================
    story.append(Paragraph("• Limitations: time-consuming for extensive FAQ sets; brittle to lexical paraphrasing and synonyms; high maintenance overhead.", p_bullet))
    
    story.append(Paragraph("<b>Unconstrained generative LLM planning:</b>", p_subhead))
    story.append(Paragraph("• Advantages: natural conversational fluency, flexible comprehension of paraphrased language, and zero manual rule authoring.", p_bullet))
    story.append(Paragraph("• Limitations: prone to factual hallucinations; high latency (800–1400 ms); recurring API expenses per token.", p_bullet))

    story.append(Paragraph("<b>Statistical search and keyword retrieval:</b>", p_subhead))
    story.append(Paragraph("• Advantages: efficient vector indexing; handles term frequency weighting; robust against lexical variation.", p_bullet))
    story.append(Paragraph("• Limitations: extracts static text snippets rather than conversational syntheses; cannot synthesize multi-document reasoning.", p_bullet))

    story.append(Paragraph("<b>Proposed project approach:</b>", p_subhead))
    story.append(Paragraph("• Combines rule-based pattern matching, TF-IDF cosine similarity, and Gemini-powered RAG under a unified framework.", p_bullet))
    story.append(Paragraph("• Includes schedule simulation so response latency, API cost, out-of-scope rejection, and hallucination influence architectural evaluation.", p_bullet))
    story.append(Paragraph("• Provides both a React web interface and a FastAPI backend, with benchmarking and CSV export features described in the project source.", p_bullet))

    story.append(Paragraph("8. PROPOSED SYSTEM", p_section_title))
    story.append(Paragraph(
        "The proposed system processes an institutional FAQ dataset and converts it into structured rule patterns, TF-IDF vector matrices, and RAG "
        "grounding context. The 32 FAQs are treated as the single ground truth, and incoming student queries are routed through each architecture "
        "to evaluate comparative performance.",
        p_body
    ))
    story.append(Paragraph("<b>Main features:</b>", p_subhead))
    story.append(Paragraph("• Knowledge base management: upload or edit institutional FAQs across 11 categories with automatic index rebuilding.", p_bullet))
    story.append(Paragraph("• Rule engine: 41 priority-weighted regex patterns for deterministic pattern matching and fallback handling.", p_bullet))
    story.append(Paragraph("• Semantic retrieval: sublinear TF-IDF vectorization, stopword filtering, synonym expansion, and cosine similarity calculation.", p_bullet))
    story.append(Paragraph("• Confidence thresholding: empirical 0.35 threshold to reject out-of-scope inquiries and prevent false positives.", p_bullet))
    story.append(Paragraph("• RAG architecture: top-2 semantic context extraction coupled to Google's Gemini Flash model with strict grounding guardrails.", p_bullet))
    story.append(Paragraph("• Chat playground: individual architecture testing and 3-way simultaneous side-by-side comparison with latency tracking.", p_bullet))
    story.append(Paragraph("• Benchmark lab: execution of 50 standardized test questions (150 evaluated responses) with live progress tracking and CSV export.", p_bullet))
    story.append(Paragraph("• Analytics dashboard: calculation and visualization of 11 formal metrics including accuracy, latency, cost, and hallucination rates.", p_bullet))
    story.append(Paragraph(
        "The system uses a default confidence threshold of 0.35, an empirical rule priority range of 50 to 90, a default temperature of 0.2 for Gemini generation, "
        "and a standardized 50-question benchmark suite. These are configurable model assumptions, not unalterable production constants.",
        p_body
    ))
    story.append(PageBreak())

    # ==========================================================
    # PAGE 7: FIGURE 1, SECTION 9 (Exact Layout)
    # ==========================================================
    fig_path = r"C:\Users\Uday Shankar Praneet\.gemini\antigravity\scratch\architecture-lab\scratch\figure1_architecture.png"
    if os.path.exists(fig_path):
        # 425.169 pt x 240 pt
        img_fig = Image(fig_path, width=425, height=230)
        img_fig.hAlign = 'CENTER'
        story.append(img_fig)
        story.append(Spacer(1, 4))
    
    story.append(Paragraph("Figure 1. Architectural workflows of the three evaluated chatbot paradigms.", ParagraphStyle('FigCap', fontName='Times-Roman', fontSize=9.0, leading=12.0, alignment=1, spaceAfter=10.0)))

    story.append(Paragraph("9. RESEARCH METHODOLOGY", p_section_title))
    story.append(Paragraph(
        "The project follows a modular implementation workflow. Each stage transforms the output of the previous stage into a form "
        "that can be used by the next module.",
        p_body
    ))
    story.append(Paragraph("• Step 1 — Knowledge base input: load a curated 32-document FAQ collection for Demo University across 11 domains.", p_bullet))
    story.append(Paragraph("• Step 2 — Rule matching: normalise text, match against 41 regex patterns, resolve priority conflicts, and output answers.", p_bullet))
    story.append(Paragraph("• Step 3 — Semantic retrieval: strip stopwords, apply synonym expansion, compute TF-IDF vectors, and calculate cosine similarity.", p_bullet))
    story.append(Paragraph("• Step 4 — Threshold calibration: evaluate similarity scores against a 0.35 threshold to reject out-of-scope inquiries.", p_bullet))
    story.append(Paragraph("• Step 5 — RAG pipeline: retrieve relevant context snippets, build grounded prompt, call Gemini Flash API, and return cited answer.", p_bullet))
    story.append(Paragraph("• Step 6 — Benchmark execution: dispatch 50 test questions to all three architectures and record 150 responses.", p_bullet))
    story.append(Paragraph("• Step 7 — Response evaluation: score accuracy, latency, API cost, and hallucination flags using automated heuristics.", p_bullet))
    story.append(Paragraph("• Step 8 — Presentation and validation: display comparison metrics, export CSV manifests, and run automated unit tests.", p_bullet))

    story.append(Paragraph("<b>Input and output summary:</b>", p_subhead))

    io_rows_p7 = [
        [Paragraph("<b>Input</b>", th_style), Paragraph("<b>Processing</b>", th_style), Paragraph("<b>Output</b>", th_style)],
        [Paragraph("User query string", td_bold), Paragraph("Text normalization, regex pattern matching, and priority ranking", td_style), Paragraph("Predefined FAQ response or fallback message", td_style)],
        [Paragraph("Query + 32 FAQ documents", td_bold), Paragraph("Stopword filtering, synonym expansion, and TF-IDF vectorization", td_style), Paragraph("Sparse document and query term-weight vectors", td_style)],
        [Paragraph("Query vector + FAQ vectors", td_bold), Paragraph("Cosine similarity calculation and 0.35 confidence thresholding", td_style), Paragraph("Ranked document match, similarity score, and retrieval decision", td_style)],
        [Paragraph("Query + retrieved FAQ context", td_bold), Paragraph("Prompt augmentation, anti-hallucination guardrails, and Gemini API call", td_style), Paragraph("Grounded natural language answer and source citations", td_style)]
    ]
    t_io_p7 = Table(io_rows_p7, colWidths=[120, 200, 161.28])
    t_io_p7.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, ALT_ROW])
    ]))
    story.append(t_io_p7)
    story.append(PageBreak())

    # ==========================================================
    # PAGE 8: SECTIONS 9(cont), 10, 11 (Exact Layout)
    # ==========================================================
    io_rows_p8 = [
        [Paragraph("<b>Input</b>", th_style), Paragraph("<b>Processing</b>", th_style), Paragraph("<b>Output</b>", th_style)],
        [Paragraph("50 Benchmark questions", td_bold), Paragraph("Automated benchmark runner, response recording, and scoring heuristics", td_style), Paragraph("150 SQLite response records, metrics, and CSV exports", td_style)]
    ]
    t_io_p8 = Table(io_rows_p8, colWidths=[120, 200, 161.28])
    t_io_p8.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 3),
        ('BOTTOMPADDING', (0,0), (-1,-1), 3),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white])
    ]))
    story.append(t_io_p8)
    story.append(Spacer(1, 4))

    story.append(Paragraph("10. TOOLS AND TECHNOLOGIES REQUIRED", p_section_title))
    tech_rows = [
        [Paragraph("<b>Tool / technology</b>", th_style), Paragraph("<b>Role in the project</b>", th_style)],
        [Paragraph("Python 3", td_bold), Paragraph("Primary programming language and application logic", td_style)],
        [Paragraph("FastAPI", td_bold), Paragraph("High-performance asynchronous REST API framework and static SPA serving", td_style)],
        [Paragraph("Scikit-learn", td_bold), Paragraph("TF-IDF Vectorizer, cosine similarity metrics, and sparse matrix operations", td_style)],
        [Paragraph("NumPy & Pandas", td_bold), Paragraph("Numerical operations, latency percentiles, and tabular CSV workflows", td_style)],
        [Paragraph("SQLite", td_bold), Paragraph("Persistent relational storage for FAQs, benchmark runs, and evaluated responses", td_style)],
        [Paragraph("Google Gemini API", td_bold), Paragraph("Foundation LLM (Gemini 1.5 Flash) for grounded contextual RAG generation", td_style)],
        [Paragraph("React 18 & TypeScript", td_bold), Paragraph("Type-safe interactive single-page user interface", td_style)],
        [Paragraph("Tailwind CSS", td_bold), Paragraph("Responsive utility-first styling and modern dark AI research dashboard theme", td_style)],
        [Paragraph("Recharts & Framer Motion", td_bold), Paragraph("Interactive performance charts and micro-interaction animations", td_style)],
        [Paragraph("pytest", td_bold), Paragraph("Automated unit and integration testing suite", td_style)]
    ]
    t_tech = Table(tech_rows, colWidths=[150, 331.28])
    t_tech.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, ALT_ROW])
    ]))
    story.append(t_tech)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "The supplied requirements file pins FastAPI, Scikit-learn, NumPy, Pandas, pytest and Pydantic dependencies. The project is implemented in "
        "Python. The code also includes automated batch scripts for Windows execution (start_server.bat and run_tests.bat); this report does not claim "
        "that a multi-tenant cloud SaaS deployment has been completed.",
        p_body
    ))
    story.append(Paragraph("<b>Security and privacy considerations:</b>", p_subhead))
    story.append(Paragraph(
        "The supplied project is primarily a local research and benchmarking prototype. Query fields may contain user-entered inquiry information, "
        "so users should avoid entering unnecessary personal data. The repository manages Gemini API keys via environment variables (.env) and excludes "
        "them from version control. The repository does not document an enterprise OAuth2 single-sign-on system or encrypted cloud database. These should "
        "be considered before deployment with real student information.",
        p_body
    ))

    story.append(Paragraph("11. SYSTEM ARCHITECTURE", p_section_title))
    story.append(Paragraph(
        "The system is organised into five logical layers: user interface, API and routing, AI engines, benchmark evaluation, and storage.",
        p_body
    ))
    story.append(Paragraph("<b>Architecture flow:</b>", p_subhead))

    arch_rows = [
        [Paragraph("<b>Layer</b>", th_style), Paragraph("<b>Main responsibility</b>", th_style), Paragraph("<b>Main module(s)</b>", th_style)],
        [Paragraph("Presentation", td_bold), Paragraph("Single-architecture chat, side-by-side comparison, benchmark runner, and charts", td_style), Paragraph("App.tsx, PlaygroundPage.tsx, BenchmarkLabPage.tsx (React)", td_style)],
        [Paragraph("API & Routing", td_bold), Paragraph("REST API endpoints, request validation, CORS, CSV/JSON streaming", td_style), Paragraph("main.py, endpoints.py (FastAPI)", td_style)],
        [Paragraph("AI Engines", td_bold), Paragraph("Rule matching, TF-IDF vectorization, cosine similarity, and RAG generation", td_style), Paragraph("rule_engine.py, retrieval_engine.py, rag_engine.py", td_style)],
        [Paragraph("Optimisation & Eval", td_bold), Paragraph("Benchmark execution, response scoring, hallucination detection, metrics calculation", td_style), Paragraph("benchmark_runner.py, evaluator.py, analytics_service.py", td_style)],
        [Paragraph("Data and testing", td_bold), Paragraph("Knowledge base persistence, SQLite tables, sample data, and unit tests", td_style), Paragraph("database.py, seed_faqs.json, test_*.py", td_style)]
    ]
    t_arch = Table(arch_rows, colWidths=[100, 221.28, 160])
    t_arch.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, ALT_ROW])
    ]))
    story.append(t_arch)
    story.append(Spacer(1, 3))

    story.append(Paragraph(
        "Request lifecycle: the user submits a query, the API normalizes the input string, and dispatches it to the selected engine. Pairwise cosine "
        "similarity checks compare the query against FAQ vectors, which are supplied to the RAG prompt builder where applicable. The user runs benchmark "
        "testing, and the evaluator returns accuracy and latency metrics, which the interface presents",
        p_body
    ))
    story.append(PageBreak())

    # ==========================================================
    # PAGE 9: SECTIONS 11(cont), 12, 13 (Exact Layout)
    # ==========================================================
    story.append(Paragraph(
        "alongside the architecture visualisation and available benchmark information.",
        p_body
    ))
    story.append(Paragraph(
        "The RAG engine uses strict prompt guardrails with few-shot grounding instructions. It explicitly refuses queries when retrieved context "
        "similarity falls below the confidence cutoff rather than silently fabricating an answer under the generative label. The user interface "
        "refers to this option as an LLM-based RAG architecture.",
        p_body
    ))
    story.append(Spacer(1, 2))
    story.append(Paragraph(
        "USER QUERY → NORMALIZATION → VECTOR SEARCH → SIMILARITY THRESHOLD → RAG PROMPT → RESULTS",
        ParagraphStyle('FlowText', fontName='Times-Bold', fontSize=8.5, leading=11.0, alignment=1, spaceAfter=8.0)
    ))

    story.append(Paragraph("12. EXPECTED OUTCOMES AND TESTING", p_section_title))
    story.append(Paragraph(
        "The intended outcome is a working prototype that converts an FAQ database into a multi-architecture conversational platform and "
        "produces candidate answers that can be inspected and compared. The system is designed to provide more realistic evaluation metrics "
        "than theoretical estimates when the benchmark accurately represents real-world enquiry distributions.",
        p_body
    ))

    test_rows = [
        [Paragraph("<b>Evaluation area</b>", th_style), Paragraph("<b>Metric / validation</b>", th_style), Paragraph("<b>Evidence available in supplied project</b>", th_style)],
        [Paragraph("Rule pattern matching", td_bold), Paragraph("Correct identification and ordering of regex priority rules", td_style), Paragraph("Automated rule tests; 41 regex rules in rule_engine.py", td_style)],
        [Paragraph("Vector extraction", td_bold), Paragraph("Term frequency and inverse document frequency representation", td_style), Paragraph("Retrieval tests and Scikit-learn TF-IDF implementation", td_style)],
        [Paragraph("Similarity calculation", td_bold), Paragraph("Cosine distance accuracy and thresholding behavior", td_style), Paragraph("Automated retrieval engine tests", td_style)],
        [Paragraph("Architecture comparison", td_bold), Paragraph("Candidate response, latency, token cost and hallucination score", td_style), Paragraph("Three engine implementations", td_style)],
        [Paragraph("Out-of-scope handling", td_bold), Paragraph("Rejection rate on unrelated inquiries (sports, weather)", td_style), Paragraph("0.35 confidence threshold in retrieval_engine.py", td_style)],
        [Paragraph("Benchmark evaluation", td_bold), Paragraph("Mean accuracy, latency percentiles, and category breakdown", td_style), Paragraph("Automated 50-question benchmark runner", td_style)],
        [Paragraph("Software validation", td_bold), Paragraph("Passing unit and integration tests", td_style), Paragraph("16 unit tests passed when the test modules were run", td_style)]
    ]
    t_test = Table(test_rows, colWidths=[120, 180, 181.28])
    t_test.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 2.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.5),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, ALT_ROW])
    ]))
    story.append(t_test)
    story.append(Spacer(1, 4))

    story.append(Paragraph(
        "The verified test result is 16 passing tests across test_rule_engine.py, test_retrieval_engine.py, test_evaluator.py and test_benchmark.py. "
        "In addition, 13 end-to-end integration tests were executed against all FastAPI endpoints, verifying 100% operational connectivity.",
        p_body
    ))
    story.append(Paragraph(
        "Empirical benchmark results recorded from executing all 50 test questions demonstrate: (i) Rule-Based Engine achieved 88.0% accuracy with an average "
        "latency of 0.26 ms; (ii) Semantic Retrieval achieved 90.0% accuracy with an average latency of 0.13 ms; and (iii) Out-of-scope rejection reached "
        "100.0% across both non-generative architectures. Such values represent reproducible experimental findings recorded in the SQLite database.",
        p_body
    ))

    story.append(Paragraph("13. APPLICATIONS AND SCOPE", p_section_title))
    story.append(Paragraph("<b>Potential applications:</b>", p_subhead))
    story.append(Paragraph("• Small institutional helpdesks planning automated student inquiry handling.", p_bullet))
    story.append(Paragraph("• Demonstrations and teaching exercises involving pattern matching, information retrieval and generative AI.", p_bullet))
    story.append(Paragraph("• Comparative experiments involving deterministic rules, statistical retrieval, and prompt-engineered LLMs.", p_bullet))
    story.append(Paragraph("<b>Included in the current project scope:</b>", p_subhead))
    story.append(Paragraph("• Single institutional FAQ dataset with 32 verified demonstration questions across 11 categories.", p_bullet))
    story.append(Paragraph("• Priority-weighted regular expression matching and sublinear TF-IDF vector retrieval.", p_bullet))
    story.append(Paragraph("• Cosine similarity search with an empirical 0.35 confidence threshold.", p_bullet))
    story.append(Paragraph("• Retrieval-Augmented Generation schedule simulation and three chatbot engine approaches.", p_bullet))
    story.append(Paragraph("• React and FastAPI interfaces, synthetic FAQ generation, automated tests and benchmark utilities.", p_bullet))
    story.append(Paragraph("<b>Outside the current scope / limitations:</b>", p_subhead))
    story.append(PageBreak())

    # ==========================================================
    # PAGE 10: SECTIONS 13(cont), 14, 15 (Exact Layout)
    # ==========================================================
    story.append(Paragraph("• Live student records, fee payment processing, and authenticated portal integrations are not established by the supplied code.", p_bullet))
    story.append(Paragraph("• The knowledge base is treated as static text; it is not automatically synchronised to live enterprise campus databases.", p_bullet))
    story.append(Paragraph("• The model uses single-turn question-answering rather than multi-turn conversational dialogue state tracking.", p_bullet))
    story.append(Paragraph("• The default token cost estimate is a simulation parameter and requires calibration against live provider invoices.", p_bullet))
    story.append(Paragraph("• Synonym expansion depends on predefined dictionaries; unusual domain jargon may require dictionary additions.", p_bullet))
    story.append(Paragraph("• The rule engine is limited to 41 hand-crafted regex patterns by design.", p_bullet))

    story.append(Paragraph("<b>Future enhancements:</b>", p_subhead))
    story.append(Paragraph("• Integrate live student information systems and real-world payment gateway APIs.", p_bullet))
    story.append(Paragraph("• Add multi-turn conversational memory and user session context tracking.", p_bullet))
    story.append(Paragraph("• Extend the model to dense neural embeddings using sentence-transformers and vector databases (e.g. Chroma/Milvus).", p_bullet))
    story.append(Paragraph("• Improve synonym expansion using automated word2vec or domain ontology embeddings.", p_bullet))
    story.append(Paragraph("• Add multi-institutional benchmark datasets and repeatable experiment reports for cross-domain evaluation.", p_bullet))
    story.append(Paragraph("• Introduce user authentication and secure handling of student identification data for production deployment.", p_bullet))

    story.append(Paragraph("14. PROJECT TIMELINE", p_section_title))
    story.append(Paragraph(
        "The supplied source archive does not include dated development records. The following is therefore an indicative project "
        "workflow for presenting the stages of the work; it should not be interpreted as a verified record of the group’s actual "
        "week-by-week activity.",
        p_body
    ))

    time_rows = [
        [Paragraph("<b>Indicative phase</b>", th_style), Paragraph("<b>Work planned / represented</b>", th_style)],
        [Paragraph("Phase 1", td_bold), Paragraph("Define the comparative chatbot problem and architectural evaluation model", td_style)],
        [Paragraph("Phase 2", td_bold), Paragraph("Curate FAQ knowledge base and synthetic institutional dataset", td_style)],
        [Paragraph("Phase 3", td_bold), Paragraph("Implement rule-based pattern matching and regex priority weighting", td_style)],
        [Paragraph("Phase 4", td_bold), Paragraph("Implement text normalization, synonym expansion and stopword filtering", td_style)],
        [Paragraph("Phase 5", td_bold), Paragraph("Implement TF-IDF vectorization and pairwise cosine similarity calculation", td_style)],
        [Paragraph("Phase 6", td_bold), Paragraph("Implement confidence thresholding and out-of-scope refusal logic", td_style)],
        [Paragraph("Phase 7", td_bold), Paragraph("Implement RAG prompt augmentation and Gemini Flash integration", td_style)],
        [Paragraph("Phase 8", td_bold), Paragraph("Develop 50-question benchmark suite across four question tiers", td_style)],
        [Paragraph("Phase 9", td_bold), Paragraph("Develop React single-page interface and FastAPI REST backend", td_style)],
        [Paragraph("Phase 10", td_bold), Paragraph("Add benchmarking, analytics visualisation and CSV export", td_style)],
        [Paragraph("Phase 11", td_bold), Paragraph("Run automated unit tests and refine module integration", td_style)],
        [Paragraph("Phase 12", td_bold), Paragraph("Prepare documentation, viva defense guide and final project demonstration", td_style)]
    ]
    t_time = Table(time_rows, colWidths=[120, 361.28])
    t_time.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY_COLOR),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_GRAY),
        ('TOPPADDING', (0,0), (-1,-1), 2.0),
        ('BOTTOMPADDING', (0,0), (-1,-1), 2.0),
        ('VALIGN', (0,0), (-1,-1), 'TOP'),
        ('ROWBACKGROUNDS', (0,1), (-1,-1), [colors.white, ALT_ROW])
    ]))
    story.append(t_time)
    story.append(Spacer(1, 4))

    story.append(Paragraph("15. CONCLUSION", p_section_title))
    story.append(Paragraph(
        "The Architecture Lab brings together pattern matching, statistical information retrieval and generative large language "
        "models in a modular chatbot evaluation prototype. It normalizes queries, matches regex patterns, computes vector cosine "
        "similarities using TF-IDF and uses those distances to synthesize grounded answers under factual constraints.",
        p_body
    ))
    story.append(Paragraph(
        "The project includes three architecture implementations, schedule simulation, two user-facing interfaces, sample-FAQ management and "
        "benchmarking utilities. The supplied automated test modules produced 16 passing tests during verification. This supports the",
        p_body
    ))
    story.append(PageBreak())

    # ==========================================================
    # PAGE 11: SECTIONS 15(cont), 16 (Exact Layout)
    # ==========================================================
    story.append(Paragraph(
        "functional implementation of the tested components, while further multi-turn benchmarking and enterprise calibration "
        "remain necessary before operational deployment.",
        p_body
    ))
    story.append(Paragraph(
        "Overall, the project demonstrates how classic pattern matching and information retrieval techniques can be combined with "
        "generative foundation models to support a practical institutional enquiry planning task.",
        p_body
    ))

    story.append(Paragraph("16. REFERENCES", p_section_title))

    ref_list = [
        "[1] J. Weizenbaum, “ELIZA—a computer program for the study of natural language communication between man and machine,” Communications of the ACM, vol. 9, no. 1, pp. 36–45, 1966, doi: 10.1145/365153.365168.",
        "[2] K. M. Colby, “Artificial Paranoia: A Computer Simulation of Paranoid Processes,” Pergamon Press, 1975.",
        "[3] G. Salton and M. J. McGill, “Introduction to Modern Information Retrieval,” McGraw-Hill, New York, 1983.",
        "[4] S. E. Robertson, S. Walker, S. Jones, M. M. Hancock-Beaulieu, and M. Gatford, “Okapi at TREC-3,” NIST Special Publication 500-225, pp. 109–126, 1995.",
        "[5] A. Vaswani, N. Shazeer, N. Parmar, J. Uszkoreit, L. Jones, A. N. Gomez, L. Kaiser, and I. Polosukhin, “Attention is all you need,” in Advances in Neural Information Processing Systems, vol. 30, pp. 5998–6008, 2017.",
        "[6] Z. Ji, N. Lee, R. Frieske, T. Yu, D. Su, Y. Xu, E. Ishii, Y. J. Bang, A. Madotto, and P. Fung, “Survey of hallucination in natural language generation,” ACM Computing Surveys, vol. 55, no. 12, pp. 1–38, 2023, doi: 10.1145/3571730.",
        "[7] P. Lewis, E. Perez, A. Piktus, F. Petroni, V. Karpukhin, N. Goyal, H. Küttler, M. Lewis, W. Yih, T. Rocktäschel, S. Riedel, and D. Kiela, “Retrieval-augmented generation for knowledge-intensive NLP tasks,” in Advances in Neural Information Processing Systems, vol. 33, pp. 9459–9474, 2020.",
        "[8] F. Pedregosa et al., “Scikit-learn: Machine Learning in Python,” Journal of Machine Learning Research, vol. 12, pp. 2825–2830, 2011.",
        "[9] S. Ramirez, “FastAPI Documentation.” [Online]. Available: https://fastapi.tiangolo.com/",
        "[10] React, “React Documentation.” [Online]. Available: https://react.dev/",
        "[11] pytest, “pytest Documentation.” [Online]. Available: https://docs.pytest.org/"
    ]

    for ref in ref_list:
        story.append(Paragraph(ref, ParagraphStyle('ExactRef', fontName='Times-Roman', fontSize=8.0, leading=11.5, spaceAfter=4.0, alignment=4)))

    # Build the document using ExactCanvas
    doc.build(story, canvasmaker=ExactCanvas)
    print(f"Successfully generated EXACT replica PDF: {pdf_path}")

    # Copy to Desktop
    desktop = os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Desktop")
    if not os.path.exists(desktop):
        desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
    dest_pdf = os.path.join(desktop, "Architecture_Lab_Project_Report_Exact.pdf")
    shutil.copy(pdf_path, dest_pdf)
    print(f"Copied exact PDF to Desktop: {dest_pdf}")

if __name__ == "__main__":
    build_pdf()
