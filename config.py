# config.py

# ✅ Database Connection Details
DB_NAME = "faqdb"
DB_USER = "admin"
DB_PASSWORD = "admin"
DB_HOST = "localhost"
DB_PORT = "5432"

# ✅ SBERT Model
SBERT_MODEL = "all-MiniLM-L6-v2"

# ✅ LLM Model
LLM_MODEL = "TheBloke/Llama-2-7B-Chat-GGUF"
LLM_TYPE = "llama"

# ✅ Similarity Thresholds
VECTOR_SEARCH_THRESHOLD = 0.35
BM25_MATCH_THRESHOLD = 0.5

# ✅ JWT Authentication Configuration (Add These)
SECRET_KEY = "yaskdask;dma;smda;lsdma;smd"  # Change this to a strong secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 300 # Token expiry time in minutes
