import os
import shutil
import docx
from docx.shared import Inches, Pt, RGBColor, Mm
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.table import WD_TABLE_ALIGNMENT, WD_ALIGN_VERTICAL
from docx.oxml import OxmlElement, parse_xml
from docx.oxml.ns import qn, nsdecls

def set_cell_background(cell, fill_hex):
    shading_elm = parse_xml(f'<w:shd {nsdecls("w")} w:fill="{fill_hex}"/>')
    cell._tc.get_or_add_tcPr().append(shading_elm)

def set_cell_margins(cell, top=100, bottom=100, left=150, right=150):
    tcPr = cell._tc.get_or_add_tcPr()
    tcMar = OxmlElement('w:tcMar')
    for m, val in [('top', top), ('bottom', bottom), ('left', left), ('right', right)]:
        node = OxmlElement(f'w:{m}')
        node.set(qn('w:w'), str(val))
        node.set(qn('w:type'), 'dxa')
        tcMar.append(node)
    tcPr.append(tcMar)

def set_table_borders(table, color="808080", sz="4", val="single"):
    tblPr = table._tbl.tblPr
    borders = parse_xml(f'''
        <w:tblBorders {nsdecls("w")}>
            <w:top w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:left w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:bottom w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:right w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideH w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
            <w:insideV w:val="{val}" w:sz="{sz}" w:space="0" w:color="{color}"/>
        </w:tblBorders>
    ''')
    tblPr.append(borders)

def add_page_number_field(run):
    fldSimple = parse_xml(r'<w:fldSimple %s w:instr="PAGE"/>' % nsdecls('w'))
    run._r.append(fldSimple)

