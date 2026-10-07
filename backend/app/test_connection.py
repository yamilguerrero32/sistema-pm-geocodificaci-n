# -------------------------------------------- Aqui se está probando la conexión hacia la base de datos. -------------------------------------------------

from sqlalchemy import text

from app.database import engine

with engine.connect() as connection:
    result = connection.execute(text("SELECT 1"))
    print("Resultado:", result.scalar())