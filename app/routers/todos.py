from fastapi import APIRouter, HTTPException, status
from typing import List
from ..schemas import Todo, TodoCreate # Schemas faylidan chaqiramiz

router = APIRouter(prefix="/todos", tags=["To-Do"])

todos_db = []
id_counter = 1

@router.get("/", response_model=List[dict])
def get_todos():
    """Barcha vazifalar ro'yxatini olish"""
    return todos_db

@router.post("/", status_code=status.HTTP_201_CREATED)
def create_todo(todo: Todo):
    """Yangi vazifa qo'shish"""
    global id_counter
    new_todo = todo.dict()
    new_todo["id"] = id_counter
    todos_db.append(new_todo)
    id_counter += 1
    return new_todo

@router.put("/{todo_id}")
def update_todo(todo_id: int, updated_todo: Todo):
    """Mavjud vazifani tahrirlash"""
    for index, todo in enumerate(todos_db):
        if todo["id"] == todo_id:
            todos_db[index].update(updated_todo.dict())
            return todos_db[index]
    raise HTTPException(status_code=404, detail="Vazifa topilmadi")

@router.delete("/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int):
    """Vazifani o'chirish"""
    for index, todo in enumerate(todos_db):
        if todo["id"] == todo_id:
            todos_db.pop(index)
            return
    raise HTTPException(status_code=404, detail="Vazifa topilmadi")