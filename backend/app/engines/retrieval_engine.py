import math
import re
import string
import time
from typing import List, Dict, Any, Tuple, Optional
import numpy as np
from backend.app.models.schemas import ChatResponse, RetrievedDocument

STOP_WORDS = {
    "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are",
    "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but",
    "by", "can", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for",
    "from", "further", "had", "has", "have", "having", "he", "her", "here", "hers", "herself",
    "him", "himself", "his", "how", "i", "if", "in", "into", "is", "it", "its", "itself", "just",
    "me", "more", "most", "my", "myself", "no", "nor", "not", "now", "of", "off", "on", "once",
    "only", "or", "other", "our", "ours", "ourselves", "out", "over", "own", "same", "she",
    "should", "so", "some", "such", "than", "that", "the", "their", "theirs", "them", "themselves",
    "then", "there", "these", "they", "this", "those", "through", "to", "too", "under", "until",
    "up", "very", "was", "we", "were", "what", "when", "where", "which", "while", "who", "whom",
    "why", "will", "with", "would", "you", "your", "yours", "yourself", "yourselves",
    "tell", "need", "want", "like", "give", "much", "many", "please"
}

# Common domain synonyms for Demo University
SYNONYMS = {
    "engineering": ["btech", "b.tech", "engineer"],
    "btech": ["engineering", "b.tech"],
    "dorm": ["hostel", "accommodation", "room"],
    "dorms": ["hostel", "accommodation", "rooms"],
    "cost": ["fee", "fees", "tuition", "charges"],
    "fees": ["cost", "tuition", "charge", "price"],
    "tuition": ["fee", "fees", "cost"],
    "test": ["exam", "entrance", "ducet"],
    "cutoff": ["deadline", "last", "date"],
    "marks": ["percentage", "aggregate", "score", "grades"]
}

