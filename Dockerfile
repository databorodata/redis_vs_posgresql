# Используйте официальный образ Python 3.9
FROM python:3.9-slim

# Установите рабочий каталог в контейнере
WORKDIR /app

# Копируйте файлы проекта в контейнер
COPY . /app

# Установите зависимости
RUN pip install --no-cache-dir -r requirements.txt

# Запустите приложение
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
