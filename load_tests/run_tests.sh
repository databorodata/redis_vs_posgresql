#!/bin/bash

# Запуск первого теста с Locust для Redis
#locust /load_tests locustio/locust -f /load_tests/locustfile_redis.py  --html /load_tests/result_redis.html --headless --only-summary  -u $NUM_USERS -r $HATCH_RATE --run-time $RUN_TIME --host=http://app:8000
#locust -f /load_tests/locustfile_redis.py --html /load_tests/result_redis.html --headless --only-summary -u $NUM_USERS -r $HATCH_RATE --run-time $RUN_TIME --host=http://app:8000
#locust /load_tests locustio/locust -f /load_tests/locustfile_redis.py  --html /load_tests/result_redis.html --headless --only-summary  -u $NUM_USERS -r $HATCH_RATE --run-time $RUN_TIME --host=http://localhost:8000
locust -f /load_tests/locustfile_redis.py --html /load_tests/result_redis.html --headless --only-summary -u $NUM_USERS -r $HATCH_RATE --run-time $RUN_TIME --host=http://localhost:8000

sleep 10

# Запуск второго теста с Locust для SQL
#locust /load_tests locustio/locust -f /load_tests/locustfile_sql.py  --html /load_tests/result_sql.html --headless --only-summary  -u $NUM_USERS -r $HATCH_RATE --run-time $RUN_TIME --host=http://localhost:8000
#locust /load_tests locustio/locust -f /load_tests/locustfile_sql.py  --html /load_tests/result_sql.html --headless --only-summary  -u $NUM_USERS -r $HATCH_RATE --run-time $RUN_TIME --host=http://app:8000
locust -f /load_tests/locustfile_sql.py --html /load_tests/result_sql.html --headless --only-summary -u $NUM_USERS -r $HATCH_RATE --run-time $RUN_TIME --host=http://localhost:8000
#locust -f /load_tests/locustfile_sql.py --html /load_tests/result_sql.html --headless --only-summary -u $NUM_USERS -r $HATCH_RATE --run-time $RUN_TIME --host=http://app:8000
