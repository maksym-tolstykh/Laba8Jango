import psycopg2
from psycopg2 import OperationalError, Error
from dotenv import load_dotenv
from faker import Faker
import os
import random

# Завантаження змінних з файлу .env
load_dotenv()

# Отримання змінних з оточення
db_host = os.getenv('DB_HOST')
db_name = os.getenv('DB_NAME')
db_user = os.getenv('DB_USER')
db_password = os.getenv('DB_PASSWORD')

# Ініціалізація Faker для генерації фейкових даних
fake = Faker(locale="uk_UA")

# Список матеріалів
materials_data = [
    ("Деревина", 100),
    ("Лак", 45),
    ("Сталеві деталі", 250)
]

try:
    # Підключення до бази даних PostgreSQL
    conn = psycopg2.connect(
        host=db_host,
        database=db_name,
        user=db_user,
        password=db_password
    )
    print("З'єднання з базою даних відкрите.")
    cursor = conn.cursor()

    # Вставка даних для постачальників (4 постачальника)
    suppliers_data = []
    for _ in range(4):
        company_name = fake.company()
        contact_person = fake.name()
        phone = fake.phone_number()  # Генерація номера телефону
        bank_account = fake.bban()[:20]  # Генерація випадкового банківського рахунку
        suppliers_data.append((company_name, contact_person, phone, bank_account))

    cursor.executemany('''
        INSERT INTO inventory_supplier (company_name, contact_person, phone, bank_account)
        VALUES (%s, %s, %s, %s);
    ''', suppliers_data)
    print("Постачальники успішно додані.")

    # Вставка даних для матеріалів
    cursor.executemany('''
        INSERT INTO inventory_material (material_name, price)
        VALUES (%s, %s);
    ''', materials_data)
    print("Матеріали успішно додані.")

    # Отримання ID постачальників та матеріалів
    cursor.execute('SELECT id FROM inventory_supplier;')
    supplier_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute('SELECT id FROM inventory_material;')
    material_ids = [row[0] for row in cursor.fetchall()]

    # Вставка даних для поставок (22 поставки)
    deliveries_data = []
    for _ in range(22):
        delivery_date = fake.date_this_year()
        supplier_id = random.choice(supplier_ids)
        material_id = random.choice(material_ids)
        delivery_days = random.randint(1, 7)
        quantity = random.randint(1, 1000)  # Генерація випадкової кількості матеріалів
        deliveries_data.append((delivery_date, supplier_id, material_id, delivery_days, quantity))

    cursor.executemany('''
        INSERT INTO inventory_delivery (delivery_date, supplier_id, material_id, delivery_days, quantity)
        VALUES (%s, %s, %s, %s, %s);
    ''', deliveries_data)
    print("Поставки успішно додані.")

    # Застосування змін
    conn.commit()

except OperationalError as e:
    print(f"Помилка при підключенні до бази даних: {e}")
except Error as e:
    print(f"Помилка при виконанні SQL-запиту: {e}")
    conn.rollback()  # Відкочування змін у разі помилки
finally:
    if conn:
        cursor.close()
        conn.close()
        print("З'єднання з базою даних закрите.")
