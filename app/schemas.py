from pydantic import BaseModel, EmailStr
from typing import Optional
from datetime import datetime

# ─── POST SCHEMAS ─────────────────────────────

class PostBase(BaseModel):
    title: str              # post title
    content: str            # post content
    published: bool = True  # default = True

class PostCreate(PostBase):
    pass  # used when creating a post (same fields as base)

class PostUpdate(PostBase):
    pass  # used when updating a post (same fields)

class PostResponse(PostBase):
    id: int                 # comes from DB
    created_at: datetime    # timestamp from DB
    owner_id: Optional[int] = None  # may be None

    class Config:
        from_attributes = True  # allows reading from ORM (DB model)

# ─── USER SCHEMAS ─────────────────────────────

class UserCreate(BaseModel):
    username: str
    email: EmailStr   # automatically checks valid email
    password: str

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True  # ORM → schema conversion


# app/schemas.py

# ... (boshqa klasslar)

class UserResponse(BaseModel):
    id: int
    username: str
    email: EmailStr
    created_at: datetime

    class Config:
        from_attributes = True

class PostResponse(PostBase): # Bu mavjud klass
    id: int
    created_at: datetime
    owner_id: Optional[int]

    class Config:
        from_attributes = True

# Yangi klass: Post egasi bilan birga
class PostWithOwner(PostResponse):
    owner: Optional[UserResponse] = None # models.py dagi 'owner' relationship nomi bilan bir xil bo'lishi shart


# Kategoriya uchun asosiy schema
class CategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

# Kategoriya yaratish uchun schema
class CategoryCreate(CategoryBase):
    pass

# Ma'lumotni qaytarish (Response) uchun schema
class CategoryResponse(CategoryBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True # Pydantic v2 uchun (v1 bo'lsa orm_mode = True)