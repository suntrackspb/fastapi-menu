## Homework in course from YLab

![](https://img.shields.io/badge/python-3.10-blue?style=flat-square)
![](https://img.shields.io/badge/fastapi-0.100.0-red?style=flat-square)
![](https://img.shields.io/badge/SQLAlchemy-1.4.39-red?style=flat-square)
![](https://img.shields.io/badge/asyncpg-0.28.0-red?style=flat-square)
[![pre-commit](https://img.shields.io/badge/pre--commit-enabled-brightgreen?logo=pre-commit)](https://github.com/pre-commit/pre-commit)


Tested:
* on **Manjaro Linux**: conda package manager, python 3.10.12
* on **WSL2 Ubuntu**: pip package manager, Python 3.10.6
* on **Windows 11**: pip package manager, Python 3.11.3

## Run on Docker:
```commandline
git clone https://github.com/suntrackspb/fastapi-menu.git
```
```shell
cd fastapi-menu
```
```shell
docker-compose up
```


## Run on local:
```commandline
git clone https://github.com/suntrackspb/fastapi-menu.git
```

```shell
# Create PostgreSQL database instance
docker run -itd \
	--name fastapi-menu-db \
	-e POSTGRES_PASSWORD=postgres \
	-p 5432:5432 \
	-v /data:/var/lib/postgresql/data \
	postgres
```
or use your PostgreSQL Server, but you need change auth data in .env file
```shell
cd fastapi-menu
```
Edit .env file, set: `DB_HOST=localhost`
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
```
Open http://localhost:8000/docs/