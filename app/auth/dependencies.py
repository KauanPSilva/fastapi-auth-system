from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
from sqlalchemy.orm import Session
from app.database import get_db
from app.auth import jwt
from app import models


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/auth/login")

def get_current_user(token: str = Depends(oauth2_scheme), db: Session = Depends(get_db)) -> models.User:

    payload = jwt.verify_token(token)

    if not payload:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="token invalid or expired")
    
    user_id = payload.get("sub")
    user = db.query(models.User).filter(models.User.id == user_id).first()

    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user