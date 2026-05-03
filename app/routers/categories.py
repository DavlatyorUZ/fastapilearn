from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from .. import models, schemas
from ..database import get_db

router = APIRouter(
    prefix="/categories",
    tags=["Categories"]
)

# ─── CREATE ───────────────────────────────────
@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.CategoryResponse)
def create_category(category: schemas.CategoryCreate, db: Session = Depends(get_db)):
    new_category = models.Category(**category.dict())
    db.add(new_category)
    db.commit()
    db.refresh(new_category)
    return new_category

# ─── READ ALL ─────────────────────────────────
@router.get("/", response_model=List[schemas.CategoryResponse])
def get_categories(db: Session = Depends(get_db)):
    return db.query(models.Category).all()

# ─── READ ONE ─────────────────────────────────
@router.get("/{id}", response_model=schemas.CategoryResponse)
def get_category(id: int, db: Session = Depends(get_db)):
    category = db.query(models.Category).filter(models.Category.id == id).first()
    if not category:
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi")
    return category

# ─── UPDATE ───────────────────────────────────
@router.put("/{id}", response_model=schemas.CategoryResponse)
def update_category(id: int, updated_cat: schemas.CategoryCreate, db: Session = Depends(get_db)):
    category_query = db.query(models.Category).filter(models.Category.id == id)
    if not category_query.first():
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi")
    category_query.update(updated_cat.dict(), synchronize_session=False)
    db.commit()
    return category_query.first()

# ─── DELETE ───────────────────────────────────
@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_category(id: int, db: Session = Depends(get_db)):
    category_query = db.query(models.Category).filter(models.Category.id == id)
    if not category_query.first():
        raise HTTPException(status_code=404, detail="Kategoriya topilmadi")
    category_query.delete(synchronize_session=False)
    db.commit()
    return None