from time import sleep
import psutil
from locust import SequentialTaskSet, task
import uuid
from locust.exception import StopUser
from requests import RequestException
from time import time
# from dotenv import load_dotenv
import os

# load_dotenv()

CPU_THRESHOLD=int(os.environ.get("CPU_THRESHOLD"))

cpu_loads = []
start_time = time()
print("Тесты стартовали")


class UserBehavior(SequentialTaskSet):
    db_type: str

    def __init__(self, parent):
        super().__init__(parent)
        self.environment = parent.environment  # Сохраняем ссылку на environment

    def on_start(self):
        self.user_data = self.generate_user_data()
        self.task_counter = 0

    def check_cpu_load(self):
        global cpu_loads, start_time
        cpu_load = psutil.cpu_percent(interval=1)
        cpu_loads.append(cpu_load)
        if cpu_load > CPU_THRESHOLD:
            print(f"Высокая загрузка ЦП: {cpu_load}%. Остановка тестов.")
            time_now = time()
            print(f"тесты продлились {time_now - start_time}")
            self.environment.runner.quit()

    def generate_user_data(self):
        unique_id = str(uuid.uuid4())
        return {
            "name": f"user_{unique_id}",
            "email": f"user_{unique_id}@example.com",
            "password": f"password_{unique_id}",
            "is_active": True,
            "is_superuser": False,
            "is_verified": False
        }

    @task
    def register(self):
        self.check_cpu_load()
        if self.task_counter == 0:
            try:
                response = self.client.post(f"/auth/{self.db_type}/register", json=self.user_data)
                if response.status_code == 201:
                    self.task_counter += 1
            except RequestException as e:
                print(f"Ошибка при регистрации: {e}")
                sleep(3)
                self.register()

    @task
    def login(self):
        self.check_cpu_load()
        if self.task_counter == 1:
            try:
                data = {
                    "username": self.user_data['email'],
                    "password": self.user_data['password']
                }
                response = self.client.post(f"/auth/{self.db_type}/login", data=data)
                if response.status_code == 200:
                    self.task_counter += 1
                    response_data = response.json()
                    if 'access_token' in response_data:
                        self.token = response_data['access_token']
            except RequestException as e:
                print(f"Ошибка при входе: {e}")
                sleep(3)
                self.login()

    @task
    def logout(self):
        self.check_cpu_load()
        if self.task_counter == 2:
            try:
                headers = {"Authorization": f"Bearer {self.token}"}
                response = self.client.post(f"/auth/{self.db_type}/logout", headers=headers)
                if response.status_code in [200, 204]:
                    self.task_counter += 1
            except RequestException as e:
                print(f"Ошибка при выходе: {e}")
                sleep(3)
                self.logout()

    def on_stop(self):
        if self.task_counter >= 2:
            raise StopUser()
        else:
            super().on_stop()
