import random

from tests.functional.testdata.common import film_list, genre_list, person_list

films_length = len(film_list)
not_existing_film_uuid = "5dbb7428-2df4-4abc-b4f4-0cb65b4135e8"


def get_film(idx=0) -> dict:
    """Возвращается фильм из списка films с рандомным жанром и персонами."""

    genre = random.choice(genre_list)
    random.shuffle(person_list)

    return {
        "uuid": film_list[idx]["uuid"],
        "title": film_list[idx]["title"],
        "imdb_rating": film_list[idx]["imdb_rating"],
        "description": "test_description",
        "genre": [
            {
                "uuid": genre["uuid"],
                "name": genre["name"],
            }
        ],
        "actors": [
            {
                "uuid": person_list[0]["uuid"],
                "full_name": person_list[0]["full_name"],
            },
            {
                "uuid": person_list[1]["uuid"],
                "full_name": person_list[1]["full_name"],
            },
            {
                "uuid": person_list[2]["uuid"],
                "full_name": person_list[2]["full_name"],
            },
        ],
        "writers": [
            {
                "uuid": person_list[3]["uuid"],
                "full_name": person_list[3]["full_name"],
            },
            {
                "uuid": person_list[4]["uuid"],
                "full_name": person_list[4]["full_name"],
            },
        ],
        "directors": [
            {
                "uuid": person_list[5]["uuid"],
                "full_name": person_list[5]["full_name"],
            },
        ],
    }


def get_film_list():
    return [get_film(idx) for idx in range(films_length)]
