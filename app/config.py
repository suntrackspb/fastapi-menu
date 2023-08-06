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

POSTGRES_URL: str = f'postgresql+asyncpg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}'


REDIS_HOST: str = os.getenv('REDIS_HOST', default='localhost')
REDIS_PORT: int = int(os.getenv('REDIS_PORT', default='6379'))

REDIS_URL = f'redis://{REDIS_HOST}:{REDIS_PORT}'
