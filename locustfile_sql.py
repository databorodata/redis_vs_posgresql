from locust import HttpUser, SequentialTaskSet, between, task
import uuid
from locust.exception import StopUser
from requests import RequestException
from time import sleep


class UserBehavior(SequentialTaskSet):
    def on_start(self):
        self.user_data = self.generate_user_data()
        self.task_counter = 0

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
        if self.task_counter == 0:
            try:
                response = self.client.post("/auth/sql/register", json=self.user_data)
                if response.status_code == 201:
                    self.task_counter += 1
            except RequestException as e:
                print(f"Ошибка при регистрации: {e}")
                sleep(3)
                self.register()

    @task
    def login(self):
        if self.task_counter == 1:
            try:
                data = {
                    "username": self.user_data['email'],
                    "password": self.user_data['password']
                }
                response = self.client.post("/auth/sql/login", data=data)
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
        if self.task_counter == 2:
            try:
                headers = {"Authorization": f"Bearer {self.token}"}
                response = self.client.post("/auth/sql/logout", headers=headers)
                if response.status_code in [200, 204]:
                    self.task_counter += 1
            except RequestException as e:
                print(f"Ошибка при выходе: {e}")
                sleep(3)
                self.logout()

    def on_stop(self):
        super().on_stop()
        if self.task_counter >= 2:
            raise StopUser()


class LookAroundUser(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5, 30)