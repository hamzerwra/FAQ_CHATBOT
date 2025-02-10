# usercontroller.py

from fastapi import Request, HTTPException, Depends, APIRouter
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import JSONResponse
from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from database import get_db_connection  # ✅ Import database connection
from config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES

# ✅ Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ OAuth2 scheme for token authentication
# ✅ Middleware for JWT Authentication
class JWTAuthMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        """Middleware to verify JWT token for protected routes."""
        if request.url.path in ["/login", "/docs", "/openapi.json","/register"]:  # ✅ Allow public routes
            return await call_next(request)

        token = request.headers.get("Authorization")

        if not token or not token.startswith("Bearer "):
            return JSONResponse(status_code=401, content={"detail": "Missing or invalid token"})

        token = token.split("Bearer ")[1]  # Extract actual token

        try:
            payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
            request.state.user = payload.get("sub")  # ✅ Store authenticated username in request.state
        except JWTError:
            return JSONResponse(status_code=401, content={"detail": "Invalid or expired token"})

        return await call_next(request)

# ✅ Get User from Database
def get_user_from_db(username: str):
    """Retrieve user details from the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, password FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()

    if user:
        return {"username": user[0], "hashed_password": user[1]}
    return None

# ✅ Verify Password
def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# ✅ Authenticate User
def authenticate_user(username: str, password: str):
    user = get_user_from_db(username)
    if not user or not verify_password(password, user["hashed_password"]):
        return False
    return user

# ✅ Generate JWT Token
def create_access_token(data: dict, expires_delta: timedelta):
    to_encode = data.copy()
    expire = datetime.utcnow() + expires_delta
    to_encode.update({"exp": expire})
    return jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)

# ✅ Login Endpoint (Uses Database for Authentication)

def login_for_access_token(form_data):
    user = authenticate_user(form_data.username, form_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(
        data={"sub": user["username"]}, expires_delta=timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return {"access_token": access_token, "token_type": "bearer"}

# ✅ Helper Function to Get Authenticated User
async def get_current_user(request: Request):
    """Retrieve authenticated user from middleware."""
    user = getattr(request.state, "user", None)
    if not user:
        raise HTTPException(status_code=401, detail="Authentication required")
    return user
