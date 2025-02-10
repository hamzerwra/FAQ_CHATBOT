# # retrieval.py

from database import get_db_connection
from embeddings import  get_text_embedding,bm25_search
from config import VECTOR_SEARCH_THRESHOLD

# def retrieve_faq(user_query):
#     """Retrieves the most relevant FAQ from PGVector & BM25 Backup."""
#     try:
#         conn = get_db_connection()
#         if not conn:
#             return "Not Known"
#         cursor = conn.cursor()

#         # ✅ Generate Embedding for User Query
#         query_embedding = get_text_embedding(user_query)

#         # ✅ Query PGVector for the closest match
#         cursor.execute(
#             """
#             SELECT question, answer, embedding <=> %s::vector AS distance
#             FROM company_faqs
#             ORDER BY distance ASC
#             LIMIT 1;
#             """,
#             (query_embedding,)
#         )

#         result = cursor.fetchone()
#         cursor.close()
#         conn.close()

#         # ✅ If PGVector finds a match, return it
#         if result and result[2] < VECTOR_SEARCH_THRESHOLD:
#             return result[1]

#         # ✅ Use BM25 Backup Search
#         return bm25_search(user_query)

#     except Exception as e:
#         return f"❌ Database error: {e}"
def retrieve_faq(user_query):
    """Retrieves the most relevant FAQ from PGVector & BM25 Backup."""
    try:
        conn = get_db_connection()
        if not conn:
            return "Not Known"
        cursor = conn.cursor()

        # ✅ Generate Embedding for User Query
        query_embedding = get_text_embedding(user_query)

        # ✅ Query PGVector for the closest match
        cursor.execute(
            """
            SELECT question, answer, embedding <=> %s::vector AS distance
            FROM company_faqs
            ORDER BY distance ASC
            LIMIT 1;
            """,
            (query_embedding,)
        )

        result = cursor.fetchone()
        cursor.close()
        conn.close()

        # ✅ If PGVector finds a match, return it
        if result and result[2] < VECTOR_SEARCH_THRESHOLD:
            return result[1]

        # ✅ Use BM25 Backup Search (Only if PGVector fails)
        bm25_result = bm25_search(user_query)
        if bm25_result.lower() != "not known":
            print(f"✅ DEBUG: BM25 Match Found: {bm25_result}")
            return bm25_result

        # ✅ If BM25 returns "Not Known", log it
        if bm25_result.lower() == "not known":
            print(f"❌ DEBUG: BM25 Match Discarded for Query: '{user_query}'")

        return bm25_result  # ✅ Return BM25 response or "Not Known"

    except Exception as e:
        return f"❌ Database error: {e}"

