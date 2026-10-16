# Імпортую бібліотеки для роботи з PostgreSQL
import os
import psycopg2
from dotenv import load_dotenv

# Завантажую налаштування з файлу .env
load_dotenv()

# Підключаюся до бази даних
conn = psycopg2.connect(
    dbname="goit_cs_hw_03",
    user="postgres",
    password=os.getenv("POSTGRES_PASSWORD"),
    host="localhost",
    port="5432"
)

# Створюю курсор для виконання SQL-запитів
cursor = conn.cursor()

# Створюю таблицю користувачів
cursor.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        fullname VARCHAR(100),
        email VARCHAR(100) UNIQUE
    );
""")

# Створюю таблицю статусів
cursor.execute("""
    CREATE TABLE IF NOT EXISTS status (
        id SERIAL PRIMARY KEY,
        name VARCHAR(50) UNIQUE
    );
""")

# Створюю таблицю завдань зі зв'язками між таблицями
cursor.execute("""
    CREATE TABLE IF NOT EXISTS tasks (
        id SERIAL PRIMARY KEY,
        title VARCHAR(100),
        description TEXT,
        status_id INTEGER REFERENCES status(id),
        user_id INTEGER REFERENCES users(id) ON DELETE CASCADE
    );
""")

# Зберігаю зміни в базі даних
conn.commit()

# Закриваю курсор
cursor.close()

# Закриваю з'єднання з базою даних
conn.close()