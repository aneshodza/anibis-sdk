"""Live tests against the real www.anibis.ch (anonymous). Run with ``pytest -m live``.

Kept deliberately small (~15 requests) to stay polite to anibis.ch.
"""

import pytest

from anibis_sdk import AnibisClient

pytestmark = pytest.mark.live


@pytest.fixture(scope="module")
def client():
    with AnibisClient() as c:
        yield c


@pytest.fixture(scope="module")
def lausanne(client):
    return next(
        loc
        for loc in client.localities.search("lausanne")
        if loc["localityID"] == "geo-city-lausanne"
    )


@pytest.fixture(scope="module")
def first_page(client):
    return client.search("velo").fetch()


def echo(filters, name):
    f = next(f for f in filters if f["name"] == name)
    return (
        f.get("pricingValue")
        or f.get("locationValue")
        or f.get("selectedOption")
        or f.get("selectedOptions")
    )


def test_search_and_paginate(first_page):
    assert first_page.total_count > 1000
    assert len(first_page.listings) == 30
    second = first_page.next()
    assert second is not None and second.listings
    assert not {x["listingID"] for x in first_page.listings} & {
        x["listingID"] for x in second.listings
    }


def test_listing_details_and_seller_profile(client, first_page):
    listing_id = first_page.listings[0]["listingID"]
    detail = client.listings.get(listing_id)
    assert detail["listingID"] == listing_id
    seller = detail["sellerInfo"]["publicAccountID"]
    assert client.profiles.get(seller)["listings"]["totalCount"] >= 1


def test_filters_change_counts_and_are_echoed(client, lausanne):
    total = client.search().category("cars").update_filters()["listings"]["totalCount"]
    assert total > 1000

    def check(builder, name, expected):
        res = builder.update_filters()
        assert 0 < res["listings"]["totalCount"] < total, name
        assert echo(res["filters"], name) == expected, name

    cars = lambda: client.search().category("cars")
    check(cars().price(min=1000, max=5000), "price", {"min": 1000, "max": 5000, "freeOnly": False})
    check(
        cars().location(lausanne).radius(10),
        "location",
        {"selectedLocalities": [{"__typename": "Locality", **lausanne}], "radius": 10},
    )
    check(cars().select("companyAd", "private"), "companyAd", "private")


def test_categories_featured_and_browse(client):
    assert len(client.categories.tree()) > 10
    featured = client.categories.featured()
    assert client.browse(featured[0]["searchToken"]).fetch().total_count > 0


def test_suggestions(client):
    sug = client.suggestions.search("vel")
    assert [s for g in sug["suggestionGroups"] for s in g.get("suggestions") or []]
