from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.config import settings

class TokenHandler:

    def create_access_token(data: dict, expires_delta: timedelta = None):

        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + timedelta(minutes=30)
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


    def create_refresh_token(data: dict, expires_delta: timedelta = None): 

        to_encode = data.copy()
        expire = datetime.now(timezone.utc) + (expires_delta or timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS))
        to_encode.update({"exp": expire})
        return jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)


    def verify_token(token: str):
        
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
            return payload
        
        except JWTError:
            return None

    def tokenResponse(access_token, refresh_token):
    
        return {
            "access_token": access_token,
            "refresh_token": refresh_token,
            "token_type": "bearer"
        }