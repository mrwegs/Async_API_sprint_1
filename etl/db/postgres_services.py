import backoff
import psycopg2
from mixin import ConnMixin
from psycopg2.extras import DictCursor


class PostgresExtractor(ConnMixin):

    @backoff.on_exception(backoff.expo, psycopg2.OperationalError, max_tries=3)
    def _create_connection(self):
        self.connection_name = 'Postgres'
        db_name = self.config.DB_NAME
        db_user = self.config.DB_USER
        db_password = self.config.DB_PASSWORD
        db_host = self.config.DB_HOST
        db_port = self.config.DB_PORT
        postgres_url = f"postgresql://{db_user}:{db_password}@{db_host}:{db_port}/{db_name}"
        return psycopg2.connect(postgres_url, options='-c search_path=' + 'content', cursor_factory=DictCursor)

    @backoff.on_exception(backoff.expo, psycopg2.OperationalError, max_tries=3)
    def extract_data(self, query: str):
        with self.connection.cursor() as cur:
            cur.execute(query)
            while data := cur.fetchmany(self.config.CHUNK):
                yield data
