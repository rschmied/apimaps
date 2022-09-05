"tests for the api list class / module"

import apimaps.apilist as apl


def test_api_class():
    "test the API class"

    api = apl.API("test", "http://api.test.test/", "description")
    assert api.name == "test"
    assert api.uri == "http://api.test.test/"
    assert api.description == "description"
    assert api.use_token is True


def test_api_short():
    "test the short / fast API list"

    alist = apl.apilist(all_apis=False)
    assert len(alist) == 2


def test_api_long():
    "test the long API list"

    alist = apl.apilist()
    assert len(alist) == 19


def test_api_output():
    "test API output / help creation"

    alist = apl.apilist(all_apis=False)
    output = apl.printable(alist)
    assert len(output) == len(alist) + 2


def test_single():
    "test single API retrieval"

    alist = apl.single_api("people")
    assert len(alist) == 1
    alist = apl.single_api("does-not-exist")
    assert len(alist) == 0
