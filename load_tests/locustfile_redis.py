from locust import HttpUser, between, events
from load_tests.tasks import UserBehavior
from locust.runners import MasterRunner, LocalRunner, WorkerRunner

class RedisUserBehavior(UserBehavior):
    db_type: str = "redis"


class LoadTestingRedis(HttpUser):
    host = "http://localhost:8000"
    tasks = [RedisUserBehavior]
    wait_time = between(5, 50)


def stop_test_on_cpu_warning(environment, **kwargs):
    """
    Останавливает тест, если срабатывает предупреждение о высокой нагрузке на CPU.
    """
    print("Высокая нагрузка на CPU, останавливаем тесты.")
    environment.runner.quit()


@events.init.add_listener
def on_locust_init(environment, **kwargs):
    """
    Добавляет обработчик события cpu_warning.
    """
    if isinstance(environment.runner, (MasterRunner, LocalRunner, WorkerRunner)):
        events.cpu_warning.add_listener(stop_test_on_cpu_warning)
