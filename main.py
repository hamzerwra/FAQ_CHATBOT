from fastapi import FastAPI
import uvicorn
from router import router  # ✅ Import all routes
from controller.usercontroller import JWTAuthMiddleware
 # ✅ Import authentication middleware

# ✅ Initialize FastAPI App
app = FastAPI()

# ✅ Register Middleware
app.add_middleware(JWTAuthMiddleware)

# ✅ Register API Routers
app.include_router(router)  # ✅ Includes `/register` and `/faq`

if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)
from fastapi.middleware.cors import CORSMiddleware

# Create the app instance
app = FastAPI()

# Allow all origins (you can restrict it later if needed)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all domains
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods (GET, POST, etc.)
    allow_headers=["*"],  # Allows all headers
)

# Your FastAPI routes go here
