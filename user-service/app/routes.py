from fastapi import APIRouter, HTTPException
from app.schemas import UserRegister, UserLogin, TokenResponse
from app.auth import hash_password, verify_password, create_token

router = APIRouter()

#Base de datos en memoria por ahora
users_db = {}

@router.post("/register")
def register(user: UserRegister):
    if user.email in users_db:
        raise HTTPException(status_code=400, detail="Email ya registrado.")
    
    users_db[user.email] = {
        "email": user.email,
        "full_name": user.full_name,
        "password": hash_password(user.password)
    }

    return {"mensaje": "Usuario registrado correctamente"}

@router.post("/login", response_model=TokenResponse)
def login(user: UserLogin):
    db_user = users_db.get(user.email)
    
    if not db_user or not verify_password(user.password, db_user["password"]):
        raise HTTPException(status_code=401, detail="Credenciales incorrectas")
    
    token = create_token({"sub": user.email, "name": db_user["full_name"]})
    
    return {"access_token": token, "token_type": "bearer"}