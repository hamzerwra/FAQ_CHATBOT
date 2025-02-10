
# # embeddings.py

# from sentence_transformers import SentenceTransformer
# from rank_bm25 import BM25Okapi
# import numpy as np
# from config import SBERT_MODEL

# # ✅ Load SBERT Model
# sbert_model = SentenceTransformer(SBERT_MODEL)

# # ✅ Load BM25 for Keyword Matching (Backup Search)
# faq_data = [
#     ("What are your working hours?", "Our office is open from 9 AM to 5 PM."),
#     ("What is the refund policy?", "We offer refunds within 30 days."),
#     ("How can I contact support?", "Email us at support@company.com."),
# ]
# faq_questions = [q[0].split() for q in faq_data]
# bm25 = BM25Okapi(faq_questions)

# def get_text_embedding(text):
#     """Generates a text embedding using SBERT."""
#     return sbert_model.encode(text).tolist()

# def bm25_search(user_query):
#     """Performs keyword-based search using BM25."""
#     tokenized_query = user_query.split()
#     bm25_scores = bm25.get_scores(tokenized_query)
#     best_match_index = np.argmax(bm25_scores)
#     best_match_score = bm25_scores[best_match_index]

#     return faq_data[best_match_index][1] if best_match_score > 0 else "Not Known"

from rank_bm25 import BM25Okapi
import numpy as np
from sentence_transformers import SentenceTransformer
from config import SBERT_MODEL

# ✅ Load SBERT Model
sbert_model = SentenceTransformer(SBERT_MODEL)

def get_text_embedding(text):
    """Generates a text embedding using SBERT."""
    return sbert_model.encode(text).tolist()

# ✅ Define FAQ Data
faq_data = [
    ("What are your working hours?", "Our office is open from 9 AM to 5 PM."),
    ("What is the refund policy?", "We offer refunds within 30 days."),
    ("How can I contact support?", "Email us at support@company.com."),
]

# ✅ Prepare BM25 Model
faq_questions = [q[0].split() for q in faq_data]  # Tokenize questions
bm25 = BM25Okapi(faq_questions)  # Initialize BM25 model

def bm25_search(user_query):
    """Performs keyword-based search using BM25 and ensures relevance."""
    tokenized_query = user_query.split()
    bm25_scores = bm25.get_scores(tokenized_query)
    best_match_index = np.argmax(bm25_scores)
    best_match_score = bm25_scores[best_match_index]

    # ✅ Only return result if it meets a confidence threshold
    if best_match_score > 0.75:  # 🔥 Adjust threshold (higher = more strict)
        return faq_data[best_match_index][1]  # ✅ Return relevant answer

    print(f"❌ DEBUG: BM25 discarded '{faq_data[best_match_index][1]}' for Query: '{user_query}' (Low Score: {best_match_score})")
    return "Not Known"  # 🔥 If score is too low, return "Not Known"
