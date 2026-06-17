from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import router
from app.database import engine
from app import models
from prometheus_fastapi_instrumentator import Instrumentator
import logging
import os

load_dotenv()

models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="User Service", version="1.0.0",
    docs_url="/docs" if os.getenv("ENV") != "production" else None, redoc_url=None)

app.include_router(router, prefix="/users")

Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}