FROM python:3.8

# Установка Locust
RUN pip install locust

# Копирование Locust файла в контейнер
COPY locustfile.py /locustfile.py

# Команда для запуска Locust
CMD ["locust", "-f", "/locustfile.py", "--headless", "-u", "100", "-r", "10", "--run-time", "1m"]

