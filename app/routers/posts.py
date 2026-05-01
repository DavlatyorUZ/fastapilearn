from fastapi import APIRouter, status, HTTPException
from typing import List
from ..schemas import PostCreate, PostResponse


router = APIRouter(prefix="/posts", tags=["Posts"])
posts_db = [{"id": 1, "title": "Birinchi post", "content": "Salom dunyo"}]
post_id = 1

@router.get("/", response_model=List[PostResponse])
def get_posts():
    return posts_db

@router.post("/", status_code=status.HTTP_201_CREATED, response_model=PostResponse)
def create_post(post: PostCreate):
    global post_id
    post_dict = post.dict()
    post_dict["id"] = post_id
    post_id += 1
    posts_db.append(post_dict)
    return post_dict

@router.get("/{post_id}")
def get_post(post_id: int):
    """
    **Bitta postni ID orqali olish**

    Bu endpoint orqali bazadagi aniq bir post ma'lumotlarini qaytaramiz.

    - **post_id**: Qidirilayotgan postning unikal identifikatori (integer).
    
    *Agar post topilmasa, 404 xatolik qaytariladi.*
    """
    for post in posts_db:
        if post["id"] == post_id:
            return post
    
    # Post topilmasa xatolik qaytarish
    raise HTTPException(
        status_code=status.HTTP_404_NOT_FOUND, 
        detail=f"{post_id} ID ga ega post topilmadi"
    )

@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    for index, post in enumerate(posts_db):
        if post["id"] == post_id:
            posts_db.pop(index)
            return None
    raise HTTPException(status_code=404, detail="Post topilmadi")