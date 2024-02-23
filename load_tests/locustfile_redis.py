from locust import HttpUser, between

from load_tests.tasks import UserBehavior


class RedisUserBehavior(UserBehavior):
    db_type: str = "redis"


class LoadTestingRedis(HttpUser):
    host = "http://localhost:8000"
    tasks = [RedisUserBehavior]
    wait_time = between(5, 30)
