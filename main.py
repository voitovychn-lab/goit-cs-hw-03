
import os
from pymongo import MongoClient
from dotenv import load_dotenv

# Завантажую налаштування з файлу .env
load_dotenv()

# Підключаюся до MongoDB
client = MongoClient(os.getenv("MONGO_URI"))

# Вибираю базу даних і колекцію котів
db = client["cats_db"]
collection = db["cats"]


# Виводжу всіх котів із колекції
def show_all_cats():
    cats = list(collection.find())

    if not cats:
        print("Котів не знайдено")
        return

    for cat in cats:
        print(cat)


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


# Додаю нову характеристику коту
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


# Видаляю всіх котів із колекції
def delete_all_cats():
    confirm = input("Видалити всіх котів? (так/ні): ")

    if confirm.lower() == "так":
        result = collection.delete_many({})
        print("Видалено котів:", result.deleted_count)
    else:
        print("Видалення скасовано")


# Створюю меню для вибору операцій
def main():
    try:
        client.admin.command("ping")
        print("Успішно підключено до MongoDB!")

        while True:
            print("\n--- МЕНЮ ---")
            print("1. Показати всіх котів")
            print("2. Знайти кота за ім'ям")
            print("3. Додати кота")
            print("4. Змінити вік кота")
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
                    print("Завершую роботу")
                    break
                else:
                    print("Невідома команда")
            except ValueError:
                print("Помилка: введіть правильне число")

    except Exception as e:
        print("Помилка:", e)

    finally:
        # Закриваю підключення до MongoDB
        client.close()


if __name__ == "__main__":
    main()
