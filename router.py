from fastapi import APIRouter, Depends, HTTPException, status,Request,Query
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel
import logging
from transformers import LlamaForCausalLM, LlamaTokenizer
from retervial import retrieve_faq
from llm import generate_response
from controller.usercontroller import get_current_user, login_for_access_token
from controller.register import RegisterRequest, register_user
from controller.context import store_user_context, get_previous_response
# Logger setup
logger = logging.getLogger(__name__)

# Main API Router
router = APIRouter()

# Include Registration Router


# Response Models
class FAQResponse(BaseModel):
    answer: str

class TokenResponse(BaseModel):
    access_token: str
    token_type: str


#FAQ Endpoint
# @router.get("/faq", response_model=FAQResponse)
# def faq_endpoint(question: str, user: str = Depends(get_current_user)):
#     """Handles incoming FAQ queries. Requires Authentication."""
#     try:
#         context = retrieve_faq(question)
#         return {"answer": generate_response(question, context), "user": user}
#     except Exception as e:
#         logger.error(f"FAQ query failed: {e}")
#         raise HTTPException(status_code=500, detail="Internal Server Error")

# @router.get("/faq")
# def faq_endpoint(question: str, user: dict = Depends(get_current_user)):  
#     """Handles user questions, retrieves stored responses from DB & FAQs, and uses LLM."""

#     # ✅ 1️⃣ Check if the question exists in the database (either user_context or company_faqs)
#     stored_response = get_previous_response(question)
    
#     if stored_response and stored_response != "Not Known.":
#         print(f"✅ DEBUG: Returning stored response: {stored_response}")  # ✅ Debugging
#         return {"answer": stored_response}  # ✅ Directly return stored response

#     # ✅ 2️⃣ Fetch company FAQs (Backup in case get_previous_response fails)
#     company_faq_context = retrieve_faq(question)
#     print(f"✅ DEBUG: Retrieved FAQ context: {company_faq_context}")  # ✅ Debugging

#     # ✅ 3️⃣ Call LLM if no stored answer exists
#     response = generate_response(question, company_faq_context)
#     print(f"✅ DEBUG: LLM Response: {response}")  # ✅ Debugging

#     # ✅ 4️⃣ Store response in PostgreSQL only if LLM generates a valid answer
#     if response.lower() not in ["not known", "", None]:
#         store_user_context(question, response)

#     return {"answer": response}

# ✅ FAQ Endpoint (Ensures Correct Answer is Given & Stored)
# ✅ FAQ Endpoint with Enhanced Handling
@router.get("/faq", response_model=FAQResponse)
def faq_endpoint(
    question: str = Query(..., description="Enter the question you want to ask"),
    user: dict = Depends(get_current_user)
):  
    """Handles user questions, retrieves stored responses from DB & FAQs, and uses LLM."""

    # ✅ 1️⃣ Retrieve FAQ Context First (Primary Source)
    faq_context = retrieve_faq(question)
    logger.info(f"✅ Retrieved FAQ context: {faq_context}") 

    # ✅ 2️⃣ Fetch stored response from `user_context`
    stored_response = get_previous_response(question)
    print(stored_response,'hereere')

    # ✅ 3️⃣ Always call LLM regardless of FAQ or stored response
    response = generate_response(question, faq_context)
    logger.info(f"✅ LLM Response: {response}")

    # ✅ 4️⃣ If LLM returns a valid response, store it in `user_context`
    if response.lower() not in ["not known", "", None]:
        store_user_context(question, response)
        logger.info(f"✅ Stored LLM response in `user_context`: {response}")

    return {"answer": response}





# Login Endpoint
@router.post("/login", response_model=TokenResponse)
def login(form_data: OAuth2PasswordRequestForm = Depends()):
    """Handles user login and returns an access token."""
    try:
        return login_for_access_token(form_data)
    except Exception as e:
        logger.error(f"Login failed: {e}")
        raise HTTPException(status_code=401, detail="Invalid credentials")
# Register Endpoint
@router.post("/register")
def register(register_data: RegisterRequest):
    """Handles user registration."""
    logger.info("Registering new user")
    try:
        return register_user(register_data)
    except Exception as e:
        logger.error(f"Registration failed: {e}")
        raise HTTPException(status_code=400, detail=str(e))
