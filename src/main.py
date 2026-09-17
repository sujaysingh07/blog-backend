from fastapi import FastAPI, APIRouter
import uvicorn
from src.model.user_model import User
from src.model.blog_model import Blog
from src.utils.db import Base, engine
from fastapi.middleware.cors import CORSMiddleware
from src.routes.auth_routes import auth_router
from src.routes.blog_routes import blog_router
from src.routes.ai_routes import ai_router

app = FastAPI(title="admin dashboard")
def start_dev():
    uvicorn.run("src.main:app", host="127.0.0.1", port=8000, reload=True)
origins = [
    "http://localhost:5173",  # Vite default port
    "http://localhost:3000",  # React/Next.js default port
    "http://127.0.0.1:5173",
    # Add any other specific frontend URLs here
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,  # Only allows requests from the origins listed above
    allow_credentials=True,  # REQUIRED: Allows the frontend to send HttpOnly cookies
    allow_methods=["*"],  # Allows all HTTP methods (GET, POST, PUT, DELETE, OPTIONS)
    allow_headers=["*"],  # Allows all headers (Authorization, Content-Type)
)
Base.metadata.create_all(bind=engine)

global_router = APIRouter(prefix="/api/v1")

global_router.include_router(auth_router)
global_router.include_router(blog_router)
global_router.include_router(ai_router)
app.include_router(global_router)


@app.get("/home")
def home():
    return {"message": "All system is operational."}
