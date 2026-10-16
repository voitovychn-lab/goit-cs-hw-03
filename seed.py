import os
from dotenv import load_dotenv

load_dotenv()


# Імпортую бібліотеки для роботи з PostgreSQL і генерації даних
import psycopg2
from faker import Faker
import random

# Створюю об'єкт Faker для генерації тестових даних
fake = Faker()

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

# Додаю три статуси завдань
statuses = ["new", "in progress", "completed"]

for status in statuses:
    cursor.execute(
        "INSERT INTO status (name) VALUES (%s) ON CONFLICT (name) DO NOTHING;",
        (status,)
    )

# Отримую ідентифікатори статусів
cursor.execute("SELECT id FROM status;")
status_ids = [row[0] for row in cursor.fetchall()]

# Генерую та додаю 10 користувачів
for _ in range(10):
    cursor.execute(
        "INSERT INTO users (fullname, email) VALUES (%s, %s) ON CONFLICT (email) DO NOTHING;",
        (fake.name(), fake.unique.email())
    )

# Отримую ідентифікатори користувачів
cursor.execute("SELECT id FROM users;")
user_ids = [row[0] for row in cursor.fetchall()]

# Генерую та додаю 20 завдань для випадкових користувачів
for _ in range(20):
    cursor.execute(
        """
        INSERT INTO tasks (title, description, status_id, user_id)
        VALUES (%s, %s, %s, %s);
        """,
        (
            fake.sentence(nb_words=4),
            fake.text(max_nb_chars=200),
            random.choice(status_ids),
            random.choice(user_ids)
        )
    )

# Зберігаю всі зміни в базі даних
conn.commit()

# Закриваю курсор
cursor.close()

# Закриваю з'єднання з базою даних
conn.close()