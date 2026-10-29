"""Unofficial Python client for anibis.ch.

anibis.ch runs on the same platform and GraphQL API as tutti.ch, so
:class:`AnibisClient` is a :class:`tutti_sdk.TuttiClient` pointed at anibis's
web API. Search, results, sessions and errors all come from
`tutti-sdk <https://aneshodza.github.io/tutti-sdk/>`_.

Only the anonymous read API is supported: search, listings, seller profiles,
categories and suggestions. The inherited ``account`` and ``messaging``
resources talk to tutti's login and are not supported on anibis.
"""

__docformat__ = "restructuredtext"

from tutti_sdk import (
    AppConfig,
    FileSessionStore,
    InMemorySessionStore,
    SearchBuilder,
    SearchResult,
    Session,
    TuttiClient,
    TuttiError,
    TuttiGraphQLError,
    TuttiHttpError,
    TuttiNetworkError,
    TuttiValidationError,
)

ANIBIS_API_URL = "https://www.anibis.ch/api"


def anibis_web_app() -> AppConfig:
    """Client identity of the anibis.ch website, sent with every request."""
    return AppConfig(
        version="",
        app_id="",
        source="web r1.0",
        client_id="web/1.0.0+env-anibis.git-bb7bfe46",
        user_agent=(
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:158.0) Gecko/20100101 Firefox/158.0"
        ),
    )


class AnibisClient(TuttiClient):
    """Entry point for anibis.ch. Same interface as :class:`tutti_sdk.TuttiClient`.

    Without a ``session``, a fresh anonymous one with the anibis website's
    identity is created. Pass ``Session(app=anibis_web_app(), language="fr")``
    to change the language of labels and category names.
    """

    def __init__(
        self, session: Session | None = None, *, base_url: str = ANIBIS_API_URL, **kwargs
    ) -> None:
        super().__init__(session or Session(app=anibis_web_app()), base_url=base_url, **kwargs)


__all__ = [
    "ANIBIS_API_URL",
    "AnibisClient",
    "AppConfig",
    "FileSessionStore",
    "InMemorySessionStore",
    "SearchBuilder",
    "SearchResult",
    "Session",
    "TuttiError",
    "TuttiGraphQLError",
    "TuttiHttpError",
    "TuttiNetworkError",
    "TuttiValidationError",
    "anibis_web_app",
]
