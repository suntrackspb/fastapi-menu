import os

from dotenv import load_dotenv

if os.getenv("MODE") == "TEST":
    load_dotenv(".env.test")
elif os.getenv("MODE") == "PROD":
    load_dotenv(".env")
else:
    load_dotenv(".env.local")

BASE_URL: str = str(os.getenv("BASE_URL"))
USE_GOOGLE: str = str(os.getenv("USE_GOOGLE_SHEET"))
GOOGLE_REDIRECT_PORT: str = str(os.getenv("GOOGLE_REDIRECT_PORT", default="55423"))

DB_NAME: str = os.getenv("DB_NAME", default="postgres")
DB_USER: str = os.getenv("DB_USER", default="postgres")
DB_PASS: str = os.getenv("DB_PASS", default="postgres")
DB_HOST: str = os.getenv("DB_HOST", default="localhost")
DB_PORT: int = int(os.getenv("DB_PORT", default="5432"))

POSTGRES_URL: str = f"postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"


REDIS_HOST: str = os.getenv("REDIS_HOST", default="localhost")
REDIS_PORT: int = int(os.getenv("REDIS_PORT", default="6379"))
REDIS_EXPIRE: int = int(os.getenv("REDIS_CACHE_TIME", default="3600"))

REDIS_URL: str = f"redis://{REDIS_HOST}:{REDIS_PORT}"


RABBITMQ_USER: str = os.getenv("RABBITMQ_USER", default="rabbit")
RABBITMQ_PASS: str = os.getenv("RABBITMQ_PASS", default="rabbit")
RABBITMQ_HOST: str = os.getenv("RABBITMQ_HOST", default="localhost")
RABBITMQ_PORT: int = int(os.getenv("RABBITMQ_PORT", default="5672"))
RABBITMQ_URL: str = f"amqp://{RABBITMQ_USER}:{RABBITMQ_PASS}@{RABBITMQ_HOST}:{RABBITMQ_PORT}//"
