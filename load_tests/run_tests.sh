#!/bin/bash
sleep 20

# Запуск первого теста с Locust для Redis
locust -f /load_tests/locustfile_redis.py --html /load_tests/result_redis.html --headless --only-summary -u $NUM_USERS -r $HATCH_RATE --run-time $RUN_TIME --host=http://api:8000

sleep 10

# Запуск второго теста с Locust для SQL
locust -f /load_tests/locustfile_sql.py --html /load_tests/result_sql.html --headless --only-summary -u $NUM_USERS -r $HATCH_RATE --run-time $RUN_TIME --host=http://api:8000

sleep infinity