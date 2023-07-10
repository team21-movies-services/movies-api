from uuid import UUID

from .common import BaseOrjsonModel


class AuthData(BaseOrjsonModel):
    user_id: UUID
    is_superuser: bool
