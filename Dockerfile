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
