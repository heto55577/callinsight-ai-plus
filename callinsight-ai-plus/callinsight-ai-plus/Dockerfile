# Dockerfile
FROM python:3.9-slim

WORKDIR /app

# Копируем requirements
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Копируем все файлы
COPY . .

# Создаем папки
RUN mkdir -p uploads templates static

# Открываем порт
EXPOSE 5000

# Команда запуска
CMD ["python", "app.py"]