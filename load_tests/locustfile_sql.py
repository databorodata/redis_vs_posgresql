from locust import HttpUser, between, events
from load_tests.tasks import UserBehavior, start_time, cpu_loads
from time import time


class SqlUserBehavior(UserBehavior):
    db_type: str = "sql"


class LoadTestingSql(HttpUser):
    host = "http://localhost:8000"
    tasks = [SqlUserBehavior]
    wait_time = between(5, 50)


@events.quitting.add_listener
def get_redis_result(environment, **kw):
    print("тесты завершены")
    end_time = time()  # Засекаем время окончания теста
    duration = end_time - start_time  # Общее время теста

    # Расчет максимальной и средней нагрузки на CPU
    max_cpu_load = max(cpu_loads) if cpu_loads else 0
    avg_cpu_load = sum(cpu_loads) / len(cpu_loads) if cpu_loads else 0

    # Запись результатов по нагрузке cpu и времени выполнения
    with open("load_tests/result_sql/time_and_cpu_sql.txt", "w") as file:
        file.write(f"Максимальная нагрузка CPU: {max_cpu_load}%\n")
        file.write(f"Средняя нагрузка CPU: {avg_cpu_load}%\n")
        file.write(f"Общее время теста: {duration} секунд\n")