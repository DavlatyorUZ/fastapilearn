from fastapi import APIRouter, status
from ..schemas import CategoryCreate, CategoryResponse

router = APIRouter(prefix="/categories", tags=["Categories"])

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=CategoryResponse)
def create_category(category: CategoryCreate):
    # Bu yerda ma'lumotlar bazasiga saqlash logikasi bo'ladi
    new_category = {"id": 1, **category.dict()} 
    return new_category