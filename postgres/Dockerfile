FROM postgres:16.2

COPY data /data
COPY scripts /docker-entrypoint-initdb.d
RUN chmod a+r /docker-entrypoint-initdb.d/*
