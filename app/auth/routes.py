from fastapi import APIRouter, Depends, HTTPException, status
from app.auth.dependencies import get_current_user
from sqlalchemy.orm import Session
from app import models, schemas
from app.database import get_db
from app.auth.utils.exception import ExceptionHandler
from app.auth.utils.password import PasswordHandler
from app.auth.utils.token import TokenHandler


router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=schemas.UserOut)
def register(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = db.query(models.User).filter(models.User.email == user.email).first()
    
    if db_user:
        raise ExceptionHandler.bad_request("User already registered")
    
    hashed_password = PasswordHandler.get_password_hash(user.password)
    new_user = models.User(email=user.email, hashed_password=hashed_password)
    
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user


@router.post("/login", response_model=schemas.TokenResponse)
def login(login_data: schemas.LoginRequest, db: Session = Depends(get_db)):

    user = db.query(models.User).filter(models.User.email == login_data.email).first()

    if not user or not PasswordHandler.verify_password(login_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid Credencials")
    
    access_token = TokenHandler.create_access_token(data={"sub": str(user.id)})
    refresh_token = TokenHandler.create_refresh_token(data={"sub": str(user.id)})

    return TokenHandler.tokenResponse(access_token, refresh_token)


@router.post("/refesh-token", response_model=schemas.TokenResponse)
def refresh_token(refresh: schemas.RefreshRequest):
    
    payload = TokenHandler.verify_token(refresh.refresh_token)

    if not payload:
        raise HTTPException(status_code=401, detail="Refresh token invalid or expired")

    user_id = payload.get("sub")
    new_access_token = TokenHandler.create_access_token(data={"sub": user_id})
    new_refresh_token = TokenHandler.create_refresh_token(data={"sub": user_id})  

    return TokenHandler.tokenResponse(new_access_token, new_refresh_token)


@router.get("/me", response_model=schemas.UserOut)
def current_user(current_user: models.User = Depends(get_current_user)):
    
    return current_user