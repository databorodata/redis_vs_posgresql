from locust import HttpUser, between

from load_tests.tasks import UserBehavior


class SqlUserBehavior(UserBehavior):
    db_type: str = "sql"


class LoadTestingSql(HttpUser):
    host = "http://localhost:8000"
    # host = "http://0.0.0.0:8000/"
    tasks = [SqlUserBehavior]
    wait_time = between(5, 30)
