import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict, field_validator


class PersonES(BaseModel):
    id: str = Field(alias='uuid')
    name: str

    model_config = ConfigDict(populate_by_name=True)

class MoviesDTO(BaseModel):
    id: str = Field(alias='uuid')
    rating: Optional[float] = Field(alias='imdb_rating')
    title: Optional[str]
    description: Optional[str]
    genre: list[str]
    actors_names: Optional[list[str]]
    writers_names: Optional[list[str]]
    director: Optional[list[str]]
    actors: Optional[list[PersonES]]
    writers: Optional[list[PersonES]]
    modified: datetime.datetime

    @field_validator('actors_names', 'writers_names', 'director', 'actors', 'writers')
    @classmethod
    def director_list(cls, v):
        return v if v else []

    model_config = ConfigDict(populate_by_name=True)


class FilmES(BaseModel):
    uuid: str
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