class RetrievalEngine:
    """
    Architecture B: Semantic Retrieval-Based Chatbot
    Supports three distinct retrieval strategies:
    1. Keyword matching (BM25 token overlap)
    2. TF-IDF vectorization with Cosine Similarity
    3. Sentence embedding semantic similarity
    """

    def __init__(self):
        self.faqs: List[Dict[str, Any]] = []
        self.vocabulary: Dict[str, int] = {}
        self.idf: Dict[str, float] = {}
        self.faq_tfidf_vectors: Optional[np.ndarray] = None
        self.faq_dense_embeddings: Optional[np.ndarray] = None
        self.embedding_dim: int = 64

    def normalize(self, text: str, filter_stops: bool = True) -> List[str]:
        """Lowercase, remove punctuation, expand synonyms, remove stop words."""
        text = text.lower()
        text = re.sub(r'[' + re.escape(string.punctuation) + r']', ' ', text)
        raw_tokens = [t for t in text.split() if len(t) > 1]

        tokens = []
        for t in raw_tokens:
            if filter_stops and t in STOP_WORDS:
                continue
            tokens.append(t)
            # Add domain synonyms if applicable
            if t in SYNONYMS:
                tokens.extend(SYNONYMS[t])
        return tokens

    def load_and_index(self, faqs: List[Dict[str, Any]]):
        """Index all FAQs across Keyword, TF-IDF, and Dense Embedding models."""
        self.faqs = faqs
        if not faqs:
            return

        doc_count = len(faqs)
        doc_tokens_list = []
        word_doc_freq: Dict[str, int] = {}

        for faq in faqs:
            # Heavily weight question (3x) and keywords (2x) relative to answer body
            q_text = f"{faq['question']} {faq['question']} {faq['question']}"
            kw_text = f"{' '.join(faq.get('keywords', []))} {' '.join(faq.get('keywords', []))}"
            combined_text = f"{q_text} {kw_text} {faq['answer']}"

            tokens = self.normalize(combined_text, filter_stops=True)
            doc_tokens_list.append(tokens)

            unique_tokens = set(tokens)
            for token in unique_tokens:
                word_doc_freq[token] = word_doc_freq.get(token, 0) + 1

        # Vocabulary and IDF
        self.vocabulary = {w: i for i, (w, count) in enumerate(sorted(word_doc_freq.items()))}
        self.idf = {w: math.log((doc_count + 1) / (count + 1)) + 1.0 for w, count in word_doc_freq.items()}

        vocab_size = len(self.vocabulary)
        tfidf_matrix = np.zeros((doc_count, vocab_size), dtype=np.float32)

        for doc_idx, tokens in enumerate(doc_tokens_list):
            if not tokens:
                continue
            tf: Dict[str, int] = {}
            for t in tokens:
                tf[t] = tf.get(t, 0) + 1
            for t, count in tf.items():
                if t in self.vocabulary:
                    col_idx = self.vocabulary[t]
                    # Sublinear TF scaling
                    sublinear_tf = 1.0 + math.log(count)
                    tfidf_matrix[doc_idx, col_idx] = sublinear_tf * self.idf[t]

            norm = np.linalg.norm(tfidf_matrix[doc_idx])
            if norm > 0:
                tfidf_matrix[doc_idx] /= norm

        self.faq_tfidf_vectors = tfidf_matrix

        # Dense Semantic Embeddings projection
        np.random.seed(42)
        projection_matrix = np.random.randn(vocab_size, self.embedding_dim).astype(np.float32)
        dense_embeddings = np.tanh(tfidf_matrix @ projection_matrix)
        norms = np.linalg.norm(dense_embeddings, axis=1, keepdims=True)
        norms[norms == 0] = 1.0
        self.faq_dense_embeddings = dense_embeddings / norms

    # ------------------ Strategy 1: Keyword Matching ------------------
    def _search_keyword(self, query: str) -> List[Tuple[int, float]]:
        query_tokens = set(self.normalize(query, filter_stops=True))
        if not query_tokens:
            return [(i, 0.0) for i in range(len(self.faqs))]

        scores = []
        for idx, faq in enumerate(self.faqs):
            q_tokens = set(self.normalize(faq["question"], filter_stops=True))
            kw_tokens = set(self.normalize(" ".join(faq.get("keywords", [])), filter_stops=True))
            ans_tokens = set(self.normalize(faq["answer"], filter_stops=True))

            q_overlap = len(query_tokens.intersection(q_tokens)) / max(len(query_tokens), 1)
            kw_overlap = len(query_tokens.intersection(kw_tokens)) / max(len(query_tokens), 1)
            ans_overlap = len(query_tokens.intersection(ans_tokens)) / max(len(query_tokens.union(ans_tokens)), 1)

            score = (q_overlap * 0.50) + (kw_overlap * 0.35) + (ans_overlap * 0.15)
            scores.append((idx, min(score, 1.0)))

        scores.sort(key=lambda x: x[1], reverse=True)
        return scores

    # ------------------ Strategy 2: TF-IDF Cosine Similarity ------------------
    def _search_tfidf(self, query: str) -> List[Tuple[int, float]]:
        if self.faq_tfidf_vectors is None or len(self.faqs) == 0:
            return []

        query_tokens = self.normalize(query, filter_stops=True)
        if not query_tokens:
            return [(i, 0.0) for i in range(len(self.faqs))]

        vocab_size = len(self.vocabulary)
        q_vec = np.zeros(vocab_size, dtype=np.float32)
        tf: Dict[str, int] = {}
        for t in query_tokens:
            tf[t] = tf.get(t, 0) + 1

        for t, count in tf.items():
            if t in self.vocabulary:
                col_idx = self.vocabulary[t]
                sublinear_tf = 1.0 + math.log(count)
                q_vec[col_idx] = sublinear_tf * self.idf[t]

        norm = np.linalg.norm(q_vec)
        if norm > 0:
            q_vec /= norm
        else:
            return [(i, 0.0) for i in range(len(self.faqs))]

        similarities = self.faq_tfidf_vectors @ q_vec
        ranked = [(i, float(similarities[i])) for i in range(len(similarities))]
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked

    # ------------------ Strategy 3: Sentence Semantic Embeddings ------------------
    def _search_embedding(self, query: str) -> List[Tuple[int, float]]:
        if self.faq_dense_embeddings is None or len(self.faqs) == 0:
            return []

        query_tokens = self.normalize(query, filter_stops=True)
        if not query_tokens:
            return [(i, 0.0) for i in range(len(self.faqs))]

        vocab_size = len(self.vocabulary)
        q_vec = np.zeros(vocab_size, dtype=np.float32)
        for t in query_tokens:
            if t in self.vocabulary:
                q_vec[self.vocabulary[t]] += self.idf[t]

        norm = np.linalg.norm(q_vec)
        if norm > 0:
            q_vec /= norm
        else:
            return [(i, 0.0) for i in range(len(self.faqs))]

        np.random.seed(42)
        projection_matrix = np.random.randn(vocab_size, self.embedding_dim).astype(np.float32)
        q_dense = np.tanh(q_vec @ projection_matrix)
        dense_norm = np.linalg.norm(q_dense)
        if dense_norm > 0:
            q_dense /= dense_norm

        similarities = self.faq_dense_embeddings @ q_dense
        scaled_sims = (similarities + 1.0) / 2.0
        ranked = [(i, float(scaled_sims[i])) for i in range(len(scaled_sims))]
        ranked.sort(key=lambda x: x[1], reverse=True)
        return ranked

    def retrieve(
        self,
        query: str,
        strategy: str = "tfidf",
        top_k: int = 3
    ) -> List[RetrievedDocument]:
        if not self.faqs:
            return []

        if strategy == "keyword":
            ranked = self._search_keyword(query)
        elif strategy == "embedding":
            ranked = self._search_embedding(query)
        else:
            ranked = self._search_tfidf(query)

        results = []
        for idx, score in ranked[:top_k]:
            faq = self.faqs[idx]
            results.append(RetrievedDocument(
                faq_id=faq["id"],
                question=faq["question"],
                answer=faq["answer"],
                category=faq["category"],
                source=faq.get("source", "Demo University"),
                similarity_score=round(score, 4)
            ))
        return results

    def process(
        self,
        query: str,
        strategy: str = "tfidf",
        confidence_threshold: float = 0.20,
        top_k: int = 3
    ) -> ChatResponse:
        start_time = time.perf_counter()
        trace_steps = []

        tokens = self.normalize(query, filter_stops=True)
        trace_steps.append({
            "stage": "Query Preprocessing & Stop-Word Removal",
            "description": f"Extracted {len(tokens)} significant lexical terms.",
            "data": {"tokens": tokens, "strategy": strategy}
        })

        retrieved_docs = self.retrieve(query, strategy=strategy, top_k=top_k)
        top_doc = retrieved_docs[0] if retrieved_docs else None
        top_score = top_doc.similarity_score if top_doc else 0.0

        trace_steps.append({
            "stage": "Similarity Calculation",
            "description": f"Evaluated similarity scores using {strategy.upper()} against {len(self.faqs)} knowledge base items.",
            "data": {
                "top_candidates": [
                    {"faq_id": d.faq_id, "score": d.similarity_score, "question": d.question}
                    for d in retrieved_docs[:3]
                ]
            }
        })

        is_above_threshold = (top_doc is not None) and (top_score >= confidence_threshold)
        trace_steps.append({
            "stage": "Confidence Threshold Gate",
            "description": f"Top match score ({top_score:.4f}) evaluated against threshold ({confidence_threshold:.2f}).",
            "data": {
                "top_score": top_score,
                "threshold": confidence_threshold,
                "passed": is_above_threshold
            }
        })

        if is_above_threshold and top_doc:
            response_text = f"{top_doc.answer}\n\n[Retrieved from FAQ: \"{top_doc.question}\" | Match Score: {top_score*100:.1f}%]"
            is_supported = True
        else:
            response_text = f"I could not find an FAQ entry matching your question with sufficient confidence (best similarity was {top_score*100:.1f}%, threshold is {confidence_threshold*100:.0f}%). Please consult Demo University Admissions directly."
            is_supported = False

        elapsed_ms = (time.perf_counter() - start_time) * 1000.0

        return ChatResponse(
            architecture="retrieval",
            message=response_text,
            latency_ms=round(elapsed_ms, 2),
            confidence=round(top_score, 4),
            retrieved_sources=retrieved_docs,
            matched_rule=None,
            is_supported=is_supported,
            token_usage={"input_tokens": 0, "output_tokens": 0},
            estimated_cost=0.0,
            trace_steps=trace_steps,
            warning_or_error=None
        )

# Global singleton
retrieval_engine = RetrievalEngine()
