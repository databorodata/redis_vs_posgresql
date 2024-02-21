# from locust import HttpUser, SequentialTaskSet, task, between, events
# from locust.env import Environment
# from locust.stats import stats_printer, stats_history
# import uuid
# from time import sleep
# import gevent
#
# # Настройка логирования
# from locust.log import setup_logging
# setup_logging("INFO", None)
#
# class UserBehavior(SequentialTaskSet):
#     def on_start(self):
#         self.user_data = self.generate_user_data()
#         self.task_counter = 0
#
#     def generate_user_data(self):
#         unique_id = str(uuid.uuid4())
#         return {
#             "name": f"user_{unique_id}",
#             "email": f"user_{unique_id}@example.com",
#             "password": f"password_{unique_id}",
#             "is_active": True,
#             "is_superuser": False,
#             "is_verified": False
#         }
#
#     @task
#     def register(self):
#         if self.task_counter == 0:
#             response = self.client.post(f"/auth/{self.user.db_type}/register", json=self.user_data)
#             assert response.status_code == 201
#             self.task_counter += 1
#
#     @task
#     def login(self):
#         if self.task_counter == 1:
#             data = {
#                 "username": self.user_data['email'],
#                 "password": self.user_data['password']
#             }
#             response = self.client.post(f"/auth/{self.user.db_type}/login", data=data)
#             assert response.status_code == 200
#             self.task_counter += 1
#             response_data = response.json()
#             self.token = response_data['access_token']
#
#     @task
#     def logout(self):
#         if self.task_counter == 2:
#             headers = {"Authorization": f"Bearer {self.token}"}
#             response = self.client.post(f"/auth/{self.user.db_type}/logout", headers=headers)
#             assert response.status_code in [200, 204]
#             self.task_counter += 1
#
#     def on_stop(self):
#         super().on_stop()
#
# class LoadTesting(HttpUser):
#     wait_time = between(5, 10)
#     host = "http://localhost:8000"
#     db_type = 'sql'  # Значение по умолчанию
#
#     def __init__(self, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         self.db_type = kwargs.get('db_type', self.db_type)
#
#     tasks = [UserBehavior]
#
#
#
# def run_test_for_db_type(db_type, user_count, spawn_rate, run_time, csv_prefix):
#     # Настройка и создание среды Locust
#     env = Environment(user_classes=[LoadTesting], host="http://localhost:8000")
#
#     # Установка типа базы данных для каждого экземпляра класса пользователя
#     for user_class in env.user_classes:
#         user_class.db_type = db_type
#
#     # Создание локального исполнителя
#     runner = env.create_local_runner()
#
#     # Запуск теста с записью статистики в CSV
#     runner.start(user_count=user_count, spawn_rate=spawn_rate)
#     env.events.request_success.add_listener(lambda name, response_time, response_length, **kw: print(name, response_time, response_length))
#     env.events.request_failure.add_listener(lambda name, response_time, exception, **kw: print(name, response_time, exception))
#
#     # Ожидание завершения исполнителя
#     gevent.spawn_later(run_time, lambda: runner.quit())
#     runner.greenlet.join()
#
#     # Сохранение статистики в CSV-файлы
#     stats_csv_writer = env.stats_csv_writer
#     stats_csv_writer.stats_history_enabled = True
#     stats_csv_writer.stats_history_file_prefix = csv_prefix
#     stats_csv_writer.stats_history_interval = 1  # Запись каждую секунду
#     stats_csv_writer.stats_history(env.runner)
#
#     # Остановка веб-интерфейса, если он был запущен
#     if env.web_ui:
#         env.web_ui.stop()
#
# # Параметры теста
# user_count = 10
# spawn_rate = 2
# run_time = 60  # в секундах
#
# # Запуск тестов для Redis
# run_test_for_db_type('redis', user_count, spawn_rate, run_time)
# sleep(3)  # Пауза между тестами
#
# # Запуск тестов для SQL
# run_test_for_db_type('sql', user_count, spawn_rate, run_time)
#


from locust import HttpUser, SequentialTaskSet, between, task
import uuid
from time import sleep

from locust.env import Environment
from locust.exception import StopUser
from requests import RequestException

current_db_type = 'sql'


class UserBehavior(SequentialTaskSet):
    db_type: str

    # def __init__(self, parent):
    #     super().__init__(parent)
    #     # self.db_type = parent.db_type

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
                response = self.client.post(
                    f"/auth/{self.db_type}/register",
                    json=self.user_data
                )
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
                response = self.client.post(
                    f"/auth/{self.db_type}/login",
                    data=data
                )
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
                response = self.client.post(
                    f"/auth/{self.db_type}/logout",
                    headers=headers
                )
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


class SqlUserBehavior(UserBehavior):
    db_type: str = "sql"


class RedisUserBehavior(UserBehavior):
    db_type: str = "redis"


class LoadTesting(HttpUser):
    tasks = [UserBehavior]
    wait_time = between(5, 30)

# class LoadTesting(HttpUser):
#     wait_time = between(5, 30)
    #
    # def __init__(self, *args, **kwargs):
    #     super().__init__(*args, **kwargs)
    #     self.db_type = current_db_type

    # tasks = [SqlUserBehavior]


def run_tests(db_types_list):
    global current_db_type
    for db_type in db_types_list:
        current_db_type = db_type
        env = Environment(host="http://localhost:8000")
        user = LoadTesting(environment=env)
        user.run()
        sleep(3)


db_types = ['sql', 'redis']
run_tests(db_types)
