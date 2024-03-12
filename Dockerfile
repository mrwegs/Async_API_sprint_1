FROM python:3.11.3

WORKDIR /opt/async_api

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

COPY . .

RUN pip install --upgrade pip \
    && pip install -r requirements.txt --no-cache-dir

ENTRYPOINT [ "python", "-m", "src.entypoint" ]