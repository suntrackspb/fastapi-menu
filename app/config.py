import os

from dotenv import load_dotenv

BASEDIR: str = os.path.abspath(os.path.dirname(os.path.dirname(__file__)))
load_dotenv(os.path.join(BASEDIR, '../.env'))

if os.getenv('MODE') == 'TEST':
    env_prefix = '_TEST'
else:
    env_prefix = ''

DB_NAME: str = os.getenv(f'DB_NAME{env_prefix}', default='postgres')
DB_USER: str = os.getenv(f'DB_USER{env_prefix}', default='postgres')
DB_PASS: str = os.getenv(f'DB_PASS{env_prefix}', default='postgres')
DB_HOST: str = os.getenv(f'DB_HOST{env_prefix}', default='localhost')
DB_PORT: int = int(os.getenv(f'DB_PORT{env_prefix}', default='5432'))

REDIS_URL = f"redis://{os.getenv('REDIS_HOST')}{os.getenv('REDIS_PORT')}"
