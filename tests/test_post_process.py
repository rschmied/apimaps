"tests for the post processing module"

import apimaps.post_process as pp


def test_mangle_all_without_data():
    "test the available manglers with no data"

    # ensure that new manglers get detected so that we can do a test
    assert len(pp.manglers) == 4
    data = {}
    for mangler in pp.manglers:
        mangler(data)


def test_mangle_epic(test_data):
    "test the EPIC mangler, ensure the URL is put in place"

    data = test_data("epic.json")
    assert data is not None

    pp.epic_mangle(data)
    uri: str = data["epic"][0]["url"]
    assert uri.endswith(".png")


def test_mangle_people(test_data):
    "ensure the people data is properly mangled"

    data = test_data("people.json")
    assert data is not None
    pp.astro_mangle(data)
    assert data["people"]["vehicle"]


def test_mangle_natural(test_data):
    "ensure the natural events data is properly mangled"

    data = test_data("natural.json")
    assert data is not None
    pp.natural_mangle(data)
    assert len(data["natural"]) == 1
    categories = list(data["natural"].keys())
    assert categories[0] == "Severe Storms"


def test_mangle_bodies(test_data):
    "ensure the celestial bodies data is properly mangled"

    data = test_data("bodies.json")
    assert data is not None
    pp.bodies_mangle(data)
    assert data["bodies"]["total_count"] == 2
    assert len(data["bodies"]["categories"]) == 2
