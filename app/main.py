from fastapi import FastAPI
from .routers import posts, users, auth

# ← models.Base.metadata.create_all(bind=engine)  O'CHIRILDI!

app = FastAPI(
    title="Blog API",
    description="FastAPI + PostgreSQL + JWT + Alembic",
    version="4.0.0"
)

app.include_router(posts.router)
app.include_router(users.router)
app.include_router(auth.router)

@app.get("/")
def root():
    return {"xabar": "Blog API v4.0 — Alembic bilan!"}