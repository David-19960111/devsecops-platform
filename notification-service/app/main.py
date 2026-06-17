from fastapi import FastAPI, BackgroundTasks
from pydantic import BaseModel
from dotenv import load_dotenv
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
    resource=Resource.create({"service.name": "notification-service"})
)
exporter = OTLPSpanExporter(endpoint="http://jaeger:4318/v1/traces")
provider.add_span_processor(BatchSpanProcessor(exporter))
trace.set_tracer_provider(provider)

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Notification Service", version="1.0.0",
    docs_url="/docs" if os.getenv("ENV") != "production" else None, redoc_url=None)

FastAPIInstrumentor.instrument_app(app)

class Notification(BaseModel):
    type: str
    recipient: str
    message: str

async def send_notification(notification: Notification):
    logger.info(f"Enviando {notification.type} a {notification.recipient}: {notification.message}")

@app.post("/notify")
async def send(notification: Notification, background_tasks: BackgroundTasks):
    background_tasks.add_task(send_notification, notification)
    return {"status": "sent", "type": notification.type, "recipient": notification.recipient}

@app.get("/health")
def health():
    return {"status": "ok", "service": "notification-service"}

Instrumentator().instrument(app).expose(app)