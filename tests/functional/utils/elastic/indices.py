from enum import Enum

from tests.functional.utils.elastic.genres import genres_index_mapping
from tests.functional.utils.elastic.movies import movies_index_mapping
from tests.functional.utils.elastic.persons import persons_index_mapping


class EsIndices(Enum):
    GENRES = "genres", genres_index_mapping
    PERSONS = "persons", persons_index_mapping
    MOVIES = "movies", movies_index_mapping
