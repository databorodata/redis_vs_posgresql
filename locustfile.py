from locust import HttpUser, task, between
import uuid


class LookAroundUser(HttpUser):
    wait_time = between(1, 3)

    def on_start(self):
        self.registered = False
        self.logged_in = False
        self.register()

    def register(self):
        unique_id = str(uuid.uuid4())
        self.username = f"user_{unique_id}"
        self.email = f"{self.username}@example.com"
        self.password = f"password_{unique_id}"

        user_data = {
            "name": self.username,
            "email": self.email,
            "password": self.password,
            "is_active": True,
            "is_superuser": False,
            "is_verified": False
        }

        response = self.client.post("/auth/register", json=user_data)
        if response.status_code == 201:
            self.registered = True
            self.login()

    def login(self):
        if self.registered:
            headers = {"Content-Type": "application/x-www-form-urlencoded"}
            data = f"username={self.email}&password={self.password}"
            response = self.client.post("/auth/redis_strategy/login", data=data, headers=headers)
            if response.status_code == 200:
                response_data = response.json()
                if 'access_token' in response_data:
                    self.token = response_data['access_token']
                    self.logged_in = True

    @task
    def logout(self):
        if self.logged_in:
            headers = {"Authorization": f"Bearer {self.token}"}
            response = self.client.post("/auth/redis_strategy/logout", headers=headers)
            if response.status_code in [200, 204]:
                self.logged_in = False
