import math

from elasticsearch import AsyncElasticsearch, NotFoundError
from fastapi import Depends
from pydantic import UUID4

from src.db.abstract import AbstractFilmRepository, AbstractGenreRepository, AbstractPersonRepository, SearchAfterType
from src.models.film import FilmDetail
from src.models.genre import Genre
from src.models.person import Person
from src.models.search import FilmsSearchParams, PersonSearchParams

from .adapter import get_elastic
from .models import FilmDocument, FilmDocumentGenrePart, PersonDocument
from .query_builders import FilmSearchQueryBuilder, PersonSearchQueryBuilder


class ElasticsearchFilmRepository(AbstractFilmRepository):
    _INDEX = "movies"

    def __init__(self, elastic: AsyncElasticsearch):
        self._elastic = elastic

    async def get_by_id(self, film_id: UUID4) -> FilmDetail | None:
        try:
            response = await self._elastic.get(self._INDEX, str(film_id))
        except NotFoundError:
            return None

        return FilmDocument(**response["_source"]).to_domain_model()

    async def query(self, search_query_params: FilmsSearchParams) -> list[FilmDetail]:
        resp = await self._elastic.search(
            index=self._INDEX,
            body=FilmSearchQueryBuilder(search_query_params).build(),
        )

        film_documents = [FilmDocument(**response_hit["_source"]) for response_hit in resp["hits"]["hits"]]

        return [film_document.to_domain_model() for film_document in film_documents]

    async def query_with_pagination(
        self,
        search_query_params: FilmsSearchParams,
    ) -> tuple[int, SearchAfterType, list[FilmDetail]]:
        resp = await self._elastic.search(
            index=self._INDEX,
            body=FilmSearchQueryBuilder(search_query_params).build(),
        )

        film_documents = [FilmDocument(**response_hit["_source"]) for response_hit in resp["hits"]["hits"]]
        domain_films = [film_document.to_domain_model() for film_document in film_documents]
        pages = math.ceil(resp["hits"]["total"]["value"] / search_query_params.page_size)
        search_after = None
        if resp["hits"].get("hits"):
            search_after = resp["hits"]["hits"][-1].get("sort")

        return pages, search_after, domain_films


class ElasticsearchPersonRepository(AbstractPersonRepository):
    _INDEX = "persons"

    def __init__(self, elastic: AsyncElasticsearch):
        self._elastic = elastic

    async def get_by_id(self, person_id: UUID4) -> Person | None:
        try:
            response = await self._elastic.get(self._INDEX, str(person_id))
        except NotFoundError:
            return None

        return PersonDocument(**response["_source"]).to_domain_model()

    async def query_with_pagination(
        self,
        search_query_params: PersonSearchParams,
    ) -> tuple[int, SearchAfterType, list[Person]]:
        resp = await self._elastic.search(
            index=self._INDEX,
            body=PersonSearchQueryBuilder(search_query_params).build(),
        )

        domain_persons = [
            PersonDocument(**response_hit["_source"]).to_domain_model() for response_hit in resp["hits"]["hits"]
        ]
        pages = math.ceil(resp["hits"]["total"]["value"] / search_query_params.page_size)
        search_after = None
        if resp["hits"].get("hits"):
            search_after = resp["hits"]["hits"][-1].get("sort")

        return pages, search_after, domain_persons


class ElasticsearchGenreRepository(AbstractGenreRepository):
    _INDEX = "genres"

    def __init__(self, elastic: AsyncElasticsearch):
        self._elastic = elastic

    async def get_by_id(self, genre_id: UUID4) -> Genre | None:
        try:
            response = await self._elastic.get(self._INDEX, str(genre_id))
        except NotFoundError:
            return None

        return FilmDocumentGenrePart(**response["_source"]).to_domain_model()

    async def query(self) -> list[Genre]:
        resp = await self._elastic.search(index=self._INDEX)

        genre_documents = [
            FilmDocumentGenrePart(**response_hit["_source"]).to_domain_model() for response_hit in resp["hits"]["hits"]
        ]

        return genre_documents


def get_film_repository(
    elastic: AsyncElasticsearch = Depends(get_elastic),
):
    return ElasticsearchFilmRepository(elastic)


def get_person_repository(
    elastic: AsyncElasticsearch = Depends(get_elastic),
):
    return ElasticsearchPersonRepository(elastic)


def get_genre_repository(
    elastic: AsyncElasticsearch = Depends(get_elastic),
):
    return ElasticsearchGenreRepository(elastic)
