from .database import engine


def check_database_connection() -> bool:
    try:
        connection = engine.connect()
        connection.close()
        return True
    except Exception:
        return False


if __name__ == "__main__":
    if check_database_connection():
        print("✅ PostgreSQL ga muvaffaqiyatli ulandi!")
    else:
        print("❌ Bazaga ulanishda xato yuz berdi.")