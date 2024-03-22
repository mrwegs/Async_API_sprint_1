import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class PersonES(BaseModel):
    id: str = Field(alias='uuid')
    name: str

    model_config = ConfigDict(populate_by_name=True)


class MoviesDTO(BaseModel):
    id: str = Field(alias='uuid')
    rating: float | None = Field(alias='imdb_rating')
    title: str | None
    description: str | None
    genre: list[str]
    actors_names: list[str] | None
    writers_names: list[str] | None
    director: list[str] | None
    actors: list[PersonES] | None
    writers: list[PersonES] | None
    modified: datetime.datetime

    @field_validator('actors_names', 'writers_names', 'director', 'actors', 'writers')
    @classmethod
    def director_list(cls, v):
        return v if v else []

    model_config = ConfigDict(populate_by_name=True)


class FilmES(BaseModel):
    uuid: str
    title: str
    imdb_rating: float
    roles: list[str]


class PersonsDTO(BaseModel):
    person_id: str = Field(alias='uuid')
    full_name: str
    films: list[FilmES]
    modified: datetime.datetime

    model_config = ConfigDict(populate_by_name=True)


class GenresDTO(BaseModel):
    id: str = Field(alias='uuid')
    name: str
    modified: datetime.datetime

    model_config = ConfigDict(populate_by_name=True)
