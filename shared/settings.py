from pathlib import Path

from dotenv import load_dotenv
from envparse import env

load_dotenv(env("DOTENV_FILE", default=None))

BASE_DIR = Path(__file__).resolve().parent.parent


ENVIRONMENT = env("ENVIRONMENT", default="local")
TELEGRAM_TOKEN = env("TELEGRAM_TOKEN", default="")

# postgresql
PG_USERNAME = env("POSTGRES_USER", default="hobrus")
PG_PASSWORD = env("POSTGRES_PASSWORD", default="123321")
PG_HOST = env("DB_HOST", default="127.0.0.1")
PG_PORT = env.int("DB_PORT", default=5432)
PG_DB = env("POSTGRES_DB", default="LessonsStore_db")
PG_PROTOCOL = env("POSTGRES_PROTOCOL", default="postgresql+asyncpg")
PG_URI_QUERY = env("POSTGRES_URI_QUERY", default=str())
