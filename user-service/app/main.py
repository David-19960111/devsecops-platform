from fastapi import FastAPI
from dotenv import load_dotenv
from app.routes import router
from app.database import engine
from app import models
from prometheus_fastapi_instrumentator import Instrumentator
from opentelemetry import trace
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.sdk.resources import Resource
from opentelemetry.sdk.trace.export import BatchSpanProcessor
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.instrumentation.fastapi import FastAPIInstrumentor
import logging
import os

load_dotenv()

provider = TracerProvider(
    resource=Resource.create({"service.name": "user-service"})
)
exporter = OTLPSpanExporter(endpoint="http://jaeger:4318/v1/traces")
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

models.Base.metadata.create_all(bind=engine)

logging.basicConfig(level=logging.INFO)

app = FastAPI(title="User Service", version="1.0.0",
    docs_url="/docs" if os.getenv("ENV") != "production" else None, redoc_url=None)

FastAPIInstrumentor.instrument_app(app)

app.include_router(router, prefix="/users")

Instrumentator().instrument(app).expose(app)

@app.get("/health")
def health():
    return {"status": "ok", "service": "user-service"}