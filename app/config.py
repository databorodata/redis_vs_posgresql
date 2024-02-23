from dotenv import load_dotenv
import os

load_dotenv()

REDIS_HOST = os.environ.get("REDIS_HOST")
REDIS_PORT = os.environ.get("REDIS_PORT")
REDIS_DB = os.environ.get("REDIS_DB")

DB_HOST=os.environ.get("POSTGRES_HOST")
DB_NAME=os.environ.get("POSTGRES_DB")
DB_PASS=os.environ.get("POSTGRES_PASSWORD")
DB_PORT=os.environ.get("POSTGRES_PORT")
DB_USER=os.environ.get("POSTGRES_USER")

