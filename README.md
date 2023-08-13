## Homework in course from YLab

![](https://img.shields.io/badge/python-3.10-blue?style=flat-square)
![](https://img.shields.io/badge/fastapi-0.100.0-red?style=flat-square)
![](https://img.shields.io/badge/SQLAlchemy-1.4.39-red?style=flat-square)
![](https://img.shields.io/badge/asyncpg-0.28.0-red?style=flat-square)
![](https://img.shields.io/badge/aioredis-2.0.1-red?style=flat-square)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)

## Installation:
```commandline
git clone https://github.com/suntrackspb/fastapi-menu.git
```
```shell
cd fastapi-menu
```


## Run on Docker:
```shell
#Start
docker-compose up -d
```
Open http://localhost:8000/docs/
```shell
#Stop & delete
docker-compose down --rmi all --remove-orphans
```

## Run Tests on Docker:
```shell
docker-compose -f docker-compose-test.yaml up -d

docker start -a fastapi_test_app
```
```shell
#Stop & delete
docker-compose down --rmi all --remove-orphans
```

## Run on local:

Tested:
* on **Manjaro Linux**: conda package manager, python 3.10.12
* on **WSL2 Ubuntu**: pip package manager, Python 3.10.6
* on **Windows 11**: pip package manager, Python 3.11.3

```shell
# Create PostgreSQL database instance
docker run -itd \
	--name fastapi-menu-db \
	-e POSTGRES_PASSWORD=postgres \
	-p 5432:5432 \
	-v /dist:/var/lib/postgresql/dist \
	postgres
```
or use your PostgreSQL Server, but you need change auth data in .env file

and edit hosts, set:
```text
DB_HOST=localhost
REDIS_HOST=localhost
```
```shell
#Linux:
python3 -m venv venv

#Windows PowerShell:
python -m venv venv
```
```shell
#Linux:
source venv/bin/activate

#Windows PowerShell:
.\venv\Scripts\Activate.ps1
```
```shell
#Linux:
pip install -r requirements.txt

#Windows PowerShell:
.\venv\Scripts\python.exe -m pip install -r requirements.txt
```
```shell
#Linux:
python3 run.py

#Windows PowerShell:
python run.py

#Run Tests
pytest
```
Open http://localhost:8000/docs/
