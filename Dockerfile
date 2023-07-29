FROM python:3.10-slim
WORKDIR /app
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1
COPY ./pip-requirements.txt .
RUN pip install --upgrade pip && pip install -r pip-requirements.txt --no-cache-dir
COPY . .
