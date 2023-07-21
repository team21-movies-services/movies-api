import aiohttp
import pytest

from tests.functional.settings import test_settings
from tests.functional.utils.fixture_types import HTTPResponse


@pytest.fixture
async def session():
    session = aiohttp.ClientSession()
    yield session
    await session.close()


@pytest.fixture
def make_get_request(session: aiohttp.ClientSession):
    async def inner(endpoint: str, params: dict | None = None) -> HTTPResponse:
        url = f"{test_settings.service_url}{endpoint}"
        auth_header = {"Authorization": test_settings.test_user_jwt}
        async with session.get(url, params=params, headers=auth_header) as response:
            return HTTPResponse(
                body=await response.json(),
                status=response.status,
            )

    return inner
