from fastapi import APIRouter

from .films import router as films_router
from .genres import router as genres_router
from .persons import router as persons_router
from .status import router as status_router

api_v1_router = APIRouter()

api_v1_router.include_router(films_router, prefix="/films")
api_v1_router.include_router(genres_router, prefix="/genres")
api_v1_router.include_router(persons_router, prefix="/persons")
api_v1_router.include_router(status_router, prefix="/status")
