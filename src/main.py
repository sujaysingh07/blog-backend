from fastapi import FastAPI
from src.model.user_model import User
from src.utils.db import Base,engine
from src.routes.auth_routes import auth_router
app = FastAPI(title="admin dashboard")

Base.metadata.create_all(bind=engine)

app.include_router(
    auth_router
)

@app.get("/home")
def home():
    return {
        "message": "All system is operational."
    }
