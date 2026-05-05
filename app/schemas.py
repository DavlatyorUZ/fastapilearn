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

class PostWithOwner(PostResponse):
    owner: Optional[OwnerInfo] = None
    category: Optional[CategoryResponse] = None


# ─── TOKEN SCHEMAS ────────────────────────────
class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[str] = None