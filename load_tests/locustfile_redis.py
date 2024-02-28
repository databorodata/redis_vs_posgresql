from locust import HttpUser, between, events
from load_tests.tasks import UserBehavior, start_time, cpu_loads
from time import time
# from dotenv import load_dotenv
import os

# load_dotenv()

MIN_WAIT=int(os.environ.get("MIN_WAIT"))
MAX_WAIT=int(os.environ.get("MAX_WAIT"))


CPU_THRESHOLD=int(os.environ.get("CPU_THRESHOLD"))

class RedisUserBehavior(UserBehavior):
    db_type: str = "redis"


class LoadTestingRedis(HttpUser):
    host = "http://localhost:8000"
    tasks = [RedisUserBehavior]
    wait_time = between(MIN_WAIT, MAX_WAIT)


@events.quitting.add_listener
def get_redis_result(environment, **kw):
    print("тесты завершены")
    end_time = time()
    duration = end_time - start_time

    max_cpu_load = max(cpu_loads) if cpu_loads else 0
    avg_cpu_load = sum(cpu_loads) / len(cpu_loads) if cpu_loads else 0

    with open("load_tests/result_redis/time_and_cpu_redis.txt", "w") as file:
        file.write(f"Максимальная нагрузка CPU: {max_cpu_load}%\n")
        file.write(f"Средняя нагрузка CPU: {avg_cpu_load}%\n")
        file.write(f"Общее время теста: {duration} секунд\n")
