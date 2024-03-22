FROM python:3.11.3

WORKDIR /opt/async_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

ENTRYPOINT gunicorn -w 4 -k uvicorn.workers.UvicornWorker --bind unix:/tmp/fastapi.sock src.entrypoint:app