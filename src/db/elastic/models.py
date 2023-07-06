from pydantic import UUID4, BaseModel, Field

from src.models.film import FilmDetail, FilmPerson
from src.models.genre import Genre
from src.models.person import Person, RoleEnum, RoleFilm


class PersonDocumentFilmsPart(BaseModel):
    uuid: UUID4
    roles: list[str]

    def to_domain_model(self) -> RoleFilm:
        return RoleFilm(uuid=self.uuid, roles=[RoleEnum(role) for role in self.roles])

    @staticmethod
    def to_domain_models(person_document_film_parts: list["PersonDocumentFilmsPart"]) -> list[RoleFilm]:
        return [person_part.to_domain_model() for person_part in person_document_film_parts]


class PersonDocument(BaseModel):
    uuid: UUID4
    full_name: str
    films: list[PersonDocumentFilmsPart] = Field(default_factory=list)

    def to_domain_model(self) -> Person:
        return Person(
            uuid=self.uuid,
            full_name=self.full_name,
            films=PersonDocumentFilmsPart.to_domain_models(self.films),
        )


class FilmDocumentPersonPart(BaseModel):
    uuid: UUID4
    full_name: str

    def to_domain_model(self) -> FilmPerson:
        return FilmPerson(uuid=self.uuid, full_name=self.full_name)

    @staticmethod
    def to_domain_models(person_parts: list["FilmDocumentPersonPart"]) -> list[FilmPerson]:
        return [person_part.to_domain_model() for person_part in person_parts]


class FilmDocumentGenrePart(BaseModel):
    uuid: UUID4
    name: str

    def to_domain_model(self) -> Genre:
        return Genre(uuid=self.uuid, name=self.name)

    @staticmethod
    def to_domain_models(genre_parts: list["FilmDocumentGenrePart"]) -> list[Genre]:
        return [genre_part.to_domain_model() for genre_part in genre_parts]


class FilmDocument(BaseModel):
    uuid: UUID4
    imdb_rating: float
    title: str
    description: str | None = ""
    genre: list[FilmDocumentGenrePart] = Field(default_factory=list)
    actors_names: list[str] = Field(default_factory=list)
    actors: list[FilmDocumentPersonPart] = Field(default_factory=list)
    directors: list[FilmDocumentPersonPart] = Field(default_factory=list)
    writers: list[FilmDocumentPersonPart] = Field(default_factory=list)
    writers_names: list[str] = Field(default_factory=list)

    def to_domain_model(self) -> FilmDetail:
        return FilmDetail(
            uuid=self.uuid,
            title=self.title,
            imdb_rating=self.imdb_rating,
            description=self.description,
            genre=FilmDocumentGenrePart.to_domain_models(self.genre),
            actors=FilmDocumentPersonPart.to_domain_models(self.actors),
            writers=FilmDocumentPersonPart.to_domain_models(self.writers),
            directors=FilmDocumentPersonPart.to_domain_models(self.directors),
        )
