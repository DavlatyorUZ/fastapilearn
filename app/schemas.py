from pydantic import BaseModel, EmailStr
from typing import Optional, List
from datetime import datetime


# ─── USER SCHEMAS ─────────────────────────────
class UserBase(BaseModel):
    username: str
    email: EmailStr

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True


# ─── OWNER INFO (Post uchun qisqa ma'lumot) ───
class OwnerInfo(BaseModel):
    id: int
    username: str
    email: EmailStr

    class Config:
        from_attributes = True


# ─── CATEGORY SCHEMAS ─────────────────────────
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class CategoryCreate(CategoryBase):
    pass

class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True


# ─── POST SCHEMAS ─────────────────────────────
class PostBase(BaseModel):
    title: str
    content: str
    published: bool = True
    category_id: Optional[int] = None

class PostCreate(PostBase):
    pass

class PostUpdate(BaseModel):
    title: Optional[str] = None
    content: Optional[str] = None
    published: Optional[bool] = None
    category_id: Optional[int] = None

class PostResponse(PostBase):
    id: int
    created_at: datetime
    owner_id: Optional[int] = None
    owner: Optional[OwnerInfo] = None
    category: Optional[CategoryResponse] = None

    class Config:
        from_attributes = True


# ─── AUTH & TOKEN SCHEMAS ─────────────────────

class Token(BaseModel):
    """Login va Refresh muvaffaqiyatli bo'lganda qaytariladigan format"""
    access_token: str
    refresh_token: str
    token_type: str

class TokenData(BaseModel):
    """Token dekod qilinganda ichidan olinadigan ma'lumot"""
    id: Optional[str] = None

class RefreshTokenRequest(BaseModel):
    """/refresh endpointiga yuboriladigan JSON so'rov formati"""
    refresh_token: str

class PasswordChange(BaseModel):
    """Parolni o'zgartirish so'rovi uchun format"""
    old_password: str
    new_password: str