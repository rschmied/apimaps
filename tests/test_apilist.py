"tests for the api list class / module"

import pytest
import apimaps.apilist as apl


def test_api_class():
    "test the API class"

    api = apl.API("test", "http://api.test.test/", "description")
    assert api.name == "test"
    assert api.uri == "http://api.test.test/"
    assert api.description == "description"
    assert api.use_token is True


def test_all_apis():
    "test the long API list"

    alist = apl.apilist()
    assert len(alist) == 19


def test_api_output():
    "test API output / help creation"

    alist = apl.apilist()
    output = apl.printable(alist)
    assert len(output) == len(alist) + 2


def test_api_set():
    "test single API retrieval"

    alist = apl.get_api_set({"people"})
    assert len(alist) == 1

    alist = apl.get_api_set({"iss", "people"})
    assert len(alist) == 2

    with pytest.raises(ValueError):
        alist = apl.get_api_set({"does-not-exist"})
