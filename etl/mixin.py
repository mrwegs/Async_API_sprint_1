import logging

from pydantic_settings import BaseSettings


class ConnMixin:
    def __init__(self, config: BaseSettings):
        self.config = config
        self.connection = None
        self.logger = logging.getLogger("connections")

    def __enter__(self):
        self.connection = self._create_connection()
        self.logger.info(f"Подключение к {self.connection_name} успешно.")
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.connection:
            self.connection.close()
            self.logger.info(f"Отключение от {self.connection_name} успешно.")
        else:
            self.logger.warning(f"Нет активного подключения к {self.connection_name} для отключения.")
