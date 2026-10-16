
import os
from dotenv import load_dotenv
from pymongo import MongoClient
from pymongo.errors import PyMongoError

# Завантажую дані з файлу .env
load_dotenv()

# Підключаюся до MongoDB
client = MongoClient(os.getenv("MONGO_URI"))
db = client.cats_db
collection = db.cats


# Виводжу всіх котів
def show_all_cats():
    cats = collection.find()
    found = False

    for cat in cats:
        print(cat)
        found = True

    if not found:
        print("Котів не знайдено")


# Шукаю кота за ім'ям
def find_cat():
    name = input("Введіть ім'я кота: ")
    cat = collection.find_one({"name": name})

    if cat:
        print(cat)
    else:
        print("Кота не знайдено")


# Додаю нового кота
def add_cat():
    name = input("Введіть ім'я кота: ")
    age = int(input("Введіть вік кота: "))
    features = input("Введіть характеристики через кому: ").split(",")

    cat = {
        "name": name,
        "age": age,
        "features": [feature.strip() for feature in features]
    }

    collection.insert_one(cat)
    print("Кота додано")


# Оновлюю вік кота
def update_cat_age():
    name = input("Введіть ім'я кота: ")
    age = int(input("Введіть новий вік: "))

    result = collection.update_one(
        {"name": name},
        {"$set": {"age": age}}
    )

    if result.matched_count:
        print("Вік кота оновлено")
    else:
        print("Кота не знайдено")


# Додаю характеристику коту
def add_cat_feature():
    name = input("Введіть ім'я кота: ")
    feature = input("Введіть нову характеристику: ")

    result = collection.update_one(
        {"name": name},
        {"$addToSet": {"features": feature}}
    )

    if result.matched_count:
        print("Характеристику додано")
    else:
        print("Кота не знайдено")


# Видаляю кота за ім'ям
def delete_cat():
    name = input("Введіть ім'я кота: ")

    result = collection.delete_one({"name": name})

    if result.deleted_count:
        print("Кота видалено")
    else:
        print("Кота не знайдено")


# Видаляю всіх котів
def delete_all_cats():
    confirm = input("Видалити всіх котів? (так/ні): ")

    if confirm.lower() == "так":
        result = collection.delete_many({})
        print(f"Видалено котів: {result.deleted_count}")
    else:
        print("Видалення скасовано")


# Створюю меню програми
def main():
    while True:
        print("\nМеню MongoDB:")
        print("1. Показати всіх котів")
        print("2. Знайти кота за ім'ям")
        print("3. Додати кота")
        print("4. Оновити вік кота")
        print("5. Додати характеристику коту")
        print("6. Видалити кота")
        print("7. Видалити всіх котів")
        print("0. Вийти")

        choice = input("Виберіть дію: ")

        try:
            if choice == "1":
                show_all_cats()
            elif choice == "2":
                find_cat()
            elif choice == "3":
                add_cat()
            elif choice == "4":
                update_cat_age()
            elif choice == "5":
                add_cat_feature()
            elif choice == "6":
                delete_cat()
            elif choice == "7":
                delete_all_cats()
            elif choice == "0":
                print("Завершення роботи")
                break
            else:
                print("Невірний вибір")

        except ValueError:
            print("Помилка: введіть правильне число")

        except PyMongoError as e:
            print("Помилка MongoDB:", e)


# Запускаю програму
if __name__ == "__main__":
    try:
        client.admin.command("ping")
        main()
    except PyMongoError as e:
        print("Помилка підключення до MongoDB:", e)
    finally:
        client.close()
