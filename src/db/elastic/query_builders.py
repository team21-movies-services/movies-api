from enum import StrEnum
from typing import Any, Type

from src.models.search import BaseSearchParams, FilmsSearchParams, PersonSearchParams


class SortOrder(StrEnum):
    ASCENDING = "asc"
    DESCENDING = "desc"


class CommonSortField(StrEnum):
    UUID = "uuid"
    SCORE = "_score"


class SearchQueryBuilder:
    def __init__(self, search_params: BaseSearchParams, search_field: str):
        self._search_params = search_params
        self._search_field = search_field

    def build(self) -> dict[str, Any]:
        body: dict[str, Any] = {"size": self._search_params.page_size}

        sort = self._build_sort()
        if sort is not None:
            body["sort"] = sort
        else:
            body["sort"] = {
                CommonSortField.SCORE: SortOrder.DESCENDING,
                CommonSortField.UUID: SortOrder.ASCENDING,
            }

        if self._search_params.page_number:
            page = max(0, self._search_params.page_number - 1)
            body["from"] = self._search_params.page_size * page
        elif self._search_params.search_after:
            body["search_after"] = self._build_search_after()

        query = self._build_query()
        if query is not None:
            body["query"] = query

        return body

    def _build_sort(self) -> dict[StrEnum, SortOrder] | None:
        sort_param = self._search_params.sort
        if sort_param is None:
            return None

        sort_fields_enum = self.get_sort_fields()
        if sort_fields_enum is None:
            return None

        has_leading_dash = sort_param.startswith("-")
        sort_field = sort_param[1:] if has_leading_dash else sort_param

        if not self._has_sort_field(sort_fields_enum, sort_field):
            return None

        sort_order = SortOrder.DESCENDING if has_leading_dash else SortOrder.ASCENDING

        return {
            sort_fields_enum(sort_field): sort_order,
            CommonSortField.UUID: SortOrder.ASCENDING,
        }

    def _build_search_after(self) -> list[Any] | None:
        search_after = self._search_params.search_after
        if search_after is None:
            return None

        return search_after.split(",")

    def _build_query(self) -> dict[str, Any] | None:
        query_parts = self._get_query_parts()
        if len(query_parts) == 0:
            return None

        return {
            "bool": {
                "must": query_parts,
            },
        }

    def _get_query_parts(self) -> list[dict[str, Any]]:
        search_query = self._search_params.query
        if search_query is None:
            return []

        return [
            {
                "match": {
                    self._search_field: {
                        "query": search_query,
                        "fuzziness": "auto",
                    },
                },
            },
        ]

    def get_sort_fields(self) -> Type[StrEnum] | None:
        return None

    @staticmethod
    def _has_sort_field(sort_field: Type[StrEnum], value: str) -> bool:
        return value in [sort_field_value for sort_field_value in sort_field]


class FilmSortField(StrEnum):
    IMDB_RATING = "imdb_rating"


class PersonSortField(StrEnum):
    FULL_NAME = "full_name"


class FilmSearchQueryBuilder(SearchQueryBuilder):
    def __init__(self, search_params: FilmsSearchParams, search_field: str = "title"):
        super().__init__(search_params, search_field)

        self._genre = search_params.genre
        self._person = search_params.person

    def _get_query_parts(self) -> list[dict[str, Any]]:
        query_parts = super()._get_query_parts()

        if self._genre is not None:
            query_parts.append(
                {
                    "nested": {
                        "path": "genre",
                        "query": {
                            "match": {"genre.uuid": str(self._genre)},
                        },
                    },
                },
            )

        if self._person is not None:
            query_parts.append(
                {
                    "bool": {
                        "should": [
                            {
                                "nested": {
                                    "path": "actors",
                                    "query": {"bool": {"must": [{"match": {"actors.uuid": self._person}}]}},
                                },
                            },
                            {
                                "nested": {
                                    "path": "directors",
                                    "query": {"bool": {"must": [{"match": {"directors.uuid": self._person}}]}},
                                },
                            },
                            {
                                "nested": {
                                    "path": "writers",
                                    "query": {"bool": {"must": [{"match": {"writers.uuid": self._person}}]}},
                                },
                            },
                        ],
                    },
                },
            )

        return query_parts

    def get_sort_fields(self) -> Type[StrEnum]:
        return FilmSortField


class PersonSearchQueryBuilder(SearchQueryBuilder):
    def __init__(self, search_params: PersonSearchParams, search_field: str = "full_name"):
        super().__init__(search_params, search_field)

    def get_sort_fields(self) -> Type[StrEnum]:
        return PersonSortField
