import random

from tests.functional.testdata.common import film_list, person_list

person_roles = ["actor", "writer", "director"]


def get_person(idx: int):
    """Возвращает личность из person_list."""

    return {
        "uuid": person_list[idx]["uuid"],
        "full_name": person_list[idx]["full_name"],
        "films": [
            {
                "uuid": random.choice(film_list)["uuid"],
                "roles": [
                    random.choice(person_roles),
                ],
            },
        ],
    }


def get_persons_list():
    return [get_person(idx) for idx in range(len(person_list))]
