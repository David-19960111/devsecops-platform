from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas import UserRegister, UserLogin, TokenResponse
from app.auth import hash_password, verify_password, create_token
from app.models import User
from app.database import get_db

router = APIRouter()

@router.post("/register")
def register(user: UserRegister, db: Session = Depends(get_db)):
    existing = db.query(User).filter(User.email == user.email).first()
    if existing:
        raise HTTPException(status_code=400, detail="Email ya registrado")
    
    new_user = User(
        email=user.email,
        full_name=user.full_name,
        hashed_password=hash_password(user.password)
    )
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return {"mensaje": "Usuario registrado correctamente", "id": str(new_user.id)}

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin, db: Session = Depends(get_db)):
    db_user = db.query(User).filter(User.email == user.email).first()
    
    if not db_user or not verify_password(user.password, db_user.hashed_password):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = create_token({"sub": db_user.email, "name": db_user.full_name})
    
    return {"access_token": token, "token_type": "bearer"}