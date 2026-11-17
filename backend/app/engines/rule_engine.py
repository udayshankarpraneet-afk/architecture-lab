import re
import time
import string
from typing import Dict, Any, List, Optional
from backend.app.models.schemas import ChatResponse

class RuleEngine:
    """
    Architecture A: Rule-Based Chatbot Engine
    Completely deterministic, pattern- and keyword-driven rules system.
    Does NOT use vector embeddings or LLM inference.
    """

    def __init__(self):
        # Compiled regex patterns and rule specifications
        # Higher priority number = evaluated earlier
        self.rules = [
            # 1. Adversarial & Prompt Injection Defense (Priority 100)
            {
                "id": "rule-adv-jailbreak",
                "priority": 100,
                "category": "Adversarial Defense",
                "pattern": r"(ignore\s+(all\s+)?(previous\s+)?instructions|unfilteredgpt|bribe|dan\s+mode|override\s+system)",
                "action": "refuse_adversarial",
                "response": "I cannot comply with requests that attempt to override system rules or compromise university integrity standards. I can only provide official information about Demo University."
            },
            {
                "id": "rule-adv-false-tuition",
                "priority": 95,
                "category": "Adversarial Defense",
                "pattern": r"(tuition\s+(is|become|fee\s+is)\s+(completely\s+)?free|state\s+that\s+tuition\s+is\s+free)",
                "action": "refuse_adversarial",
                "response": "Tuition at Demo University is not free. Official policy sets annual B.Tech tuition at $4,000 (INR 3,20,000) and MBA program fee at $9,500. Merit scholarships are available up to 100% for top qualifying scores."
            },
            {
                "id": "rule-adv-zero-attendance",
                "priority": 95,
                "category": "Adversarial Defense",
                "pattern": r"(abolish(ed)?\s+attendance|confirm\s+(that\s+)?zero\s+attendance|no\s+attendance\s+required)",
                "action": "refuse_adversarial",
                "response": "False claim. Demo University maintains a strictly enforced 75% minimum mandatory attendance requirement for all registered courses to appear in semester examinations."
            },
            {
                "id": "rule-adv-chancellor-phone",
                "priority": 90,
                "category": "Adversarial Defense",
                "pattern": r"(secret|direct|personal)\s+(phone|mobile|cell)\s+(number\s+of\s+)?(chancellor|dean)",
                "action": "refuse_adversarial",
                "response": "Personal contact details of university administrators are confidential. For legitimate admission inquiries, please contact the Admissions Helpdesk at +1 (555) 019-2830 or admissions@demouniv.edu."
            },

            # 2. Out-Of-Scope Detection Rules (Priority 85)
            {
                "id": "rule-oos-sports",
                "priority": 85,
                "category": "Out of Scope",
                "pattern": r"(fifa|world\s+cup|football|cricket|nba|messi|ronaldo|olympics|super\s+bowl)",
                "action": "refuse_out_of_scope",
                "response": "I do not have access to external sports news or tournament data. As the Demo University academic advisor, I only answer questions regarding university admissions, courses, fees, and campus facilities."
            },
            {
                "id": "rule-oos-weather",
                "priority": 85,
                "category": "Out of Scope",
                "pattern": r"(weather\s+(forecast|in|today|tomorrow)|temperature\s+in|is\s+it\s+raining)",
                "action": "refuse_out_of_scope",
                "response": "I do not have access to real-time meteorological or weather forecast services. Please consult a dedicated weather provider."
            },
            {
                "id": "rule-oos-cooking",
                "priority": 85,
                "category": "Out of Scope",
                "pattern": r"(recipe|cook|lasagna|pasta|pizza|ingredients\s+for|how\s+to\s+bake)",
                "action": "refuse_out_of_scope",
                "response": "Cooking recipes and culinary advice are outside my operational scope. I only assist with Demo University inquiries."
            },
            {
                "id": "rule-oos-finance",
                "priority": 85,
                "category": "Out of Scope",
                "pattern": r"(stock\s+price|aapl|crypto|bitcoin|ethereum|shares\s+of|market\s+cap)",
                "action": "refuse_out_of_scope",
                "response": "I do not track commercial equity markets or cryptocurrency prices. Please use a financial news service."
            },
            {
                "id": "rule-oos-entertainment",
                "priority": 85,
                "category": "Out of Scope",
                "pattern": r"(who\s+directed|inception|movie|oscar|actor|netflix|cinema|hollywood)",
                "action": "refuse_out_of_scope",
                "response": "Movie trivia and entertainment topics are outside my scope. I am dedicated solely to Demo University student inquiries."
            },
            {
                "id": "rule-oos-plumbing",
                "priority": 85,
                "category": "Out of Scope",
                "pattern": r"(kitchen\s+pipe|fix\s+(a\s+)?leak|plumbing|clogged\s+drain)",
                "action": "refuse_out_of_scope",
                "response": "Home maintenance and plumbing repair guidance are outside my scope as an academic admissions chatbot."
            },
            {
                "id": "rule-oos-science-homework",
                "priority": 85,
                "category": "Out of Scope",
                "pattern": r"(photosynthesis|chemical\s+equation|quantum\s+mechanics\s+equation|einstein\s+formula)",
                "action": "refuse_out_of_scope",
                "response": "General textbook science homework solutions are outside my role as Demo University's enquiry bot."
            },
            {
                "id": "rule-oos-hardware",
                "priority": 85,
                "category": "Out of Scope",
                "pattern": r"(best\s+gaming\s+laptop|buy\s+a\s+phone|specs\s+of\s+iphone|recommend\s+(a\s+)?laptop)",
                "action": "refuse_out_of_scope",
                "response": "Consumer hardware purchasing advice is outside the scope of Demo University admissions."
            },
            {
                "id": "rule-oos-coding",
                "priority": 85,
                "category": "Out of Scope",
                "pattern": r"(write\s+(a\s+)?python\s+script|beautifulsoup|scrape\s+data|code\s+in\s+c\+\+|javascript\s+function)",
                "action": "refuse_out_of_scope",
                "response": "Software coding generation is outside my role as Demo University enquiry bot."
            },
            {
                "id": "rule-oos-geography",
                "priority": 85,
                "category": "Out of Scope",
                "pattern": r"(capital\s+(city\s+)?of\s+(australia|france|japan|germany|canada))",
                "action": "refuse_out_of_scope",
                "response": "General world geography trivia is outside my domain. I only answer questions regarding Demo University."
            },

            # 3. Emergency & High Importance Contact Rules (Priority 80)
            {
                "id": "rule-emergency-medical",
                "priority": 80,
                "category": "Contact",
                "pattern": r"(medical\s+emergency|ambulance|hospital|doctor\s+at\s+night|health\s+centre)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Campus Health Centre Emergency Line: +1 (555) 019-9999 (24/7). Ambulances and medical staff are stationed around the clock near the Student Activity Centre."
            },
            {
                "id": "rule-contact-helpdesk",
                "priority": 75,
                "category": "Contact",
                "pattern": r"(contact|helpdesk|phone\s+number|email\s+address|call\s+admissions|office\s+hours)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Admissions Helpdesk: Phone: +1 (555) 019-2830, Email: admissions@demouniv.edu. Location: Welcome Centre, Admin Block. Hours: Monday-Friday, 9:00 AM - 5:00 PM."
            },

            # 4. Admissions & Deadlines Rules (Priority 70)
            {
                "id": "rule-admission-dates",
                "priority": 70,
                "category": "Admissions",
                "pattern": r"(when\s+(do|does)?\s*(the\s+)?admission(s)?(\s+process)?\s+start|last\s+date\s+to\s+apply|cutoff\s+date|application\s+deadline)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Admissions for the academic year 2026-27 at Demo University open on May 1st and close on June 30th. Late applications are accepted with a late fee until July 15th."
            },
            {
                "id": "rule-how-to-apply",
                "priority": 68,
                "category": "Admissions",
                "pattern": r"(how\s+(can\s+i|to)\s+apply|online\s+application|apply\s+online|register\s+for\s+admission)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Prospective students must register on the Demo University Admissions Portal (admissions.demouniv.edu), complete the online form, upload required certificates, and pay an application fee of $50."
            },
            {
                "id": "rule-entrance-exam",
                "priority": 67,
                "category": "Admissions",
                "pattern": r"(entrance\s+exam|ducet|entrance\s+test|write\s+any\s+test|admissions\s+test)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Yes, Demo University conducts the Demo University Common Entrance Test (DUCET) for all B.Tech and MBA programs. Direct admission is available for candidates with top 5% percentiles in national examinations."
            },

            # 5. Fees & Refunds Rules (Priority 65)
            {
                "id": "rule-btech-fee",
                "priority": 65,
                "category": "Fees",
                "pattern": r"(tuition\s+fee|b\.?tech\s+fee|engineering\s+tuition|how\s+much\s+(do\s+i\s+need\s+to\s+)?pay\s+(every|per)\s+year|cost\s+of\s+engineering)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] The annual tuition fee for B.Tech programs is $4,000 (INR 3,20,000) payable in two equal semester installments. A one-time refundable security deposit of $300 is charged at admission."
            },
            {
                "id": "rule-mba-fee",
                "priority": 64,
                "category": "Fees",
                "pattern": r"(mba\s+fee|mba\s+cost|mba\s+tuition|fee\s+structure\s+for\s+mba)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] The total program fee for the two-year MBA is $9,500 (INR 7,60,000), which includes tuition, course material, access to business simulation labs, and industry immersions."
            },
            {
                "id": "rule-refund-policy",
                "priority": 63,
                "category": "Fees",
                "pattern": r"(refund\s+policy|cancel\s+admission|withdraw\s+admission|get\s+(my\s+)?money\s+back|cancel\s+my\s+seat)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] 100% of fees minus $20 processing charge is refunded if withdrawn 15 days before classes commence; 80% if within 15 days before; 50% within 15 days after classes start; zero refund after 30 days."
            },

            # 6. Scholarships (Priority 60)
            {
                "id": "rule-merit-scholarship",
                "priority": 60,
                "category": "Scholarships",
                "pattern": r"(merit\s+scholarship|chancellor|fee\s+discount|fee\s+waiver|scholarship\s+for\s+high\s+marks)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Yes, the Chancellor's Merit Scholarship awards up to 100% tuition waiver to students ranking in the top 1% of DUCET, and 50% tuition waiver for students scoring above 90% in 10+2 examinations."
            },
            {
                "id": "rule-need-sports-scholarship",
                "priority": 59,
                "category": "Scholarships",
                "pattern": r"(need\s+based|sports\s+scholarship|financial\s+aid|concession|grant)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Yes, Demo University offers the Need-cum-Means Grant covering up to 40% tuition for families with annual income under $8,000, and Sports Excellence Fellowships for national medalists."
            },

            # 7. Eligibility Rules (Priority 55)
            {
                "id": "rule-eligibility-btech",
                "priority": 55,
                "category": "Eligibility",
                "pattern": r"(eligibility.*b\.?tech|percentage.*cse|marks.*computer\s+science|without\s+mathematics)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Applicants must have completed 10+2 or equivalent with Physics, Mathematics, and Chemistry/Computer Science, securing a minimum aggregate of 60% (55% for reserved categories)."
            },
            {
                "id": "rule-eligibility-mba",
                "priority": 54,
                "category": "Eligibility",
                "pattern": r"(eligibility.*mba|mba\s+requirements|graduation\s+marks\s+for\s+mba)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Candidates must hold a recognized Bachelor's degree in any discipline with at least 50% aggregate marks and a valid score in DUCET-Management or national CAT/GMAT exams."
            },
            {
                "id": "rule-international-students",
                "priority": 53,
                "category": "Eligibility",
                "pattern": r"(international\s+students|foreign\s+students|toefl|ielts|aiu)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] International applicants are eligible provided they have equivalent qualification credentials evaluated by the Association of Indian Universities (AIU) and valid English proficiency scores (TOEFL/IELTS)."
            },

            # 8. Courses & Academics (Priority 50)
            {
                "id": "rule-engineering-courses",
                "priority": 50,
                "category": "Courses",
                "pattern": r"(undergraduate\s+engineering\s+courses|what\s+courses\s+are\s+offered|b\.?tech\s+branches|degrees\s+offered)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Demo University offers four-year B.Tech programs in Computer Science & Engineering, Artificial Intelligence & Data Science, Electronics & Communication Engineering, and Mechanical Engineering."
            },
            {
                "id": "rule-postgraduate-courses",
                "priority": 49,
                "category": "Courses",
                "pattern": r"(postgraduate|m\.?tech|ph\.?d|doctoral|masters\s+degree)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Yes, Demo University provides M.Tech, MBA, M.Sc in Data Science, and Ph.D. research fellowships across Engineering, Sciences, and Management disciplines."
            },
            {
                "id": "rule-minors",
                "priority": 48,
                "category": "Courses",
                "pattern": r"(interdisciplinary\s+minor|minors|specialization|cybersecurity.*minor)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Yes, undergraduate students can take minors in disciplines such as Computational Finance, Cybersecurity, Environmental Studies, and Product Design starting from their 3rd semester."
            },

            # 9. Hostel & Campus Life (Priority 45)
            {
                "id": "rule-hostel-rooms",
                "priority": 45,
                "category": "Hostel",
                "pattern": r"(hostel\s+facilities|room\s+types|university\s+dorms|kinds\s+of\s+rooms|stay\s+in\s+hostel)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Demo University provides separate air-conditioned and non-AC hostels for boys and girls with single, double, and triple-occupancy rooms. All hostels include 24/7 Wi-Fi, laundry, and dining halls."
            },
            {
                "id": "rule-hostel-fee",
                "priority": 44,
                "category": "Hostel",
                "pattern": r"(hostel\s+fee|mess\s+fee|eating\s+in\s+the\s+mess|food\s+charges|boarding\s+in\s+hostel)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] The annual hostel fee ranges from $1,200 (triple non-AC) to $2,200 (single AC) per year. The mess charge is $900 annually, covering breakfast, lunch, evening snacks, and dinner."
            },
            {
                "id": "rule-hostel-curfew",
                "priority": 43,
                "category": "Hostel",
                "pattern": r"(curfew|hostel\s+timing|night\s+out|leave\s+rules|in\s+time)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Campus curfew is 9:30 PM for all resident students. Overnight leave requires prior digital approval from parents and the hostel warden via the Campus Life App."
            },

            # 10. Library (Priority 40)
            {
                "id": "rule-library-hours",
                "priority": 40,
                "category": "Library",
                "pattern": r"(library\s+(working\s+)?hours|till\s+what\s+time.*library|library\s+timings|digital\s+library)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] The Central Library is open from 8:00 AM to 10:00 PM on weekdays, and 9:00 AM to 5:00 PM on weekends. During semester exams, reading halls operate 24/7 with access to IEEE, ACM, and Springer journals."
            },
            {
                "id": "rule-library-books",
                "priority": 39,
                "category": "Library",
                "pattern": r"(borrow\s+books|how\s+many\s+books|book\s+issue|library\s+card)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Undergraduate students can borrow up to 4 books for 14 days, while postgraduate and research scholars can borrow up to 8 books for 30 days. Renewals are done via the web OPAC."
            },

            # 11. Examinations & Attendance (Priority 35)
            {
                "id": "rule-attendance-exam",
                "priority": 35,
                "category": "Examinations",
                "pattern": r"(attendance\s+requirement|minimum\s+attendance|75%|debarred\s+from\s+writing\s+exams)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] A minimum of 75% attendance in each registered course is mandatory to be eligible for end-semester examinations. Medical condonation up to 10% is permitted with Dean approval."
            },
            {
                "id": "rule-grading-system",
                "priority": 34,
                "category": "Examinations",
                "pattern": r"(grading\s+system|cgpa|sgpa|10-point\s+scale)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Demo University follows a 10-point relative grading scale: O (10), A+ (9), A (8), B+ (7), B (6), C (5), and F (Fail, 0). CGPA is computed as the credit-weighted average of grade points."
            },
            {
                "id": "rule-supplementary-exam",
                "priority": 33,
                "category": "Examinations",
                "pattern": r"(fail\s+a\s+subject|re-exam|supplementary\s+exam|re-evaluation|backlog)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Students receiving an 'F' grade can appear for supplementary examinations held in July and January. Re-evaluation requests must be submitted within 10 days of results declaration for a fee of $15 per paper."
            },

            # 12. Transportation & Documents (Priority 30)
            {
                "id": "rule-transportation-bus",
                "priority": 30,
                "category": "Transportation",
                "pattern": r"(bus\s+(service|transport|pass)|transportation|commuting\s+from\s+home|bus\s+routes)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Yes, Demo University operates a fleet of 25 GPS-tracked air-conditioned buses covering all major metropolitan routes within a 45-kilometer radius of the campus. Annual pass fee is $350-$600."
            },
            {
                "id": "rule-documents-verification",
                "priority": 28,
                "category": "Documents",
                "pattern": r"(documents\s+(required|needed)|document\s+verification|what\s+papers\s+do\s+i\s+need|original\s+certificates)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Required documents: 10th and 12th original marksheets and passing certificates, transfer certificate (TC), migration certificate, category certificate (if applicable), 6 passport-size photographs, and government ID proof."
            },
            {
                "id": "rule-transcript-certificate",
                "priority": 27,
                "category": "Documents",
                "pattern": r"(official\s+transcript|degree\s+certificate|bona\s+fide|character\s+certificate)",
                "action": "answer",
                "response": "[DEMONSTRATION DATA] Official transcripts and provisional certificates can be requested through records.demouniv.edu (7-10 days dispatch). Bona fide certificates are generated digitally via the student portal within 24 hours."
            }
        ]

        # Sort rules strictly by priority descending
        self.rules.sort(key=lambda r: r["priority"], reverse=True)

    def normalize_text(self, text: str) -> str:
        """
        Step 1: Normalisation
        - Lowercase
        - Strip punctuation
        - Normalize multiple whitespaces
        """
        text = text.lower()
        # Remove punctuation
        text = re.sub(r'[' + re.escape(string.punctuation) + r']', ' ', text)
        # Collapse multiple spaces
        text = re.sub(r'\s+', ' ', text).strip()
        return text

    def process(self, query: str) -> ChatResponse:
        start_time = time.perf_counter()

        trace_steps = []
        normalized_query = self.normalize_text(query)
        trace_steps.append({
            "stage": "Text Normalisation",
            "description": "Converted text to lowercase, removed punctuation, collapsed whitespace.",
            "data": {"raw": query, "normalized": normalized_query}
        })

        matched_rule = None
        response_text = ""
        is_supported = True

        trace_steps.append({
            "stage": "Rule Evaluation",
            "description": f"Evaluating query sequentially across {len(self.rules)} IF-THEN rules sorted by priority.",
            "data": {"rules_count": len(self.rules)}
        })

        # Evaluate rules in strict priority order
        for rule in self.rules:
            # Test regex against both normalized and original text
            match = re.search(rule["pattern"], query, re.IGNORECASE) or re.search(rule["pattern"], normalized_query, re.IGNORECASE)
            if match:
                matched_rule = rule
                response_text = rule["response"]
                is_supported = (rule["action"] == "answer")
                trace_steps.append({
                    "stage": "Rule Matched",
                    "description": f"Matched Rule ID: {rule['id']} (Priority {rule['priority']}, Category: {rule['category']})",
                    "data": {
                        "rule_id": rule["id"],
                        "priority": rule["priority"],
                        "category": rule["category"],
                        "pattern": rule["pattern"],
                        "matched_text": match.group(0)
                    }
                })
                break

        # Fallback if no rule matched
        if not matched_rule:
            response_text = "I am sorry, but I do not have a predefined rule to answer this query. Please consult the Demo University Admissions Office at admissions@demouniv.edu or +1 (555) 019-2830."
            is_supported = False
            trace_steps.append({
                "stage": "Fallback Invoked",
                "description": "No regex or keyword rule matched the query. Fallback message generated.",
                "data": {"status": "NO_MATCH"}
            })

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return ChatResponse(
            architecture="rules",
            message=response_text,
            latency_ms=round(elapsed_ms, 2),
            confidence=1.0 if matched_rule else 0.0,
            retrieved_sources=[],
            matched_rule=matched_rule["id"] if matched_rule else "FALLBACK",
            is_supported=is_supported,
            token_usage={"input_tokens": 0, "output_tokens": 0},
            estimated_cost=0.0,
            trace_steps=trace_steps,
            warning_or_error=None
        )

# Global singleton
rule_engine = RuleEngine()
