from fastapi import FastAPI
from .routers import posts,  categories # Kategoriyani chaqiring

app = FastAPI(
    title="Blog API",
    description="FastAPI bilan yaratilgan Blog API",
    version="1.0.0"
)

# Routers
app.include_router(posts.router)

@app.get("/")
def root():
    return {"xabar": "Blog API ga xush kelibsiz!"}


app.include_router(posts.router)
app.include_router(categories.router)