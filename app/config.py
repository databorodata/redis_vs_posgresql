from dotenv import load_dotenv
import os

load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_DB = os.environ.get("REDIS_DB")

DB_HOST=os.environ.get("DB_HOST")
DB_NAME=os.environ.get("DB_NAME")
DB_PASS=os.environ.get("DB_PASS")
DB_PORT=os.environ.get("DB_PORT")
DB_USER=os.environ.get("DB_USER")

