from locust import HttpUser, SequentialTaskSet, between, task
import uuid
from time import sleep

from locust.exception import StopUser


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
        # print(self.user_data['name'], self.task_counter, 'register start')
        if self.task_counter == 0:
            response = self.client.post("/auth/register", json=self.user_data)
            # print(self.user_data['name'], 'register done', 'status_code:', response.status_code)
            if response.status_code == 201:
                self.task_counter += 1

    @task
    def login(self):
        # print(self.user_data['name'], self.task_counter, 'login start')
        if self.task_counter == 1:
            data = {
                "username": self.user_data['email'],
                "password": self.user_data['password']
            }
            response = self.client.post("/auth/redis_strategy/login", data=data)
            # print(self.user_data['name'], 'login done', 'status_code:', response.status_code)
            if response.status_code == 200:
                self.task_counter += 1
                response_data = response.json()
                if 'access_token' in response_data:
                    self.token = response_data['access_token']
                    # print(self.user_data['name'], 'token:', self.token)

    @task
    def logout(self):
        # print(self.user_data['name'], self.task_counter, 'logout start')
        if self.task_counter == 2:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.client.post("/auth/redis_strategy/logout", headers=headers)
            # print(self.user_data['name'], 'logout done', 'status_code:', response.status_code)
            self.task_counter += 1
            # print(self.user_data['name'], 'user---------------done')

    def on_stop(self):
        super().on_stop()
        if self.task_counter >= 2:
            raise StopUser()


class LookAroundUser(HttpUser):
    # host = "http://localhost:8089"
    tasks = [UserBehavior]
    wait_time = between(5, 30)

# locust -f locustfile.py --host=http://localhost:8089
