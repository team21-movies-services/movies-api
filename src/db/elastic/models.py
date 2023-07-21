from pydantic import UUID4, BaseModel, Field

from src.api.response_models import film_response, genre_response, person_response


class PersonDocumentFilmsPart(BaseModel):
    uuid: UUID4
    roles: list[str]

    def to_domain_model(self) -> person_response.RoleFilmResponse:
        return person_response.RoleFilmResponse(
            uuid=self.uuid,
            roles=[person_response.RoleEnum(role) for role in self.roles],
        )

    @staticmethod
    def to_domain_models(
        person_document_film_parts: list["PersonDocumentFilmsPart"],
    ) -> list[person_response.RoleFilmResponse]:
        return [person_part.to_domain_model() for person_part in person_document_film_parts]


class PersonDocument(BaseModel):
    uuid: UUID4
    full_name: str
    films: list[PersonDocumentFilmsPart] = Field(default_factory=list)

    def to_domain_model(self) -> person_response.PersonFilmResponse:
        return person_response.PersonFilmResponse(
            uuid=self.uuid,
            full_name=self.full_name,
            films=PersonDocumentFilmsPart.to_domain_models(self.films),
        )


class FilmDocumentPersonPart(BaseModel):
    uuid: UUID4
    full_name: str

    def to_domain_model(self) -> person_response.PersonResponse:
        return person_response.PersonResponse(uuid=self.uuid, full_name=self.full_name)

    @staticmethod
    def to_domain_models(person_parts: list["FilmDocumentPersonPart"]) -> list[person_response.PersonResponse]:
        return [person_part.to_domain_model() for person_part in person_parts]


class FilmDocumentGenrePart(BaseModel):
    uuid: UUID4
    name: str

    def to_domain_model(self) -> genre_response.GenreResponse:
        return genre_response.GenreResponse(uuid=self.uuid, name=self.name)

    @staticmethod
    def to_domain_models(genre_parts: list["FilmDocumentGenrePart"]) -> list[genre_response.GenreResponse]:
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

    def to_detail_model(self) -> film_response.FilmDetailResponse:
        return film_response.FilmDetailResponse(
            uuid=self.uuid,
            title=self.title,
            imdb_rating=self.imdb_rating,
            description=self.description,
            genre=FilmDocumentGenrePart.to_domain_models(self.genre),
            actors=FilmDocumentPersonPart.to_domain_models(self.actors),
            writers=FilmDocumentPersonPart.to_domain_models(self.writers),
            directors=FilmDocumentPersonPart.to_domain_models(self.directors),
        )

    def to_film_model(self) -> film_response.FilmResponse:
        return film_response.FilmResponse(
            uuid=self.uuid,
            title=self.title,
            imdb_rating=self.imdb_rating,
        )
