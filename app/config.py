import os
from dotenv import load_dotenv

BASEDIR: str = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(BASEDIR, "../.env"))


DB_NAME: str = os.getenv("DB_NAME", default="postgres")
DB_USER: str = os.getenv("DB_USER", default="postgres")
DB_PASS: str = os.getenv("DB_PASS", default="postgres")
DB_HOST: str = os.getenv("DB_HOST", default="localhost")
DB_PORT: str = os.getenv("DB_PORT", default="5432")
