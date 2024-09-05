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

# redis
REDIS_HOST = env("REDIS_HOST", default="redis")
REDIS_DB = env("REDIS_DB", default="0")
REDIS_PORT = env.int("REDIS_PORT", default=6379)
REDIS_PROTOCOL = env("REDIS_PROTOCOL", default="redis")

# minio S3
S3_ENDPOINT = env("S3_ENDPOINT")
S3_BUCKET = env("S3_BUCKET", default="bucket-media")
S3_ACCESS_KEY = env("S3_ACCESS_KEY")
S3_SECRET_KEY = env("S3_SECRET_KEY")
S3_SECURE = env.bool("S3_SECURE", default=False)

# yookassa
YOO_KASSA_TOKEN = env("YOO_KASSA_TOKEN")

# extra
SUPPORT_ACCOUNT = env("SUPPORT_ACCOUNT")

# admins telegram id
ADMINS_TG_ID = [int(admin_id) for admin_id in env.list("ADMINS_TG_ID", default=[])]
