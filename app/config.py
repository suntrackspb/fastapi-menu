import os
from dotenv import load_dotenv

BASEDIR: str = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(BASEDIR, "../.env"))


DB_NAME: str = os.getenv("DB_NAME", default="postgres")
DB_USER: str = os.getenv("DB_USER", default="postgres")
DB_PASS: str = os.getenv("DB_PASS", default="postgres")
DB_HOST: str = os.getenv("DB_HOST", default="localhost")
DB_PORT: str = os.getenv("DB_PORT", default="5432")

DB_NAME_TEST: str = os.getenv("DB_NAME_TEST", default="postgres")
DB_USER_TEST: str = os.getenv("DB_USER_TEST", default="postgres")
DB_PASS_TEST: str = os.getenv("DB_PASS_TEST", default="postgres")
DB_HOST_TEST: str = os.getenv("DB_HOST_TEST", default="localhost")
DB_PORT_TEST: str = os.getenv("DB_PORT_TEST", default="5432")
