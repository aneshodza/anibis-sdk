"""Offline tests against a mocked transport — no network."""

import json

import httpx

from anibis_sdk import AnibisClient, Session, anibis_web_app


def recording_client(**kwargs) -> tuple[AnibisClient, list[httpx.Request]]:
    seen: list[httpx.Request] = []

    def handler(request: httpx.Request) -> httpx.Response:
        request.read()
        seen.append(request)
        return httpx.Response(200, json={"data": {"searchLocalities": []}})

    return AnibisClient(transport=httpx.MockTransport(handler), **kwargs), seen


def test_requests_go_to_anibis_web_graphql():
    client, seen = recording_client()
    client.localities.search("lausanne")

    req = seen[0]
    assert str(req.url) == "https://www.anibis.ch/api/v10/graphql"
    assert req.headers["X-Tutti-Client-Identifier"] == "web/1.0.0+env-anibis.git-bb7bfe46"
    assert req.headers["X-Tutti-Source"] == "web r1.0"
    assert req.headers["User-Agent"].startswith("Mozilla/5.0")
    assert req.headers["X-Tutti-Hash"] == client.session.tutti_hash
    assert json.loads(req.content)["operationName"] == "SearchLocalities"


def test_custom_session_keeps_anibis_host():
    client, seen = recording_client(session=Session(app=anibis_web_app(), language="fr"))
    client.localities.search("lausanne")
    assert seen[0].url.host == "www.anibis.ch"
    assert seen[0].headers["Accept-Language"] == "fr"


def test_each_client_gets_its_own_device_hash():
    assert AnibisClient().session.tutti_hash != AnibisClient().session.tutti_hash
