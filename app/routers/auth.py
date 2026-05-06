from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.orm import Session
# Oauth2 modulini to'g'ri chaqirish (loyihangiz strukturasi bo'yicha)
from .. import models, schemas, oauth2, database
from ..utils.hashing import verify_password

router = APIRouter(tags=["Authentication"])

# ─── LOGIN ENDPOINT ───────────────────────────
@router.post("/login", response_model=schemas.Token)
def login(
    user_credentials: OAuth2PasswordRequestForm = Depends(), 
    db: Session = Depends(database.get_db)
):
    # 1. Foydalanuvchini email orqali qidirish (OAuth2 username maydonidan email keladi)
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()

    # 2. Foydalanuvchi mavjudligi va parolni tekshirish
    if not user or not verify_password(user_credentials.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Email yoki parol noto'g'ri"
        )

    # 3. Tokenlarni yaratish (oauth2.py faylida ushbu funksiyalar bo'lishi shart)
    access_token = oauth2.create_access_token(data={"user_id": user.id})
    refresh_token = oauth2.create_refresh_token(data={"user_id": user.id})

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer"
    }

# ─── REFRESH TOKEN ENDPOINT ───────────────────
@router.post("/refresh", response_model=schemas.Token)
def refresh_access_token(
    request: schemas.RefreshTokenRequest, 
    db: Session = Depends(database.get_db)
):
    # 1. Refresh tokenni tekshirish va ichidan user_id ni olish
    user_id = oauth2.verify_refresh_token(request.refresh_token)
    
    if not user_id:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Refresh token yaroqsiz yoki muddati o'tgan"
        )
    
    # 2. Foydalanuvchi hali ham bazada borligini tekshirish (id ni int ga o'tkazamiz)
    user = db.query(models.User).filter(models.User.id == int(user_id)).first()
    
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, 
            detail="Foydalanuvchi topilmadi"
        )

    # 3. Yangi juftlikni yaratish (Refresh Token Rotation)
    new_access_token = oauth2.create_access_token(data={"user_id": user.id})
    new_refresh_token = oauth2.create_refresh_token(data={"user_id": user.id})

    return {
        "access_token": new_access_token,
        "refresh_token": new_refresh_token,
        "token_type": "bearer"
    }

# ─── LOGOUT ENDPOINT ──────────────────────────
@router.post("/logout")
def logout():
    # Stateless JWT ishlatilganda logout frontendda tokenni o'chirish orqali bajariladi
    return {"message": "Muvaffaqiyatli chiqildi. Tokenlarni brauzer xotirasidan o'chiring."}