import bcrypt
from jose import jwt
from datetime import datetime, timedelta
import os

def hash_password(password: str) -> str:
    return bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

def verify_password(plain: str, hashed: str) -> bool:
    return bcrypt.checkpw(plain.encode('utf-8'), hashed.encode('utf-8'))

def create_token(data: dict) -> str:
    payload = data.copy()
    expire = datetime.utcnow() + timedelta(hours=24)
    payload.update({"exp": expire})
    return jwt.encode(payload, os.getenv("JWT_SECRET"), algorithm="HS256")