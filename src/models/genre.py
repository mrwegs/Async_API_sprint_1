from src.models.dumps import BaseOrjsonModel


class Genre(BaseOrjsonModel):
    """Класс для описания жанра"""

    uuid: str
    name: str
