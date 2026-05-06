from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    # .env ni chetga surib, qiymatlarni to'g'ridan-to'g'ri yozamiz
    database_url: str = "postgresql://postgres:1@localhost:5432/blog_db"
    secret_key: str = "46f636820ba083e6ea38445bda54e00b98f4f0177945f535463eb2dd31399a33"
    debug: bool = False
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 30
    

settings = Settings()