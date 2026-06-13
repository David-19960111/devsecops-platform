from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import router
import os

load_dotenv()

app = FastAPI(title="User Service", version="1.0.0")

app.include_router(router, prefix="/users")

@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}