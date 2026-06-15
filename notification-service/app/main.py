from fastapi import FastAPI
from pydantic import BaseModel
from dotenv import load_dotenv
import logging
import os

load_dotenv()

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

app = FastAPI(title="Notification Service", version="1.0.0")

class Notification(BaseModel):
    type: str
    recipient: str
    message: str

@app.post("/notify")
def send_notification(notification: Notification):
    logger.info(f"Enviando {notification.type} a {notification.recipient}: {notification.message}")
    return {"status": "sent", "type": notification.type, "recipient": notification.recipient}

@app.get("/health")
def health():
    return {"status": "ok", "service": "notification-service"}