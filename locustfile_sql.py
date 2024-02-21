from locust import HttpUser, between

from tasks import UserBehavior


class SqlUserBehavior(UserBehavior):
    db_type: str = "sql"


class LoadTestingSql(HttpUser):
    host = "http://localhost:8000"
    tasks = [SqlUserBehavior]
    wait_time = between(5, 30)
