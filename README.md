# Тестируем под нагрузкой работу с базами данных Postgresql и Redis

Учёбно-исследовательский проект. Сравниваем результаты работы стека Fastapi + Postgresql и Fastapi + Postgresql под нагрузочными тестами.

Тесты проводятся при помощи Locust. Тестируемый сценарий поведения пользователя: регистрация (register) - аутентификация (login) - выход (logout).

Маршруты регистрации и аутентификации реализованы с помощью библиотеки Fastapi Users.

## Настройка и оптимизация используемых баз данных

### Redis

Работа Redis дополнительно оптимизирована использованием библиотеки Orjson, для ускорения сериализации данных.

### Postgresql

Работа Posgresql оптимизированна увеличинием кол-ва пула открытых сессий (POOL_SIZE, MAX_OVERFLOW). Данный параметр можно редактировать в файле app/config здесь:

https://github.com/databorodata/redis_vs_posgresql/blob/compare_load/.env.load_tests#L18

## Настройка тестов

В файле .env.load_tests по ссылке:

https://github.com/databorodata/redis_vs_posgresql/blob/compare_load/.env.load_tests#L13

можно регулировать следующие параметры тестирования:

NUM_USERS=100 - Кол-во одновременно тестируемых пользователей

HATCH_RATE=3 - Кол-во пользователей добавляемых тестов за одну секунду

RUN_TIME=10m - Ограничение времени прохождения теста

MIN_WAIT=5 - Минимальное время задержки между выполнением действия пользователем

MAX_WAIT=50 - Максимальное время задержки между выполнением действия пользователем

CPU_THRESHOLD=90 - Ограничение нагрузки на CPU при прохождение теста. Если показатель будет превышен, тест завершится до своего штатного окончания

## Результаты тестов

При запуске проекта через докер, после завершения тестирования результаты записываются в директории result_redis и result_sql соответственно.
Их можно найти по ссылкам:

https://github.com/databorodata/redis_vs_posgresql/tree/compare_load/load_tests/result_redis

https://github.com/databorodata/redis_vs_posgresql/tree/compare_load/load_tests/result_sql

В файлах с расширением .csv будут записаны результаты в табличной форме для последующего анализа

Файлы с растением .html можно открыть в вашем браузере, в них содержится статистика, предоставляемая Locust, в том числе графики.

В файлах с расширением .txt содержится статистика по нагрузке CPU и времени выполнения теста.

## Начало работы

### Предварительные условия

Что нужно установить на ваш компьютер для использования проекта:
Python 3.10, PostgreSQL

### Установка

Пошаговый процесс установки и запуска проекта:

1. Клонируйте репозиторий:

   ```bash
   https://github.com/databorodata/redis_vs_posgresql.git

2. Перейдите в директорию проекта:

   ```bash
   cd /project/path

3. Создайте и активируйте виртуальное окружение:

   ```bash
   python3 -m venv venv

   source venv/bin/activate

4. Установите зависимости из файла requirements.txt:

   ```bash
   pip install -r requirements.txt
   
5. В файле env.load_tests внесите необходимые корректировки переменных отвечающих за настройку БД и тестов, если это необходимо.

## Развёртывание в Docker

### Запуск приложения в Docker

1. Перейдите в директорию проекта:

   ```bash
   cd /project/path

2. Чтобы запустить приложение, используйте следующую команду в вашем терминале

   ```bash
   docker-compose up -d
