import psycopg2  # ✅ Import psycopg2 for database operations
from langchain_community.llms import CTransformers
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain
from config import LLM_MODEL, LLM_TYPE
from pydantic import BaseModel
from retervial import retrieve_faq  # ✅ Import retrieve_faq function
from controller.context import get_previous_response, store_user_context  # ✅ Import context functions

# ✅ Load LLM Model
llm = CTransformers(
    model=LLM_MODEL,
    model_type=LLM_TYPE,
    config={'temperature': 0.7, 'max_new_tokens': 256}
)

# ✅ Define Prompt
template = """
You are an AI assistant that provides answers strictly based on the given context.
STRICTLY FOLLOW THESE RULES:

1. If the context is "Not Known", respond exactly: "Not Known."
2. Answer the question using only the context. Do NOT add any extra details.
3. Do NOT generate additional information or paraphrase the context.
4. If the answer is not in the context, respond with "Not Known."
5. Answer in the same language as the question.
6. If you do not know the answer, ."
7. strictly give only company revelant question's response rest respond with "Not Known.

Context: {context}
Question: {question}
Final Answer:
"""

class QueryModelRequest(BaseModel):
    question: str

# # ✅ Set up Prompt Template
prompt = PromptTemplate(template=template, input_variables=["context", "question"])

# # ✅ Create LLM Chain
qa_chain = LLMChain(llm=llm, prompt=prompt)


def generate_response(user_query, additional_context=None):
    """
    Handles FAQ retrieval and LLM processing.
    - Retrieves context from both `company_faqs` and `user_context`
    - Sends retrieved context to LLM for final response.
    - Stores only valid FAQ responses in `user_context`.
  
    # """

    # ✅ 1️⃣ Retrieve FAQ context and stored context
    faq_context = retrieve_faq(user_query)
    stored_context = get_previous_response(user_query)
    
    final_context = ""

    # ✅ 2️⃣ Combine FAQ and stored context if valid
    if faq_context and faq_context.lower() != "not known":
        final_context += faq_context + "\n"
    
    if stored_context and stored_context.lower() != "not known":
        final_context += stored_context

    # ✅ 3️⃣ Add additional context if provided
    if additional_context:
        final_context += "\n" + additional_context

    # ✅ 4️⃣ If no valid context exists, return "Not Known."
    if not final_context.strip():
        print(f"❌ DEBUG: No relevant context found for '{user_query}', enforcing 'Not Known.'")
        return "Not Known."

    print(f"✅ DEBUG: Sending context to LLM:\n{final_context}")

    # ✅ 5️⃣ Call LLM to generate response
    response = qa_chain.run({"context": final_context, "question": user_query}).strip()

    # # ✅ 6️⃣ If LLM response is invalid, not related to FAQ, or not "Not Known", enforce "Not Known."
    # if response.lower() in ["not known", "", None] or not is_related_to_faq(user_query, response):
    #     print(f"❌ DEBUG: LLM response is invalid ('{response}'), enforcing 'Not Known.'")
    #     return "Not Known."

    # ✅ 7️⃣ Store only valid FAQ responses in `user_context`
    store_user_context(user_query, response)

    return response


# def is_related_to_faq(question, faq_response):
#     """
#     Check if the FAQ response is actually relevant to the question.
#     This checks if the question is mentioned in the FAQ response.
#     """
#     return question.lower() in faq_response.lower()