def build_docx():
    doc = docx.Document()
    
    # Page setup - A4
    section = doc.sections[0]
    section.page_width = Mm(210)
    section.page_height = Mm(297)
    section.left_margin = Mm(20)
    section.right_margin = Mm(20)
    section.top_margin = Mm(22)
    section.bottom_margin = Mm(20)
    
    # Configure Normal Style
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Times New Roman'
    normal_style.font.size = Pt(9.5)
    normal_style.font.color.rgb = RGBColor(0, 0, 0)
    normal_style.paragraph_format.line_spacing = 1.15
    normal_style.paragraph_format.space_after = Pt(4)

    # Configure Footer
    footer = section.footer
    footer_p = footer.paragraphs[0]
    footer_p.text = ""
    footer_p.paragraph_format.tab_stops.add_tab_stop(Mm(170), docx.enum.text.WD_TAB_ALIGNMENT.RIGHT)
    
    r_left = footer_p.add_run("Artificial Intelligence Foundations | CSE276")
    r_left.font.name = 'Times New Roman'
    r_left.font.size = Pt(8)
    r_left.font.color.rgb = RGBColor(100, 100, 100)
    
    r_tab = footer_p.add_run("\t")
    
    r_pg = footer_p.add_run()
    r_pg.font.name = 'Times New Roman'
    r_pg.font.size = Pt(8)
    r_pg.font.color.rgb = RGBColor(100, 100, 100)
    add_page_number_field(r_pg)

    # Helper functions
    def add_h1(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(14)
        p.paragraph_format.space_after = Pt(5)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(14)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0, 0, 0)
        return p

    def add_subhead(text):
        p = doc.add_paragraph()
        p.paragraph_format.space_before = Pt(7)
        p.paragraph_format.space_after = Pt(3)
        p.paragraph_format.keep_with_next = True
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        r.font.bold = True
        return p

    def add_p(text, justify=True):
        p = doc.add_paragraph()
        p.paragraph_format.space_after = Pt(4)
        if justify:
            p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p.add_run(text)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(9.5)
        return p

    def add_bullet(text):
        p = doc.add_paragraph()
        p.paragraph_format.left_indent = Inches(0.25)
        p.paragraph_format.first_line_indent = Inches(-0.15)
        p.paragraph_format.space_after = Pt(2.5)
        p.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r_b = p.add_run("•  ")
        r_b.font.name = 'Times New Roman'
        r_b.font.bold = True
        r_txt = p.add_run(text)
        r_txt.font.name = 'Times New Roman'
        r_txt.font.size = Pt(9.5)
        return p

    # ==========================================================
    # PAGE 1: TITLE PAGE
    # ==========================================================
    logo_path = r"C:\Users\Uday Shankar Praneet\.gemini\antigravity\scratch\architecture-lab\scratch\extracted_imgs\Im43.png"
    if os.path.exists(logo_path):
        p_logo = doc.add_paragraph()
        p_logo.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_logo.paragraph_format.space_after = Pt(15)
        p_logo.add_run().add_picture(logo_path, width=Inches(3.8))
    else:
        p_univ = doc.add_paragraph()
        p_univ.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_univ.paragraph_format.space_after = Pt(20)
        r = p_univ.add_run("LOVELY PROFESSIONAL UNIVERSITY\nTransforming Education Transforming India")
        r.font.name = 'Times New Roman'
        r.font.size = Pt(16)
        r.font.bold = True

    p_dept = doc.add_paragraph()
    p_dept.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_dept.paragraph_format.space_after = Pt(30)
    r = p_dept.add_run("Department of Computer Science and Engineering")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(9)

    p_pr = doc.add_paragraph()
    p_pr.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_pr.paragraph_format.space_after = Pt(14)
    r = p_pr.add_run("PROJECT REPORT")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(18)
    r.font.bold = True

    p_title = doc.add_paragraph()
    p_title.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_title.paragraph_format.space_after = Pt(6)
    r = p_title.add_run("ARCHITECTURE LAB: COMPARATIVE CHATBOT ARCHITECTURE STUDY")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(16)
    r.font.bold = True

    p_sub = doc.add_paragraph()
    p_sub.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_sub.paragraph_format.space_after = Pt(35)
    r = p_sub.add_run("A Comparative Evaluation of Rule-Based, Semantic Retrieval and LLM-Based RAG Systems Using an Institutional FAQ Knowledge Base")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(10)
    r.font.italic = True

    p_subreq = doc.add_paragraph()
    p_subreq.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subreq.paragraph_format.space_after = Pt(2)
    r = p_subreq.add_run("Submitted in partial fulfilment of the requirements for the degree of\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(9)
    r2 = p_subreq.add_run("Bachelor of Technology\n")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(9)
    r2.font.bold = True
    r3 = p_subreq.add_run("Computer Science and Engineering (Artificial Intelligence and Machine Learning)")
    r3.font.name = 'Times New Roman'
    r3.font.size = Pt(9)

    doc.add_paragraph().paragraph_format.space_after = Pt(15)

    p_course = doc.add_paragraph()
    p_course.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_course.paragraph_format.space_after = Pt(25)
    r = p_course.add_run("Course: Artificial Intelligence Foundations\nSubject Code: CSE276")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(9)
    r.font.bold = True

    p_subby = doc.add_paragraph()
    p_subby.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_subby.paragraph_format.space_after = Pt(4)
    r = p_subby.add_run("Submitted by")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(9)
    r.font.bold = True

    p_students = doc.add_paragraph()
    p_students.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_students.paragraph_format.space_after = Pt(25)
    r = p_students.add_run(
        "Lakshay Parashar   |   University Registration No.: 12523688   |   Roll No.: 40\n"
        "Rishabh Pandey   |   University Registration No.: 12523544   |   Roll No.: 41\n"
        "Uday Shankar Praneet   |   University Registration No.: 12524685   |   Roll No.: 42"
    )
    r.font.name = 'Times New Roman'
    r.font.size = Pt(9)

    p_guide = doc.add_paragraph()
    p_guide.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_guide.paragraph_format.space_after = Pt(30)
    r = p_guide.add_run("Under the guidance of\n")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(9)
    r.font.bold = True
    r2 = p_guide.add_run("Ms. Priyanshi Saxena")
    r2.font.name = 'Times New Roman'
    r2.font.size = Pt(9)

    p_lpu = doc.add_paragraph()
    p_lpu.alignment = WD_ALIGN_PARAGRAPH.CENTER
    r = p_lpu.add_run("Lovely Professional University")
    r.font.name = 'Times New Roman'
    r.font.size = Pt(9)

    doc.add_page_break()

    # ==========================================================
    # PAGE 2: ACKNOWLEDGEMENT
    # ==========================================================
    add_h1("ACKNOWLEDGEMENT")
    add_p(
        "We would like to express our sincere gratitude to Ms. Priyanshi Saxena for her guidance, support and valuable suggestions "
        "during the development of this project. Her direction helped us approach the problem systematically and improve our "
        "understanding of natural language processing, semantic retrieval, and large language model architectures."
    )
    add_p(
        "We also acknowledge Lovely Professional University and the Department of Computer Science and Engineering for providing "
        "the academic environment and learning opportunities that supported this work. Finally, we thank all group members for their "
        "contributions to the planning, implementation, testing and documentation of the Architecture Lab Comparative Chatbot Study."
    )
    doc.add_page_break()

    # ==========================================================
    # PAGE 3: TABLE OF CONTENTS
    # ==========================================================
    add_h1("TABLE OF CONTENTS")
    toc_data = [
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
    t_toc = doc.add_table(rows=len(toc_data), cols=2)
    t_toc.alignment = WD_TABLE_ALIGNMENT.CENTER
    for idx, (title_str, page_str) in enumerate(toc_data):
        row = t_toc.rows[idx]
        row.cells[0].width = Inches(5.5)
        row.cells[1].width = Inches(1.0)
        p0 = row.cells[0].paragraphs[0]
        p0.paragraph_format.space_after = Pt(2)
        r0 = p0.add_run(title_str)
        r0.font.name = 'Times New Roman'
        r0.font.bold = True
        r0.font.size = Pt(9.5)
        
        p1 = row.cells[1].paragraphs[0]
        p1.alignment = WD_ALIGN_PARAGRAPH.RIGHT
        p1.paragraph_format.space_after = Pt(2)
        r1 = p1.add_run(page_str)
        r1.font.name = 'Times New Roman'
        r1.font.size = Pt(9.5)
    doc.add_page_break()

    # ==========================================================
    # PAGE 4: SECTIONS 1, 2, 3, 4
    # ==========================================================
    add_h1("1. TITLE OF PROJECT")
    add_p("Architecture Lab: Comparative Chatbot Architecture Study: Rules vs Retrieval vs LLM-Based RAG.")

    add_h1("2. ABSTRACT")
    add_p(
        "The Architecture Lab is a software system designed to assist educational institutions and enterprise developers in evaluating "
        "and selecting conversational enquiry architectures. The system combines pattern matching, information retrieval and generative "
        "large language models to process user queries, estimate similarity against an institutional knowledge base, construct grounded "
        "responses and compare alternative conversational architectures."
    )
    add_p(
        "The rule-processing module uses regular expressions and priority weighting to identify direct factual enquiries across institutional domains. "
        "Patterns are matched against normalized user strings to execute deterministic lookup. The retrieval module uses sublinear TF-IDF vectorization "
        "and cosine similarity to search an institutional FAQ collection, then applies an empirical confidence threshold of 0.35 to verify answer relevance."
    )
    add_p(
        "The generative module models conversational question answering as a Retrieval-Augmented Generation (RAG) pipeline. It combines "
        "semantic search with Google's Gemini Flash model to synthesize natural language answers from retrieved context. Schedule simulation accounts "
        "for response latency, operational API token cost, hallucination detection, out-of-scope rejection and setup maintenance effort. A React web "
        "interface and a FastAPI REST service are included in the project source."
    )
    add_p(
        "The source repository includes automated tests for rule, retrieval, evaluator and benchmark modules. Running the listed test modules in "
        "the supplied project archive produced 16 passing tests. The software also includes 50-question multi-tier benchmarking and analytics "
        "visualisation functionality; numerical comparative performance results demonstrate 88.0% accuracy for rules and 90.0% accuracy for semantic retrieval."
    )

    add_h1("3. INTRODUCTION")
    add_p(
        "Conversational AI systems serve as primary communication interfaces between organizations and end users. This interaction involves "
        "diverse user queries and can become operationally difficult when questions use colloquial phrasing and organizations have strict factual constraints."
    )
    add_p(
        "A response that appears fluent may be impractical if it hallucinates non-existent college policies or incorrect fee amounts. "
        "Similarly, a rule-based engine with low latency may still perform poorly if a student expresses their query with unanticipated vocabulary. A "
        "useful enquiry system therefore needs to consider both the linguistic flexibility of the model and the factual constraints associated "
        "with institutional policies."
    )
    add_p(
        "This project addresses the problem by treating the FAQ database as a controlled knowledge base. Text pre-processing normalizes user queries, "
        "while vectorization extracts statistical term weights. Cosine similarity is then applied to the FAQ collection to estimate semantic relevance. "
        "These distances and context snippets are passed to an LLM prompt builder, which compares different retrieval and generation paradigms."
    )
    add_p(
        "The system is intended as a decision-support prototype. It allows a user to explore individual architectures or run side-by-side comparisons, "
        "execute standardized 50-question benchmarks, and inspect comparative metrics through an interactive graphical interface."
    )

    add_h1("4. PROBLEM STATEMENT")
    add_p(
        "Educational institutions may deploy conversational chatbots manually or rely on generative models that do not ground responses in verified policies. "
        "Manual planning becomes harder as the number of student queries increases, particularly when each inquiry requires strict policy adherence. A generative "
        "chatbot may fabricate tuition fees or deadlines if unconstrained, or may incur avoidable latency and API expense if simple queries are routed to massive LLMs."
    )
    add_p(
        "The problem addressed by this project is to develop a system that can: (i) ingest a verified 32-document institutional FAQ database; (ii) implement "
        "deterministic rule matching, statistical vector retrieval, and LLM-based RAG under identical constraints; (iii) evaluate response latency and "
        "factual accuracy; and (iv) determine and compare architectural trade-offs using a standardized 50-question benchmark suite."
    )
    doc.add_page_break()

    # ==========================================================
    # PAGE 5: SECTIONS 4(cont), 5, 6, 7
    # ==========================================================
    add_p(
        "The system uses a single-institution FAQ knowledge base model. It is not presented as a live multi-tenant university enterprise system, an "
        "unbounded open-web search crawler or an automated admissions transactional portal."
    )

    add_h1("5. AIM AND OBJECTIVES")
    add_p("<b>Aim:</b> To develop a comparative chatbot benchmarking prototype that combines rule-based pattern matching, statistical semantic retrieval and LLM-based RAG optimisation.")
    add_subhead("Objectives:")
    add_bullet("Curate an institutional knowledge base of 32 verified FAQs across 11 categories for Demo University.")
    add_bullet("Engineer a deterministic rule engine incorporating 41 priority-weighted regular expression patterns.")
    add_bullet("Implement a statistical retrieval engine using TF-IDF vectorization, synonym expansion, and cosine similarity.")
    add_bullet("Establish an empirical confidence threshold of 0.35 to reject out-of-scope inquiries reliably.")
    add_bullet("Integrate an LLM-based RAG pipeline using Google's Gemini Flash model with anti-hallucination prompt guardrails.")
    add_bullet("Implement and compare three chatbot architectures across direct, paraphrased, out-of-scope, and adversarial queries.")
    add_bullet("Provide interactive interfaces for single-architecture testing, 3-way side-by-side comparison, and analytics.")
    add_bullet("Include automated unit tests and benchmarking utilities to support functional validation and architectural comparison.")

    add_h1("6. LITERATURE REVIEW")
    add_p(
        "Conversational AI has evolved across pattern matching, statistical retrieval and transformer-based generation. Weizenbaum introduced "
        "ELIZA, demonstrating that regular expressions and keyword decomposition can simulate human dialogue without semantic comprehension [1]. "
        "Baker and Colby examined the boundaries of syntactic chatbots, establishing their efficiency in highly structured domains [2]."
    )
    add_p(
        "Salton and McGill formalized the Vector Space Model (VSM) and Term Frequency-Inverse Document Frequency (TF-IDF) weighting, mapping text "
        "to high-dimensional sparse vectors [3]. Robertson et al. extended statistical retrieval with BM25 probabilistic ranking [4]. These works "
        "demonstrate that statistical similarity can resolve vocabulary mismatches without requiring manual syntactic rule definitions."
    )
    add_p(
        "Vaswani et al. introduced the Transformer architecture, enabling large language models to generate fluent, context-aware prose [5]. "
        "Ji et al. surveyed hallucinations in natural language generation, highlighting that unconstrained LLMs frequently invent plausible but "
        "factually incorrect claims [6]. Lewis et al. proposed Retrieval-Augmented Generation (RAG) to ground LLM generation in verified documents [7]."
    )
    add_subhead("Research gap and project positioning:")
    add_p(
        "The reviewed work establishes the theoretical basis for pattern matching, statistical retrieval and augmented generation. The project "
        "combines these elements in a practical comparative prototype: rather than evaluating models in isolation, it exposes all three to the "
        "identical FAQ knowledge base, executes identical benchmark questions and evaluates response latency, cost, and accuracy under unified metrics. "
        "This is an implementation-oriented integration; it is not claimed to introduce a new language foundation model."
    )

    add_h1("7. EXISTING SYSTEM")
    add_p(
        "Common approaches to conversational inquiry systems include manual rule matching, unconstrained generative LLMs, and keyword-based search "
        "portals. Each approach has limitations when applied to institutional question-answering."
    )
    add_subhead("Manual rule-based planning:")
    add_bullet("Advantages: simple to start, deterministic, zero operational API cost, and sub-millisecond response time.")
    doc.add_page_break()

    # ==========================================================
    # PAGE 6: SECTIONS 7(cont), 8
    # ==========================================================
    add_bullet("Limitations: time-consuming for extensive FAQ sets; brittle to lexical paraphrasing and synonyms; high maintenance overhead.")

    add_subhead("Unconstrained generative LLM planning:")
    add_bullet("Advantages: natural conversational fluency, flexible comprehension of paraphrased language, and zero manual rule authoring.")
    add_bullet("Limitations: prone to factual hallucinations; high latency (800–1400 ms); recurring API expenses per token.")

    add_subhead("Statistical search and keyword retrieval:")
    add_bullet("Advantages: efficient vector indexing; handles term frequency weighting; robust against lexical variation.")
    add_bullet("Limitations: extracts static text snippets rather than conversational syntheses; cannot synthesize multi-document reasoning.")

    add_subhead("Proposed project approach:")
    add_bullet("Combines rule-based pattern matching, TF-IDF cosine similarity, and Gemini-powered RAG under a unified framework.")
    add_bullet("Includes schedule simulation so response latency, API cost, out-of-scope rejection, and hallucination influence architectural evaluation.")
    add_bullet("Provides both a React web interface and a FastAPI backend, with benchmarking and CSV export features described in the project source.")

    add_h1("8. PROPOSED SYSTEM")
    add_p(
        "The proposed system processes an institutional FAQ dataset and converts it into structured rule patterns, TF-IDF vector matrices, and RAG "
        "grounding context. The 32 FAQs are treated as the single ground truth, and incoming student queries are routed through each architecture "
        "to evaluate comparative performance."
    )
    add_subhead("Main features:")
    add_bullet("Knowledge base management: upload or edit institutional FAQs across 11 categories with automatic index rebuilding.")
    add_bullet("Rule engine: 41 priority-weighted regex patterns for deterministic pattern matching and fallback handling.")
    add_bullet("Semantic retrieval: sublinear TF-IDF vectorization, stopword filtering, synonym expansion, and cosine similarity calculation.")
    add_bullet("Confidence thresholding: empirical 0.35 threshold to reject out-of-scope inquiries and prevent false positives.")
    add_bullet("RAG architecture: top-2 semantic context extraction coupled to Google's Gemini Flash model with strict grounding guardrails.")
    add_bullet("Chat playground: individual architecture testing and 3-way simultaneous side-by-side comparison with latency tracking.")
    add_bullet("Benchmark lab: execution of 50 standardized test questions (150 evaluated responses) with live progress tracking and CSV export.")
    add_bullet("Analytics dashboard: calculation and visualization of 11 formal metrics including accuracy, latency, cost, and hallucination rates.")
    add_p(
        "The system uses a default confidence threshold of 0.35, an empirical rule priority range of 50 to 90, a default temperature of 0.2 for Gemini generation, "
        "and a standardized 50-question benchmark suite. These are configurable model assumptions, not unalterable production constants."
    )
    doc.add_page_break()

    # ==========================================================
    # PAGE 7: FIGURE 1, SECTION 9 & I/O Table
    # ==========================================================
    fig_path = r"C:\Users\Uday Shankar Praneet\.gemini\antigravity\scratch\architecture-lab\scratch\figure1_architecture.png"
    if os.path.exists(fig_path):
        p_fig = doc.add_paragraph()
        p_fig.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_fig.paragraph_format.space_after = Pt(2)
        p_fig.add_run().add_picture(fig_path, width=Inches(5.8))
        
        p_cap = doc.add_paragraph()
        p_cap.alignment = WD_ALIGN_PARAGRAPH.CENTER
        p_cap.paragraph_format.space_after = Pt(10)
        r_c = p_cap.add_run("Figure 1. Architectural workflows of the three evaluated chatbot paradigms.")
        r_c.font.name = 'Times New Roman'
        r_c.font.size = Pt(9)

    add_h1("9. RESEARCH METHODOLOGY")
    add_p(
        "The project follows a modular implementation workflow. Each stage transforms the output of the previous stage into a form "
        "that can be used by the next module."
    )
    add_bullet("Step 1 — Knowledge base input: load a curated 32-document FAQ collection for Demo University across 11 domains.")
    add_bullet("Step 2 — Rule matching: normalise text, match against 41 regex patterns, resolve priority conflicts, and output answers.")
    add_bullet("Step 3 — Semantic retrieval: strip stopwords, apply synonym expansion, compute TF-IDF vectors, and calculate cosine similarity.")
    add_bullet("Step 4 — Threshold calibration: evaluate similarity scores against a 0.35 threshold to reject out-of-scope inquiries.")
    add_bullet("Step 5 — RAG pipeline: retrieve relevant context snippets, build grounded prompt, call Gemini Flash API, and return cited answer.")
    add_bullet("Step 6 — Benchmark execution: dispatch 50 test questions to all three architectures and record 150 responses.")
    add_bullet("Step 7 — Response evaluation: score accuracy, latency, API cost, and hallucination flags using automated heuristics.")
    add_bullet("Step 8 — Presentation and validation: display comparison metrics, export CSV manifests, and run automated unit tests.")

    add_subhead("Input and output summary:")

    io_table_data = [
        ("Input", "Processing", "Output"),
        ("User query string", "Text normalization, regex pattern matching, and priority ranking", "Predefined FAQ response or fallback message"),
        ("Query + 32 FAQ documents", "Stopword filtering, synonym expansion, and TF-IDF vectorization", "Sparse document and query term-weight vectors"),
        ("Query vector + FAQ vectors", "Cosine similarity calculation and 0.35 confidence thresholding", "Ranked document match, similarity score, and retrieval decision"),
        ("Query + retrieved FAQ context", "Prompt augmentation, anti-hallucination guardrails, and Gemini API call", "Grounded natural language answer and source citations"),
        ("50 Benchmark questions", "Automated benchmark runner, response recording, and scoring heuristics", "150 SQLite response records, metrics, and CSV exports")
    ]

    t_io = doc.add_table(rows=len(io_table_data), cols=3)
    t_io.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_io)
    
    col_w = [Inches(1.6), Inches(2.6), Inches(2.4)]
    for r_idx, row_data in enumerate(io_table_data):
        row = t_io.rows[r_idx]
        is_hdr = (r_idx == 0)
        for c_idx, text_val in enumerate(row_data):
            cell = row.cells[c_idx]
            cell.width = col_w[c_idx]
            set_cell_margins(cell, top=60, bottom=60, left=100, right=100)
            if is_hdr:
                set_cell_background(cell, "1F3750")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "FFFFFF")
            else:
                set_cell_background(cell, "F8FAFC")
                
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(text_val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if is_hdr:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            elif c_idx == 0:
                r.font.bold = True
    doc.add_page_break()

    # ==========================================================
    # PAGE 8: SECTIONS 10 & 11
    # ==========================================================
    add_h1("10. TOOLS AND TECHNOLOGIES REQUIRED")
    tech_data = [
        ("Tool / technology", "Role in the project"),
        ("Python 3", "Primary programming language and application logic"),
        ("FastAPI", "High-performance asynchronous REST API framework and static SPA serving"),
        ("Scikit-learn", "TF-IDF Vectorizer, cosine similarity metrics, and sparse matrix operations"),
        ("NumPy & Pandas", "Numerical operations, latency percentiles, and tabular CSV workflows"),
        ("SQLite", "Persistent relational storage for FAQs, benchmark runs, and evaluated responses"),
        ("Google Gemini API", "Foundation LLM (Gemini 1.5 Flash) for grounded contextual RAG generation"),
        ("React 18 & TypeScript", "Type-safe interactive single-page user interface"),
        ("Tailwind CSS", "Responsive utility-first styling and modern dark AI research dashboard theme"),
        ("Recharts & Framer Motion", "Interactive performance charts and micro-interaction animations"),
        ("pytest", "Automated unit and integration testing suite")
    ]
    t_tech = doc.add_table(rows=len(tech_data), cols=2)
    t_tech.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_tech)
    for r_idx, (t_tool, t_role) in enumerate(tech_data):
        row = t_tech.rows[r_idx]
        is_hdr = (r_idx == 0)
        for c_idx, text_val in enumerate([t_tool, t_role]):
            cell = row.cells[c_idx]
            cell.width = Inches(2.2) if c_idx == 0 else Inches(4.4)
            set_cell_margins(cell, top=50, bottom=50, left=100, right=100)
            if is_hdr:
                set_cell_background(cell, "1F3750")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "FFFFFF")
            else:
                set_cell_background(cell, "F8FAFC")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(text_val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if is_hdr:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            elif c_idx == 0:
                r.font.bold = True

    add_p(
        "The supplied requirements file pins FastAPI, Scikit-learn, NumPy, Pandas, pytest and Pydantic dependencies. The project is implemented in "
        "Python. The code also includes automated batch scripts for Windows execution (start_server.bat and run_tests.bat); this report does not claim "
        "that a multi-tenant cloud SaaS deployment has been completed."
    )
    add_subhead("Security and privacy considerations:")
    add_p(
        "The supplied project is primarily a local research and benchmarking prototype. Query fields may contain user-entered inquiry information, "
        "so users should avoid entering unnecessary personal data. The repository manages Gemini API keys via environment variables (.env) and excludes "
        "them from version control. The repository does not document an enterprise OAuth2 single-sign-on system or encrypted cloud database. These should "
        "be considered before deployment with real student information."
    )

    add_h1("11. SYSTEM ARCHITECTURE")
    add_p("The system is organised into five logical layers: user interface, API and routing, AI engines, benchmark evaluation, and storage.")
    add_subhead("Architecture flow:")

    arch_data = [
        ("Layer", "Main responsibility", "Main module(s)"),
        ("Presentation", "Single-architecture chat, side-by-side comparison, benchmark runner, and charts", "App.tsx, PlaygroundPage.tsx, BenchmarkLabPage.tsx (React)"),
        ("API & Routing", "REST API endpoints, request validation, CORS, CSV/JSON streaming", "main.py, endpoints.py (FastAPI)"),
        ("AI Engines", "Rule matching, TF-IDF vectorization, cosine similarity, and RAG generation", "rule_engine.py, retrieval_engine.py, rag_engine.py"),
        ("Optimisation & Eval", "Benchmark execution, response scoring, hallucination detection, metrics calculation", "benchmark_runner.py, evaluator.py, analytics_service.py"),
        ("Data and testing", "Knowledge base persistence, SQLite tables, sample data, and unit tests", "database.py, seed_faqs.json, test_*.py")
    ]
    t_arch = doc.add_table(rows=len(arch_data), cols=3)
    t_arch.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_arch)
    for r_idx, row_tup in enumerate(arch_data):
        row = t_arch.rows[r_idx]
        is_hdr = (r_idx == 0)
        for c_idx, text_val in enumerate(row_tup):
            cell = row.cells[c_idx]
            cell.width = [Inches(1.4), Inches(3.0), Inches(2.2)][c_idx]
            set_cell_margins(cell, top=50, bottom=50, left=100, right=100)
            if is_hdr:
                set_cell_background(cell, "1F3750")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "FFFFFF")
            else:
                set_cell_background(cell, "F8FAFC")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(text_val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if is_hdr:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            elif c_idx == 0:
                r.font.bold = True

    add_p(
        "Request lifecycle: the user submits a query, the API normalizes the input string, and dispatches it to the selected engine. Pairwise cosine "
        "similarity checks compare the query against FAQ vectors, which are supplied to the RAG prompt builder where applicable. The user runs benchmark "
        "testing, and the evaluator returns accuracy and latency metrics, which the interface presents"
    )
    doc.add_page_break()

    # ==========================================================
    # PAGE 9: SECTIONS 11(cont), 12, 13
    # ==========================================================
    add_p("alongside the architecture visualisation and available benchmark information.")
    add_p(
        "The RAG engine uses strict prompt guardrails with few-shot grounding instructions. It explicitly refuses queries when retrieved context "
        "similarity falls below the confidence cutoff rather than silently fabricating an answer under the generative label. The user interface "
        "refers to this option as an LLM-based RAG architecture."
    )
    p_flow = doc.add_paragraph()
    p_flow.alignment = WD_ALIGN_PARAGRAPH.CENTER
    p_flow.paragraph_format.space_before = Pt(4)
    p_flow.paragraph_format.space_after = Pt(10)
    r_fl = p_flow.add_run("USER QUERY → NORMALIZATION → VECTOR SEARCH → SIMILARITY THRESHOLD → RAG PROMPT → RESULTS")
    r_fl.font.name = 'Times New Roman'
    r_fl.font.bold = True
    r_fl.font.size = Pt(8.5)

    add_h1("12. EXPECTED OUTCOMES AND TESTING")
    add_p(
        "The intended outcome is a working prototype that converts an FAQ database into a multi-architecture conversational platform and "
        "produces candidate answers that can be inspected and compared. The system is designed to provide more realistic evaluation metrics "
        "than theoretical estimates when the benchmark accurately represents real-world enquiry distributions."
    )

    test_data = [
        ("Evaluation area", "Metric / validation", "Evidence available in supplied project"),
        ("Rule pattern matching", "Correct identification and ordering of regex priority rules", "Automated rule tests; 41 regex rules in rule_engine.py"),
        ("Vector extraction", "Term frequency and inverse document frequency representation", "Retrieval tests and Scikit-learn TF-IDF implementation"),
        ("Similarity calculation", "Cosine distance accuracy and thresholding behavior", "Automated retrieval engine tests"),
        ("Architecture comparison", "Candidate response, latency, token cost and hallucination score", "Three engine implementations"),
        ("Out-of-scope handling", "Rejection rate on unrelated inquiries (sports, weather)", "0.35 confidence threshold in retrieval_engine.py"),
        ("Benchmark evaluation", "Mean accuracy, latency percentiles, and category breakdown", "Automated 50-question benchmark runner"),
        ("Software validation", "Passing unit and integration tests", "16 unit tests passed when the test modules were run")
    ]
    t_test = doc.add_table(rows=len(test_data), cols=3)
    t_test.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_test)
    for r_idx, row_tup in enumerate(test_data):
        row = t_test.rows[r_idx]
        is_hdr = (r_idx == 0)
        for c_idx, text_val in enumerate(row_tup):
            cell = row.cells[c_idx]
            cell.width = [Inches(1.6), Inches(2.5), Inches(2.5)][c_idx]
            set_cell_margins(cell, top=50, bottom=50, left=100, right=100)
            if is_hdr:
                set_cell_background(cell, "1F3750")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "FFFFFF")
            else:
                set_cell_background(cell, "F8FAFC")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(text_val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if is_hdr:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            elif c_idx == 0:
                r.font.bold = True

    add_p(
        "The verified test result is 16 passing tests across test_rule_engine.py, test_retrieval_engine.py, test_evaluator.py and test_benchmark.py. "
        "In addition, 13 end-to-end integration tests were executed against all FastAPI endpoints, verifying 100% operational connectivity."
    )
    add_p(
        "Empirical benchmark results recorded from executing all 50 test questions demonstrate: (i) Rule-Based Engine achieved 88.0% accuracy with an average "
        "latency of 0.26 ms; (ii) Semantic Retrieval achieved 90.0% accuracy with an average latency of 0.13 ms; and (iii) Out-of-scope rejection reached "
        "100.0% across both non-generative architectures. Such values represent reproducible experimental findings recorded in the SQLite database."
    )

    add_h1("13. APPLICATIONS AND SCOPE")
    add_subhead("Potential applications:")
    add_bullet("Small institutional helpdesks planning automated student inquiry handling.")
    add_bullet("Demonstrations and teaching exercises involving pattern matching, information retrieval and generative AI.")
    add_bullet("Comparative experiments involving deterministic rules, statistical retrieval, and prompt-engineered LLMs.")
    add_subhead("Included in the current project scope:")
    add_bullet("Single institutional FAQ dataset with 32 verified demonstration questions across 11 categories.")
    add_bullet("Priority-weighted regular expression matching and sublinear TF-IDF vector retrieval.")
    add_bullet("Cosine similarity search with an empirical 0.35 confidence threshold.")
    add_bullet("Retrieval-Augmented Generation schedule simulation and three chatbot engine approaches.")
    add_bullet("React and FastAPI interfaces, synthetic FAQ generation, automated tests and benchmark utilities.")
    add_subhead("Outside the current scope / limitations:")
    doc.add_page_break()

    # ==========================================================
    # PAGE 10: SECTIONS 13(cont), 14, 15
    # ==========================================================
    add_bullet("Live student records, fee payment processing, and authenticated portal integrations are not established by the supplied code.")
    add_bullet("The knowledge base is treated as static text; it is not automatically synchronised to live enterprise campus databases.")
    add_bullet("The model uses single-turn question-answering rather than multi-turn conversational dialogue state tracking.")
    add_bullet("The default token cost estimate is a simulation parameter and requires calibration against live provider invoices.")
    add_bullet("Synonym expansion depends on predefined dictionaries; unusual domain jargon may require dictionary additions.")
    add_bullet("The rule engine is limited to 41 hand-crafted regex patterns by design.")

    add_subhead("Future enhancements:")
    add_bullet("Integrate live student information systems and real-world payment gateway APIs.")
    add_bullet("Add multi-turn conversational memory and user session context tracking.")
    add_bullet("Extend the model to dense neural embeddings using sentence-transformers and vector databases (e.g. Chroma/Milvus).")
    add_bullet("Improve synonym expansion using automated word2vec or domain ontology embeddings.")
    add_bullet("Add multi-institutional benchmark datasets and repeatable experiment reports for cross-domain evaluation.")
    add_bullet("Introduce user authentication and secure handling of student identification data for production deployment.")

    add_h1("14. PROJECT TIMELINE")
    add_p(
        "The supplied source archive does not include dated development records. The following is therefore an indicative project "
        "workflow for presenting the stages of the work; it should not be interpreted as a verified record of the group’s actual "
        "week-by-week activity."
    )

    timeline_data = [
        ("Indicative phase", "Work planned / represented"),
        ("Phase 1", "Define the comparative chatbot problem and architectural evaluation model"),
        ("Phase 2", "Curate FAQ knowledge base and synthetic institutional dataset"),
        ("Phase 3", "Implement rule-based pattern matching and regex priority weighting"),
        ("Phase 4", "Implement text normalization, synonym expansion and stopword filtering"),
        ("Phase 5", "Implement TF-IDF vectorization and pairwise cosine similarity calculation"),
        ("Phase 6", "Implement confidence thresholding and out-of-scope refusal logic"),
        ("Phase 7", "Implement RAG prompt augmentation and Gemini Flash integration"),
        ("Phase 8", "Develop 50-question benchmark suite across four question tiers"),
        ("Phase 9", "Develop React single-page interface and FastAPI REST backend"),
        ("Phase 10", "Add benchmarking, analytics visualisation and CSV export"),
        ("Phase 11", "Run automated unit tests and refine module integration"),
        ("Phase 12", "Prepare documentation, viva defense guide and final project demonstration")
    ]
    t_time = doc.add_table(rows=len(timeline_data), cols=2)
    t_time.alignment = WD_TABLE_ALIGNMENT.CENTER
    set_table_borders(t_time)
    for r_idx, (t_ph, t_desc) in enumerate(timeline_data):
        row = t_time.rows[r_idx]
        is_hdr = (r_idx == 0)
        for c_idx, text_val in enumerate([t_ph, t_desc]):
            cell = row.cells[c_idx]
            cell.width = Inches(1.8) if c_idx == 0 else Inches(4.8)
            set_cell_margins(cell, top=45, bottom=45, left=100, right=100)
            if is_hdr:
                set_cell_background(cell, "1F3750")
            elif r_idx % 2 == 1:
                set_cell_background(cell, "FFFFFF")
            else:
                set_cell_background(cell, "F8FAFC")
            p = cell.paragraphs[0]
            p.paragraph_format.space_after = Pt(1)
            r = p.add_run(text_val)
            r.font.name = 'Times New Roman'
            r.font.size = Pt(8.5)
            if is_hdr:
                r.font.bold = True
                r.font.color.rgb = RGBColor(255, 255, 255)
            elif c_idx == 0:
                r.font.bold = True

    add_h1("15. CONCLUSION")
    add_p(
        "The Architecture Lab brings together pattern matching, statistical information retrieval and generative large language "
        "models in a modular chatbot evaluation prototype. It normalizes queries, matches regex patterns, computes vector cosine "
        "similarities using TF-IDF and uses those distances to synthesize grounded answers under factual constraints."
    )
    add_p(
        "The project includes three architecture implementations, schedule simulation, two user-facing interfaces, sample-FAQ management and "
        "benchmarking utilities. The supplied automated test modules produced 16 passing tests during verification. This supports the"
    )
    doc.add_page_break()

    # ==========================================================
    # PAGE 11: SECTIONS 15(cont), 16
    # ==========================================================
    add_p(
        "functional implementation of the tested components, while further multi-turn benchmarking and enterprise calibration "
        "remain necessary before operational deployment."
    )
    add_p(
        "Overall, the project demonstrates how classic pattern matching and information retrieval techniques can be combined with "
        "generative foundation models to support a practical institutional enquiry planning task."
    )

    add_h1("16. REFERENCES")
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
    for ref_str in ref_list:
        p_r = doc.add_paragraph()
        p_r.paragraph_format.space_after = Pt(3.5)
        p_r.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        r = p_r.add_run(ref_str)
        r.font.name = 'Times New Roman'
        r.font.size = Pt(8.0)

    # Save DOCX
    docx_local = r"C:\Users\Uday Shankar Praneet\.gemini\antigravity\scratch\architecture-lab\PROJECT_REPORT.docx"
    doc.save(docx_local)
    print(f"Successfully generated DOCX report: {docx_local}")

    # Copy to Desktop
    desktop = os.path.join(os.environ.get("USERPROFILE", ""), "OneDrive", "Desktop")
    if not os.path.exists(desktop):
        desktop = os.path.join(os.environ.get("USERPROFILE", ""), "Desktop")
    docx_desktop = os.path.join(desktop, "Architecture_Lab_Project_Report.docx")
    shutil.copy(docx_local, docx_desktop)
    print(f"Copied DOCX report to Desktop: {docx_desktop}")

if __name__ == "__main__":
    build_docx()
