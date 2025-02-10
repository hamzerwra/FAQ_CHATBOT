# controller/register.py

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from passlib.context import CryptContext
from database import get_db_connection
# ✅ Password Hashing
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

# ✅ User Registration Request Model
class RegisterRequest(BaseModel):
    username: str
    password: str

# ✅ Check if User Exists in Database
def user_exists(username: str):
    """Check if a user already exists in the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username FROM users WHERE username = %s", (username,))
    user = cursor.fetchone()
    conn.close()
    
    return user is not None  # ✅ Return True if user exists

# ✅ Store New User in Database
def save_user_to_db(username: str, hashed_password: str):
    """Insert a new user into the database."""
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute("INSERT INTO users (username, password) VALUES (%s, %s)", (username, hashed_password))
    conn.commit()
    conn.close()

# ✅ Registration Function
def register_user(register_data: RegisterRequest):
    """Handles user registration and password hashing."""

    if user_exists(register_data.username):
        raise HTTPException(status_code=400, detail="Username already exists")

    hashed_password = pwd_context.hash(register_data.password)  # ✅ Hash password before storing
    save_user_to_db(register_data.username, hashed_password)  # ✅ Save to DB

    return {"message": "User registered successfully"}
