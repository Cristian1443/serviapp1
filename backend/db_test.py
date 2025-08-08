import psycopg2
import os
from dotenv import load_dotenv

load_dotenv()

def test_db_connection():
    try:
        conn = psycopg2.connect(
            host=os.getenv("DB_HOST"),
            port=os.getenv("DB_PORT"),
            dbname=os.getenv("DB_NAME"),
            user=os.getenv("DB_USER"),
            password=os.getenv("DB_PASSWORD")
        )
        cur = conn.cursor()
        cur.execute("SELECT 1;")
        result = cur.fetchone()
        cur.close()
        conn.close()
        print(f"✅ Conexión a la base de datos exitosa: {result}")
    except Exception as e:
        print("❌ Error conectando a la base de datos:", str(e))
