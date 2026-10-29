# anibis-sdk (Python)

Unofficial Python client for [anibis.ch](https://www.anibis.ch). It covers search with filters and pagination, listing details, seller profiles, categories and search suggestions.

anibis.ch runs on the same platform and GraphQL API as tutti.ch. `AnibisClient` is therefore a [tutti-sdk](https://github.com/aneshodza/tutti-sdk) client pointed at anibis's web API: same builder, same results, same sessions.

> ⚠️ Not affiliated with anibis.ch. Respect anibis.ch's terms of service and rate limits.

## Install

```sh
pip install anibis-sdk    # or: uv add anibis-sdk
```

API reference: https://aneshodza.github.io/anibis-sdk/. For the full search and result API, see the [tutti-sdk docs](https://aneshodza.github.io/tutti-sdk/).

## Usage

```python
from anibis_sdk import AnibisClient

with AnibisClient() as client:
    lausanne = next(
        l for l in client.localities.search("lausanne") if l["localityID"] == "geo-city-lausanne"
    )
    result = (
        client.search("vélo")
        .price(max=500)
        .location(lausanne)
        .radius(10)
        .select("companyAd", "private")
        .fetch()
    )
    result.total_count, result.listings
    for listing in result.paginate():
        ...

    client.listings.get("1074111697")
    client.categories.tree()
    client.profiles.get(public_account_id)
    client.suggestions.search("vél")
```

For French labels and category names, pass `AnibisClient(Session(app=anibis_web_app(), language="fr"))`.

Only the anonymous read API is supported. The `account` and `messaging` resources inherited from tutti-sdk talk to tutti's login and don't work on anibis.

## Development

```sh
uv sync
uv run pytest            # offline unit tests
uv run pytest -m live    # + live tests against www.anibis.ch
uv run pdoc anibis_sdk   # browse the API docs locally
```

Commits follow [Conventional Commits](https://www.conventionalcommits.org/). [release-please](https://github.com/googleapis/release-please) keeps a release PR open on `main`. Merging it tags the release, publishes to PyPI, and deploys the API docs to GitHub Pages.
