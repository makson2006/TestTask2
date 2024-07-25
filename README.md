# TestTask2 Project


Цей проект реалізує простий REST API для управління IoT-пристроями, створений за допомогою aiohttp та Peewee ORM з використанням PostgreSQL як бази даних. Проект також контейнеризований з використанням Docker.

## Налаштування проекту

### Попередні вимоги

- Docker
- Docker Compose

### Інструкції по встановленню

1. Клонуйте репозиторій до вашої локальної машини:

   ```bash
   git clone git@github.com:makson2006/TestTask2.git
   cd TestTask2

   
2.Створіть файл Dockerfile з наступним вмістом:

# Використовуємо базовий образ Python
FROM python:3.10-slim

# Встановлюємо робочу директорію
WORKDIR /app

# Копіюємо файли проекту до контейнера
COPY . .

# Встановлюємо залежності
RUN pip install --no-cache-dir -r requirements.txt

# Вказуємо команду для запуску додатка
CMD ["python", "main.py"]

Створіть файл docker-compose.yml з наступним вмістом:

version: '3.8'

services:
  db:
    image: postgres:13
    environment:
      POSTGRES_DB: testdb2
      POSTGRES_USER: postgres
      POSTGRES_PASSWORD: postgres
    volumes:
      - postgres_data:/var/lib/postgresql/data

  web:
    build: .
    ports:
      - "8080:8080"
    environment:
      DATABASE_URL: postgres://postgres:postgres@db:5432/testdb2
    depends_on:
      - db

volumes:
  postgres_data:


Запустіть контейнери:

docker-compose up --build


Створення пристрою

POST /device
Content-Type: application/json

{
  "name": "Device1",
  "type": "Sensor",
  "login": "device_login",
  "password": "device_password",
  "location": 1,
  "api_user": 1
}


Отримання пристрою
GET /device/{id}


Оновлення пристрою
PUT /device/{id}
Content-Type: application/json

{
  "name": "UpdatedDeviceName"
}

Видалення пристрою

DELETE /device/{id}
