import psycopg2
from database import get_db_connection

# # ✅ Function to store question & response without user_id
# def store_user_context(question: str, response: str):
#     """Stores the question and response in PostgreSQL."""
#     conn = get_db_connection()
#     cursor = conn.cursor()

#     try:
#         # ✅ Insert or Update: Prevent duplicate questions
#         cursor.execute("""
#             INSERT INTO user_context (question, response)
#             VALUES (%s, %s)
#             ON CONFLICT (question) DO UPDATE SET response = EXCLUDED.response;
#         """, (str(question), str(response)))  # ✅ Ensure correct types

#         conn.commit()
#     except psycopg2.Error as e:
#         print(f"❌ Database Error: {e}")  # ✅ Debugging
#     finally:



# def store_user_context(question: str, response: str):
#     """
#     Stores the question and response in PostgreSQL.
#     - If response is 'Not Known', it does NOT store the data.
#     - Only stores FAQ-related responses.
#     """

#     # ✅ Ensure we only store valid FAQ-related responses
#     if response.strip().lower() == "not known":
#         print(f"❌ DEBUG: Skipping storage for '{question}' as response is 'Not Known'.")
#         return  # ❌ Do NOT store anything

#     print(f"✅ DEBUG: Proceeding to store '{question}' with response '{response}'.")

#     # ✅ Connect to the database
#     conn = get_db_connection()
#     if conn is None:
#         print(f"❌ DEBUG: Failed to connect to the database. Skipping storage.")
#         return  # ❌ Do NOT continue without a valid connection

#     cursor = conn.cursor()

#     try:
#         print("❓ DEBUG: Inside the try block. Preparing to execute the insert query.")

#         # ✅ Insert into `user_context` and prevent duplicates with ON CONFLICT clause
#         cursor.execute("""
#             INSERT INTO user_context (question, response)
#             VALUES (%s, %s)
#             ON CONFLICT (question) DO UPDATE SET response = EXCLUDED.response;
#         """, (question, response))  # ✅ Ensure correct types (use placeholders)

#         conn.commit()

#         # ✅ Check if rows were affected
#         print(f"✅ DEBUG: {cursor.rowcount} row(s) affected.")
#         print(f"✅ DEBUG: Stored response for '{question}' in `user_context`.")

#     except psycopg2.Error as e:
#         print(f"❌ Database Error: {e}")  # ✅ Debugging

#     finally:
#         cursor.close()  # Always close the cursor
#
def store_user_context(question: str, response: str):
    """
    Stores the question and response in PostgreSQL.
    - If response is 'Not Known', it does NOT store the data.
    - Only stores FAQ-related responses.
    """

    # ✅ Ensure we only store valid FAQ-related responses
    if response.strip().lower() == "not known":
        print(f"❌ DEBUG: Skipping storage for '{question}' as response is 'Not Known'.")
        return  # ❌ Do NOT store anything

    print(f"✅ DEBUG: Proceeding to store '{question}' with response '{response}'.")

    # ✅ Connect to the database
    conn = get_db_connection()
    if conn is None:
        print(f"❌ DEBUG: Failed to connect to the database. Skipping storage.")
        return  # ❌ Do NOT continue without a valid connection

    cursor = conn.cursor()

    try:
        print("❓ DEBUG: Inside the try block. Preparing to execute the insert query.")

        # ✅ Insert into `user_context` and prevent duplicates with ON CONFLICT clause
        cursor.execute("""
            INSERT INTO user_context (question, response)
            VALUES (%s, %s)
            ON CONFLICT (question) DO UPDATE SET response = EXCLUDED.response;
        """, (question, response))  # ✅ Ensure correct types (use placeholders)

        conn.commit()

        # ✅ Check if rows were affected
        print(f"✅ DEBUG: {cursor.rowcount} row(s) affected.")
        print(f"✅ DEBUG: Stored response for '{question}' in `user_context`.")

    except psycopg2.Error as e:
        print(f"❌ Database Error: {e}")  # ✅ Debugging

    finally:
        cursor.close()  # Always close the cursor
        conn.close()  # Close the connection


def is_related_to_faq(question, faq_response):
    """Check if the FAQ response is actually relevant to the question."""
    return question.lower() in faq_response.lower()


def get_previous_response(question: str):
    """Fetches response for a given question from user_context and company_faqs."""
    
    conn = get_db_connection()
    cursor = conn.cursor()

    try:
        # ✅ 1️⃣ Check user_context first (previously stored user responses)
        cursor.execute("""
            SELECT response FROM user_context 
            WHERE question = %s
            ORDER BY timestamp DESC
            LIMIT 1;
        """, (question,))

        result = cursor.fetchone()
        
        if result:
            print(f"✅ DEBUG: Found stored user response: {result[0]}")  # ✅ Debugging
            return result[0]
      

        # ✅ 2️⃣ If not found, check company_faqs (predefined FAQ responses)
        cursor.execute("""
            SELECT answer FROM company_faqs
            WHERE question = %s
            LIMIT 1;
        """, (question,))

        result = cursor.fetchone()

        if result:
            print(f"✅ DEBUG: Found predefined FAQ answer: {result[0]}")  # ✅ Debugging
            return result[0]

        # ✅ 3️⃣ If no response found, return "Not Known."
        print("❌ DEBUG: No response found in both user_context and company_faqs.")
        return "Not Known."

    except psycopg2.Error as e:
        print(f"❌ Database Error: {e}")  # ✅ Debugging
        return "Not Known."
    
    finally:
        conn.close()

