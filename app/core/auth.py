from fastapi import Depends

from fastapi_users.authentication.strategy.db import (
    AccessTokenDatabase,
    DatabaseStrategy,
)
from fastapi_users.authentication import (
    AuthenticationBackend,
    CookieTransport,
)

from app.services.tokens import get_access_token_db
from app.models.tokens import AccessToken

cookie_transport = CookieTransport(cookie_max_age=3600, cookie_name="access_token")


def get_database_strategy(
    access_token_db: AccessTokenDatabase[AccessToken] = Depends(get_access_token_db),
) -> DatabaseStrategy:
    return DatabaseStrategy(access_token_db, lifetime_seconds=3600)


auth_backend = AuthenticationBackend(
    name="jwt",
    transport=cookie_transport,
    get_strategy=get_database_strategy,
)
