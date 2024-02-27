from locust import HttpUser, between, events
from locust.runners import MasterRunner, LocalRunner, WorkerRunner
from load_tests.tasks import UserBehavior


class SqlUserBehavior(UserBehavior):
    db_type: str = "sql"


class LoadTestingSql(HttpUser):
    host = "http://localhost:8000"
    tasks = [SqlUserBehavior]
    wait_time = between(5, 15)


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