from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import router
from prometheus_fastapi_instrumentator import Instrumentator
import os

load_dotenv()

app = FastAPI(title="User Service", version="1.0.0")

app.include_router(router, prefix="/users")

Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}