from jose import JWTError, jwt
from datetime import datetime, timedelta, timezone
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session

from . import models, schemas, database, config

# Sozlamalarni yuklash
settings = config.settings

# Token qayerdan olinishini ko'rsatish
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

# ─── ACCESS TOKEN YARATISH ───────────────────
def create_access_token(data: dict):
    to_encode = data.copy()
    
    # datetime.utcnow() eskirgan, yangi standart: datetime.now(timezone.utc)
    expire = datetime.now(timezone.utc) + timedelta(minutes=settings.access_token_expire_minutes)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    
    return encoded_jwt

# ─── REFRESH TOKEN YARATISH ──────────────────
def create_refresh_token(data: dict):
    to_encode = data.copy()
    
    # Refresh token odatda uzoqroq vaqt (masalan, 7 kun) amal qiladi
    expire = datetime.now(timezone.utc) + timedelta(days=7)
    
    to_encode.update({"exp": expire})
    
    encoded_jwt = jwt.encode(
        to_encode, 
        settings.secret_key, 
        algorithm=settings.algorithm
    )
    
    return encoded_jwt

# ─── TOKENNI VERIFIKATSIYA QILISH ────────────
def verify_access_token(token: str, credentials_exception):
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        
        # Login'da "user_id" deb berayotganimiz uchun bu yerda ham "user_id" olish kerak
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
        
        token_data = schemas.TokenData(id=str(user_id))
        
    except JWTError:
        raise credentials_exception

    return token_data

# ─── REFRESH TOKENNI TEKSHIRISH ───────────────
def verify_refresh_token(token: str):
    try:
        payload = jwt.decode(
            token, 
            settings.secret_key, 
            algorithms=[settings.algorithm]
        )
        
        # Sizning login kodingizda "user_id" ishlatilgan, shuning uchun "sub" emas "user_id"
        user_id: str = payload.get("user_id")
        
        if user_id is None:
            return None
            
        return user_id
    except JWTError:
        return None

# ─── JORIY FOYDALANUVCHINI OLISH ─────────────
def get_current_user(
    token: str = Depends(oauth2_scheme), 
    db: Session = Depends(database.get_db)
):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Token yaroqsiz yoki muddati o'tgan",
        headers={"WWW-Authenticate": "Bearer"},
    )

    token_data = verify_access_token(token, credentials_exception)

    # Bazadan user_id orqali foydalanuvchini qidirish
    user = db.query(models.User).filter(models.User.id == int(token_data.id)).first()

    if user is None:
        raise credentials_exception

    return user