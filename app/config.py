import os
from dotenv import load_dotenv

BASEDIR: str = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(BASEDIR, "../.env"))

if os.getenv("MODE") == "TEST":
    DB_NAME: str = os.getenv("DB_NAME_TEST", default="postgres")
    DB_USER: str = os.getenv("DB_USER_TEST", default="postgres")
    DB_PASS: str = os.getenv("DB_PASS_TEST", default="postgres")
    DB_HOST: str = os.getenv("DB_HOST_TEST", default="localhost")
    DB_PORT: int = int(os.getenv("DB_PORT_TEST", default="6543"))
else:
    DB_NAME: str = os.getenv("DB_NAME", default="postgres")
    DB_USER: str = os.getenv("DB_USER", default="postgres")
    DB_PASS: str = os.getenv("DB_PASS", default="postgres")
    DB_HOST: str = os.getenv("DB_HOST", default="localhost")
    DB_PORT: int = int(os.getenv("DB_PORT", default="5432"))
